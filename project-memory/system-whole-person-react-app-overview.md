# systemWholePerson / react-app:项目介绍与文档集成

**收录日期:** 2026-11-10
**本地路径:** `C:\Users\h224847\code\学习-code\react\react-app`
**远程仓库:** `https://github.com/JIEHONGAIWEB/systemWholePerson`(台账中的"维护长久-项目建设",见 [long-term-maintenance-register.md](long-term-maintenance-register.md))
**类型:** 个人学习/实验项目 + AI 协作工作台(非 WPO 业务代码)
**来源:** 项目 README、`AGENTS.md`、`docs/`、`skills/`、`src/master/`、`public/docs/system-manual.md` 等;内容以仓库为准。

> Related: [WPO Agent-Native 机会分析](../analysis/2026-11-10-wpo-agent-native-opportunity-analysis.md)、
> [DFS Dojo Armour 介绍](dfs-dojo-armour-overview.md)、
> [AI Agent 趋势探索](../analysis/2026-11-10-ai-agent-trend-exploration-analysis.md)。

## 1. 一句话

一个基于 **Create React App** 的"**个人工作台 + AI-first 知识仓库**":把本地代码/组件预览、网址书签、站内文档、流程图实验室、华夏文明地图/日历集中到一个菜单页;同时用 `AGENTS.md`、`skills/`、`prompts/`、`docs/` 把"每次对话都沉淀可复用知识"变成仓库规则,并用 **LangGraph** 做了一条"需求 → 拆分 → 代码"的自动生成流水线(master workflow)。

> 仓库根 `README.md` 其实是 CRA 默认说明 + 一段 AI 技能入口,真正的系统介绍在 `public/docs/system-manual.md`。

## 2. 真正的价值

1. **AI-first 仓库治理的完整样板**:`AGENTS.md` 规定"聊天是过程,docs 才是交付物";固定的知识落点(requirements / architecture / decisions / implementation / runbooks / knowledge / open-questions);配套 `templates/`(ADR、API、Bug、Decision、Feature、Skill)。可直接复制到别的项目。
2. **把"沉淀"做成技能**:`docs-update-each-chat`、`docs-project-bootstrap-notes`(v1–v3)、`olivia-docs-acticture`(建文档结构)、`olivia-targeted-commit`、`olivia-git-opt`、`commit-to-skill` 等,把"做完一件事就记录成文档/技能"自动化。这正是 [WPO Agent 分析 5.5](../analysis/2026-11-10-wpo-agent-native-opportunity-analysis.md) 里"用户自己沉淀流程"的个人版实践。
3. **一条跑得通的 Agent 流水线原型**:LangGraph `analysis → split → code`,能读需求 md、读 skill 作为提示、调用 Claude(服务端或本地 `claude --print` CLI)生成代码,前端可在 Spike 预览区直接触发并展示结构化结果。
4. **文档系统本身是产品**:站内文档可新增/编辑/重命名/删除/拖拽排序/搜索,通过本地 `docs-server` 写回 `public/docs/`;流程图可保存到 `docs/flowcharts`。
5. **踩坑已记录**:LangGraph 节点命名、ESM/CJS、浏览器不能打包 Anthropic Node SDK、Node 20 的 EBADENGINE 等,都有 IMPL/ARCH 文档。

## 3. 技术栈

| 部分 | 技术 |
| --- | --- |
| 前端 | React 19、`react-scripts` 5(CRA)、Ant Design 6、ReactFlow 11(流程图)、ECharts 6、MapLibre GL 5(地图)、Mermaid 11 |
| Agent | `@langchain/langgraph` 1.x、`langchain` 1.x、`@langchain/core`、`@langchain/anthropic`、`@anthropic-ai/sdk` |
| 本地服务 | `scripts/docs-server.js`(Node `http`,默认端口 3100,CRA 通过 `proxy` 代理) |
| 数据 | `public/data/`(日历、年度结果、积分 JSON)、`public/docs/`(站内文档,含 timeline 与 flowcharts) |
| 测试 | Testing Library、Jest(CRA 自带) |

常用命令:`npm start`(前端)、`npm run docs:server`(文档写回服务,需另开)、`npm run crawl:analyze`(爬虫分析)、`node scripts/run-master-workflow.js "<需求>"`(跑 master 工作流)。

## 4. 功能模块地图

| 模块 | 位置 | 说明 |
| --- | --- | --- |
| 工作台菜单 + 预览 | `src/olivia/`、`src/core/plugins/` | 菜单聚合(`menuRegistry`)+ 预览路由(`previewRegistry`)均为**插件链**;菜单配置在 `src/plugins/links/config/*`(file/work/learn/docs/design/plan/knowledge) |
| 站内文档系统 | `public/docs/`、`scripts/docs-server.js` | 左侧目录支持搜索、拖拽排序(可跨分类)、折叠、分类标题编辑、空分类 |
| 流程图实验室 | `src/component/FlowchartLab.js`、`FlowchartDrawLab.js` | 节点增删改、样式(背景/边框色)、复制样式、树形排版、**父节点拖拽联动子节点**、自动保存、多流程、保存到/加载自 `docs/flowcharts` |
| 华夏文明地图与日历 | `src/spike/HuaxiaCivilization.js`、`map-info/` | 多区域叠加图层、日期详情面板与 docs 文件双向同步、积分面板、LinkBoard;日历面板可对年度事件做时间序列解析、按主题分类并**同步生成文档与同名流程图** |
| 节点地图可视化 | REQ-20260714 | 读取全部节点上图,按年份/关键字筛选,列表/详情联动,缺坐标提示 |
| 图形/动效实验 | `src/spike/*`(Blob、Neon、Halo、Canvas 等) | 视觉实验 |
| 数据/爬虫 | `src/code/`、`scripts/crawler-analyze.js` | 衍生数据与爬虫分析 |
| **master workflow** | `src/master/` | 见第 5 节 |

## 5. master workflow(LangGraph 需求→代码流水线)

```
__start__ → analysis_node → split_node → code_node → __end__
```

| 节点 | 文件 | 职责 |
| --- | --- | --- |
| `analysis_node` | `requirement.node.js` | 需求分析 |
| `split_node` | `split.node.js` | 拆分功能列表(featureList),读取 skill |
| `code_node` | `code.node.js`(含 `code.browser.js` / `code.server.js`) | 生成代码;server 分支调用 `claude --print` |

- **共享状态**(`state.js`,`Annotation.Root`):`requirement`、`requirementFilePath`、`outputPath`、`planInput`、`analysis`、`skillExecution`、`featureList`、`generator`、`codeMeta`、`code`。
- **Skill 注入**:`skill/readAllSkills.js` 用 `ChatPromptTemplate` 聚合多个 `SKILL.md`;默认读取 `olivia-design-plan`(技术交付规划师:目标→交付物→功能→任务→依赖→风险→顺序→计划);读到 ZIP/二进制会报错,避免污染提示词。
- **模型路由**:浏览器优先请求后端 `POST /api/llm/anthropic/generate-code`(密钥只在服务端 `ANTHROPIC_API_KEY`);失败回退 OpenAI `gpt-4o-mini`;再失败用兜底代码。`codeMeta.provider` 记录来源。
- **本地 Claude Code CLI**:`src/master/claude-local/callClaudeCLI-local.js` 用 `spawn("claude", args, { cwd, stdio: ["ignore","pipe","pipe"] })`,忽略 stdin 避免挂起。
- **入口**:`scripts/run-master-workflow.js` 对 `src/master` 打 Babel 补丁(源码是 ESM,而项目未声明 `"type": "module"`);也可在 Spike 预览区的 `MasterWorkflowExample` 触发。
- **当前限制**:纯线性图,**无条件分支、无循环、无 checkpoint**。

### 踩坑清单

1. `StateGraph` 必须传入 state schema(`AgentStateAnnotation`)。
2. 节点名不能与 state 字段重名(如 `analysis`、`code`),所以统一以 `_node` 结尾。
3. CRA(Webpack 5)不能把 Anthropic Node 依赖打进浏览器 bundle;密钥不要放浏览器 localStorage。
4. 当前 Node 20 对部分包有 `EBADENGINE`(要求 ≥ 22)警告,未阻断。
5. `reaearch/` 目录名为现有拼写,勿"顺手改"以免断引用。

## 6. `docs/` 知识落点(AGENTS.md 规定)

| 目录 | 用途 | 命名 |
| --- | --- | --- |
| `requirements/` | 需求、用户故事、验收标准 | `REQ-YYYYMMDD-slug` |
| `architecture/` | 架构图、模块关系、数据流 | `ARCH-YYYYMMDD-slug` |
| `decisions/` | ADR,只追加不删改 | — |
| `implementation/` | 实现细节与非显然逻辑 | `IMPL-YYYYMMDD-slug` |
| `runbooks/` | 部署/回滚/排障/验证步骤 | `RB-slug` |
| `knowledge/` | 领域知识、选型、踩坑 | `KB-slug` |
| `open-questions/` | 待决事项 | `OQ-slug-YYYYMMDD` |
| `context/` | 与本仓库 OILFieldKnow 同构的分类(api、business-model、data-model、design-system、frontend、project-memory、skills、workflow) | — |

另有 `memory/`(conversations / checkpoints / summaries,存放长期会话产物,区别于 `docs/context/project-memory` 的整理版)。

**编码政策:** Requirements → Architecture → Tasks → Code → Review → Knowledge。**知识政策:** 出现新业务规则、架构、API、流程、编码模式,立即更新对应文档。

## 7. 技能(`skills/`)与提示词(`prompts/`)

| 技能 | 用途 |
| --- | --- |
| `docs-update-each-chat` | 每次对话后分析做了什么并记录成文档 |
| `docs-project-bootstrap-notes`(v1/v2/v3,中英文) | 把文档型提交快照转成可复用的"新项目经验沉淀"指令;v3 用最小 `applyTo`、非破坏性 |
| `olivia-docs-acticture` | 为整个项目新建文档结构 |
| `olivia-targeted-commit` / `olivia-git-opt` / `commit-message-scope-resolver` / `commit-to-skill` / `pre-push-safety` / `git-remote-set.sh` | Git 提交、范围、推送安全与远程设置 |
| `olivia-design-plan` | 设计文档 → 技术交付计划(**注意:原件是 docx,已转换且 XML 有损坏,二进制备份保留**) |
| `olivia-analysis-address-requirement-completion-ratio` | 分析某地址的需求完成率(默认把 done/closed/completed/已完成/已关闭 视为完成) |
| `olivia-test-plan-todo-list` | 测试计划与待办 |
| `dfs-angular-upgrade` / `dfs-frontend-review` | DFS Angular 升级与前端评审 |
| 目录型占位 | `Angular`、`Azure`、`Cytoscape`、`ECharts`、`MapLibre`、`Oilfield`、`RxJS`、`TypeScript`、`Git` |

`prompts/` 含 architecture、debug、optimize、react-developer、doc-update、clear、read 等通用提示,`prompts/done/` 存已完成任务的提示。

## 8. 站内文档中值得读的内容(`public/docs/`)

- **`system-manual.md`**:系统说明书(定位、运行方式、菜单→预览主链路、插件注册表)。
- **`AI做什么.md`**:提出 **Runtime = AI 的大脑操作系统**,职责:Memory 加载(每天创建 memory)、Context 压缩(场景化)、Tool 调用(沉淀的 tool)、Agent 生命周期(start/end/条件)、Token 预算、Cache、Routing。
- **`学习一次性完成10个feature.md`**:先让 AI **只出计划不写代码**:Feature List、依赖、实现顺序、风险、每个 Feature 涉及的文件。
- **`新建项目的沉淀.md`**:每次操作都用技能记录成文档的工作法。
- 另有 changelog、crawler-manual、timeline(按日期的大量时间线文档)、flowcharts(含 `分析wpo`、`ai-coding-框架` 两张与本主题相关的流程图 JSON)。

## 9. 与 WPO Agent 想法的对照

| WPO Agent 分析中的概念 | 此项目中的对应 | 可借鉴/差距 |
| --- | --- | --- |
| 5.5 用户自己沉淀流程 | 技能 + `docs-update-each-chat` + 模板 | 已有"沉淀"习惯和格式;**缺"可复用性测试"**(泛化/重放/黄金样例) |
| 5.3 动态界面引擎 / 组件注册表 | 菜单插件链 + 预览插件链(`menuRegistry` / `previewRegistry`) | 插件注册表思想一致,可作为"组件注册表"的轻量参考 |
| 流程引擎(Workflow Engine → Skills / Planner / Multi-Agent → Tool Calling → Context → Memory) | `IMPL-20260703` 流程图 + master workflow | 概念图已有,实现只有线性三节点 |
| 5.2 数据发现、工具调用 | 暂无 | 未涉及 |
| Human-in-the-loop 确认 | 暂无 | master workflow 无确认节点、无 checkpoint |
| 评估与审计 | 暂无 | 无评估集,无调用日志 |
| 权限 | 暂无 | `.env` 与 API Key 管理较简单 |

**可直接复用到 WPO Agent 的几点:**
1. `AGENTS.md` 的"聊天是过程,docs 是交付物"政策与目录约定。
2. "先出计划不写代码"的多 feature 工作法(Feature List / 依赖 / 顺序 / 风险 / 涉及文件)。
3. 技能聚合注入提示词的做法(`readAllSkills`)。
4. LangGraph 的状态定义与节点命名规则。
5. 服务端持有密钥、浏览器只调后端的模型路由模式。

## 10. 优化空间

- **master workflow**:加审查节点 + 条件边(失败重试/修订循环);引入 checkpointer 支持中断恢复;加人工确认节点;记录每次运行的输入、技能、模型、输出以便审计和回放。
- **技能质量**:`olivia-design-plan` 的原件 XML 有损坏,宜从原文档重新导出 UTF-8 markdown;目录型技能占位(Oilfield、ECharts 等)尚无内容。
- **评估**:为技能和工作流建立黄金样例与回归测试(对应分析 5.5 的可复用性测试)。
- **工程化**:仓库根 `README.md` 仍是 CRA 默认内容,宜改写为真正的入口;`build/` 与 `node_modules/` 体积大,确认 `.gitignore` 是否已排除;Node 版本升级到 ≥ 22 消除 EBADENGINE;`reaearch/` 拼写在不破坏引用前提下修正。
- **安全**:`.env` 与密钥管理(只在服务端读取,不入库);docs-server 的路径校验已限制 `/docs/` 前缀并拒绝 `..`,新增接口时保持同等校验。
- **未决事项**:`huaxia-score-2.json` 的正式消费链路未确认(见仓库 `OQ-scoredata-source-20260702`)。

## 11. 如何使用本文

- 想复用"AI-first 仓库规则":看第 6、7 节,复制 `AGENTS.md`、`templates/`、`docs/` 结构。
- 想做 Agent 工作流:看第 5 节与踩坑清单。
- 想对照 WPO Agent 路线:看第 9 节。
