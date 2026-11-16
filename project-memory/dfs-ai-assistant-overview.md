# DFS AI Assistant(ai-assistant)项目说明

**日期:** 2026-11-12
**来源:** ai-assistant 项目的 README.md、AGENTS.md、docs/ARCHITECTURE.md,并核对了目录结构和部分源码文件头
**状态:** 摘要说明

> Related: [dspdm-mcp](../api/mcp/dspdm-mcp.md)(NL→SQL 查询服务)、
> [wim-mcp](../api/mcp/wim-mcp.md)(井完整性证据服务)、
> [AI Agent 趋势探索](../analysis/2026-11-10-ai-agent-trend-exploration-analysis.md)。

## 1. 先说结论:文档之间有出入

这个项目经历过一次 **Harmony 迁移**,三份文档反映的是不同时期:

| 文档 | 描述的是 |
| --- | --- |
| README.md、docs/ARCHITECTURE.md | **迁移前**:本服务自己运行 Agent(编排器、工具注册表、子代理、沙箱) |
| AGENTS.md(最新) | **迁移后**:Agent 的执行与扩展(工具、子代理、提示词、技能)**全部在 Harmony 运行时**;本服务只保留数据和配置相关的功能 |

我核对了目录:`pymsp_plugin/common/` 下现在只有 `config`、`infra`、`tools`(仅 `glossary.py` 和 `domain_glossary.json`)、`utils`;`pymsp_plugin/chat/routers/` 下没有 agent 或 chat 路由,而有 `harmony_proxy_router.py`。**所以以 AGENTS.md 为准:README 和 ARCHITECTURE 里关于本地编排器、工具注册、沙箱的大部分内容已经过时。**

## 2. 它现在做什么(迁移后)

DFS AI Assistant 是 FastAPI 服务(Python 3.13),现在是 Harmony Agent 平台的**数据与配置侧后端**,同时托管聊天界面:

| 能力 | 说明 | 位置 |
| --- | --- | --- |
| 知识库管理 | 知识库、文档、分块的增删改查,用于 RAG(pgvector) | `pymsp_plugin/knowledge/` |
| 视图结构与 SQL 示例的维护 | 为 [dspdm-mcp](../api/mcp/dspdm-mcp.md) 的 `query_database` **维护目录数据**(view schema、few-shot SQL 示例) | `chat/routers/dspdm_views_manager_router.py`、`dspdm_sql_example_router.py` |
| MCP 服务器配置 | 管理租户可用的 MCP 服务(增删改查、验证连通) | `chat/routers/mcp_config_router.py` |
| 页面提示词、设置、仪表盘 | 页面级提示词、租户设置、dashboard | `page_prompt_router.py`、`setting_router.py`、`dashboard_router.py` |
| Harmony 代理 | 在浏览器和 Harmony 之间转发携带用户文本的请求(见下) | `chat/routers/harmony_proxy_router.py` |
| 井筒示意图 | 提供井筒示意图数据,由 `@dswc-wom/well-schematic` 渲染 | `pymsp_plugin/solution/` |
| 租户接入 | 向 Tenant Manager 注册和开通 | `pymsp_plugin/onboarding/` |
| 前端 | Angular 20 单页应用(`agent-widgets/`),构建产物放在 `pymsp/static`,支持 Module Federation | `agent-widgets/` |
| 评测 | 基于 LangSmith 的 Agent 评测运行器 | `evaluate/` |

### Harmony 代理路由(一个值得知道的权宜之计)

- **问题:** 平台的 WAF 会误判发往 Harmony 公网入口的自由文本聊天内容。
- **做法:** 浏览器把请求体 base64 编码后发给本服务,本服务解码后经内部网络转发给 Harmony,响应原样流式返回(WAF 只检查入站请求)。
- 转发两个接口:AG-UI 运行流(`POST /agui/threads/{thread_id}/runs/stream`)和创建会话(`POST /threads`)。
- 它是"哑管道",不解析请求和 SSE 事件;注释明确说这是**临时桥接**,真正的长期方案是在 Harmony 端点上申请 WAF 路径例外,之后这个路由可以去掉。

## 3. 技术栈

| 层 | 技术 |
| --- | --- |
| 后端 | FastAPI、Python 3.13、Uvicorn |
| AI/LLM | LangChain、LangGraph、LiteLLM(Azure OpenAI 等) |
| 数据库 | PostgreSQL、SQLModel、SQLAlchemy、PGVector |
| 前端 | Angular 20、NgRx、PrimeNG、ECharts、Module Federation |
| 消息 | Confluent Kafka |
| 监控 | New Relic |
| CI/CD | Jenkins、Docker、Kubernetes(Helm) |

结构上是 `pymsp`(核心框架:服务、配置、插件加载)加 `pymsp_plugin/`(业务插件,按 `SERVICE_ROOT_EXT`,默认 `/msp`,挂载路由)。

## 4. 主要接口(来自 README,需对照现状)

| 接口 | 说明 |
| --- | --- |
| `GET /` | Angular 单页应用 |
| `GET /msp/well-schematic?id=` | 井筒示意图数据 |
| `GET·POST·PUT·DELETE /msp/v1/knowledge` | 知识库管理 |
| `GET·POST·PUT·DELETE /msp/v1/mcp-servers` | MCP 服务配置 |
| `GET·POST·PUT·DELETE /msp/v1/prompt` | 提示词管理 |
| `GET /msp/v1/view-schema` | 数据库视图结构管理 |
| `GET /msp/home/health`、`/msp/home/readiness` | 存活/就绪探针 |
| `GET /apidocs/ui/` | Swagger UI |

> README 里还列了 `POST /msp/v1/agent/chat`(AG-UI 流式聊天)、`/skill`、`/tool-management`、`/analytics` 等,对应已被移除的本地 Agent 部分,**很可能已不存在**,请以代码和 Swagger 为准。

## 5. 技能(Skills)

`scripts/skills/` 里保存技能定义(每个目录一个 `SKILL.md`),这些技能在 Harmony 运行时使用。目录里能看到:

| 类别 | 技能 |
| --- | --- |
| 通用产出 | `export-excel`、`generate-html` |
| 实体与可视化 | `entity-card`、`well-map`、`well-schematic`、`well-report` |
| 生产诊断 | `well-decline`、`production-drop-diagnosis` |
| 井完整性(WIM) | `wim-risk-contributors`、`wim-action-plan-advisor`、`wim-executive-summary` |

> 技能的具体内容我没有逐个阅读,上表只是目录名,用途请以各 `SKILL.md` 为准。

## 6. 文本到 SQL 的检索设计(已迁到 dspdm-mcp)

README 详细描述了视图检索:**术语表扩展 → 稠密向量 + BM25 → RRF 融合 → LLM 写 SQL**,以及 few-shot 示例的两条路径(始终开启的示例注入;可选的"已验证模板填槽"快速通道)。

迁移后:

- 检索评测脚本和用例**已搬到 `dspdm-mcp/evaluate/`**,原因是这里的检索实现已不在请求路径上,且两份实现已经分叉,这里 36 个用例有 19 个已与目录不符。
- 本服务仍保留 `glossary.py` / `domain_glossary.json`,并负责视图结构和 SQL 示例的**维护**(种子脚本在 `scripts/`)。
- 实现细节请看 [dspdm-mcp 文档](../api/mcp/dspdm-mcp.md)。

## 7. 认证

- API 受 Keycloak JWT 保护,`Authorization: Bearer <token>`;租户来自 `tenantid` 声明。
- 前端作为 iframe 嵌入时,通过 `postMessage` 从父应用拿 token,并自动附加到请求。
- 注意:`IS_DEBUG` 会跳过签名校验,audience 校验已关闭;非本地环境不要开 `IS_DEBUG`。
- 项目约定不提供关闭 TLS 校验的开关。

## 8. 评测(LangSmith)

`evaluate/` 对真实环境(本地 devstack 或 Tiger)发起真实聊天,并对结果评分,是 Agent 的回归测试,不是单元测试。

- 组成:环境文件、数据集、评分器、`runner.py`。
- 评分器:`tool_selection`、`outcome_status`、`placement_canvas_match`、`node_metadata_match`、`correctness`、`no_error`、`response_length`。
- **现状:** AGENTS.md 说 `evaluate_agent.py`、`schema_integrity_eval.py`、`skill_visibility_eval.py`、`agent_target.py` 因依赖已删除的本地编排器而**已损坏**,需要另行决定如何重做;README 里的评测运行方式因此大概率不能直接用。
- 当前没有自动化的检索质量评测门禁(`rag_groundedness_eval.py` 已删除)。

## 9. 数据

PostgreSQL,三类库/连接:solution、dspdm、`dfs_ai`(`harmony_dfs`)。主要表:聊天表(conversation、message、dashboard)、agent 表(prompt、tool_config、mcp_server_config、agent、sub_agent、skill 等)、知识库表(knowledge、document、document_chunk 等)。docs 里有多 Agent 表结构的方案文档(`agent_schema_multiagent_proposal.md`、`agent_schema_consolidation.md`)。

## 10. 与其他项目的关系

```
浏览器(chatbot-ui / agent-widgets)
   │  (经 harmony_proxy_router 转发聊天请求)
   ▼
Harmony(Agent 运行时:编排、工具、子代理、技能、提示词)
   │ 调用 MCP
   ├──► dspdm-mcp(自然语言查生产库)
   ├──► wim-mcp(井完整性证据)
   └──► rag-mcp(知识检索,文档中提到,未见详情)

ai-assistant(本服务):知识库 / 视图结构与 SQL 示例维护 / MCP 配置 / 页面提示词 / 前端托管
```

## 11. 对本项目(WPO)的启示

- **Agent 运行时与数据/配置分离:** 业务数据维护和 Agent 编排分属不同服务,WPO 做 Agent 时也可以把"知识与配置管理"独立出来。
- **MCP 配置可运行时调整:** 新增外部工具不用改代码,在界面里添加 MCP 服务即可。这与 [WPO 引入 MCP 分析](../analysis/2026-11-10-wpo-mcp-requirement-analysis.md) 的思路一致。
- **示例即资产:** 经过验证的 `问题 → SQL` 示例被当作提升准确率的最高杠杆,"业务沉淀"的做法值得借鉴。
- **评测要跟着架构走:** 架构迁移让评测脚本大面积失效,说明评测依赖越少越稳。

## 12. 边界与待确认

- 文档未说明 Harmony 的具体形态,以及 rag-mcp 和 dspdm-mcp 是否已在代码里接入(ARCHITECTURE 的 Open items 写"未在代码中确认")。
- README 与 ARCHITECTURE 大量内容已过时,是否有计划更新?
- `CICD/build.sh` 会先构建 `agent-widgets/`;文档说该目录不在检出里,但我看到当前目录里有 `agent-widgets/`,这条已知问题可能已不成立。
- 评测脚本的重构方案尚未决定。
- 我没有读源码实现,只读了文档、目录结构和个别文件头。
