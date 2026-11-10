# 助手详细文档(Agents Detail)

本页汇总仓库内全部 **17 个助手条目**的用途、规则、输入输出、定义文件与启动调用方式。
返回入口:[DIRECTORY-INDEX.md](../DIRECTORY-INDEX.md)

---

## 总览

| 助手 | 类型 | 定义文件 | 启动方式 |
|---|---|---|---|
| [message-polisher](#message-polisher) | Claude Code 代理 | [.claude/agents/message-polisher.md](../.claude/agents/message-polisher.md) | <mark>`请使用 message-polisher 代理润色:<内容>`</mark> |
| [code-review-request](#code-review-request) | Claude Code 代理 | [.claude/agents/code-review-request.md](../.claude/agents/code-review-request.md) | <mark>`请使用 code-review-request 代理:<PR 说明>`</mark> |
| [standup-update](#standup-update) | Claude Code 代理 | [.claude/agents/standup-update.md](../.claude/agents/standup-update.md) | <mark>`请使用 standup-update 代理:<今天做了什么>`</mark> |
| [release-announcement](#release-announcement) | Claude Code 代理 | [.claude/agents/release-announcement.md](../.claude/agents/release-announcement.md) | <mark>`请使用 release-announcement 代理:<发布内容>`</mark> |
| [meeting-summary](#meeting-summary) | Claude Code 代理 | [.claude/agents/meeting-summary.md](../.claude/agents/meeting-summary.md) | <mark>`请使用 meeting-summary 代理:<会议记录>`</mark> |
| [issue-response](#issue-response) | Claude Code 代理 | [.claude/agents/issue-response.md](../.claude/agents/issue-response.md) | <mark>`请使用 issue-response 代理:<问题和进展>`</mark> |
| [doc-sync](#doc-sync) | Claude Code 代理 | [.claude/agents/doc-sync.md](../.claude/agents/doc-sync.md) | <mark>`请使用 doc-sync 代理:<文件路径或粘贴内容>`</mark> |
| [doc-translator](#doc-translator) | Claude Code 代理 | [.claude/agents/doc-translator.md](../.claude/agents/doc-translator.md) | <mark>`请使用 doc-translator 代理:<中文文档描述>`</mark> |
| [daily-review](#daily-review) | Claude Code 代理 | [.claude/agents/daily-review.md](../.claude/agents/daily-review.md) | <mark>`请使用 daily-review 代理:<今天的工作内容>`</mark> |
| [git-branch-sync](#git-branch-sync) | Claude Code 代理 | [.claude/agents/git-branch-sync.md](../.claude/agents/git-branch-sync.md) | <mark>`请使用 git-branch-sync 代理:同步 <仓库路径>`(可加"并推送"/"提交并推送")</mark> |
| [zh-angulardeveloper](#zh-angulardeveloper) | Copilot Agent(中文版) | [zh-AngularDEveloper.agent.md](copilot/zh-AngularDEveloper.agent.md) | <mark>Copilot Chat 选择 `angularDeveloper`</mark> |
| [senior-angular-engineer](#senior-angular-engineer) | Copilot Agent(英文版) | [Senior Angular Engineer + Requirement Analyst + Reviewer.agent.md](<copilot/Senior Angular Engineer + Requirement Analyst + Reviewer.agent.md>) | <mark>Copilot Chat 选择 `angularDeveloper`</mark> |
| [message-polisher-agent](#message-polisher-agent) | Copilot Agent | [Message Polisher Agent.agent.md](<copilot/Message Polisher Agent.agent.md>) | <mark>Copilot Chat 选择 `Message Polisher Agent`</mark> |
| [git-branch-sync-assistant](#git-branch-sync-assistant) | Copilot Agent | [git-branch-sync-assistant.agent.md](copilot/git-branch-sync-assistant.agent.md) | <mark>Copilot Chat 选择 `Git Branch Sync Assistant`</mark>,或<mark>直接运行脚本</mark> |
| [discuss-docs](#discuss-docs) | Copilot 角色提示词 | [discuss-docs.agent.md](copilot/discuss-docs.agent.md) | 文件未定义启动方式(待确认) |
| [docs-analysis](#docs-analysis) | 文档目录规范 | [docs-analysis.agent.md](copilot/docs-analysis.agent.md) | 不可直接调用,作为规范参考 |
| [angularDeveloper 模板](#angulardeveloper-模板) | Copilot Agent 模板 | [angularDeveloper.agent.md](copilot/angularDeveloper.agent.md) | 未完成,暂无启动方式 |

---

## 启动方式

### Claude Code 代理

在 Claude Code 会话中用自然语言指定代理名称:

- `请使用 <代理名> 代理:<输入内容>`
- 也可以写成 `<原话> <代理名>`(以 message-polisher 为例)

代理定义位于 [.claude/agents/](../.claude/agents/)。新增代理文件后需要重启会话才能识别。

### Copilot Agent

1. 在仓库根目录创建 `.github/agents/`(当前仓库中不存在)。
2. 把需要的 `.agent.md` 文件复制到该目录。
3. 在 Copilot Chat 的 Agent 下拉中选择对应名称(见各助手的"启动方式")。

注意:`zh-AngularDEveloper` 与 `Senior Angular Engineer + ...` 的 Agent 名称都是 `angularDeveloper`,同一仓库只启用其中一个。

### 脚本调用

```powershell
.\workflow\development\git-branch-sync-assistant.ps1 -RepoPath "C:\path\to\your\repo"
.\workflow\development\git-branch-sync-assistant.ps1 -RepoPath "C:\path\to\your\repo" -Push
.\workflow\development\git-branch-sync-assistant.ps1 -RepoPath "C:\path\to\your\repo" -Push -CreateCommit
```

---

## 一、Claude Code 代理

沟通类代理(除 doc-sync、doc-translator 外的 7 个)的规则统一维护在 [communication/](communication/) 下的同名文件中。代理只负责读取规则并输出成品,不另行定义规则。

### message-polisher

- **定义文件**:[.claude/agents/message-polisher.md](../.claude/agents/message-polisher.md)
- **规则来源**:[communication/message-polisher.md](communication/message-polisher.md)
- **工具**:Read
- **用途**:把口语、零散的表达整理成可直接发送的专业中文消息。
- **规则要点**:
  - 固定输出中文(除非明确要求翻译)。
  - 保留原意,不增删信息,不推测业务背景。
  - 控制在 1–5 句话,只输出成品。
- **不负责**:技术实现说明、代码总结、需求分析、文档编写。
- **启动**:<mark>`请使用 message-polisher 代理润色:<内容>`,或 `<原话> message-polisher`</mark>。
- **示例**:输入"我已经改好了,你有空帮我看看有没有问题。",输出可直接发送的中文消息。

### code-review-request

- **定义文件**:[.claude/agents/code-review-request.md](../.claude/agents/code-review-request.md)
- **规则来源**:[communication/code-review-request.md](communication/code-review-request.md)
- **工具**:Read
- **用途**:生成向 reviewer 发起 PR Review 的请求消息。
- **输出结构**:`改了什么` / `为什么改` / `请重点看`,PR 链接放在显眼位置。
- **规则要点**:
  - 始终输出中文,控制在 3–6 句话或要点列表加结尾致谢。
  - 用户提到紧迫性(如"今天要上")时需礼貌说明。
  - 不推测用户未提及的技术细节,不解释代码内部实现。
- **不负责**:汇总整个 PR diff、解释架构决策、生成 PR description。
- **启动**:<mark>`请使用 code-review-request 代理:<PR 说明>`</mark>。

### standup-update

- **定义文件**:[.claude/agents/standup-update.md](../.claude/agents/standup-update.md)
- **规则来源**:[communication/standup-update.md](communication/standup-update.md)
- **工具**:Read
- **用途**:把零散工作内容整理成站会消息。
- **输出结构**:**昨天** / **今天** / **阻碍**三段。
- **规则要点**:
  - 每条为"一个动作 + 一个结果或状态"。
  - 没有阻碍时写"无",不能省略该段。
  - 全文不超过 10 行;保留任务单号和 PR 号。
- **不负责**:解释 bug 修复细节、重新排序条目、添加时间估算。
- **启动**:<mark>`请使用 standup-update 代理:<今天做了什么>`</mark>。

### release-announcement

- **定义文件**:[.claude/agents/release-announcement.md](../.claude/agents/release-announcement.md)
- **规则来源**:[communication/release-announcement.md](communication/release-announcement.md)
- **工具**:Read
- **用途**:生成功能上线或 Bug 修复的发布通知。
- **输出结构**:标题 `📢 [模块] 已发布` / 发布内容 / 影响范围 / 是否需要操作 / 已知问题(有则写)。
- **规则要点**:
  - 不添加用户未提及的变更;不解释内部实现。
  - 需要用户操作的事项(如刷新页面、清缓存)单独标出。
  - 控制在 6–10 行。
- **不负责**:完整 Release Notes、Changelog、替代 PR description 或 ADR。
- **启动**:<mark>`请使用 release-announcement 代理:<发布内容>`</mark>。

### meeting-summary

- **定义文件**:[.claude/agents/meeting-summary.md](../.claude/agents/meeting-summary.md)
- **规则来源**:[communication/meeting-summary.md](communication/meeting-summary.md)
- **工具**:Read
- **用途**:把会议笔记整理成会议总结(对齐会、复盘会等)。
- **输出结构**:背景 / 结论 / 待确认 / 行动项(表格:事项、负责人、截止时间)。
- **规则要点**:
  - 不添加会议中未提及的内容,不推测未达成共识的决策。
  - 责任人或截止时间不明确时写"待确认"。
  - 行动项必须具体;控制在 15 行以内。
- **不负责**:记录完整对话过程、替代正式会议纪要。
- **启动**:<mark>`请使用 meeting-summary 代理:<会议记录>`</mark>。

### issue-response

- **定义文件**:[.claude/agents/issue-response.md](../.claude/agents/issue-response.md)
- **规则来源**:[communication/issue-response.md](communication/issue-response.md)
- **工具**:Read
- **用途**:回复 Bug / Issue 报告人,说明状态和进展。
- **输出结构**:
  - 已定位根因时:感谢反馈 → 根因 → 当前状态 → 预计修复时间。
  - 尚在排查时:已收到 → 当前排查进展 → 需要对方提供的信息。
- **规则要点**:
  - 不承诺用户未说明的修复时间;根因未明时如实说"正在排查",不编造原因。
  - 口语化,去掉"经核对""麻烦""如有其他问题请随时告知"等套话。
  - 控制在 3–8 句话。
- **不负责**:技术根因分析、Incident Report、Post-mortem。
- **启动**:<mark>`请使用 issue-response 代理:<问题和进展>`</mark>。

### daily-review

- **定义文件**:[.claude/agents/daily-review.md](../.claude/agents/daily-review.md)
- **规则来源**:[communication/daily-review.md](communication/daily-review.md)
- **工具**:Read
- **用途**:把当天零散的工作记录整理成每日回顾,格式与 `daily-log/` 保持一致。
- **输出结构**:**今日完成** / **沉淀价值** / **待跟进** / **遇到的问题** / **明日计划**五段。
- **规则要点**:
  - 只整理用户提供或文件中已有的内容,不添加未提及的完成项、问题或计划。
  - 未完成事项放入「待跟进」,不归入「今日完成」。
  - 「沉淀价值」只写用户明确说明的价值;没有则写"无"。
  - 无问题写"暂无",无计划写"待定",各段不得省略;全文 25 行以内。
- **不负责**:站会消息(使用 standup-update)、周报/月报、解释 bug 技术原因、修改历史日期日志(除非明确要求)。
- **启动**:<mark>`请使用 daily-review 代理:<今天的工作内容>`</mark>,或 <mark>`请使用 daily-review 代理回顾 daily-log/YYYY-MM-DD.md`</mark>。

### git-branch-sync

- **定义文件**:[.claude/agents/git-branch-sync.md](../.claude/agents/git-branch-sync.md)(Claude Code 版,与 [git-branch-sync-assistant](#git-branch-sync-assistant) 规则一致)
- **工具**:Read、Glob、Grep、Bash。
- **用途**:一句话完成 fetch → 创建 `sync/<base>/update-<时间戳>` 分支 → (可选)提交 → (可选)推送 → 校验远端。
- **输入**:仓库路径;模式(默认仅本地创建 / 创建并推送 / 创建+提交+推送)。
- **输出**:`base branch | new branch | status` 结果表格,并列出失败/跳过项。
- **安全规则**:不 reset / 不删除 / 不 force push;推送与 `git add -A` 提交前先确认并展示 `git status`。
- **首选脚本**:[git-branch-sync-assistant.ps1](../workflow/development/git-branch-sync-assistant.ps1);完整流程见 [workflow/development/README.md](../workflow/development/README.md)。
- **启动**:<mark>`请使用 git-branch-sync 代理:同步 C:\path\to\your\repo 并推送`</mark>。

### doc-sync

- **定义文件**:[.claude/agents/doc-sync.md](../.claude/agents/doc-sync.md)
- **规则来源**:本文件内置(路由表直接写在定义文件中)
- **工具**:Read, Write, Edit, Glob, Grep, Bash
- **用途**:按路由规则把文档归类并同步到知识库对应文件夹,同时更新目标文件夹 README 索引。
- **自动触发**:描述中包含"同步/归档/整理/分发文档到对应目录"时。
- **工作流程**:
  1. 读取指定文件或粘贴文本。
  2. 按路由表判定类型;无法判定或命中多个时列出候选目录请用户确认。
  3. 同步(复制而非移动),沿用原文件名;粘贴文本用 `YYYY-MM-DD-简短英文主题.md`。
  4. 更新目标目录 `README.md` 索引。
- **规则要点**:
  - 目标同名文件已存在时先对比;相同则跳过,不同则询问用户,不擅自覆盖。
  - 不删除文件;移动操作需用户明确要求。
  - 只在知识库根目录内操作,不碰 `.claude/` 等隐藏或临时文件。
- **输出**:Sync Result 表格、Needs Confirmation、Index Updates。
- **启动**:<mark>`请使用 doc-sync 代理:<文件路径或粘贴内容>`</mark>。

### doc-translator

- **定义文件**:[.claude/agents/doc-translator.md](../.claude/agents/doc-translator.md)
- **规则来源**:本文件内置
- **工具**:Read, Write, Edit, Glob, Grep
- **用途**:把中文文档或描述翻译成英文,并提取关键信息清单。
- **自动触发**:描述中包含"翻译文档、提取要点列表"时。
- **输出结构**:Translation(译文)+ Key Information(主题、关键术语、人员/部门、日期、指标、待办事项)。
- **规则要点**:
  - 保持原意与格式;不确定的术语在译文后标注 `(?)` 并在末尾列出请用户确认。
  - 每次翻译自动保存到 [translations/](../translations/),文件名 `YYYY-MM-DD-简短主题.md`;同名文件加序号,不覆盖。
  - 原文已是英文则只做信息提取。
- **启动**:<mark>`请使用 doc-translator 代理:<中文文档描述>`</mark>。

---

## 二、Copilot Agent

Copilot 的 `.agent.md` 文件位于 [copilot/](copilot/)。启动统一为:复制到 `.github/agents/` 后在 Copilot Chat 的 Agent 下拉中选择。

### zh-angulardeveloper

- **定义文件**:[zh-AngularDEveloper.agent.md](copilot/zh-AngularDEveloper.agent.md)
- **Agent 名称**:`angularDeveloper`(中文版)
- **工具**:read, search, edit, execute, todo
- **参数提示**:输入需求文档、Jira、设计稿(Figma)、Bug 描述、优化需求或开发任务。
- **用途**:企业级 Angular 交付(以 Tech Lead 视角)。
- **工作流程**:12 个阶段依次执行:需求发现 → 需求对比 → 架构评审 → 修改清单 → 影响分析 → 方案设计(至少两个方案)→ 任务拆分 → 开发前 Review → 代码实现 → Self Review → 验证 → 交付。
- **核心原则**:没有完成需求分析前不允许直接写代码;不猜测业务逻辑;优先复用;不修改无关代码。
- **代码标准**:优先 Standalone Component、Signal、`inject()`、OnPush、async pipe、trackBy;避免 `any`、嵌套 subscribe、内存泄漏。
- **每次输出包含**:需求总结、新旧对比、架构评审、修改清单、影响分析、技术方案、Task 拆分、风险、验收标准、修改文件、实现、Self Review、Validation、Deliverables。
- **完成定义(DoD)**:业务、架构、开发、测试、质量、文档、发布七类检查项全部满足。
- **启动**:<mark>复制到 `.github/agents/` → Copilot Chat 选择 `angularDeveloper`</mark>。

### senior-angular-engineer

- **定义文件**:[Senior Angular Engineer + Requirement Analyst + Reviewer.agent.md](<copilot/Senior Angular Engineer + Requirement Analyst + Reviewer.agent.md>)
- **Agent 名称**:`angularDeveloper`(英文版)
- **工具**:read, search, edit, execute, todo
- **用途**:与中文版相同的 12 阶段交付流程,英文撰写。
- **与中文版的差异**:内容结构一致;英文版的 Expected Output 为 14 项,Phase 与 DoD 表述更简练。
- **启动**:<mark>复制到 `.github/agents/` → Copilot Chat 选择 `angularDeveloper`</mark>。⚠️ 与中文版同名,只启用一个。

### message-polisher-agent

- **定义文件**:[Message Polisher Agent.agent.md](<copilot/Message Polisher Agent.agent.md>)
- **Agent 名称**:`Message Polisher Agent`(文件无 frontmatter,名称取自标题)
- **用途**:把口语化表达改写为自然、简洁的英文消息,可直接发到 Teams / Slack。
- **规则要点**:
  - 默认输出英文;输入为中文时输出英文(可配置)。
  - 保持原意,不增删信息,不推测业务背景。
  - 控制在 2–5 句话。
- **不负责**:技术实现说明、Code Review 总结、需求分析、文档编写。
- **启动**:<mark>复制到 `.github/agents/` → Copilot Chat 选择 `Message Polisher Agent`</mark>。

### git-branch-sync-assistant

- **定义文件**:[git-branch-sync-assistant.agent.md](copilot/git-branch-sync-assistant.agent.md)
- **Agent 名称**:`Git Branch Sync Assistant`
- **模型与工具**:模型 GPT-5.3-Codex;工具 run_in_terminal、read_file、list_dir。
- **用途**:同步远端分支,为每个远端分支生成带时间戳的 update 分支。
- **分支命名**:`sync/<base-branch>/update-<yyyyMMdd-HHmmss>`;`<base-branch>` 中的 `/` 替换为 `-`;同一批次使用统一时间戳。
- **工作流程**:
  1. 确认仓库路径与远端(默认 `origin`)。
  2. 执行 `git fetch --all --prune`。
  3. 枚举 `origin/*` 分支(排除 `origin/HEAD`)。
  4. 逐个创建更新分支。
  5. 如需要则推送到远端。
  6. 输出结果表格:`base branch | new branch | status`。
- **安全规则**:不做破坏性操作(不 reset、不删除分支);已存在的分支跳过并标记;单个失败记录后继续。
- **首选脚本**:[git-branch-sync-assistant.ps1](../workflow/development/git-branch-sync-assistant.ps1),脚本不存在时才临时构造命令。
- **启动**:
  - Agent 方式:<mark>复制到 `.github/agents/` → Copilot Chat 选择 `Git Branch Sync Assistant`</mark>。
  - 脚本方式:见上方"脚本调用"。

### discuss-docs

- **定义文件**:[discuss-docs.agent.md](copilot/discuss-docs.agent.md)
- **Agent 名称**:无 frontmatter;文件以角色"Senior Frontend Reviewer"开头。
- **用途**:对代码变更或需求生成评审摘要和团队沟通消息。
- **输出结构**:Quick Summary、Main Changes、Risks、Suggested Review Focus、Teams Message。
- **规则要点**:使用要点列表;Teams Message 不超过 150 字。
- **启动**:文件未定义启动方式(待确认)。可作为提示词内容粘贴到对话中使用。

### docs-analysis

- **定义文件**:[docs-analysis.agent.md](copilot/docs-analysis.agent.md)
- **类型**:文档目录规范,不是可调用的 Agent。
- **内容**:需求文档目录 `docs/requirements/` 的结构与职责,包括 README(当前最新需求)、`versions/`(历史版本,禁止修改)、change-log、bug-history、enhancement-history、decision-log、open-questions、developer-guide、qa-checklist、release-notes、glossary、assets。
- **原则**:每个功能只有一个最新版本;历史版本永久保留;所有需求变更、Bug、优化都必须可追踪。
- **启动**:不适用,作为规范参考。

### angularDeveloper 模板

- **定义文件**:[angularDeveloper.agent.md](copilot/angularDeveloper.agent.md)
- **状态**:未完成的模板。description 与正文仍为占位文字。
- **启动**:暂无可用启动方式。完成后再参照上方 Copilot 启动步骤使用。

---

## 三、注意事项

- **同名冲突**:中文版与英文版 Angular 助手的 Agent 名称都是 `angularDeveloper`,同一仓库只启用其中一个。
- **缺少 `.github/agents/`**:仓库中没有该目录,首次使用 Copilot Agent 前需要手动创建并复制文件。
- **无 frontmatter 的文件**:`discuss-docs`、`docs-analysis` 与 `Message Polisher Agent` 没有 frontmatter,在 Copilot 中的识别方式取决于运行环境,使用前建议先验证。
- **规则只维护一份**:沟通类代理的规则在 [communication/](communication/) 中维护,修改后 Claude Code 代理会自动读取最新内容。
