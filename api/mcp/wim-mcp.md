# wim-mcp:DFSWIM 井完整性 MCP 服务说明

**日期:** 2026-11-12
**来源:** wim-mcp 项目 README(用户提供)
**状态:** 摘要说明(基于 README 整理;架构细节见项目内 `docs/ARCHITECTURE.md`,本文未读取)

> Related: [WPO 引入 MCP 需求分析](../../analysis/2026-11-10-wpo-mcp-requirement-analysis.md)、
> [DFS Well Integrity Management 简介](../../frontend/dfs-well-integrity-management-intro.md)。

## 1. 一句话

wim-mcp 是给 **Harmony** 使用的 **DFSWIM(Well Integrity Management)MCP 服务**:把 DFSWIM 现有的井完整性 API 包装成一组 **只读的证据检索工具**,让 Agent 能按井查询风险、操作限值等**证据**。

它是**证据检索层**,**不是**权威的 WFM 计算。

## 2. 设计要点

| 要点 | 说明 |
| --- | --- |
| 按领域组织 | 一个 MCP 服务暴露多个领域的工具(RiskRank、Operating Limits、Well Directory);领域不是各自独立的 Agent |
| 只读 | 所有工具都是 `READ_ONLY_EVIDENCE`,不写入、不给建议 |
| 证据而非结论 | 返回上游报告的数据、来源引用和限制说明;不做限值判定、不挑选主导因素 |
| 部分快照 | 当前只覆盖规格中的一部分,每个结果都标 `snapshotStatus = PARTIAL` |
| 显式缺口 | 未实现的阶段用 `NOT_READY` 占位工具表示,而不是悄悄缺失 |
| 无数据库 | 服务本身无状态,直接调用上游 DFSWIM 服务 |

## 3. 工具清单

### 已实现(只读证据)

| 工具 | 参数 | 返回 |
| --- | --- | --- |
| `analyze_well_risk` | `well_id: int` | 风险快照:上报的计算风险/覆盖风险(override)、风险驱动因素、关联异常、校验问题,以及带引用的 `engineeringAssessment` |
| `analyze_well_operating_limits` | `well_id: int` | 当前操作限值快照:测量值、已配置的压力限值、报警设置、数据源状态;**不做限值评估** |
| `resolve_well_name` | `name: str` | `RESOLVED` / `AMBIGUOUS` / `NOT_FOUND` / `INCONCLUSIVE` / `UNAVAILABLE`;有歧义时返回候选井(含 field / asset / country) |

### 占位(始终返回 `NOT_READY`)

| 工具 | 对应阶段 | 缺什么 |
| --- | --- | --- |
| `detect_risk_change` | Stage 3:风险变化检测 | 缺历史版本数据 |
| `resolve_wfm_drivers` | Stage 4:WFM 主导因素判定 | 缺权威的 WFM 汇总服务 |
| `search_precedents` | Stage 5:同井/跨井先例检索 | 缺相应服务 |
| `assess_actions` | Stage 6:受治理的措施建议/路由 | 缺 Operator Policy Pack 服务 |

占位工具返回 `PendingCapabilityResult`:`status = "NOT_READY"`、`reason`、`blockingDependencies`、`specificationReferences`。它们**不调用任何上游服务**。README 明确说这是对"项目不写占位模块"规则的**有意例外**,目的是让缺口显式、可被机器读取;上游依赖就绪后,应替换成真实实现,不要保留占位。

## 4. 当前范围:部分快照

`analyze_well_risk` 基于 DFSWIM 风险分析规格(规格文件标题显示为 v1,正文标识为 v2),只实现了其中一部分。每个结果都会报告:

- `mode = READ_ONLY_EVIDENCE`,`snapshotStatus = PARTIAL`
- `validation.overallStatus`:
  - `NOT_ANALYSIS_READY`:核心当前风险仍有阻塞项;
  - 否则 `ANALYSIS_READY_WITH_LIMITATIONS`(**永远不会是** `ANALYSIS_READY`);
- 明确的问题清单、来源引用,**没有建议**。

README 指出,以下内容是有意不实现的:主导因素选择、操作限值报警评估、历史/类比对比等(详情见项目的 `AGENTS.md`)。

## 5. 认证与租户

| 项目 | 行为 |
| --- | --- |
| Token 来源 | Harmony 在每次工具调用时转发**调用用户的 Bearer token**;不使用服务端静态账号 |
| 缺少 token | 工具调用被拒绝 |
| 工具发现 | `tools/list` 保持开放 |
| 验证 | 配置了 `WIM_JWT_JWKS_URL` 时,先校验签名、issuer、audience;未配置(本地开发)时,**任何格式合法的 Bearer token 都被接受且不验证** |
| 转发 | 校验过的调用方 token 原样转发给 WIM 服务 |
| 权限 | **井级权限仍由 WIM / 网关负责**;wim-mcp 自身不做 |

> 注意:未配置 JWKS 时不要让服务暴露在 `localhost` 之外。

## 6. 配置(环境变量)

复制 `.env.example` 为 `.env`,不要提交 `.env`。

| 变量 | 默认 | 说明 |
| --- | --- | --- |
| `WIM_WORKFLOW_BASE_URL` / `WIM_WFM_BASE_URL` / `WIM_COMMON_BASE_URL` | — | DFSWIM 服务根地址(`/v1/wim/...` 之前);只能由运维配置,**不能作为工具参数** |
| `WIM_WELL_INFO_BASE_URL` | 空 | 井信息服务根地址,可选;用于获取井类型/生产方式以读取 WFM 设置,为空时把 WFM 设置作为明确的限制报告 |
| `WIM_OPERATING_LOOKBACK_DAYS` | `30` | 读取最新油管/环空压力和流量行的回看窗口(不是数据新鲜度判断) |
| `WIM_HTTP_TIMEOUT_SECONDS` | `30` | 单次上游请求超时 |
| `WIM_MAX_RESPONSE_BYTES` / `WIM_MAX_EVIDENCE_ROWS` | `2097152` / `100` | 响应字节和行数上限;超限会明确报告(`RESPONSE_TOO_LARGE` / `TRUNCATED`),不会静默截断 |
| `WIM_WELL_DIRECTORY_CACHE_SECONDS` / `WIM_WELL_DIRECTORY_MAX_ROWS` | `300` / `50000` | 按调用者缓存井层级的 TTL 和扫描上限 |
| `WIM_JWT_JWKS_URL` / `WIM_JWT_ISSUER` / `WIM_JWT_AUDIENCE` / `WIM_JWT_ALGORITHMS` | 空 / 空 / 空 / `RS256` | 调用方 token 校验;JWKS URL 为空即关闭校验 |
| `PORT` | `2042` | 本地运行的绑定端口(容器内固定 `8080`) |

## 7. 运行与测试

| 场景 | 做法 |
| --- | --- |
| 本地运行 | `uv sync`,然后 `uv run --env-file .env python server.py`;监听 `http://0.0.0.0:$PORT/mcp`(Streamable HTTP);`/health` 只表示存活,不代表 WIM 可连通 |
| Windows | `scripts\windows\start_server.bat` 设置服务根地址并启动(`--check` 只校验配置) |
| 单元测试 | `uv run pytest -q`,只用合成数据,不调用已部署的 WIM 服务 |
| 手动端到端 | `WIM_WELL_ID=6415 MCP_BEARER_TOKEN=<token> uv run python tests/check_client.py`;Windows 用 `scripts\windows\test_mcp.bat` |
| 无真实环境演示 | `scripts/demo/mock_wim_server.py`(Starlette,端口 9000)用预置数据提供与真实 DFSWIM API 相同的响应结构;wim-mcp 的三个服务根都指向它即可完整演示。仅用于演示,不接入 `server.py` |
| Docker | `docker build -t harmony-wim-mcp:dev .`,`docker run --rm -p 2042:2042 --env-file .env harmony-wim-mcp:dev` |
| docker compose | `docker compose up`,服务在 `http://localhost:2042/mcp`;无数据库,可指向本地 mock |

## 8. 调用链

```
用户 ──► Harmony(Agent)
            │  带用户 Bearer token
            ▼
        wim-mcp (MCP, /mcp)
            │  校验 token(可选 JWKS),原样转发
            ▼
   DFSWIM 服务(Workflow / WFM / Common / Well Info)
            │  井级权限在这里/网关执行
            ▼
        返回证据 → 带来源引用、限制说明、状态
```

## 9. 对本项目的启示

wim-mcp 是一个已落地的 MCP 例子,和 [WPO 引入 MCP 需求分析](../../analysis/2026-11-10-wpo-mcp-requirement-analysis.md) 里的设想高度相关,可借鉴的做法:

| 做法 | 可借鉴点 |
| --- | --- |
| 只读证据层 + 不下结论 | 把"取数"和"判断"分开,降低 Agent 误导风险 |
| 状态词汇明确 | `PARTIAL`、`NOT_ANALYSIS_READY`、`RESOLVED/AMBIGUOUS/NOT_FOUND` 等让 Agent 能区分"没数据"和"出错" |
| `resolve_well_name` | 名称有歧义时返回候选,而不是猜(与 UI 自动执行分析里的 `AMBIGUOUS` 思路一致) |
| 占位工具 `NOT_READY` | 缺口显式、机器可读,而不是悄悄缺失 |
| 用户 token 透传 | 不用静态账号,权限由下游执行 |
| 截断显式报告 | 响应过大或行数过多时明确标记,不静默截断 |
| 运维配置地址 | 服务根地址不作为工具参数,防止被诱导调用任意地址 |
| Mock 服务 | 无真实环境也能完整演示和测试 |

## 10. 边界与待确认

- 本文只基于 README;`docs/ARCHITECTURE.md`、`AGENTS.md`、规格文件和 MCP/Prompt/Skills 职责划分方案**未读取**,细节以项目内文档为准。
- README 提到"all three tools",但表格列了 7 个工具(3 个已实现 + 4 个占位),应指 3 个已实现工具。
- 规格文件名为 `DFSWIM Risk Analysis Agent - v1.md`,README 说其标题标识为规格 v2,版本表述需向项目确认。
- Harmony 的具体形态和与 WPO 项目的关系,README 未说明。
