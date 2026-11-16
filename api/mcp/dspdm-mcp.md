# dspdm-mcp:DSPDM 生产数据库自然语言查询 MCP 服务

**日期:** 2026-11-12
**来源:** dspdm-mcp 项目的 README.md、AGENTS.md、docs/ARCHITECTURE.md
**状态:** 摘要说明(基于项目文档整理,未阅读源码)

> Related: [wim-mcp](wim-mcp.md)(同类 MCP,按井取证据)、
> [WPO 引入 MCP 需求分析](../../analysis/2026-11-10-wpo-mcp-requirement-analysis.md)。

## 1. 一句话

dspdm-mcp 是一个 **MCP 服务(Python,Streamable HTTP,端点 `/mcp`,默认端口 2040)**,让 Agent 能用**自然语言**查询 **DSPDM(Decision Space Production Data Model)** 上游油气**生产**数据库:井、油田、设施、日/实时产量、试井、停产/事件、风险等。

核心做法:**检索相关的视图结构和示例 SQL → 让 LLM 写一条 SELECT → 解析并加固 SQL → 只读执行 → 返回行数据,量大时导出 Excel 并返回下载链接。** 它由 Harmony 代表已登录用户调用。

它是 DFS 插件内 `sql_agent` 和实体工具的独立移植版。

## 2. 三个工具

| 工具 | 参数 | 返回 |
| --- | --- | --- |
| `query_database` | `question: str` | JSON 行数组;或特殊回复:`__AUTO_EXPORT__`、`__QUERY_TOO_LARGE__`、`__NEED_CLARIFICATION__`、无匹配/错误文本 |
| `resolve_entity` | `name: str`,`declared_type: str = ""` | JSON,含 `status`:resolved / ambiguous / not_found。**提到具体名称时应先调用它** |
| `get_entity_card` | `entity_type: str`,`entity_id: str` | 井 / 油田 / 设施的卡片文本 |

**重要约束:`question` 必须自包含。** 工具只收到这一个字符串,看不到对话。调用方 Agent 要先把所有指代解析进去:

- 用户追问"上个月呢?"→ 必须发送"show me production for well MANDAK POPE last month"。
- 原样转发用户的话会悄悄丢掉主语。

## 3. `query_database` 如何工作

```
问题 ─► ① 检索 ─► ② 生成 SQL ─► ③ 守卫 ─► ④ 成本预检 ─► ⑤ 只读执行 ─► ⑥ 分层返回
          │            │            │ 失败/拒绝 → 带原因回到 ② 修复(最多 N 轮)
     目录库(pgvector)  LLM(经代理)
```

| 步骤 | 做什么 |
| --- | --- |
| ① 检索 | 在目录库(`view_schema`、`sql_example`)里做 **BM25 + 向量检索**,用 RRF 融合;候选带 `similarity`(真实余弦,仅关键词命中时为空)和 `rank` |
| ② 生成 | 用问题、匹配的视图结构和示例构造提示,LLM 只写**一条 SELECT**;失败时有修复轮次(`DSPDM_SQL_REPAIR_ATTEMPTS`) |
| ③ 守卫 | 在**解析后的语法树**上检查和改写,见第 4 节 |
| ④ 成本预检 | 对**不加行数上限**的查询做 `EXPLAIN (FORMAT JSON)`,超过 `DSPDM_MAX_PLAN_COST`(默认 200000)就拒绝,防止交叉连接这类"合法但极昂贵"的查询 |
| ⑤ 执行 | 执行库会话设置 `search_path` 和语句超时(默认 30000 ms) |
| ⑥ 分层返回 | 见下表 |

**结果分三层:**

| 行数 | 处理 | 模型能看到什么 |
| --- | --- | --- |
| ≤ 200(`DSPDM_QUERY_MAX_ROWS`) | 直接以 JSON 返回 | 行数据 |
| ≤ 5000(`DSPDM_EXPORT_MAX_ROWS`) | 完整结果写入 Excel,用用户 token 上传到 File Manager,返回下载引用 | 只有 `__AUTO_EXPORT__` 消息,**行数据不进 LLM** |
| 更多 | 返回 `__QUERY_TOO_LARGE__`,请用户缩小范围 | 提示 |

导出层需要 `FILE_MANAGER_URL` 和转发的用户 token。

## 4. SQL 守卫(最关键的部分)

守卫在 `tools/sql_guard.py`,基于 sqlglot 的语法树,而不是正则:

| 规则 | 说明 |
| --- | --- |
| 只允许一条只读 SELECT | 写、DDL、加锁、`SELECT INTO`、CTE、`UNION` 在树的任何位置都拒绝 |
| **函数白名单** | 不是黑名单。黑名单只能挡住"想到过的";旧的 20 项黑名单曾放过会写数据的函数。sqlglot 认识的内置函数(聚合、窗口、日期、字符串等)被信任,未识别的函数必须在白名单里 |
| 表白名单 | 每张表必须在该租户的视图目录里;`public` 以外的 schema 一律拒绝,碰不到 `pg_catalog` / `information_schema` |
| **租户谓词** | 每个读取表的 SELECT 作用域里,**每个关系**都会加上 `TENANT_ID` 条件(含子查询,按别名限定);无条件注入。如果 SQL 写的是**另一个租户**,直接拒绝,而不是悄悄返回 0 行 |
| 行数上限与排序 | 只加在最外层 SELECT,不放宽模型自己写的更小上限;没有 ORDER BY 时按第一个日期列补上,没有日期列就标记为"无序" |

守卫拒绝会带着具体原因进入修复轮次,拒绝的函数名会进入遥测记录,白名单据此增长,而不是凭猜测。

## 5. 认证与租户

| 项目 | 行为 |
| --- | --- |
| Token | Harmony 在每次 `tools/call` 转发调用者的 Keycloak JWT |
| 校验 | RS256 签名、`exp`,设置了 issuer 时校验 issuer;**不校验 audience** |
| 租户 | 来自 token 的 `tenantid` 声明(`DSPDM_TENANT_JWT_CLAIM`);没有静态租户配置;**无租户的 token 被拒绝** |
| `tools/list` | 保持开放,无需 token |
| 工具参数 | 租户和用户**从不**接受工具入参,只来自请求上下文 |
| 开发模式 | 未配置 JWKS 时不校验,会接受未认证的 `tools/call` |
| Token 用途 | 同时存入 `ContextVar`,导出层用它以用户身份调用 File Manager |

## 6. 数据存储

| 库 | 配置 | 内容 |
| --- | --- | --- |
| 目录库(catalogue) | `DSPDM_AI_DB_NAME` | 视图结构、SQL 示例、元数据,pgvector;检索用 |
| 执行库(exec) | `DSPDM_DB_NAME`(`dspdm_model`) | 生产数据:井、油田、设施、产量、试井、停产、事件;只读查询,有超时 |

两个库在代码里始终分开;DSN 由 `DSPDM_URL` 和账号密码组装,或直接给完整 DSN。其中三个视图通过 postgres_fdw 读取 `dfs_solution`(`wim` + `wpo`)。

## 7. 租户隔离现状(需要重点知道)

文档于 2026-11-05 在线上库实测,结论是:

- 三个库里的行级安全(RLS)策略**对这个服务实际不生效**:服务以 `postgres` 连接,它是所有表和视图的所有者,而没有表设置 `FORCE ROW LEVEL SECURITY`,表所有者会绕过自己的策略。实测:绑定某租户后,`vw_well_basic_info` 仍返回 5 个租户共 2724 行(该租户 518 行)。
- 所以**租户边界就是生成 SQL 里的谓词**,即守卫本身,不是兜底措施。
- 三个外部表视图(`vw_well_anomaly`、`vw_well_risk_rank_history`、`vw_wfm_test_history`)RLS 无论如何都覆盖不到(postgres_fdw 不转发 GUC),守卫是它们**唯一**的边界。字面量租户谓词还能被下推到远端,比 `current_setting(...)` 少取数据。
- 修复方案 `deploy/sql/001_tenant_isolation.sql`(把 9 个视图改为只读角色所有)被**搁置**:没有 `CREATE ROLE` 权限。文档明确说"不要围绕它落地来做计划"。
- 目录库完全没有 RLS(56 张表里 46 张有 `tenant_id` 列,无一受保护),靠手写的参数化查询保证;另有 34 张(`dfs_solution`)和 10 张(`dspdm_model`)有 `tenant_id` 但未启用 RLS。

## 8. 配置概要

> 只列变量名和用途;具体值来自 `.env`(本地)或 DSIS 远程配置/密钥(部署)。不要把 `.env.example` 中的值复制到文档或代码。

| 类别 | 变量 |
| --- | --- |
| 数据库 | `DSPDM_URL`、`DSPDM_USERNAME`、`DSPDM_PASSWORD`、`DSPDM_DB_NAME`、`DSPDM_AI_DB_NAME`(或完整 DSN) |
| LLM | `HARMONY_LLM_PROXY_URL`(必需,所有嵌入和 SQL 生成都经它,无直连 Azure 的退路)、嵌入/SQL 部署名 |
| 限额 | `DSPDM_QUERY_MAX_ROWS`(200)、`DSPDM_EXPORT_MAX_ROWS`(5000)、`DSPDM_MAX_PLAN_COST`(200000)、`DSPDM_STATEMENT_TIMEOUT_MS`(30000) |
| 检索与修复 | `DSPDM_HYBRID_RETRIEVAL`、`DSPDM_CANDIDATE_POOL`、`DSPDM_SQL_REPAIR_ATTEMPTS` 等 |
| 导出 | `FILE_MANAGER_URL` |
| 认证 | `DSPDM_JWT_JWKS_URL`、`DSPDM_JWT_ISSUER`、`DSPDM_JWT_ALGORITHMS`、`DSPDM_TENANT_JWT_CLAIM`、`KC_ROOT_URL`、`KC_DSIS_REALM` |
| 其他 | `PORT`(2040) |

另有两点:
- **租户覆盖**:部分限额和检索参数可按租户覆盖,从 `config_metadata`(`dfs_ai.mcp`,`mcp_name='dspdm'`)读取,每进程缓存 60 秒,无效值回退到环境变量。
- **DSIS 远程配置**:启动时从 DSIS Config Service 拉取并用 `setdefault` 合并,显式设置的值优先;不可达时只警告,继续使用环境变量。

## 9. 领域词表与可测量的检索质量

| 内容 | 说明 |
| --- | --- |
| `tools/domain_glossary.json` | 把用户的说法映射到规范概念(问题级),文档称带来 top-1 +11.1 个百分点 |
| 列的合法取值 | 由脚本从数据库生成并挂在列上,**不手写**——大小写或措辞不对不会报错,只会返回 0 行 |
| 约定类说明 | 模型推不出的约定(如"shut in" = `WELL_STATUS = 'Inactive'`)写在列的 `description` 里 |
| `time_dimensions` | 按文件顺序匹配,先匹配先得,所以具体项在前(`integrity_test` 在 `well_test` 之前) |
| 评估 | `evaluate/view_retrieval_eval.py` 衡量视图检索的 top-1 / top-3;改检索前后都要跑,对照 `evaluate/BASELINE.md` |
| 可观测 | 每次调用输出一行 `dspdm_query` JSON 日志,`outcome` 是统计无匹配/澄清/守卫拒绝/修复/导出比例的聚合键 |

## 10. 运行与测试

| 场景 | 做法 |
| --- | --- |
| 安装 | `uv sync`(公司代理报 `UnknownIssuer` 时加 `UV_NATIVE_TLS=true`) |
| 启动 | `uv run --env-file .env python server.py`,监听 `http://0.0.0.0:$PORT/mcp` |
| 单元测试 | `uv run pytest`(不连数据库和网络) |
| 冒烟测试 | `MCP_URL=http://localhost:2040/mcp DSPDM_QUESTION="how many wells we have?" uv run python tests/check_client.py`,需要运行中的服务和真实数据库 |
| 本地 LLM 代理 | 代理地址是集群内名字,本地需 `kubectl port-forward` 后改指向 localhost |
| Docker | 需从仓库根目录构建(构建上下文包含 `mcp/dspdm`) |
| docker compose | 启动 `pgvector/pgvector:pg16` 和 MCP 服务;初始化脚本放 `docker/initdb/` |

## 11. 与 wim-mcp 的对比

| 维度 | dspdm-mcp | [wim-mcp](wim-mcp.md) |
| --- | --- | --- |
| 数据源 | DSPDM 生产数据库(直接查库) | DFSWIM 的 REST API |
| 查询方式 | 自然语言 → LLM 生成 SQL | 固定工具、按 `well_id` 取证据 |
| 范围 | 开放式问题(产量、试井、停产、风险等) | 风险、操作限值、井名解析 |
| 结果形态 | 行数据 / Excel 导出 | 带来源引用的证据快照,不下结论 |
| 主要风险 | LLM 生成 SQL 的安全与成本,租户边界全靠守卫 | 上游 API 的覆盖与缺口 |
| 认证 | 转发 Keycloak JWT,租户取自 `tenantid` | 转发 Bearer token,权限由 WIM/网关执行 |

## 12. 对本项目(WPO)的启示

- **自然语言取数**:WPO 的 Agent 想法(见 [Agent-Native 分析](../../analysis/2026-11-10-wpo-agent-native-opportunity-analysis.md))中的"数据发现、查询"可以参考这套"检索 + 生成 + 守卫"的做法。
- **安全设计可直接借鉴**:函数白名单、表白名单、租户谓词逐关系注入、成本预检、分层返回(大结果不进 LLM)。
- **自包含问题**:调用 Agent 必须把指代解析完再调用,这一条应写入 Agent 提示。
- **可度量**:检索质量有评估脚本和基线,改动前后对比,不靠争论。
- **局限**:SQL 由 LLM 生成,正确性和安全依赖守卫;数据库层没有兜底。

## 13. 边界与待确认

- 本文只基于三份文档,未读源码、`.env.example` 和部署清单。
- 文档中有几处不一致:
  - `tests/check_client.py` 默认连 `2051`,服务默认 `2040`,需要显式设置 `MCP_URL`。
  - Docker 构建命令引用 `mcp/dspdm/Dockerfile`,而当前检出里 Dockerfile 在仓库根目录,路径对应的是 `dfs-ai` 大仓库。
  - AGENTS.md 说 `dfs-ai/.gitignore` 忽略 `uv.lock`,但这份检出里有 `uv.lock`。
- 租户隔离的搁置迁移何时落地,文档没有时间表。
- 与 WPO / WSO 数据的对应关系(DSPDM 视图与 WPO API)文档未说明。
