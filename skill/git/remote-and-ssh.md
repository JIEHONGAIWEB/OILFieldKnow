# Git 远程仓库与 SSH 密钥配置

常用场景:把本地项目推到新的 GitHub 仓库、切换/新增远程、用 SSH 代替 HTTPS 认证。

## 1. 关联远程仓库并首次推送(HTTPS)

```bash
git remote add origin https://github.com/<org>/<repo>.git
git branch -M main          # 把当前分支重命名为 main
git push -u origin main     # 首次推送并建立上游跟踪
```

- `-M` 为强制重命名;`-u` 之后可直接用 `git push` / `git pull`。
- 若提示 `remote origin already exists`,说明已有 origin,改用下面的"新增/切换远程"。

## 2. 新增 / 删除 / 切换远程

```bash
git remote -v                                   # 查看现有远程
git remote remove new_origin                    # 删除名为 new_origin 的远程
git remote add new_origin git@github.com:<org>/<repo>.git   # 新增 SSH 地址的远程
git remote set-url origin <新地址>               # 直接修改已有远程地址(更简洁)
```

- 远程名(`origin`、`new_origin`)只是别名,可同时存在多个,推送时指定:`git push new_origin main`。
- HTTPS 地址形如 `https://github.com/...`,SSH 地址形如 `git@github.com:...`。

## 3. 生成 SSH 密钥

```bash
ssh-keygen -t rsa -b 2048 -C "<your-email>"
```

- 按提示回车使用默认路径,生成 `~/.ssh/id_rsa`(**私钥**)和 `~/.ssh/id_rsa.pub`(**公钥**)。
- Windows Git Bash 下公钥路径:`/c/Users/<用户名>/.ssh/id_rsa.pub`。
- 查看公钥内容:`cat ~/.ssh/id_rsa.pub`,复制后到 GitHub → Settings → SSH and GPG keys → New SSH key 粘贴。
- 验证连通:`ssh -T git@github.com`。

### 安全注意
- **只上传公钥(.pub)**,私钥 `id_rsa` 绝不能提交、分享或贴到聊天里。
- 推荐改用更安全的 Ed25519:`ssh-keygen -t ed25519 -C "<your-email>"`(RSA 建议至少 3072/4096 位,2048 偏弱)。
- 建议设置 passphrase,避免私钥泄露后被直接使用。
- 笔记里不要写真实邮箱等个人信息,用占位符。

## 4. 常见问题

| 现象 | 原因 / 处理 |
| --- | --- |
| `remote origin already exists` | 已有 origin;用 `git remote set-url` 或换名字 |
| `Permission denied (publickey)` | 公钥未添加到 GitHub,或未加载私钥(`ssh-add ~/.ssh/id_rsa`) |
| 推送被拒绝(non-fast-forward) | 远程有本地没有的提交;先 `git pull --rebase` 再推送 |
