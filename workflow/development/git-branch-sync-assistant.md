# Git 分支自动同步助手

用于批量读取远端分支，并为每个分支生成一个包含当前时间的 update 分支名。

## 目标

- 自动同步远端分支列表（默认 `origin`）。
- 为每个远端分支创建一个新分支。
- 新分支命名包含当前时间，便于追踪。
- 可选：自动推送到远端。
- 可选：在每个新分支提交一份“当前时间更新记录”。

## 脚本位置

- `workflow/development/git-branch-sync-assistant.ps1`

## 分支命名规则

新分支名称格式：

- `sync/<base-branch>/update-<yyyyMMdd-HHmmss>`

示例：

- 基础分支 `main` -> `sync/main/update-20261110-154500`
- 基础分支 `feature/wso-map` -> `sync/feature-wso-map/update-20261110-154500`

说明：

- 脚本会把基础分支名中的 `/` 替换成 `-`，防止层级过深。
- 时间戳在同一次执行中统一，便于批次追踪。
- 默认跳过 `sync/`（或你设置的 `-Prefix`）前缀远端分支，避免递归生成套娃分支。

## 使用方式

在 PowerShell 中执行：

```powershell
# 仅在本地创建分支（不推送）
.\workflow\development\git-branch-sync-assistant.ps1 -RepoPath "C:\path\to\your\repo"

# 创建后自动推送到 origin
.\workflow\development\git-branch-sync-assistant.ps1 -RepoPath "C:\path\to\your\repo" -Push

# 创建 + 推送 + 每个分支提交“当前时间更新记录”
.\workflow\development\git-branch-sync-assistant.ps1 -RepoPath "C:\path\to\your\repo" -Push -CreateCommit
```

## 可选参数

- `-RepoPath`：目标仓库路径，默认当前目录。
- `-Remote`：远端名，默认 `origin`。
- `-Prefix`：分支名前缀，默认 `sync`。
- `-Push`：是否推送新分支到远端。
- `-CreateCommit`：是否在新分支里提交“当前时间更新记录”。

## CreateCommit 行为

启用 `-CreateCommit` 后，会在每个分支生成文件：

- `.branch-sync/update-<base-branch>.md`

并执行：

- `git add -A`（将当前所有改动文件纳入暂存）
- `git commit -m "chore: update current time for <base-branch> (<timestamp>)"`

## 注意事项

- 脚本不会删除任何已有分支。
- 如果目标分支名已存在，会跳过并在结果中标记 `skipped`。
- 执行前建议先 `git fetch --all --prune` 保持远端分支信息最新。
- 如果仓库有严格保护策略，请确认你有推送权限。
