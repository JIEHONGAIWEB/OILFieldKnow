# Subsurface Studio:Harmony 扩展的完整示例项目

**日期:** 2026-11-12
**来源:** Subsurface Studio 项目 README(用户提供的文本)
**状态:** 摘要与分析(只基于 README;`docs/capabilities.md`、`docs/architecture.md`、`docs/demo-script.md` 及源码未读取)

> Related: [DFS AI Assistant 项目说明](dfs-ai-assistant-overview.md)、
> [DFS Dojo Armour 项目介绍](dfs-dojo-armour-overview.md)、
> [UI 自动执行 + Agent Steps 分析](../analysis/2026-11-12-ui-automation-agent-steps-analysis.md)、
> [dspdm-mcp](../api/mcp/dspdm-mcp.md)、[wim-mcp](../api/mcp/wim-mcp.md)。

## 1. 一句话

**Subsurface Studio 是一个完整的 Harmony 扩展(extension)示例**,面向**油藏建模与测井解释**,场景是一个合成油田 **Aurora**。它在一个能跑的项目里展示 Harmony 扩展能带来的**全部能力**:界面、多 Agent 团队、聊天里的组件、工作流、MCP 服务、自带后端,以及"界面借工具给 Agent、Agent 反过来操作界面"。

定位是两件事:**演示 Harmony 能做什么**,以及**作为模板,在做自己的扩展时复制**。所有数据(Aurora、Northwind Demo Energy、井和数字)都是合成的,不来自真实油田。

## 2. 它展示了哪些能力

| 能力 | 在本项目里的体现 |
| --- | --- |
| **Harmony 壳里的视图** | 油田地图、测井曲线查看器、产量图表、实时钻井数据流 |
| **4 个协同的 Agent** | 3 个在扩展里声明,1 个自带(BYO,纯 LangGraph);含子代理(其中一个私有)、共享/私有/借用的技能、记忆、审批、护栏、引用、评分标准(rubric)、中间件、动态脚本 |
| **5 个聊天组件** | Agent 和工作流可以在聊天里画出来:`log-plot`、`pay-summary`、`production-chart`、`volumetrics-card`、`screening-board` |
| **3 个工作流** | 2 个在工作流画布上画(其中一个是聊天型),1 个用代码写 |
| **第二个无界面扩展** | 一个技能库,第一个扩展依赖它 |
| **MCP 服务** | 工具、一个 MCP App、一个资源和提示词 |
| **扩展自己的后端** | 经 Harmony 网关访问 |
| **视图借工具给 Agent** | 聊天可以驱动屏幕(选井、缩放、高亮) |
| **视图发起 API 写入** | 视图能启动工作流并流式显示 |

## 3. 项目结构

```
extension/                    Harmony 扩展(manifest harmony.dev/v2)
  manifest.json               扩展提供什么、允许访问什么
  index.html, src/            视图(React)和聊天卡片(React),用 Vite 构建
  agents/<name>/              subsurface-lead、petrophysicist、reservoir-engineer、production-engineer(BYO)
  skills/<name>/              petrophysics-playbook、reserves-reporting、aurora-scripts(脚本技能)
  components/<name>/          log-plot、pay-summary、production-chart、volumetrics-card、screening-board
  workflows/<name>/           well-screening 和 drilling-desk(画布),volumetrics-report(代码)
library/                      subsurface-library:无界面扩展,含一个共享技能及其脚本
services/subsurface-data/     Aurora 数据服务(Python):MCP 在 /mcp,REST 在 /v1
services/production-engineer/ BYO Agent(Python,LangGraph),经 Harmony Agent Protocol 访问
scripts/showcase.sh           启动、发布、安装、绑定,一步到位
tools/emit-workflow.mjs       从图重新生成画布工作流脚本
vendor/                       本次构建安装的 Harmony npm 包
docs/                         实现说明和现场演示脚本
```

关键设计:**数据服务有两张脸**——给 Agent 用 MCP,给视图用 REST。两者读同一份数据。

## 4. 四个 Agent 的分工

| Agent | 角色(根据名称推断) | 备注 |
| --- | --- | --- |
| `subsurface-lead` | 团队负责人:读井数据、画组件、通过借来的工具操作视图 | 在示例里读井、画 log-plot、选井、缩放、高亮 |
| `petrophysicist` | 岩石物理:测井解释(示例提到 Simandoux 解释) | 可在 Agent 选择器里直接选 |
| `reservoir-engineer` | 油藏工程:剩余采收率、储量报告 | 示例里被 lead 请教,也写储量说明 |
| `production-engineer` | 生产工程 | **BYO Agent**:用 LangGraph 写,独立服务,经 Harmony Agent Protocol 接入,运行在 Claude 上 |

> 各 Agent 的具体职责以 `agents/<name>/system_prompt.md` 为准,上表是基于名称和示例的推断。

## 5. 试用场景(来自 README)

**在界面旁边的聊天里:**

| 提问 | 发生什么 |
| --- | --- |
| "看一下 AUR-02:净产层多少?画测井图并在视图里高亮产层" | lead 经 MCP 读井 → 画 log-plot 组件 → 通过视图借出的工具选井、缩放、高亮产层 |
| "按净产层大小显示油田地图,圈出最好的两口井" | MCP App;点井看井卡片,再点 "Interpret this well" 把消息送回聊天 |
| "AUR-11 现在钻头在钻什么?" | 实时钻井数据流 |
| "问问油藏工程师 AUR-01 的剩余采收量" | lead 委托给 reservoir-engineer |
| 在 Agent 选择器选 Petrophysicist,要求对 AUR-06 做 Simandoux 解释 | 直接和专业 Agent 对话 |

**在扩展页面(或视图顶部的 Workflows):**

| 工作流 | 发生什么 |
| --- | --- |
| Well Screening | 用默认参数启动,回答它提出的问题,看筛选看板出现 |
| Volumetrics Report | P90/P50/P10 卡片;油藏工程师写储量说明;若开启收件箱,会收到通知 |

`docs/demo-script.md` 是 15 分钟的演示讲解稿。

## 6. 运行

**前置:** Docker、Node 20+、uv、一份 Harmony 源码(需先构建 single 容器镜像:在 `projects/harmony/vnext` 运行 `./dev single build`)。`hmny` 命令行来自同一源码(`clients/hmny-cli-ts`)或 Harmony 的开发者页面(`?view=dev`)。

**环境变量(README 给了三个):** `HARMONY_REPO`(Harmony 源码的 vnext 目录)、`HMNY_BASE_URL`、`HMNY_TENANT_ID`。

**一条命令:** `scripts/showcase.sh up`,依次做五步,每步可单独执行:

| 步骤 | 做什么 |
| --- | --- |
| `secrets` | 写 `.env`(两个随机密钥)和 `.harmony.env`(把密钥绑定给 Harmony) |
| `harmony` | 用 `.harmony.env` 重启 Harmony single(数据卷保留) |
| `data` | 构建数据服务和 BYO Agent,在 Harmony 的网络命名空间内启动(`127.0.0.1:8710` 与 `:8720`) |
| `publish` | 发布库;再打包扩展(构建视图并封装)并发布 |
| `install` | 信任发布者,在工作区安装两个扩展,授予 API 写权限,绑定后端 |

然后打开 `http://127.0.0.1:2024/?view=subsurface-studio`。`scripts/showcase.sh status` 查看运行状态。从另一个终端重新 `./dev single up` 之后,要再运行一次 `scripts/showcase.sh data`,因为数据服务与 single 容器共享网络,要跟着它走。

## 7. 如何改造成自己的扩展

各部分相互独立,一次改一处:

| 部分 | 怎么改 |
| --- | --- |
| 数据 | 把 `services/subsurface-data/aurora/` 换成对自己系统的调用;**保留两张脸**:MCP 给 Agent,REST 给视图 |
| Agent | 改 `agents/*/system_prompt.md` 和设置;工具名格式是 `<server>__<tool>` |
| 组件 | 在 `components/<name>/` 写 `component.json` 的 schema,在 `src/cards/<name>/` 写 React 卡片;数据太大、不适合让模型传递时,用 `backend_get` 读取 |
| 视图 | 改 `extension/src/`;**所有对 Harmony 的调用都经 `harmony.*`**,沙箱里 `localStorage` 和 `fetch` 不能用 |
| 工作流 | 在扩展编辑器里打开(`?view=extension-editor&id=subsurface-studio`),或运行 `hmny dev ext serve extension` 让画布和文件夹保持同步 |

发布注意:改 `manifest.json` 里的 `id`、`name`、`publisher`;**每次发布都要提升 `version`,版本不可变**。部署到本地 single 容器之外时,要改 Agent 和工作流设置里的 MCP 地址,以及绑定里的后端地址(见 `docs/architecture.md`)。

## 8. 对 Harmony 版本的要求

这个示例是边构建边发现 Harmony 缺口的产物,需要以下修复:

| 修复 | 没有它会怎样 |
| --- | --- |
| 停靠式聊天要让组件能读自己的数据(`HarmonyChat` 上的 `serverTools`,由扩展聊天面板设置) | 测井图和产量图在停靠聊天里画不出来 |
| 声明了子代理的工作流必须能完成初始化(`workflow_runner.py`),作为子代理使用的成员要拿到自己的组件(`resolver.py`) | 带子代理的工作流在初始化时失败 |
| 推理代理要向 BYO Agent 提供 Anthropic 接口(`/v1/inference/anthropic/...`,适配器 SDK 里 `chat_model(request, api_type="anthropic-compatible")`),因为 production-engineer 和其他 Agent 一样运行在 Claude 上 | BYO Agent 失败 |

## 9. 测试

| 内容 | 命令 |
| --- | --- |
| 数据、鉴权、REST 和 MCP | `cd services/subsurface-data && uv run pytest` |
| 视图类型检查 | `cd extension && npm run typecheck` |
| 清单和成员检查 | `hmny extension check extension` |

## 10. 分析:对本项目的价值

### 10.1 为什么值得关注

它是目前看到的**最完整的"Harmony 扩展长什么样"**的参考:把界面、Agent、组件、工作流、MCP 和后端放在一个能跑通的例子里,并且有能力到文件的对照文档。我们之前的几份分析(Model Management / Scheduler 的 Agent 化、UI 自动执行)都可以拿它当落地参照。

### 10.2 与已有分析的对应

| 本项目的做法 | 对应的已有分析 | 意义 |
| --- | --- | --- |
| **视图借工具给 Agent**(选井、缩放、高亮) | [UI 自动执行分析](../analysis/2026-11-12-ui-automation-agent-steps-analysis.md) 的方案 A:应用内语义动作 | 这是同一思路的**已有实现**:前端把动作登记给 Agent,聊天驱动屏幕。Model Management / Scheduler 可以按同样方式借出"打开创建任务、预填触发设置"之类的工具 |
| **视图发起 API 写入,启动工作流并流式显示** | 同上,"确认后提交"与结果跟踪 | 写入需要在安装时被授予("grants API writes"),说明写权限有显式授权这一层 |
| **聊天里画组件**(log-plot、volumetrics-card 等) | [Agent-Native 分析](../analysis/2026-11-10-wpo-agent-native-opportunity-analysis.md) 的 VizSpec、组件注册表 | 组件 = `component.json` schema + React 卡片,与"Agent 选画什么,前端决定怎么画"一致 |
| **`backend_get`:数据太大时由组件自己读取,不经过模型** | Agent-Native 的"Agent 引用数据而不是复述数据" | 同一个原则:避免模型抄错数 |
| **MCP 与 REST 两张脸** | [dspdm-mcp](../api/mcp/dspdm-mcp.md)、[wim-mcp](../api/mcp/wim-mcp.md) | 数据服务一份数据,Agent 走 MCP,界面走 REST |
| **多 Agent 团队 + 子代理 + 审批 + 护栏 + 引用 + rubric** | Agent-Native 的流程沉淀与评估 | 示例里有可参照的实现点 |
| **工作流画布 + 代码工作流 + 无界面技能库** | [Scheduler 教程](../frontend/dfs-workflow-scheduler-tutorial.md) 的工作流概念 | Harmony 的"工作流"是另一套机制,不要和 DFS Workflow Scheduler 混为一谈(见下) |

### 10.3 与 WPO 场景的映射(推断)

| Subsurface Studio | WPO 里可对应的 |
| --- | --- |
| Well Screening 工作流 | 批量井筛选,例如试井校验或异常井筛选 |
| Volumetrics Report | 周期性报告类工作流 |
| petrophysicist / reservoir-engineer / production-engineer | WPO 里的试井、模型校准、监控优化等角色型 Agent(对应 [WPO 核心工作流链路](../business-model/workflows/wpo-core-workflow-chain.md)) |
| 聊天里画图并在视图里高亮 | 在 WSO / Model Management 里让聊天驱动筛选与选井 |
| 合成数据服务(Aurora) | 开发期用合成数据,避免依赖真实环境 |

### 10.4 值得借鉴的做法

- **合成数据**:全部数据生成,没有真实油田数据,适合演示和测试。
- **数据服务同时有 MCP 和 REST**,职责清楚。
- **能力到文件的映射文档**(`docs/capabilities.md`),便于新人找到"这个能力在哪个文件"。
- **一键脚本**(`showcase.sh`)把启动、发布、安装、绑定串起来,每步可单独运行。
- **版本不可变**,每次发布都升版本。
- **沙箱约束**:视图里不能用 `localStorage` 和 `fetch`,所有调用走 `harmony.*`,便于控制权限。
- **记录平台缺口**:把构建时发现的 Harmony 缺陷列成"需要的修复"。

## 11. 边界与待确认

- 本文只基于 README,未读 `docs/capabilities.md`、`docs/architecture.md`、`docs/demo-script.md`,也没有看源码和 `manifest.json`;各 Agent 的职责、各组件的 schema 以项目内文件为准。
- 你贴的步骤表格在粘贴时被压成一行,我按五个步骤(secrets / harmony / data / publish / install)重新整理,内容应与原文一致。
- README 里 `HMNY_BASE_URL` 是 `:2025`,而浏览器访问地址是 `:2024`,两者的关系(端口映射或不同服务)README 没说明。
- 这里的"工作流"指 **Harmony 的工作流**(画布或代码),与 DFS 的 Workflow Scheduler(调度已发布工作流)是不同的东西;两者能否衔接未说明。
- 能否在 WPO 的 Model Management / Scheduler 上直接用同样的扩展机制,取决于它们是否运行在 Harmony 壳内,需向团队确认。
- 示例依赖三项 Harmony 修复,是否已合入主线,README 没说。
