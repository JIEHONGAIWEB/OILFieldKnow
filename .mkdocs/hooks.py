"""把仓库根目录下的所有 .md 文件加入站点(MkDocs 不允许 docs_dir 是配置文件的父目录)。"""
import os
from mkdocs.structure.files import File

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXCLUDE_DIRS = {".claude", ".site", ".mkdocs", ".git", "node_modules", "copilot"}


def on_files(files, config):
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        for name in filenames:
            if not name.lower().endswith(".md"):
                continue
            rel = os.path.relpath(os.path.join(dirpath, name), ROOT).replace(os.sep, "/")
            if rel == ".mkdocs/index.md":
                continue
            files.append(File(rel, ROOT, config["site_dir"], config["use_directory_urls"]))
    # 根目录 README.md 作为首页:移除占位 index.md
    names = {f.src_uri for f in files}
    if "README.md" in names:
        for f in list(files):
            if f.src_uri == "index.md":
                files.remove(f)
    return files


# 侧边栏顺序与标题:先置顶的根文件,再依次为 知识类 → 技能类 → 沟通类(与 DIRECTORY-INDEX.md 一致)
PINNED_PAGES = ["README.md", "DIRECTORY-INDEX.md", "PROJECT-OVERVIEW.md"]
SECTIONS = [
    # (目录名, 侧边栏标题)
    # ---- 知识类 ----
    ("domain-knowledge", "知识 · 领域知识 Domain Knowledge"),
    ("business-model", "知识 · 业务模型 Business Model"),
    ("data-model", "知识 · 数据模型 Data Model"),
    ("api", "知识 · 接口 API"),
    ("frontend", "知识 · 前端 Frontend"),
    ("design-system", "知识 · 设计系统 Design System"),
    ("coding-standards", "知识 · 编码规范 Coding Standards"),
    ("architecture-decision", "知识 · 架构决策 Architecture Decisions"),
    ("testing", "知识 · 测试 Testing"),
    ("deployment", "知识 · 部署 Deployment"),
    ("performance", "知识 · 性能 Performance"),
    ("project-memory", "知识 · 项目记忆 Project Memory"),
    ("bug-knowledge", "知识 · Bug 知识库 Bug Knowledge"),
    ("feature-history", "知识 · 功能历史 Feature History"),
    ("open-questions", "知识 · 待确认问题 Open Questions"),
    ("daily-log", "知识 · 每日日志 Daily Log"),
    # ---- 技能类 ----
    ("skill", "技能 · 做法 Skills"),
    ("workflow", "技能 · 工作流 Workflow"),
    ("ai-rules", "技能 · AI 规则 AI Rules"),
    # ---- 沟通类 ----
    ("communication", "沟通 · 话术模板 Phrases"),
    ("agents", "沟通 · 沟通 Agent Communication Agents"),
    ("translations", "沟通 · 翻译归档 Translations"),
]


def _first_src(item):
    if getattr(item, "file", None) is not None:
        return item.file.src_uri
    for child in getattr(item, "children", None) or []:
        found = _first_src(child)
        if found:
            return found
    return None


def on_nav(nav, config, files):
    order = {d: i for i, (d, _) in enumerate(SECTIONS)}
    titles = dict(SECTIONS)

    def key(item):
        src = _first_src(item) or ""
        if src in PINNED_PAGES:
            return (0, PINNED_PAGES.index(src))
        top = src.split("/")[0]
        if top in order:
            return (1, order[top])
        return (2, 0)  # 未登记的放最后,保持原有相对顺序

    for item in nav.items:
        src = _first_src(item) or ""
        top = src.split("/")[0]
        if hasattr(item, "children") and top in titles:
            item.title = titles[top]
    nav.items.sort(key=key)  # sort 稳定
    return nav
