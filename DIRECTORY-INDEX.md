# 目录总览(Directory Index)

按三大类整理:**知识类(Knowledge)**、**技能类(Skills)**、**沟通类(Communication)**。每个目录都给出英文名、中文含义和用途。

---

## 🚀 <mark>快速入口:每天任务总结与计划</mark>

如果你每天都要写"今天完成了什么、明天计划做什么",优先用这几个位置:

- [daily-log/README.md](daily-log/README.md):说明规范(每天一个 `YYYY-MM-DD.md`)
- [daily-log/2026-11-06.md](daily-log/2026-11-06.md):现成模板(今日完成 / 遇到的问题 / 明日计划)
- [agents/communication/standup-update.md](agents/communication/standup-update.md):把零散输入整理成可直接发送的站会日报
- [agents/communication/daily-review.md](agents/communication/daily-review.md):每日回顾规则(今日完成 / 沉淀价值 / 待跟进 / 遇到的问题 / 明日计划),格式与 `daily-log/` 一致
- [.claude/agents/daily-review.md](.claude/agents/daily-review.md):每日回顾 Claude Code 代理定义
  - 启动方式:<mark>`请使用 daily-review 代理:<今天的工作内容>`</mark>,或 <mark>`请使用 daily-review 代理回顾 daily-log/YYYY-MM-DD.md`</mark>

> 建议日常流程:先用 `daily-review` 把当天的工作整理成回顾并写入 `daily-log/`,再用 `standup-update` 整理成对外同步消息。

---

## 🧭 <mark>快速入口:需求与分析过程沉淀</mark>

当你需要把"需求、分析过程、方案取舍"沉淀成可复用文档时,优先用:

- [analysis/README.md](analysis/README.md):分析文档存放规则与用途
- [analysis/_template.md](analysis/_template.md):分析过程模板（可直接复制）
- [feature-history/requirements-index.md](feature-history/requirements-index.md):需求索引与需求模板

> 建议流程:先写需求索引/需求文档,再在 `analysis/` 记录分析过程与方案取舍。

---

## 🤖 <mark>助手总览:说明与启动调用方式</mark>

仓库内共 **17 个助手条目**,分布在三处:`.claude/agents/`(Claude Code 代理,10 个)、`agents/copilot/`(Copilot Agent,7 个文件,其中 `docs-analysis` 为规范参考、`angularDeveloper` 为未完成模板)、`agents/communication/`(沟通类规则源文件,7 个 + README)。`.claude/agents/` 中的沟通类代理与 `agents/communication/` 的规则保持一一对应,规则只维护一份(见 [agents/communication/README.md](agents/communication/README.md))。

**📘 详细文档:[agents/README.md](agents/README.md)**(每个助手的用途、规则、输入输出、定义文件与启动方式,可直接点击打开)

### 启动方式速查

- **Claude Code 代理**:<mark>在会话中输入 `请使用 <代理名> 代理:<输入内容>`,或 `<原话> <代理名>`</mark>。新增代理文件后需重启会话。
- **Copilot Agent**:<mark>将 `.agent.md` 文件复制到仓库根目录的 `.github/agents/`,然后在 Copilot Chat 的 Agent 下拉中选择对应名称</mark>。(`.github/agents/` 当前仓库中不存在,需要手动创建。)
- **Git 分支同步脚本**:<mark>`.\workflow\development\git-branch-sync-assistant.ps1 -RepoPath "C:\path\to\your\repo"`</mark>(加 `-Push` 推送,加 `-CreateCommit` 生成提交。)

#### Git 分支同步快速操作卡片

1. 准备仓库并同步远端:
	`git -C "C:\path\to\your\repo" fetch --all --prune`
2. 仅创建本地 update 分支:
	`.\workflow\development\git-branch-sync-assistant.ps1 -RepoPath "C:\path\to\your\repo"`
3. 创建并推送:
	`.\workflow\development\git-branch-sync-assistant.ps1 -RepoPath "C:\path\to\your\repo" -Push`
4. 创建 + 提交 + 推送（会 `git add -A` 纳入当前所有改动）:
	`.\workflow\development\git-branch-sync-assistant.ps1 -RepoPath "C:\path\to\your\repo" -CreateCommit -Push`
5. 校验远端结果:
	`git -C "C:\path\to\your\repo" ls-remote --heads origin "sync/*/update-*"`

完整流程文档见 [workflow/development/README.md](workflow/development/README.md)。

### Claude Code 代理(`.claude/agents/`)

| 代理 | 中文含义 | 启动方式 |
|---|---|---|
| `message-polisher` | 消息润色 | <mark>`请使用 message-polisher 代理润色:<内容>`</mark> |
| `code-review-request` | 代码评审请求 | <mark>`请使用 code-review-request 代理:<PR 说明>`</mark> |
| `standup-update` | 站会更新 | <mark>`请使用 standup-update 代理:<今天做了什么>`</mark> |
| `release-announcement` | 发布通知 | <mark>`请使用 release-announcement 代理:<发布内容>`</mark> |
| `meeting-summary` | 会议总结 | <mark>`请使用 meeting-summary 代理:<会议记录>`</mark> |
| `issue-response` | Issue 回复 | <mark>`请使用 issue-response 代理:<问题和进展>`</mark> |
| `doc-sync` | 文档同步 | <mark>`请使用 doc-sync 代理:<文件路径或粘贴内容>`</mark> |
| `doc-translator` | 中译英与要点提取 | <mark>`请使用 doc-translator 代理:<中文文档描述>`</mark> |
| `daily-review` | 每日回顾 | <mark>`请使用 daily-review 代理:<今天的工作内容>`</mark>,或 <mark>`请使用 daily-review 代理回顾 daily-log/YYYY-MM-DD.md`</mark> |
| `git-branch-sync` | Git 分支同步 | <mark>`请使用 git-branch-sync 代理:同步 <仓库路径>`(可加"并推送"/"提交并推送")</mark> |

### Copilot Agent(`agents/copilot/`)

| Agent 文件 | Agent 名称 | 启动方式 |
|---|---|---|
| `zh-AngularDEveloper.agent.md` | `angularDeveloper`(中文版) | <mark>复制到 `.github/agents/`,Copilot Chat 选择 `angularDeveloper`</mark> |
| `Senior Angular Engineer + Requirement Analyst + Reviewer.agent.md` | `angularDeveloper`(英文版) | <mark>复制到 `.github/agents/`,Copilot Chat 选择 `angularDeveloper`(与中文版同名,只启用一个)</mark> |
| `Message Polisher Agent.agent.md` | `Message Polisher Agent` | <mark>复制到 `.github/agents/`,Copilot Chat 选择 `Message Polisher Agent`</mark> |
| `git-branch-sync-assistant.agent.md` | `Git Branch Sync Assistant` | <mark>复制到 `.github/agents/`,Copilot Chat 选择 `Git Branch Sync Assistant`;或直接运行脚本</mark> |
| `discuss-docs.agent.md` | 无 frontmatter(角色提示词) | 文件未定义启动方式(待确认) |
| `docs-analysis.agent.md` | 文档目录规范 | 不可直接调用,作为规范参考 |
| `angularDeveloper.agent.md` | 模板(未完成) | 暂无启动方式 |

---

## 一、知识类 Knowledge

> 项目与业务"是什么、为什么"——事实、模型、规范、历史。

### 1.1 业务与领域知识

| 目录 / 文件 | 中文含义 | 内容 |
|---|---|---|
| `domain-knowledge/` | 领域知识 | 油气专业知识 |
| ├ `drilling/` | 钻井 | 钻井相关概念 |
| ├ `reservoir/` | 油藏 | 油藏工程概念 |
| ├ `production/` | 生产 | ESP 井监控、气举井监控、SF 气井监控、产油率 KPI |
| ├ `well-operations/` | 井作业 | 井作业相关 |
| ├ `units-and-standards/` | 单位与标准 | 单位换算、行业标准 |
| ├ `glossary.md` | 术语表 | 领域术语 |
| ├ `wpo-surveillance-concepts.md` | WPO 监控概念 | 生产优化监控概念（英文） |
| ├ `wpo-surveillance-concepts-zh.md` | WPO 监控概念（中文版） | 生产优化监控概念中文译文 |
| ├ `well-model-management.md` | 井模型管理 | Well Model Management 看板的业务背景 |
| └ `spe-insight-agent.md` | SPE Insight Agent | DS365.ai 中基于 SPE 论文的 AI 助手(帖子翻译) |
| `business-model/` | 业务模型 | 业务域(`domains/`)、业务流程(`workflows/`)、术语 |

### 1.2 技术知识

| 目录 | 中文含义 | 内容 |
|---|---|---|
| `data-model/` | 数据模型 | 实体(entities)、关系(relationships)、枚举(enums)、示例(examples) |
| `api/` | 接口 | REST、GraphQL、WebSocket、接口契约(contracts) |
| `frontend/` | 前端 | 页面(pages)、路由(routing)、状态(state) |
| `design-system/` | 设计系统 | 字体(typography)、间距(spacing)、组件(components)、图表(charts) |
| `coding-standards/` | 编码规范 | 前端 Angular + PrimeNG 规范 |
| `architecture-decision/` | 架构决策记录(ADR) | 为什么这样设计,例如 Module Federation Remote |
| `testing/` | 测试 | 测试策略 |
| `deployment/` | 部署 | 部署说明 |
| `performance/` | 性能 | 性能问题与优化记录 |

### 1.3 项目记忆与历史

| 目录 / 文件 | 中文含义 | 内容 |
|---|---|---|
| `project-memory/` | 项目记忆 | 业务记忆、编码记忆、Bug 记忆 |
| `bug-knowledge/` | Bug 知识库 | 已知问题与解决方案 |
| `feature-history/` | 功能历史 | 各功能的演进记录 |
| `analysis/` | 分析沉淀 | 需求分析、方案对比、影响评估、风险记录 |
| `open-questions/` | 待确认问题 | 尚未解决的疑问 |
| `daily-log/` | 每日日志 | 按日期的工作记录 |
| `PROJECT-OVERVIEW.md` | 项目概览 | 项目整体介绍 |

---

## 二、技能类 Skills

> "怎么做"——可复用的做事方法、流程、Agent 与 Skill。

### 2.1 项目做法说明 `skill/`

| 目录 | 中文含义 |
|---|---|
| `skill/angular/` | Angular 做法 |
| `skill/chart/` | 图表做法 |
| `skill/code-review/` | 代码评审做法 |
| `skill/git/` | Git 做法(含 `clone-project`) |
| `skill/testing/` | 测试做法 |
| `workflow/` | 工作流:业务(business)、开发(development)、部署(deployment) |
| `ai-rules/` | AI 规则:约束 AI 如何协作 |

### 2.2 Copilot Skill `skill/copilot/`

| Skill | 中文含义 | 用途 |
|---|---|---|
| `commit-message-scope-resolver` | 提交信息 scope 推荐 | 根据改动的文件路径推荐 Conventional Commit 的 scope |
| `commit-to-skill` | 提交转技能 | 把一次成功的 commit 快照转成可复用的 Skill 说明 |
| `dfs-angular-upgrade` | DFS Angular 升级 | 分步骤指导 Angular 版本迁移 |
| `dfs-frontend-review` | DFS 前端评审 | 按 DFS 规范评审 Angular/PrimeNG 代码 |
| `docs-update-each-chat` | 每次对话更新文档 | 代码或配置改动后同步更新 docs |
| `olivia-analysis-address-requirement-completion-ratio` | 地址需求完成率分析 | 统计某地址的需求总量、完成量、完成比例并提示风险 |
| `olivia-analysis-code-architecture` | 代码架构分析 | 帮助理解陌生、遗留或复杂的代码库 |
| `olivia-bus-doc` | 业务文档脚手架 | 一键生成"AI 上下文优先"的项目目录结构 |
| `olivia-oil-doc` | 油田文档脚手架 | 生成油田知识库目录结构 |
| `olivia-design-plan` | 设计方案 | 方案设计 |
| `olivia-doc-week-report` | 文档周报 | 根据最近的功能文档生成周报 |
| `olivia-docs-acticture` | 文档结构 | 文档结构整理 |
| `olivia-git-opt` | Git 优化 | Git 操作优化 |
| `olivia-targeted-commit` | 精准提交 | 按指定范围安全提交,强制 Conventional Commits |
| `pre-push-safety` | 推送前安全检查 | 检查未跟踪文件、分支命名、远端、上游跟踪、最近一次提交 |

### 2.3 Agent

> 每个助手的完整说明与启动调用方式见上方「助手总览」章节,详细文档见 [agents/README.md](agents/README.md)。

| 位置 | 中文含义 | 内容 |
|---|---|---|
| `agents/copilot/` | Copilot Agent | Angular 开发 Agent(英文版 / 中文版)、需求分析 + 评审 Agent、文档讨论、文档分析、消息润色 |
| `.claude/agents/` | Claude Code 代理 | 沟通类代理,以及 `doc-sync`(文档同步)、`doc-translator`(中译英与要点提取) |

---

## 三、沟通类 Communication

> "怎么说"——话术模板与消息生成 Agent。

### 3.1 话术模板 `communication/`

| 文件 | 中文含义 | 内容 |
|---|---|---|
| `email.md` | 邮件模板 | 请求协助等邮件 |
| `feedback.md` | 反馈、催办话术 | 正向反馈、催办 |
| `meeting.md` | 会议用语 | 开场、讨论、收尾 |

### 3.2 沟通 Agent `agents/communication/`

| Agent | 中文含义 | 场景 |
|---|---|---|
| `message-polisher` | 消息润色 | 口语 / 零散表达 → 可发送的专业消息 |
| `code-review-request` | 代码评审请求 | 向队友发起 PR Review |
| `standup-update` | 站会更新 | 每日 Standup 文字更新 |
| `release-announcement` | 发布通知 | 功能上线 / Bug 修复通知 |
| `meeting-summary` | 会议总结 | 对齐会、复盘会总结 |
| `issue-response` | Issue 回复 | 向问题报告人说明状态和进展 |

### 3.3 翻译 `translations/`

| 目录 | 中文含义 | 内容 |
|---|---|---|
| `translations/` | 翻译归档 | 中译英及要点清单,按日期命名 |

---

## 速查:我要找什么?

| 我想…… | 去哪里 |
|---|---|
| 查业务 / 油气概念 | `domain-knowledge/`、`business-model/` |
| 查字段、接口、页面 | `data-model/`、`api/`、`frontend/` |
| 查为什么这样设计 | `architecture-decision/` |
| 查某个 Bug 怎么解决 | `bug-knowledge/` |
| 找可复用的做事流程 | `skill/`、`workflow/` |
| 写提交、推送代码 | `skill/copilot/olivia-targeted-commit`、`pre-push-safety` |
| 润色消息、写站会、写发布通知 | `agents/communication/` |
| 写邮件、会议、催办话术 | `communication/` |
