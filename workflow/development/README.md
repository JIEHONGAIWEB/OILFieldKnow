# development

Dev workflow: branching model, code review process, release cadence.

## Git 指令整体使用过程（分支同步助手）

适用命令：

```powershell
.\workflow\development\git-branch-sync-assistant.ps1 -RepoPath "C:\path\to\your\repo"
```

该命令用于按远端分支批量生成带时间戳的 update 分支，可选提交并推送。

### 1. 前置准备

1. 进入目标仓库目录，确认是 Git 仓库。
2. 确认本机可执行 Git 与 PowerShell 脚本。
3. 建议先同步远端信息，避免基线过旧。

建议检查命令：

```powershell
git -C "C:\path\to\your\repo" rev-parse --is-inside-work-tree
git -C "C:\path\to\your\repo" fetch --all --prune
```

### 2. 执行模式

1. 仅创建本地分支（不推送、不提交）

```powershell
.\workflow\development\git-branch-sync-assistant.ps1 -RepoPath "C:\path\to\your\repo"
```

2. 创建并推送远端分支

```powershell
.\workflow\development\git-branch-sync-assistant.ps1 -RepoPath "C:\path\to\your\repo" -Push
```

3. 创建、提交、推送（推荐用于一次性同步当前改动）

```powershell
.\workflow\development\git-branch-sync-assistant.ps1 -RepoPath "C:\path\to\your\repo" -CreateCommit -Push
```

### 3. 分支命名规则

- 新分支格式：`sync/<base-branch>/update-<yyyyMMdd-HHmmss>`
- 示例：`sync/main/update-20261110-100506`
- 同一轮执行共享一个时间戳，便于回溯。

### 4. 提交流程说明（CreateCommit）

启用 `-CreateCommit` 时，流程如下：

1. 切换到新分支。
2. 生成 `.branch-sync/update-<base-branch>.md` 时间记录文件。
3. 执行 `git add -A`，将当前所有改动纳入暂存。
4. 提交信息格式：`chore: update current time for <base-branch> (<timestamp>)`。

### 5. 结果校验

1. 检查本地是否创建成功。

```powershell
git -C "C:\path\to\your\repo" branch --list "sync/*/update-*"
```

2. 检查远端是否推送成功。

```powershell
git -C "C:\path\to\your\repo" ls-remote --heads origin "sync/*/update-*"
```

3. 检查新分支最新提交。

```powershell
git -C "C:\path\to\your\repo" log -1 --pretty=%h%x09%s sync/main/update-20261110-100506
```

### 6. 常见问题

1. 脚本执行被策略拦截。
	使用一次性绕过执行：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\workflow\development\git-branch-sync-assistant.ps1 -RepoPath "C:\path\to\your\repo" -CreateCommit -Push
```

2. 远端出现额外 sync 套娃分支。
	原因是重复把已生成的 sync 分支再次作为输入；建议在脚本中过滤 `<prefix>/` 前缀分支。

3. 推送失败但本地已创建。
	先检查权限与远端保护规则，再单独执行：

```powershell
git -C "C:\path\to\your\repo" push -u origin <new-branch-name>
```
