# DFS Well Integrity Management — Integrity KPI View

**来源：** DECISION SPACE® DIGITAL FIELD SOLVER®(DFS)Well Integrity Management 帮助文档 *Integrity Monitoring → Integrity KPI View*
**链接：** https://sdh-dfs.tiger.dazlmkengdev02.ienergycloud.solutions/api/router/spa-ui.dev.sdh-appshost.sdh/apps/spa-ui.dev/docs/home/SEARCH/integrity-monitoring/Integrity-KPI-View/
**状态：** 摘要说明(基于页面内容整理)
**上级文档：** [dfs-well-integrity-management-intro.md](dfs-well-integrity-management-intro.md)

## 概述

Integrity KPI View 是资产**当前完整性状态**的仪表盘，每次打开都会用最新数据刷新。

- 可用 **Global Search** 和表头筛选缩小表格范围。
- 鼠标悬停在图表或区块上可查看详情。
- 点击图表中的区块/柱，会下钻到对应的井列表及详细信息表。

页面包含 5 个图表，外加 KPI 趋势图、KPI 数值表、超压力限值井列表。

## 图表一览

| 图表 | 展示内容 | 要点 |
| --- | --- | --- |
| Risk Rank(风险等级) | 按 DFS WIM 企业 HSE 风险矩阵展示井当前风险等级 | 来源于 Risk Assessment and Ranking 工作流，或 Anomaly Management 中的 Override Risk Rank；无等级的井显示为 **Unranked** |
| Dispensations(豁免) | 处于豁免状态的井 | 按豁免是否 30 天内到期 / 30 天后到期分组 |
| Open Anomalies(未关闭异常) | 未关闭的现场异常数量 | 按井的 Integrity Risk Rank 分类，反映当前未关闭异常 |
| Tests Execution Status(测试执行状态) | 测试按频率的合规情况 | 状态定义见下表；频率设置参见 WFM Settings |
| Well Types/Status(井类型/状态) | 按井类型和状态汇总资产 | 类型：Oil Producer、Gas Producer、Water Injection、CO2 Injection；状态：Producing、Temporarily Stopped、Long Term Stopped 等；可用图例箭头查看全部图例 |

### Tests Execution Status 状态定义

| 状态 | 含义 |
| --- | --- |
| Compliant | 测试在频率时限内 |
| Due | 已超过第一个频率限值 |
| Overdue | 已超过第二个频率限值 |
| Critical | 已超过最后一个频率限值 |

## Well Integrity KPI 趋势图

- 展示所选 KPI 过去 **12 个月**的变化。
- 所选 KPI：Failed Barrier Tests、Failed Element Tests、Open Anomalies。
- 不同 KPI 分别绘制在 **Y1 / Y2** 轴上。

## KPI Values 表

位于趋势图旁，按月显示过去 12 个月各 KPI 的数量，并可查看、跳转到构成该数量的井。

| KPI | 统计口径 |
| --- | --- |
| Producing | 当月大部分时间在生产的井 |
| Temporarily Stopped | 当月大部分时间临时停产的井 |
| Long Term Stopped | 当月大部分时间长期停产的井 |
| Failed Barrier Tests | 当月内日期的未通过屏障测试 |
| Failed Element Tests | 当月内日期的未通过元件测试 |
| Open Anomalies | 月末仍未关闭的异常 |
| Dispensations | 月末仍有效，或当月内关闭的豁免 |
| Very High Risk | 当月最后一次风险等级为 very high |
| High Risk | 当月最后一次风险等级为 high |
| Medium Risk | 当月最后一次风险等级为 medium |
| Low Risk | 当月最后一次风险等级为 low |
| Very Low Risk | 当月最后一次风险等级为 very low |
| Unranked | 当月无风险等级 |

**操作：**

- 悬停 KPI 名称显示提示；滚动表格查看全部 KPI。
- 点击某月的 KPI 数字，查看对应井名。
- 点击井名跳转到相关页面：

| KPI 类别 | 跳转目标 |
| --- | --- |
| 井状态 | Integrity Well Summary |
| 测试 | Test Management |
| Open Anomalies / Dispensations | Anomaly Management |
| 风险等级 | Risk Assessment and Ranking |

## Wells Exceeding Pressure Operating Limits

列出**最新油管或环空压力**高于上限或低于下限的井。

- 越限值用背景色高亮(例如：油管压力高于 MATHP 为红色，低于 LTP 为蓝色)。
- 悬停压力值可看到最新已批准的操作限值(MATHP、MAASP、MAWOP、UTP、LTP)和最新操作报警(UTH、MTH、LTH)。
- 点击井名打开 **Operating Limits** 查看详情。

| 压力类型 | 上限 | 下限 |
| --- | --- | --- |
| 油管压力 Tubing | MATHP、UTP | LTP |
| 环空压力 Annulus | MAASP、MAWOP、UTP、UTH Alarm、MTH Alarm | LTH Alarm、LTP |

## 使用流程

页面没有编号步骤，基本流程：打开视图 → 查看图表和表格 → 悬停看详情 → 点击区块或井名下钻 → 用筛选或 Global Search 缩小范围。

## 备注

- 页面中的 Logic 一节只有 4 张图(images 48-51)，没有文字说明，未整理。
- 具体颜色编码在原页面 Figure 33-34 中，这里未收录。
- 页面没有给出刷新频率、权限或数据来源的更多细节。
- 中文名称为翻译，非官方译名。
