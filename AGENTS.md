# AGENTS.md

## 这个项目是做什么的（给 Agent 快速理解）

这是一个 **Oil Field Know All** 知识与协作仓库，用于支持 WPO/WPE/WSO 相关的：

- 业务与领域知识沉淀（油气专业知识、术语、模型）
- 技术实现知识沉淀（数据模型、API、前端、设计系统）
- 交付过程知识沉淀（架构决策、功能历史、Bug 经验、测试、部署）
- 团队沟通与 AI 协作（话术模板、沟通 Agent、技能说明）

---

## 这个项目的价值

> **给管理层的一句话**: 这是一个把业务知识、技术经验和交付过程沉淀为可复用资产的项目知识中枢，用于降低协作成本、缩短交接周期并提升交付确定性。

1. **减少重复沟通与重复踩坑**  
   把领域知识、架构决策、Bug 经验和功能演进集中沉淀，避免信息散落在聊天记录里。
2. **提升新人和 Agent 上手速度**  
   有清晰目录、README、互链与模板，能快速理解“项目做什么、在哪里改、怎么改”。
3. **让交付更稳定可追溯**  
   通过 ADR、feature-history、daily-log 等记录，保留“为什么这样做”的上下文，便于复盘。
4. **支持日常协作与管理同步**  
   统一日报/站会/发布沟通入口，把技术变更转成可对外同步的信息。

---

## 打开后先看什么

1. [DIRECTORY-INDEX.md](DIRECTORY-INDEX.md)  
   目录总览，包含“快速入口:每天任务总结与计划”。
2. [PROJECT-OVERVIEW.md](PROJECT-OVERVIEW.md)  
   项目整体背景与结构说明。
3. [README.md](README.md)  
   仓库用途与文档阅读方式（MkDocs）。

---

## 常用入口（高频）

- 每日任务记录与明日计划：
  - [daily-log/README.md](daily-log/README.md)
  - [daily-log/2026-11-06.md](daily-log/2026-11-06.md)
- 站会消息整理：
  - [agents/communication/standup-update.md](agents/communication/standup-update.md)
- 领域知识入口：
  - [domain-knowledge/README.md](domain-knowledge/README.md)

---

## Agent 工作建议

- 先查目录总览，再进入对应领域目录补充/更新文档。
- 文档更新优先保持“可复用、可搜索、可导航”（README + 互链）。
- 日常任务信息优先写入 `daily-log/`，对外同步可使用 standup 模板整理。
