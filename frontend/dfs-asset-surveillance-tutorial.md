# DFS Asset Surveillance 教程说明

**来源：** DECISION SPACE® DIGITAL FIELD SOLVER®(DFS)官方教程 *Asset Surveillance*
**链接：** https://dfs-ng20.tiger.dazlmkengdev02.ienergycloud.solutions/docs/Tutorial/asset_surveillance/
**状态：** 摘要说明(基于页面内容整理)

## 概述

Asset Surveillance(资产监控)通过**预定义仪表盘(dashboard)**集中展示油气田运行情况，帮助资产经理和工程师：

- 监控资产健康状况;
- 发现异常工况;
- 快速响应运行事件。

## 功能说明

### 1. Asset Summary(资产汇总)

- 资产级仪表盘，展示生产 KPI、日趋势、井清单、停产(downtime)事件等关键指标。
- **Field Type:** 支持 Oil Field 和 Gas Field。
- **数据来源:**

| 内容 | 数据来源 |
| --- | --- |
| 生产数据 | Product Volume Summary |
| 井清单 | Well Status |
| 停产事件 | PDM 中的 Downtime event 和 volume 表 |

### 2. Well Summary(单井汇总)

- 单井级仪表盘，展示井筒示意图(schematic)与参数、日趋势、实时数据等信息。
- 示意图和参数随**井类型**和**生产方式**变化，与实时图(real-time chart)类似。
- **26.2.00 版本**支持的生产方式: ESP、GL、SRP、Natural Flow、Water Injection。
- **数据来源:** Well、Well Status、Well Production Method History、Well Completion、Well Flow Measurement、Well Other Flow Measurement、Well Production Summary、Alarm、Activity、Remarks 等。

### 3. Well User Notes(井用户笔记)

- 创建和管理笔记，内容包括运行观察、监控发现、优化建议等。
- **添加笔记流程:**
  1. 新增一条 user note;
  2. 如果该笔记需要作业(job)，系统会**自动创建一个 activity**;
  3. 在 Well Activity Management 中跟进该 activity。

### 4. Well Activity Management(井活动管理)

- 创建、管理和跟踪井活动: 维护、修井(workover)、关井(shut-in)、测试、增产/干预(intervention)等。
- **活动的创建方式:**
  - 在本功能中手动创建;
  - 通过 ETL 导入;
  - 由 user note 生成(可在详情面板中查看来源笔记信息)。

### 5. Well Smart Alarms(井智能报警)

- 仪表盘，用于监控由自动化工作流基于**井流量测量数据**生成的报警。

### 6. Smart Alarms Settings(智能报警设置)

- 配置异常检测的规则和参数。
- **默认行为:** 所有井都会被监控。
- **排除:** 可将某口井排除在检测之外，例如其传感器故障时。

## 关键概念速查

| 概念 | 说明 |
| --- | --- |
| Field Type | 决定 Asset Summary 使用 Oil Field 还是 Gas Field 逻辑 |
| Production method | 决定 Well Summary 显示的示意图和参数 |
| Activity origin | 活动来源: 手动录入、ETL、user note |
| User note → Activity | 需要作业的笔记自动生成活动，在 Activity Management 跟进 |
| Smart Alarm | 工作流基于流量测量数据自动生成的报警 |

## 功能之间的关系

```
Well Summary ──(查看井状态/报警/活动/备注)
Well User Notes ──(需要作业)──▶ Well Activity Management
ETL / 手动创建 ───────────────▶ Well Activity Management
工作流 + 流量数据 ──▶ Well Smart Alarms ◀── Smart Alarms Settings(规则/排除)
```

## 使用注意事项

- Well Summary 目前仅支持 26.2.00 列出的五种生产方式，其他生产方式未在页面中说明。
- 传感器故障的井应在 Smart Alarms Settings 中排除，避免产生误报。
- 需要现场作业的发现，优先通过 user note 创建，便于追溯来源。
- 官方页面没有给出完整参数列表，除添加 user note 外也没有详细操作步骤，本文不做额外推断。
