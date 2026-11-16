# Oil Field Know All — Oilfield Project Context

## 这个项目的价值

> **给管理层的一句话**: 这是一个把业务知识、技术经验和交付过程沉淀为可复用资产的项目知识中枢，用于降低协作成本、缩短交接周期并提升交付确定性。

- **知识集中**: 把油田业务知识、技术实现知识、交付经验放在同一知识库，避免信息分散。
- **高效协作**: 统一目录与模板，便于团队成员和 AI Agent 快速定位信息并持续更新。
- **可追溯决策**: 通过 ADR、功能历史、每日记录保留决策与变更背景，支持复盘与交接。
- **对外同步**: 通过沟通模板与 Agent 把内部进展快速整理成站会/周报/发布信息。

## 快速入口

- 打开即看: [AGENTS.md](AGENTS.md)
- 目录导航: [DIRECTORY-INDEX.md](DIRECTORY-INDEX.md)

## Layout

- `business-model/`, `data-model/`, `api/`, `frontend/`, `design-system/`,
  `workflow/`, `skill/`, `project-memory/` — general AI-context categories.
- `domain-knowledge/` — 石油领域专业知识 (drilling, reservoir, production,
  well operations, units & standards).
- `coding-standards/` — project coding conventions.
- `architecture-decision/` — ADRs (see `_template.md`).
- `feature-history/` — chronological feature evolution log (see `_template.md`).
- `analysis/` — requirement/solution analysis documents (scope, options,
  impact, risks, decisions).
- `bug-knowledge/` — recurring bug patterns and fixes (see `_template.md`).
- `performance/` — performance optimization notes (see `_template.md`).
- `testing/` — testing strategy.
- `deployment/` — release process.
- `ai-rules/` — rules an AI coding assistant must follow (`rules.md`).
- `open-questions/` — unresolved items.

See the README.md inside each folder for what belongs there.

## 文档阅读器(MkDocs Material)

- 首次安装:`pip install mkdocs-material`
- <mark>**启动:双击 `serve-docs.bat`,或运行 `python -m mkdocs serve`,浏览器打开 http://127.0.0.1:8000**
- 后台启动(无窗口):双击 `start-docs.bat`;停止:双击 `stop-docs.bat`</mark>
- 修改 `.md` 文件后页面自动刷新;支持全文搜索、暗色模式
- 配置:`mkdocs.yml`;收集文档的逻辑在 `.mkdocs/hooks.py`(排除 `.claude`、`copilot` 等目录)
- 生成静态站点:`python -m mkdocs build`(输出到 `.site/`)

### Runbook:文档阅读器运维手册

#### 1. 前置条件
| 项目 | 要求 | 检查命令 |
|---|---|---|
| Python | 3.9+(已验证 3.12) | `python --version` |
| 依赖 | mkdocs-material | `pip show mkdocs-material` |

#### 2. 首次安装
```bash
pip install mkdocs-material
python -m mkdocs build      # 验证构建成功,输出到 .site/
```

#### 3. 日常启动 / 停止
- 启动:双击 `serve-docs.bat`,或 `python -m mkdocs serve`,访问 http://127.0.0.1:8000
- 停止:终端按 `Ctrl+C`
- 局域网共享给同事:`python -m mkdocs serve -a 0.0.0.0:8000`,同事访问 `http://<你的IP>:8000`(需放行防火墙 8000 端口)
- 改端口:`python -m mkdocs serve -a 127.0.0.1:8080`

#### 4. 新增 / 修改文档
- 直接在仓库任意目录增删改 `.md`,保存后页面自动刷新,无需改配置。
- 导航按目录结构自动生成;目录下放 `README.md` 作为该目录的入口页。
- 想排除某目录:编辑 `.mkdocs/hooks.py` 的 `EXCLUDE_DIRS`。

#### 5. 生成静态站点 / 发布
```bash
python -m mkdocs build        # 输出 .site/,可整体拷贝到任意静态服务器
```
`.site/` 是构建产物,不要手动修改,也不需要提交到版本库。

#### 6. 故障排查
| 现象 | 原因 | 处理 |
|---|---|---|
| `No module named mkdocs` | 未安装依赖 | `pip install mkdocs-material` |
| 端口被占用 / 打不开页面 | 8000 已被使用 | 换端口 `-a 127.0.0.1:8080`,或结束占用进程 |
| 新文档没出现在站点 | 位于被排除目录,或 `serve` 未刷新 | 检查 `EXCLUDE_DIRS`;`Ctrl+C` 后重启 |
| `docs_dir should not be the parent directory...` | 把 `docs_dir` 改成了 `.` | 保持 `docs_dir: .mkdocs`,由 hooks.py 收集文档 |
| 构建出现 `contains a link ... not found` 警告 | 文档内有断链 | 不影响浏览;按警告提示修正链接 |
| 终端中文乱码 | Windows 控制台编码 | 不影响页面;可先执行 `chcp 65001` |
| 启动时出现 EOL 提示 | Material 主题 2027-05-05 停止维护 | `set NO_MKDOCS_2_WARNING=1` 可屏蔽(bat 已设置) |

#### 7. 文件清单
| 文件 | 作用 |
|---|---|
| `mkdocs.yml` | 站点配置(主题、插件、扩展) |
| `.mkdocs/hooks.py` | 收集仓库内 `.md` 的钩子 |
| `.mkdocs/index.md` | 占位页(有根 `README.md` 时自动移除) |
| `serve-docs.bat` | 一键启动脚本 |
| `.site/` | 构建产物(可删,重新构建即生成) |

#### 8. 后续迁移
Material for MkDocs 将于 2027-05-05 停止维护,后继项目为 Zensical,可兼容现有 `mkdocs.yml`:https://zensical.org/docs/compatibility/mkdocs/migration/
