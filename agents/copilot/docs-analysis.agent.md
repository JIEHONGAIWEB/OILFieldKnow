
# 📁 Documentation Workspace Standard（文档目录规范）

所有需求文档必须按照统一目录进行维护。

原则：

- 每个功能只有一个最新版本（README.md）
- 所有历史版本永久保留
- 所有需求变更必须记录
- 所有 Bug 必须可追踪
- 所有优化必须可回溯
- 所有文档持续更新（Living Documentation）

```
docs/
└── requirements/
    ├── README.md                 # 当前最新需求概览（Latest Requirement）
    │
    ├── versions/                 # 历史版本
    │   ├── v1.0.md
    │   ├── v1.1.md
    │   ├── v1.2.md
    │   └── v2.0.md
    │
    ├── change-log.md             # 所有需求变更记录
    ├── bug-history.md            # Bug 修复历史
    ├── enhancement-history.md    # 功能优化历史
    ├── decision-log.md           # 技术/业务决策（ADR）
    ├── open-questions.md         # 待确认问题
    ├── developer-guide.md        # 前端开发指南
    ├── qa-checklist.md           # QA 测试清单
    ├── release-notes.md          # 发布说明
    ├── glossary.md               # 业务术语
    └── assets/                   # 图片、流程图、设计截图
```

---

## 📄 每个文档职责

### README.md

始终保持最新需求。

包括：

- 当前需求
- 当前版本
- 当前状态
- 最近更新
- 当前负责人
- 最新设计链接
- 最新 API
- 当前待完成事项

---

### versions/

保存每一次历史版本。

例如：

v1.0

初始需求

↓

v1.1

新增筛选

↓

v1.2

新增导出

↓

v2.0

整体重构

历史版本禁止修改。

---

### change-log.md

记录所有需求变化。

包括：

- 时间
- 修改人
- 修改原因
- 修改内容
- 影响范围
- 对应版本

---

### bug-history.md

记录所有 Bug。

包括：

- Bug ID
- 描述
- Root Cause
- 修复方案
- 修复版本
- 是否验证

---

### enhancement-history.md

记录所有优化。

包括：

- 优化原因
- 优化前
- 优化后
- 收益
- 是否影响用户

---

### decision-log.md

记录所有重要决策（ADR）。

包括：

- 为什么这样设计？
- 为什么没有采用其它方案？
- 决策日期
- 决策人
- 替代方案
- 风险

---

### open-questions.md

所有待确认问题。

包括：

- Question
- Owner
- Priority
- Status
- Expected Date

---

### developer-guide.md

开发人员真正需要阅读的文档。

包括：

- 页面结构
- Component Mapping
- Service Mapping
- API Mapping
- 数据流
- 状态流
- 修改文件
- 开发注意事项

---

### qa-checklist.md

自动维护测试清单。

包括：

- Functional Test
- Regression Test
- API Test
- UI Test
- Loading
- Empty
- Error
- Permission
- Responsive

---

### release-notes.md

记录每次上线。

包括：

新增

修改

优化

Bug 修复

Known Issues

Migration

---

### glossary.md

统一业务术语。

例如：

Production Period

Well

Forecast

Production Mode

Scenario

避免不同开发人员理解不同。

---

### assets/

保存：

- 流程图
- UI 截图
- Figma 导出
- UML
- 时序图
- 架构图

保证文档完整。