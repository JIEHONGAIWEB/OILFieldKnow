# DFS Well Integrity Management 简介

**来源：** DECISION SPACE® DIGITAL FIELD SOLVER®(DFS)Well Integrity Management 帮助文档 *Introduction*
**链接：** https://sdh-dfs.tiger.dazlmkengdev02.ienergycloud.solutions/api/router/spa-ui.dev.sdh-appshost.sdh/apps/spa-ui.dev/docs/home/SEARCH/
**状态：** 摘要说明(基于页面内容整理)

## 概述

DFS Well Integrity Management(井完整性管理)是一个基于 Web 的云原生解决方案，将各类井完整性数据转化为**按时间展示的可视化**。

- **目标用户:** 资产经理，以及井完整性、生产和现场工程师。
- **价值:** 提供资产井表现的整体视图，支持及早发现并解决潜在问题。
- **产品体系:** 属于 Halliburton DecisionSpace® 产品体系，基于 **PPDM**(Petroleum Production Data Model)标准构建。

## 功能模块

| 模块 | 说明 |
| --- | --- |
| Well Barrier Schematics Template / Well Barriers Management | 井屏障示意图模板与井屏障管理 |
| Risk Assessment and Ranking | 风险评估与排序 |
| Operating Limits | 操作限值 |
| Well Anomaly Management | 井异常管理 |
| Test Management | 测试管理 |
| Well Dispensation | 井豁免/偏离管理 |
| Annular Integrity / Pressure Management | 环空完整性/压力管理 |
| Well Events and Planned Activities | 井事件与计划活动 |
| Automated Well Failure Model | 自动化井失效模型 |
| Business Process Approval and Ticketing System | 业务流程审批与工单系统 |
| Analytics | 分析 |
| Optimization | 优化 |

此外，用户可以集成、配置并自动化任意井完整性工作流。

## 核心理念

- **Management by exception(例外管理):** 通过分析、诊断和纠正措施，让用户快速发现并处理完整性问题。
- **通知:** 可自定义事件触发的通知，并定义报警或警告何时不再生效。
- **实时与历史数据:** 在浏览器中同时展示实时井信息和历史完整性评估结果，覆盖全油田表现和短期井问题。
- **可扩展性:** 架构集中管理，用于在全球业务中推行一致的工作流程。
- **数据集成:** 可直接连接企业内各系统，并支持质量控制与质量保证流程。

## 使用入口

- 点击页面中的 **Launching** 链接启动应用。页面未给出更多步骤。

## 菜单导航(Menu Navigation)

菜单位于屏幕左侧，是进入各功能、工作流的主要入口。

- **打开方式:** 鼠标悬停在图标上查看内容，或点击左上角三条横线展开菜单。
- **使用步骤:** 展开菜单 → 选择分组 → 选择子项，进入对应视图和标签页。

| 分组 | 子项 |
| --- | --- |
| Integrity Monitoring(完整性监控) | Map View、Integrity KPI View、Integrity Well Summary |
| Integrity Workflows(完整性工作流) | Risk Assessment and Ranking、Operating Limits、Anomaly Management、Test Management、Well Classification、Annular Integrity & Pressure Management、Wellhead Audits |
| Integrity Well Information(井信息) | Events、Documents & Photos、Comments & Notes、Surveys |
| Integrity Dashboards(仪表盘) | Well Dispensation、Well Anomaly、Well Barrier Test、Well Element Test、Well Bleed & Topped，以及 Pressure Violation Alarm 汇总 |
| Integrity Tickets(工单) | Ticket Management |
| Integrity Settings(设置) | WBS Template Management、Well Barriers Management、Well Management、WFM Settings、Classification Settings、Production Data Management、Operating Alarm Settings |
| Integrity System Settings(系统设置) | Alerts Settings、Units Settings、Data Entitlement |
| 其他 | My Tasks、Help |

> 导航页只讲基础，各子项细节见各自的帮助页。来源：同一帮助站点下的 `Menu-Navigation-(1)` 页面。

## Integrity Monitoring › Map View(地图视图)

**链接：** https://sdh-dfs.tiger.dazlmkengdev02.ienergycloud.solutions/api/router/spa-ui.dev.sdh-appshost.sdh/apps/spa-ui.dev/docs/home/SEARCH/integrity-monitoring/Map-View/

**用途：** 按真实坐标展示资产下的井。**图标形状**表示该井类型下的举升/生产方式，**图标颜色**表示当前井完整性风险等级。在层级中切换油田，地图随之更新。

### 工具与功能

| 功能 | 说明 |
| --- | --- |
| Hierarchy Filters(层级筛选) | 按 Region → Country → District → Field → Well 缩小范围；使用预配置下拉框，井可用左右箭头切换。具体配置因客户而异。 |
| Map Filters(地图筛选) | 点击地图右侧中部的图层图标开关。条件：Well Type、Production Method、Well Integrity Risk Rank、Well Status、Well Classification；订阅 Audit 服务后增加 Well Operation Stage、Well Audit Risk Rank。 |
| Alerts(告警) | 列出每口井当前有效告警，点击 Map Filters 上方图标展开。 |
| Well Quick Summary(井速览) | 点击井图标弹出摘要。 |
| Full Screen / Zoom / Scale / Attribution | 全屏、缩放(按钮或滚轮，可放大查看同一井场所有井)、比例尺(随筛选和缩放更新)、地图版权信息开关。 |

### 筛选规则

- 多个条件为**与**关系：如 Oil Producer + ESP + High，仅显示同时满足三项的井。
- Classification：Classification 1 或 2 任一匹配即显示；两者均未配置的井归入 "NA"。
- "NA" 含义：
  - Production Method：未配置生产方式。
  - Well Status：最新生产数据中没有状态。
  - Classification：Classification 1 和 2 都未配置。

### Alerts 表

- **来源：** ① Risk Assessment and Ranking——最新的非 Low 风险及其风险来源；② Operating Limits——最新生产数据超出已定义限值，附描述。
- **列：** Well、Workflow Name、Alert Type、Alert Time、Description(悬停查看详情)。
- 分页显示，最新告警在最上；支持全局搜索、表头筛选、排序。

### Well Quick Summary 字段

Well Name、Well Type、Production Method、Status、Time、Gas/Injection Rate、Oil Rate、Water/Injection Rate、Tubing Pressure、Classification、Open Anomalies、Risk Rank、Risk Number、Dispensation。订阅 Audit 服务后增加 **Well Control Audit** 标签页。

### 典型使用流程

1. 在 Hierarchy Filters 选择 Region/Country/District/Field。
2. 用图层图标打开 Map Filters，选择条件缩小井范围。
3. 展开 Alerts，查看风险与操作限值告警，必要时搜索、筛选、排序。
4. 点击井图标查看 Quick Summary。
5. 缩放或全屏，细看具体井。

> 页面未定义具体图标形状和颜色(见页面 Figure 5 图例或 Map Filters)；"Logic" 小节只有图片，未整理。

## Integrity Monitoring › Integrity KPI View(完整性 KPI 视图)

**链接：** https://sdh-dfs.tiger.dazlmkengdev02.ienergycloud.solutions/api/router/spa-ui.dev.sdh-appshost.sdh/apps/spa-ui.dev/docs/home/SEARCH/integrity-monitoring/Integrity-KPI-View/

**用途：** 资产级仪表盘，展示当前完整性状态；每次打开都会重新加载最新数据。

### 图表

| 图表 | 内容 |
| --- | --- |
| Risk Rank | 按当前风险等级统计井数，基于 DFS WIM 企业 HSE 风险矩阵；等级来自 Risk Assessment and Ranking，或 Anomaly Management 中的 Override Risk Rank；无等级显示 *Unranked*。 |
| Dispensations | 处于豁免中的井，分为 30 天内到期和 30 天后到期。 |
| Open Anomalies | 按井完整性风险等级统计未关闭的现场异常。 |
| Tests Execution Status | 按测试频率状态分组：Compliant(未超频率限)、Due(超第一限)、Overdue(超第二限)、Critical(超最后一限)；频率在 WFM Settings 中设置。 |
| Well Types/Status | 按井型(Oil Producer、Gas Producer、Water Injection、CO2 Injection 等)和状态(Producing、Temporarily Stopped、Long Term Stopped)统计；图例箭头可查看全部条目。 |
| Well Integrity KPI | 近 12 个月 Failed Barrier Tests、Failed Element Tests、Open Anomalies 趋势，分用 Y1/Y2 轴。 |

### 表格

- **KPI Values Table：** 每个 KPI 近 12 个月的月度计数。
  - 点击月度数字，列出贡献该数字的井。
  - 点击井名跳转：状态 → Integrity Well Summary；测试 → Test Management；Open Anomalies / Dispensations → Anomaly Management；风险 → Risk Assessment and Ranking。
- **Wells Exceeding Pressure Operating Limits：** 最新油管或环空压力高于上限/低于下限的井，用背景色标示；悬停显示最新批准的限值和操作报警；点击井名进入 Operating Limits。

### KPI 定义

| KPI | 定义 |
| --- | --- |
| Producing / Temporarily Stopped / Long Term Stopped | 当月大部分时间处于该状态的井 |
| Failed Barrier Tests / Failed Element Tests | 当月日期内未通过的屏障/元件测试 |
| Open Anomalies | 月末仍未关闭的异常 |
| Dispensations | 月末有效或当月关闭的豁免 |
| Very High / High / Medium / Low / Very Low Risk | 当月最后一次风险等级为该级的井 |
| Unranked | 当月无风险等级的井 |

### 压力限值颜色规则

- **油管(Tubing)：** 上限 MATHP、UTP；下限 LTP。高于 MATHP 为红色，低于 LTP 为蓝色。
- **环空(Annulus)：** 上限 MAASP、MAWOP、UTP、UTH Alarm、MTH Alarm；下限 LTH Alarm、LTP。具体颜色页面仅以图示说明，无文字描述。

### 交互与流程

- 悬停看详情；全局搜索和表头筛选；点击图表扇区/柱子打开明细表；点击 KPI 数字或井名下钻。
- 流程：打开页面(自动刷新) → 看图表 → 点击扇区看井列表 → 搜索/筛选 → 点击井名进入对应工作流。

> 页面列出 MATHP、MAASP、MAWOP、UTP、LTP、UTH/MTH/LTH 缩写但未给出定义；"Logic" 小节仅有图片。

## Integrity Monitoring › Integrity Well Summary(井完整性摘要)

**链接：** https://sdh-dfs.tiger.dazlmkengdev02.ienergycloud.solutions/api/router/spa-ui.dev.sdh-appshost.sdh/apps/spa-ui.dev/docs/home/SEARCH/integrity-monitoring/Integrity-Well-Summary/

**用途：** 单井层级的落地页，集中展示井屏障示意图、屏障报告、关键工作流摘要(异常、备注、事件、计划活动)和两张完整性图表，并链接到所有井级工作流。

**页面分区：** Well Banner → Well Barriers Schematics(左) → Well Integrity Notes(示意图下方) → Integrity Charts(右半) → Integrity Barriers 标签页 → Integrity Summary 标签页 → 导航菜单与链接。

### Well Banner

Hierarchy、Well Name、Well Type、Production Method(如 ESP、Natural Flow)、Status、Classification(链接 Well Classification)、Risk Rank(链接 Risk Assessment and Ranking)、Dispensation(链接 Anomaly Management)。

### Well Barriers Schematics(井屏障示意图)

- **来源：** 使用 Landmark Profile 的精简版，基于 EDM 系统中的当前设备清单。
- **悬停字段：** Equipment Alias Name、Manufacturer、Working Pressure、ID、OD、MD Top、MD Base、Element Name、Barrier Envelope、Latest Test Date、Latest Test Result；分体设备分上下两段显示。
- **可视化编码：**
  - 屏障元件上的红绿灯颜色表示完整性状态，依据 Well Failure Matrix 规则。
  - 屏障包络：Primary 蓝、Secondary 红、Tertiary 绿、Common 紫。
  - 地面和井下设备显示测深；设备注释标注完整性备注。
- **操作：** 缩放、拖动查看井下细节；可下载示意图。
- **设置图标：** 透明度、剖开井口(3D)、2D/3D 模式；显示/隐藏注释、WBE TL(红绿灯)、屏障包络、Wellhead Only、Casing、Assemblies、Holes、Perfs、Cement、Lithology、Ref. Labels；TVD 开关(以 TVD 代替 MD)。
- **维护：** 元件、屏障标识及设备注释在 Well Barriers Management 中管理。

### Well Integrity Notes

显示 Comments & Notes 中 "Use for Annotation" = Yes 的最新 WBS Diagnostics。

### Integrity Charts

| 项目 | Annular Pressure Chart | Flow Rate Chart |
| --- | --- | --- |
| 坐标轴 | X 时间；Y1 压力；Y2 温度 | X 时间；Y1 液量；Y2 气量(自动调整) |
| 内容 | 油管头压力/温度；油管 MATHP、UTP、LTP 限值；环空 A–E 压力及各环空 MAASP、MAWOP、UTP、LTP(已定义时)；井状态及环空泄压/补压事件 | 日产量分配(测试)或注入数据，类型随井型；Well Oil、Water/Injection、Gas 及 Well Test 对应速率 |
| 默认参数 | THP 与 MATHP；Annulus A 及 A MAASP、A MAWOP；Annulus B 及 B MAASP、B MAWOP | — |
| 叠加 | — | 选定的 Comments & Notes 作为日期标记；Events 和 Planned Activities 作为阴影区 |
| 数据源 | DFS PDM 实时数据、手工录入、批量导入(Production Data Management)、泄压/补压测试(Annular Integrity & Pressure Management)、Operating Limits | DFS PDM 实时数据、手工录入、批量导入及其他数据源 |

**共同交互：** 参数选择(仅压力图)、保存图片、导出 .xlsx、刷新/重置、框选缩放、全屏、悬停十字线、可点击图例开关序列、Y 轴自动缩放与 X 轴缩放。

### Integrity Barriers 标签页

NORSOK 风格的屏障报告：

- **Well Barrier Schematic General Info：** Version Summary(当前版本)；Operating Limits Summary(油管和各环空的有效限值及生效日期)。
- **Well Barriers Summary：** 列出屏障及映射设备；展开设备可见最新元件/屏障测试——测试名称、类型、日期、结果、频率结果、监测状态、下次测试计划；测试名旁 "i" 图标悬停显示配置。
- **操作：** 导出 Integrity Barrier Report(PDF)、导出 .xlsx、刷新。

### Integrity Summary 标签页

四个汇总表，均可单独导出 Excel 和刷新：

| 表 | 内容 | 完整列表位置 |
| --- | --- | --- |
| Open Anomalies(最近 5 条) | Anomaly Type、开启天数、Status(Open、Validated、In progress)、Owner、Comments | Anomaly Management |
| Comments & Notes(最近 5 条) | Comment Type、Date、Comments、Modified By、Use for Annotations | Comments & Notes 菜单 |
| Events(最近 5 条) | Event Type、开始日期、Source、Description | Well Information › Events › Well Events |
| Planned Activities | 按所选 action group 和优先级筛选；Activity Type、起止日期、Action Owner、Use for Annotations、Comments | Well Information › Events › Well Planned Activities(编辑处) |

### 缩写

WBS(Well Barrier Schematic)、WBE(Well Barrier Element)、EDM(设备清单的系统记录源)、PDM(Production Data Management，生产与实时压力/速率数据源)。MAASP、MAWOP、MATHP、UTP、LTP 在页面中仅作为限值名称使用，未给出完整定义。

> "Logic" 小节仅有图片，未整理。

## Integrity Workflows(完整性工作流)

页面链接统一前缀：`.../docs/home/SEARCH/integrity-workflows/<页面名>/`

### Risk Assessment and Ranking(风险评估与排序)

**页面名：** `Risk-Assessment-and-Ranking`　**用途：** 展示每口井当前风险等级(RR)、计算方式、人工覆盖和历史，用于参考和审计。

- **三个部分：** Risk Rank(Current)、Risk Matrix、Risk Rank(History，默认按时间倒序)。
- **风险矩阵 5×5：** Impact A–E(Very Low → Very High)× Likelihood A–E(Not Significant → Very High)；例：rank 6 对应 Impact C、Likelihood B。
- **当前字段：**
  - Calculated：Risk Rank / Risk Number / WTL、计算时间、风险原因。
  - Override：Risk Rank / Risk Number / WTL、覆盖起止日期、Comment。
- **规则：**
  - 默认由 Well Failure Model 计算。
  - 在 Test Management 新增测试后，按所有测试结果重新排序。
  - 授权用户可通过两种方式改变当前等级：新增测试，或通过 Anomaly Management 中的异常进行 Override。
  - 历史记录保留供审计。
- WTL 页面未定义。

### Anomaly Management(异常管理)

**页面名：** `Anomaly-Management`　**用途：** 跟踪井完整性异常，从发现到关闭。

- **自动创建：** 压力操作限值被违反；测试部分失败或失败。用户也可手工创建。
- **角色：**
  - Common User：手工创建异常。
  - Approver Role 1：认领 Validation BT，验证异常并负责到关闭。
  - Approver Role 2：认领 Action Plan BT，审核批准行动计划。
- **流程：** ① 创建(所有用户，异常 Open) → ② 验证并创建行动计划(Role 1，验证或驳回) → ③ 行动计划审批(Role 2，异常转 In Progress) → ④ 行动计划完成(Role 1，关闭)。
- **Current Anomaly 标签页字段：** Observation Date、Open Date、Days Open、Opened By、Anomaly Type、Status、Validation Date、Anomaly Owner、Action Plan Creation Date、Action Plan Decision Date、Action Plan Decision By。
- **Anomaly History 标签页：** 状态为 Closed 或 Rejected，字段同上，另加 Closure Date。
- **行展开(">")：** 异常备注、验证备注、行动计划(含豁免和 Override Risk Rank 详情)、行动计划审批备注。
- **表单：** Anomaly Manual Entry Form；Edit Anomaly Entry Form(录入行动计划创建日期)；Edit Anomaly with Dispensation and Risk Rank Override Form。
- **规则：**
  - 每口井同一时间只能有一个有效豁免(Dispensation)，无有效豁免时才可发起新的。
  - Override Risk Rank 可用于降低井的风险等级。
  - 所有用户可查看行动计划，仅该异常的 Role 1 负责人可编辑(含关闭)。
- Days Open 无公式说明；BT = Business Ticket，页面未进一步定义。

### Test Management(测试管理)

**页面名：** `Test-Management`　**用途：** 授权用户记录和查看屏障完整性保证活动；测试数据存于 DFS PDM 数据库，显示当前和历史测试。含三部分：

| 部分 | 要点 |
| --- | --- |
| Element Tests(元件测试) | 记录单个井元件的测试。直接在 WIM 录入的结果无需 WI-TA 审批；非 Pass 即生成异常；保存后结果不可修改。若无同类型有效异常，则新建异常并发出异常验证工单。 |
| Barrier Tests(屏障测试) | 验证一组元件及整个屏障系统功能。测试及重复频率在 WFM Settings 中定义，此处维护。规则同上：结果不可改，非 Pass 生成异常和验证工单。 |
| Multiple Element/Barrier Tests(多元件/屏障测试) | 按定义的测试逻辑展示所选井的组合结果；当其中的元件或屏障测试结果变化时自动重新计算。列：Failures / Logic、Test Name、Test Result、Test Date、Failure Code、Impact、Likelihood、Risk Rank / Risk Number / ITL。 |

- **视图：** Current 表(每个测试名的最新一次)、History 表(之前的测试)；Element Tests 可按 Section 或 Element Name 过滤，并支持全局关键字搜索。
- **Element 表列：** Section、Element Name、Test Type、Test Name、Test Result、Test Date、Failure Code、Impact(依 WFM)、Likelihood(依 WFM)、Risk Rank / Risk Number / ITL。
- **Element Section：** Annulus A–E、Casing、Cement、Completion、Safety Critical Equipment、Tree、Tree & Wellhead Seals、Tubing、Wellhead。
- **操作：** ">" 展开 WFM 定义的参数和录入备注；右上 "+" 打开添加表单。
- **添加表单字段：** Well Name、Well Type、Production Method、Section/Barrier、Element Name(仅元件测试)、Test Name、Test Result、Test Date、Attributes(仅 WFM 定义时有，附件最大 10 MB)。
- WI-TA、ITL 页面未定义。

### Well Classification(井分类)

**页面名：** `Well-Classification`　**用途：** 按合规性或其他完整性相关参数(如与社区的距离、污染物)对井分类，不用于运营或设计考虑。主分类类型在 Classification Settings 中维护。

- **标签页：** Current Classification(当前有效分类)、Classification History(历史及决定)。
- **字段：**
  - 当前：Well Classification 1、Well Classification 2、Comments。
  - 历史：分类 1/2、Modify Request Date、Modify Request By、Decision、Decision By、Decision Date；展开行含 Comments、Comments To Ticket Approver、Comments By Ticket Approver。
- **规则：**
  - 一口井最多同时有两个分类。
  - 分类或变更需要 Role 2 审批，每次变更自动发起 Business Ticket，审批通过后才生效，旧分类转入历史。
- **流程：** 点击编辑图标 → 修改并提交 → 自动生成 BT → Role 2 审批 → 生效，旧分类进入 History。

### Annular Integrity & Pressure Management(环空完整性与压力管理)

**页面名：** `Annular-Integrity-Pressure-Management`　**用途：** 分析井参数，并记录环空泄压(bleed-off)和补压(top-up)事件。

**1. Well Data Correlation(井数据相关性)**

- 计算成对井参数的相关系数，识别正/反相关。本应隔离的系统(如油管与 A 环空)之间强相关，可能说明存在连通。
- **系数解读：** 接近 +1.00 为正相关(属性 1 升则属性 2 升，如 A 环空压力随油管井口压力变化)；接近 −1.00 为反相关；接近 0 基本无相关。
- **默认行为：** 日期范围默认 1 周；系统自动分析并选出绝对系数最大的一对，系数表按 "Correlation Coefficient 1" 以绝对值降序，首对填入 Attribute 1/2 筛选。
- **界面：** Chart 1(两属性对日期)、Chart 2(两属性互相对比)、相关系数表、筛选器 Attribute 1/2 与 Date Range 1/2。
- **日期范围：** Range 1 用于考察其他时间段；Range 2 用于在同一时段内核对，在 Chart 1 上着色、刷新 Chart 2，并填充 "Correlation Coefficient 2" 列。
- **注意：** 仅为初步筛查，用于确定调查优先级；完整性失效必须现场物理验证。

**2. Annular Pressure Management(环空压力管理)**

- 记录和跟踪环空泄压/补压事件，字段：泄压或补压的环空、体积、起止压力、24 小时后压力、备注，以及事件中按需录入的其他井参数。
- **新增：** 点击 Add → 步骤 1 录入事件并 Next → 步骤 2 录入井参数 → Save。**编辑：** 点击事件旁的编辑图标修改。
- 泄压/补压压力也会显示在 Production Data Management 中，且在那里不可修改。
- 页面未说明必填项、校验规则、相关系数公式及 24 小时压力的取值方式。

### Wellhead Audits(井口审计)

**页面名：** `Wellhead-Audits`　**用途：** 供第三方或内部审计人员创建、更新、跟踪井口审计，作为井完整性保证和合规的一部分；DFS 客户用户可与其他完整性信息一同查看。

- **界面：** 审计表(最新在上)、">" 展开详情(下载文件和图片、预览图片)、Add 按钮(弹窗表单)。
- **字段：** Well Audit ID、Audit Date、Client Representative、Auditor、Comments、Detailed Report and Support Files(审计员上传，最大 10 MB)、Well Site Pictures(最大 10 MB)。
- **规则：** 仅授权用户可更新和跟踪；文件和照片同时保存在 Integrity Well Information › Documents and Photos。
- **流程：** Integrity Workflows › Wellhead Audits → 查看表 → 点击 ">" 展开 → Add 填写并上传(各 ≤10 MB) → Save。
- WIMS = Well Integrity Management System。

> 各页的 "Logic" / "Example" 小节只有图片，未整理。**Operating Limits** 页未能读取(抓取只返回 "App Information" 标题，页面名可能不同)，待补。

## Integrity Well Information(井信息)

链接前缀：`.../docs/home/SEARCH/integrity-well-information/<页面名>/`

### Events(事件)— `Events`

- **Well Events 标签页(只读)：** 来自 DFS WIM 事件系统记录源(EDM™)或第三方系统，不能在此编辑。
  - 列：Source、Event Type、Date、Description。
  - 点击 ">" 展开：24 hr. Summary、Other Remarks、Time(起止与时长)、Op Phase、Op Code、Op Sub、Op Type、Operation Details。
  - 全局搜索可搜到展开内容中的文字。
- **Well Planned Activities 标签页：** 授权用户可直接为井录入计划活动；**Use For Annotation = Y** 时，该活动时间段会在 Flow Rate 图上高亮。
- Op Phase / Op Code / Op Sub / Op Type 页面未定义。

### Documents & Photos(文档与照片)— `Documents-and-Photos`

- **用途：** DFS WIM 文档和照片的集中库；其他工作流保存的文件在此以只读形式显示，授权用户可为单井添加、编辑、管理。
- **显示：** Type(图标)、Name、Category、Created by、Created on、Description。
- **用户管理的 Category：** Abandonment、Casing、Completion、Operations、Others、Pressure Test、Visual Inspection、Well Construction、Well Handover、Well Intervention、Well Pad/Cellar。
- **关联其他功能的 Category(只能在来源处修改)：** Annulus Pressure Measurement(来自 Annular Integrity & Pressure Management)、Well Barrier Test(Barrier Tests)、Well Element Test(Element Tests)、Wellhead Audits。
- **流程：** 点击 Add/Edit 图标 → 填写信息 → 上传文件 → Save。上传文件最大 **10 MB**。

### Comments & Notes(备注)— `Comments-Notes`

- **备注类型：** WI Comments、Operator Notes、Tree Notes、Wellhead Notes、Subsurface Notes、Other、WBS Diagnostics。
- **流程：** Add/Edit 图标 → 填写表单 → Save。
- **Use For Annotation = Y：** 该备注作为注释显示在 Flow Rate 图上；**例外：** WBS Diagnostics 显示在 Integrity Well Summary 的井屏障示意图上。
- 页面未列出表单字段、权限和校验。

### Surveys(测斜)— `Surveys`

显示 EDM 中存储的井的定向测斜数据，三部分：

| 部分 | 内容 |
| --- | --- |
| List Details | 该井关联的所有 Directional Survey；列：EDM Well Name、EDM Wellbore Name、Survey Type、Company Name、Survey Date、MDT、MDB、Datum Type、Datum Elevation、GeoX、GeoY。点击行刷新图表和表格。 |
| Chart Details | 三张图：MD vs Inclination、TVDRT vs Departure、MD vs Dogleg Severity；多个测斜可选中后叠加比较。 |
| Table Details | 所选测斜的数据点；列：MD、Inclination、Azimuth、TVDRT、TVDSS、Dogleg Severity、DX、DY。 |

页面未定义 MDT、MDB、TVDRT、TVDSS 等缩写，也没有编辑、导出、筛选说明。

## Integrity Tickets(工单)

### Ticket Management — `integrity-tickets/Ticket-Management`

- **列表视图：** 显示所有工单状态(Complete / Pending approval)；点击 Ticket ID 打开详情。
- **详情头部：** Ticket ID 及当前状态(如 In Progress)。
- **左栏 Ticket Information：** Well Name / Question、Ticket Type(如 Well Classification)、Created By、Start/End Date、Comments to Ticket Approver、Task Events(生命周期时间线)。
- **右栏：**
  - Submit：提交人，及 Audit Item、Audit Type、Category、Due Date、Question、Auditor、Corrective Action Performed。
  - Approve：当前审批状态和最近一次操作日期。
- 页面无明确业务规则和术语表；Logic 仅有截图。

## Integrity Settings(设置)

链接前缀：`.../docs/home/SEARCH/integrity-settings/<页面名>/`

### WBS Template Management(井屏障示意图模板管理)— `WBS-Template-Management`

- **用途：** 管理员/授权用户管理 WBS 模板；每个模板绑定一个井型和生产方式，可从零创建，或复制同井型、同生产方式的已有模板。模板发布并激活后，使用它的井继承其组件、属性和屏障设置。
- **示意图：** Landmark Profile 的精简版，基于 EDM 当前设备清单，通过 Schematic Wizard 添加；控件有 Settings(透明度、屏障包络、Wellhead Only、Casing、Assemblies、Holes、Perforations、Cement、Lithology、参考标签、MD/TVD 切换)、Refresh、缩放/拖动。
- **Template Inventory 列：** 选择、Template Name、Well Type、Production Method、Source Name(从零创建则空)、Status(创建后 In-Progress，发布后 Published)、Modified On/By、Actions(Edit、Delete、Publish/Unpublish、Activate/Deactivate)。
- **Well Barriers Elements 表：** Equipment Name、Alias Name(默认=设备名，可改)、MD Top、MD Base、Element Name、Element Section(在 WFM Settings 定义)、Barrier Envelope、Status(O/C，仅阀门)、Save；支持 Multiple Mapping(仅选中设备且模板为 In-Progress 时可用)、Save All、搜索、筛选、导出、刷新、重置。
- **Formation Layers 表：** Layer Name、Alias Name、MD Top/Base、Lithology、Category(默认 Inflow Zone、Reservoir、Seal)、Barrier Envelope(仅 Category = Seal 时映射)、Save。
- **Schematic Wizard 五步(仅 In-Progress 模板可编辑，其他只读)：** ① General Data(基础信息、参考标高、Deviation Survey、Formation Layers) → ② Well Design(Hole Sections、Casing Strings、Cement Jobs) → ③ Completion Details → ④ Wellbore Openings → ⑤ Wellhead & X-mas Tree。
- **流程：** 创建/复制模板 → 完成向导 → 映射设备到元件和屏障、设置阀门状态、映射 Seal 地层到屏障 → 发布 → 激活。

### Well Barriers Management(井屏障管理)— `Well-Barriers-Management`

- **用途：** 管理员将 EDM 设备清单映射到 WFM 定义的元件/屏障，支撑 WIM 的井示意图。目标：显示设备名；将实际设备映射到屏障；拆分设备并映射到不同屏障、定义 TOC(水泥顶)；设置阀门开/关；管理初始验证和工作压力；添加示意图注释。
- **示意图来源：** EDM 当前设备清单或已应用的模板。图例：Primary 蓝、Secondary 红、Tertiary 绿、Common 紫；Barrier TL 为各屏障风险红绿灯。
- **模式：** Edit Mode(点击选中，示意图与表格同步高亮)；View Mode(悬停查看别名、制造商、工作压力、ID、OD、MD、元件、屏障、最新测试日期和结果)。另有 Multiple Mapping、Edit(拆分设备、定义 TOC(仅水泥)、上传文件)、Setting、Refresh、缩放。
- **Schematic Wizard：** 仅限已分配屏障示意图的井，五步同上。
- **Version Settings：** 录入版本信息，出现在 Integrity Barriers Report 中以便版本追溯、复核、合规。
- **Elements 表列：** Equipment Name、Alias Name、MD Top/Base、Top of Cement MD、Barrier Section(拆分设备的上/下段)、Element Name、Element Section、Barrier Envelope、Status(O/C)、Initial Verification、Working Pressure、Annotation、Action(Save、Edit、Activate/Deactivate Label、Download Attachment)。
- **Formation Layers 表：** 比模板版多 Initial Verification 和 Annotation 列。

### Well Management(井管理)— `Well-Management`

- **用途：** 有编辑权限的用户在授权油田内添加井、激活/停用井(如修井或干预期间)、删除不再需要的井。
- **标签页：** Well Inventory(有效井列表)、Well Bin(已删除、可恢复的井)。
- **添加井：** 点击 "+" 打开 Add Well 表单。可选择映射 EDM Well Name 和 Wellbore Name，映射后坐标、井示意图、设备、测斜通过 ETL 从 EDM 拉取；未映射则手工录入。
- **Add Well 字段：** Is EDM Required(开启后出现 EDM Company、Project、Site、Well Name、Wellbore Name)、Is Active、Region、Country、District、Field、Well Name、Well Type、Production Method、CRS、Latitude、Longitude、Well Schematics Template(从与井型和生产方式匹配的已发布且激活模板中选择)、Well Control Audit 与 Operation Stage(仅订阅 Audit 服务时显示)、Available Annulus。
- **Multiple Schematics Setting：** 给多口井批量应用模板，分配的井自动继承模板的示意图设置。

### WFM Settings(井失效矩阵设置)— `WFM-Settings`

- **用途：** WFM(Well Failure Matrix)与 Risk Rank Matrix 是井结构设置的系统记录：定义元件和屏障失效、测试、测试结果、行动代码和风险等级；系统用 Impact 与 Likelihood 坐标计算风险等级和 ITL。初始配置从模板(附录 B、C)加载，管理员可修改，建议 WFM 文件与系统配置保持一致。
- **三个标签页：**

| 标签页 | 表列 / 表单要点 |
| --- | --- |
| Element Test Settings | 列：Section、Element Name、Test Type、Test Name、Test Result、Failure Code、Impact、Likelihood、Risk Rank / Risk Number / ITL、Action。表单：Well Type、Production Method、Section、Element Name、Test Type、Test Name、Threshold 与 Working Pressure(仅 Pressure Monitoring)、Risk Setting、Attributes(可选，类型含 Attachment、Depth、Diameter、Duration、Pressure、Temperature、Turns、Wellhead Pressure Rating)、Frequency(可选)。 |
| Barrier Test Settings | 列同上，风险输出为 BTL。表单：Well Type、Barrier、Test Type、Test Name、Risk Setting、Attributes、Frequency、Failure Code/Impact/Likelihood/Risk Rank。 |
| Multiple Element/Barrier Test Settings | 用失效代码创建多重失效规则。列：Failure/Logic、Test Name、Failure Code、Impact、Action；表单含 Failure/Logic 构建器(Undo、Redo、Clear)、Failures、Logic、Test Name、Failure Code、Impact。 |

- **频率结果规则：** 新增测试时计算测试日期与当前日期(或下一次测试日期)的时间差 DT，用三个月数阈值判断：DT < 第一值 = **Compliant**；第一～第二值 = **Due**；第二～第三值 = **Overdue**；> 第三值 = **Critical**。
- **风险设置：** Pressure Monitoring 测试需填满所有风险设置组，其他类型至少一组。

### Classification Settings(分类设置)— `Classification-Settings`

- **用途：** 自定义井分类列表，并按分类控制告警工作流。
- **添加：** 点击 "+" → 输入分类名称 → 选择不对该分类触发的工作流。
- **规则：** 只有当没有井登记到某分类时，才能删除该分类。页面未给出修改步骤和完整工作流清单。

### Production Data Management(生产数据管理)— `Production-Data-Management`

- **用途：** 汇总和查看历史井完整性生产数据，并配置各生产参数的 PI Tag。
- **Production Data 标签页：** 查看任意时间范围的数据，手工或批量添加。
  - 批量：下载模板 → 填写 → Upload Wizard 上传。向导四步：Prepare your files → Quality Check → Data Preview → Publish。
  - 单条：点击 "+" 填表。不同来源的数据以不同背景色显示(颜色可在数据库中配置)。
- **Tags Setting 标签页：** 配置 PI Tag。前提是数据源已启用数据集成；按井、按参数登记 Tag Identifier 并保存。
- PI Tag、Tag Identifier、质量检查的具体项目页面均未定义。

### Operating Alarm Settings(操作报警设置)— `Operating-Alarm-Settings`

- 按井型和生产方式设置 **UTH**(上限)、**MTH**(中限)、**LTH**(下限)阈值报警，作为同井型同生产方式井的操作限值默认值。
- **流程：** 打开 Operating Alarm Settings → 找到要改的环空 → 点击 Edit 图标 → 在表单中修改。
- 页面未列出表单字段、校验和单位。

## Integrity System Settings(系统设置)

链接前缀：`.../docs/home/SEARCH/integrity-system-settings/<页面名>/`

### Alerts Settings(告警设置)— `Alerts-Settings`

- 通过 **Alert Notification Matrix**(复选框矩阵)控制各工作流告警邮件发给哪些用户组：勾选发送，取消勾选停止。
- **Operating Limits(38 种告警)：** Tubing 的 MATHP、UTP、LTP 违反；Annulus A–E 每个有 7 种：MAASP、MAWOP、UTP、UTH Alarm、MTH Alarm、LTH Alarm、LTP。
- **Test Management(5 种)：** Very Low / Low / Medium / High / Very High Risk。
- 用户组及标签页面未列出。

### Units Settings(单位设置)— `Units-Settings`

- 配置系统显示的单位，**不做换算**，应在初始阶段设置；**除非重新配置 ETL，否则不应更改单位**。其余内容仅有截图。

### Data Entitlement(数据授权)— `Data-Entitlement`

- 管理员按井层级(Hierarchy)控制各用户组或用户名可访问哪些井。
- **流程：** 选用户组 → 选一个或多个用户名 → 在 Available 中选井组 → 用单箭头(所选)或双箭头(全部)移到 Selected → Save → 刷新页面查看。

> 以上各页的 "Logic" / "Example" 小节多为图片，未整理。

## 通用页面

### Getting Started(入门)— `getting-started/Getting-Started`

- 通过 Digital Field Solver® 平台使用本工具。
- **登录：** 打开系统管理员提供的 URL → 在 i-Energy® Cloud 登录页输入注册邮箱 → Next → 若组织要求，完成多因素认证 → 进入解决方案落地页。

### My Task(我的任务)— `my-task/My-Task`

- 查看分配给自己的工单，认领后完成或释放。菜单中的 My Tasks 图标表示有待审批工单，点击弹出列表。
- **流程：** 点击图标 → 选工单 → 在 Ticket Details 表单点 **Claim** → 选 **Complete**(批准并确认)或 **Release**(退回认领前状态)。
- 必须先认领才能完成或释放；列表只显示分配给自己的工单。

### Admin Panel(管理面板)— `admin-panel/Admin-Panel`

- 为每个 DFS WIM 用户角色按功能设置读/写权限；角色在 Admin Panel 的 Users and Roles 中定义和管理。
- **只有管理员级用户**对 Admin Panel 有读写权限。细节见 Digital Field Solver User Manual(User Interfaces › Users and Roles)。

### Application Support(应用支持)— `application-support/Application-Support`

- 通过与专家聊天获取支持。点击屏幕左下角聊天图标，填写聊天信息窗口：First/Last Name、Primary Email(从登录凭据预填)、Subject、Domain(选 "Production")、Customer Priority(High / Medium / Low)、Web email(可选的备用邮箱)。

### Glossary(术语表)— `glossary/Glossary`

| 术语 | 含义 |
| --- | --- |
| Anomaly | 偏离预期、常态或理论模型预测的情况 |
| Barrier / Barrier Element | 阻止流体在地层间流动或逸出到地面的物理对象；井通常用两道屏障。屏障元件是正确安装时帮助阻止流动的部件，其失效即所属屏障失效 |
| Well Barrier Element(WBE) | 一个或多个相互依赖的部件共同构成防止井内/井外失控流动的屏障包络 |
| CIV | Chemical Injection Valve，化学注入管线上防止井筒流体经该管线到地面的屏障元件 |
| DHSV / Downhole Safety Valve | 井下安全阀，灾难事件中的紧急关断元件(安全关键设备) |
| Failure / Impairment(I/F) | 失效：丧失预期功能；损伤：功能下降但尚未失效 |
| Date Sync | 控制其下方图表的日期范围；默认一年，可选 1 周、1 月、1 年、2 年、5 年、全部或自定义；各图使用相同同步便于比较趋势 |
| Global View / Regional View | 展示 GIS 地图和 KPI 的窗格 / 展示所选或授权区域的窗格 |
| Navigation Pane | 井页面链接：Risk Rank、Operating Limits、Anomalies、Barrier Tests、Events、Equipment Inventory、Photos、Comments and Notes、Fluid Samples、Directional Survey、Well Report、Deviation and Evaluation |
| Well Banner | 井关键信息摘要：名称、类型、区域、状态、风险数值、分类、偏离、损伤、失效、是否评估中 |
| Well Deviation | 对企业或监管标准规则的偏离 |
| Well Integrity / Well Integrity Management | 使流体保持在预期通道内并防止逸出；贯穿井生命周期维持井完整性的技术、运营和组织流程的总和 |
| Well Operating Limits | 作业者为定义井整个生命周期内可接受完整性表现而设的准则 |
| Well Risk Rank | 基于作业者 HSE 风险矩阵的风险评估分类(数字、等级或颜色) |
| Risk Assessment | 对活动风险按预定标准或目标风险水平做的系统分析 |

**缩写：** CRS 坐标参考系统；DSIS DecisionSpace® Integration Server；DFS WIM Digital Field Solver® Well Integrity Management；GIS 地理信息系统；GLV 气举阀；HSE 健康、安全与环境；KPI 关键绩效指标；MAASP 最大允许环空地面压力；MATHP 最大允许油管头压力；MAWOP 最大允许井口操作压力；MIYP 最小内屈服压力；MOC 变更管理；NOL 正常操作限值；PPDM 石油生产数据模型；RCFA 根本原因失效分析；SCE 安全关键设备；UTP / LTP 上/下限压力；UTH / MTH / LTH 上/中/下阈值；UWI 唯一井标识；WFM Well Failure Model；WIMS Well Integrity Management System；ITL / WTL / TL 个体/井/红绿灯(术语表仅给出展开，无进一步定义)。

> 术语表把 WFM 写作 "Well Failure Model"，而 WFM Settings 页写作 "Well Failure Matrix"，官方两处用词不一致。

## 帮助文档章节

Getting Started、Home、Integrity Monitoring、Integrity Workflows、Integrity Well Information、Integrity Dashboards、Integrity Tickets、Integrity Settings、Integrity System Settings、My Task、Admin Panel、Application Support、Glossary。

## 备注

- 简介部分仅为概述，没有参数定义、限制条件或版本说明；操作层面的内容见“菜单导航”及 Integrity Monitoring 三个子页(Map View、Integrity KPI View、Integrity Well Summary)。
- Integrity Workflows 已整理 6 个子页(Operating Limits 未能读取，待补)。
- Integrity Well Information、Tickets、Settings、System Settings 已整理。
- **未能读取：** Operating Limits，以及 Integrity Dashboards 下全部六项(Well Dispensation、Well Anomaly、Well Barrier Test、Well Element Test、Well Bleed & Topped、Pressure Violation Alarm)。猜测的页面名返回的都只是 "App Information" 标题，需要在浏览器中确认真实页面名或粘贴正文。
- Getting Started、My Task、Admin Panel、Application Support、Glossary 已整理(见“通用页面”)。
- WPO User Guide(GitLab Pages)需要登录，未能读取，其中 "WA Production Method Specific" 一节尚未整理。
- URL 末尾的 `SEARCH` 只是路由名，与搜索功能无关。
- 功能模块表中的中文名称为翻译，非官方译名。
