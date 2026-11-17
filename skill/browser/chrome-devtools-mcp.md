# Chrome DevTools MCP + Edge 调试浏览器

当 Claude 无法直接抓取页面(内网、需要 SSO 登录、需要 JS 渲染)时,用 Chrome DevTools MCP 控制一个真实浏览器。

## 它是什么

Google Chrome 团队发布的 MCP server(npm 包 `chrome-devtools-mcp`),底层使用 Puppeteer + Chrome DevTools Protocol,让 Claude Code 控制并检查真实浏览器。

能力:

- 操作页面:打开/切换/关闭标签页,点击、输入、填表、截图、等待元素
- 调试:读控制台日志和报错,查看网络请求/响应(状态码、头、body)
- 性能分析:录制 performance trace(LCP 等),模拟 CPU/网络限速
- DOM 与样式:页面快照,检查元素

## 本机配置(已完成)

用户级 MCP(写入 `~/.claude.json`),连接已打开的调试浏览器:

```bash
claude mcp add --scope user chrome-devtools -- npx -y chrome-devtools-mcp@latest --browserUrl http://127.0.0.1:9222
```

等价的 `.mcp.json` / VS Code MCP 配置:

```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["-y", "chrome-devtools-mcp@latest", "--browserUrl", "http://127.0.0.1:9222"]
    }
  }
}
```

不带 `--browserUrl` 时,它会自己启动一个全新的 Chrome(没有登录态)。

## Edge 调试浏览器快捷方式

桌面已创建 `Edge Debug 9222.lnk`,目标等价于:

```
"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --remote-debugging-port=9222 --user-data-dir="C:\EdgeDebug" --no-first-run
```

要点:

- `--user-data-dir=C:\EdgeDebug` 是独立 profile,必须有,否则调试端口不生效(新版 Chromium 要求非默认 profile)。
- 首次使用在这个窗口里手动登录一次 SSO,登录态会保存在 `C:\EdgeDebug`,之后复用。
- 启动前先关闭其他用这个 profile 的 Edge 窗口。
- 验证:浏览器访问 http://127.0.0.1:9222/json/version 能返回 JSON 即成功。

## 使用流程

1. **双击桌面 `Edge Debug 9222`**,在打开的 Edge 里登录需要的内网站点(首次登录后会保存在 `C:\EdgeDebug`,之后不用重复登录)
2. **重启 Claude Code 会话**(新增的 MCP 需要重新加载),输入 `/mcp` 确认 `chrome-devtools` 已连接
3. **对 Claude 说**,例如:
   - `用 chrome-devtools 打开 <URL> 并截图`
   - `读取这个页面的控制台报错`
   - `用 chrome-devtools 查看这个页面的网络请求,找出失败的接口`
   - `用 chrome-devtools 打开 <GitLab pipeline URL>,告诉我哪个 job 失败了`

> 每次使用前,先确认调试浏览器已打开(访问 http://127.0.0.1:9222/json/version 能返回 JSON),否则 MCP 会连接失败。

## 注意

- 9222 端口等于完全控制该浏览器,仅监听本机,不要对外暴露,不要用这个 profile 登录个人账号。
- 相关:`gitlab-pipeline-monitor` skill 也用它查看 GitLab pipeline/job 页面。
