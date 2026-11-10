# agents/communication — 团队沟通 Agent 集合

将开发人员的口语化表达整理成可直接发送的专业消息。

所有 Agent 默认**输出中文**。

---

## Agent 列表

| 文件 | 用途 | 典型场景 |
|------|------|----------|
| [message-polisher.md](message-polisher.md) | 通用消息润色 | 任意零散表达 → 可发送的消息 |
| [code-review-request.md](code-review-request.md) | Code Review 请求 | 向队友发起 PR Review |
| [standup-update.md](standup-update.md) | Daily Standup | 每日站会文字更新 |
| [release-announcement.md](release-announcement.md) | 发布通知 | 功能上线 / Bug 修复发布 |
| [meeting-summary.md](meeting-summary.md) | 会议总结 | 对齐会、复盘会、快速沟通后的总结 |
| [issue-response.md](issue-response.md) | Bug / Issue 回复 | 回复问题报告人，说明状态和进展 |

---

## 使用方式

将对应的 `.md` 文件内容作为 Agent 的 system prompt，然后输入你的口语表达即可。

所有 Agent 的输出均可直接复制粘贴发送，无需二次编辑。

---

## 作为 Claude Code 代理调用

已在 `.claude/agents/` 注册同名代理(内部会读取本目录对应文件,规则只维护一份):

| 代理名 | 示例 |
|--------|------|
| message-polisher | 请使用 message-polisher 代理润色:<内容> |
| code-review-request | 请使用 code-review-request 代理:<PR 说明> |
| standup-update | 请使用 standup-update 代理:<今天做了什么> |
| release-announcement | 请使用 release-announcement 代理:<发布内容> |
| meeting-summary | 请使用 meeting-summary 代理:<会议记录> |
| issue-response | 请使用 issue-response 代理:<问题和进展> |

新增的代理文件需重启会话才能被识别。

---

## Message Polisher 使用详解

把口语化、零散的话整理成可直接发给同事的消息,**意思不变**。

### 两个版本

| 版本 | 位置 | 输出语言 |
|------|------|----------|
| Claude Code 版 | [message-polisher.md](message-polisher.md) | 固定输出中文(除非明确要求翻译) |
| Copilot 版 | `agents/copilot/Message Polisher Agent.agent.md` | 默认英文,输入中文时输出英文(可配置) |

### 在 Claude Code 中使用

```text
请使用 message-polisher 代理润色:看你今天有时间,10分钟,找你 quick review 一下,修改逻辑正确。
```

输出:

```text
你今天如果有 10 分钟的话,方便帮我做个 Quick Review 吗?

主要帮我确认一下修改逻辑是否正确。

谢谢!
```

也可以简写为:`<你的原话> message-polisher`。

### 在 GitHub Copilot 中使用(英文版)

1. 把 `Message Polisher Agent.agent.md` 放进仓库的 `.github/agents/` 目录。
2. 在 Copilot Chat 的 Agent 下拉中选择 **Message Polisher Agent**。
3. 直接输入口语内容,例如"我已经改好了,你有空帮我看看有没有问题。"
4. 输出为英文,可直接复制到 Teams / Slack。

### 在其他工具中使用

将对应 `.md` 文件的全文作为 system prompt,然后输入原话即可。

### 规则与边界

- **会做**:保留原意;语气自然、礼貌、专业;控制在 1–5 句话;输出可直接发送。
- **不会做**:不补充你没说的信息;不推测业务背景;不做技术分析、代码总结、需求分析;不写文档。
- **有歧义时**:保持原意,不自行推断。信息不够时,请先把背景补进输入里。
- **需要英文**:Claude Code 版可在指令中加一句"请翻译成英文"。

### 示例

| 输入 | 输出 |
|------|------|
| 我已经改好了,你有空帮我看看有没有问题。 | 我已经修改好了。<br>你有空的时候帮我看一下有没有问题,谢谢! |
| 这个我还不太确定,你帮我确认一下。 | 这个地方我还不是很确定。<br>方便帮我确认一下吗? |
| 这个先别合,我还要改一点。 | 这个先别合并,我还需要再修改一点。<br>我改好后再通知你,谢谢! |
