# WPO 核心工作流链路:Well Test → 校验 → 校准 → 监控与优化

**日期:** 2026-11-12
**状态:** Draft(基于团队提供的五段模块定义整理;标注"推断"的部分需向团队确认)

> Related: [well-model-management.md](../../domain-knowledge/well-model-management.md)(模型生命周期与看板)、
> [wpo-surveillance-concepts-zh.md](../../domain-knowledge/wpo-surveillance-concepts-zh.md)、
> [wpe-wso-surveillance.md](../domains/wpe-wso-surveillance.md)、
> [glossary.md](../glossary.md)。

## 1. 一句话

WPO 由五个相互衔接的部分组成:**Well Test Management 产出试井记录 → Well Test Analysis / Validation 校验并审批 → Well Model Calibration 用"已批准"的试井评估并校准模型 → Well Surveillance & Optimization 用当前运行数据加上述上下文计算性能、识别异常、评估优化机会**;**Workflow Configuration** 为 WTV、WMC、WSO 三个工作流提供限值、容差、开关、敏感度范围和验收标准。

缩写:WTM = Well Test Management,WTV = Well Test Validation,WMC = Well Model Calibration,WSO = Well Surveillance & Optimization,WFC = Workflow Configuration(此缩写为本文为叙述方便所取,团队原文未给)。

## 2. 五个部分各做什么

| # | 部分 | 职责(原文要点) | 主要输入 | 主要输出 |
| --- | --- | --- | --- | --- |
| 1 | Well Test Management | 创建和维护下游工作流使用的**试井记录** | 现场试井数据(录入/导入) | 试井记录 |
| 2 | Well Test Analysis / Validation (WTV) | 检查试井数据和**水力一致性**;需要时提交用户**批准或拒绝** | 试井记录;WFC 的限值/容差 | 试井状态(Approved / Rejected 等) |
| 3 | Well Model Calibration (WMC) | 用 **Approved** 试井评估井模型,需要时**校准**;批准后的校准值可被后续 WPO 计算和后续校准使用 | Approved 试井;井模型;WFC 的容差/敏感度范围/验收标准 | 校准结果、校准值(经批准后生效) |
| 4 | Well Surveillance & Optimization (WSO) | 用当前运行信息加上适用的试井、校准、井模型上下文,计算当前性能、识别异常、评估**符合条件的**优化机会 | 当前运行数据;试井 + 校准 + 井模型上下文;WFC 的限值/开关 | 性能指标、异常、优化机会 |
| 5 | Workflow Configuration | 提供 WTV、WMC、WSO 使用的**工程限值、容差、启用开关、敏感度范围、验收标准** | 工程/管理员配置 | 配置参数 |

## 3. 数据流与依赖

```
                    ┌───────────────────────────────┐
                    │  ⑤ Workflow Configuration      │
                    │  限值 / 容差 / 启用开关 /       │
                    │  敏感度范围 / 验收标准          │
                    └───────┬─────────┬─────────┬────┘
                            │         │         │
 ① Well Test        ② WTV   ▼   ③ WMC ▼         ▼ ④ WSO
 Management  ──►  校验+审批 ──► 校准  ──► 监控 / 异常 / 优化
 (试井记录)       (Approved)   (校准值)      ▲
                                  │          │
                                  └──────────┘
                     校准值被后续 WPO 计算和后续校准使用
                     当前运行数据 ─────────────┘
```

关键依赖:

| 依赖 | 说明 |
| --- | --- |
| 试井必须先 **Approved** 才能进入校准 | WMC 只使用 Approved 试井;WTV 是这道闸门 |
| 校准值需**批准**后才可被使用 | "Approved calibration values" 才会进入后续 WPO 计算和后续校准 |
| 校准有**迭代性** | 批准的校准值也会作为后续校准的输入(链式) |
| WSO 需要三类上下文 | 适用的试井、校准、井模型;不是只靠当前运行数据 |
| 配置贯穿三个工作流 | WFC 为 WTV、WMC、WSO 提供参数,WTM 不在其适用范围内(原文未列) |

## 4. 与已有文档的对应

[well-model-management.md](../../domain-knowledge/well-model-management.md) 描述的模型生命周期是:

```
Well Production Data → Well Test → Validate Test → Well Model Calibration → KPI Evaluation → Priority Management → Engineer Action
```

与本文的对应关系:

| 生命周期环节 | 本文部分 |
| --- | --- |
| Well Test | ① WTM |
| Validate Test | ② WTV(看板上的 Approved / Pending User Action / Rejected / Awaiting Processing) |
| Well Model Calibration | ③ WMC |
| KPI Evaluation、Priority Management | 本文未覆盖(推断:属于看板层/WSO 的消费端,需确认) |
| 运行监控与优化 | ④ WSO |

另外,[wpe-wso-surveillance.md](../domains/wpe-wso-surveillance.md) 把 Well Test Management 放在 Well Surveillance 下,把 WTV/WTE 放在 WPE 下,与本文把它们看作同一条链路的不同阶段不完全一致,**两者的归属关系需要确认**(见第 7 节)。

## 5. 各部分的关键设计点(分析)

### ① Well Test Management
- 它是链路的**数据起点**:记录质量直接决定后面三步。
- "创建和维护"意味着试井记录可被修改;需要确认**修改已被批准的试井**时,是否使其重新进入校验,以及已基于它的校准如何处理(推断,待确认)。

### ② WTV
- 做两类检查:**数据检查**与**水力一致性检查**。
- "where required, presents for approval or rejection" 说明**不是所有试井都需要人工审批**:通过自动检查的可能直接通过,存疑的才请用户确认(推断:具体规则取决于 WFC 配置)。
- 它的输出状态是下游的闸门,应当是明确、可查询的状态。

### ③ WMC
- 先**评估**模型,再决定**是否需要校准**("assess and, where required, calibrate"),即评估结果可能是"模型已足够好,无需校准"。
- 校准结果需要**批准**才生效,与试井审批类似,是第二道人工把关。
- 校准值被后续计算和后续校准引用,因此需要**版本与生效范围**(哪一版校准值对哪一段时间的计算有效)——原文未说明,属推断,需确认。

### ④ WSO
- 输入是**组合上下文**:当前运行信息 + 试井 + 校准 + 井模型。上下文缺失(例如没有 Approved 试井、没有批准的校准值)时的行为需要明确:降级、提示还是不计算(推断,待确认)。
- 三个输出:当前性能、异常、优化机会。优化机会只评估"**符合条件的**"(qualifying),条件来自配置。

### ⑤ Workflow Configuration
- 五类参数:**工程限值、容差、启用开关、敏感度范围、验收标准**。
- 服务对象是 WTV、WMC、WSO 三个工作流,所以是**横向的控制面**。
- 启用开关意味着各工作流/各井可被单独启用或关闭(推断:粒度待确认,是全局、按资产还是按井)。

## 6. 风险与关注点

| 风险 | 说明 | 方向 |
| --- | --- | --- |
| 上游错误放大 | 一条错误的试井被批准后,会污染校准和 WSO 计算 | 强化 WTV 检查;审批留痕;支持撤销批准并追溯下游影响 |
| 配置变更影响面大 | WFC 改一个容差,同时影响 WTV、WMC、WSO | 配置版本化、变更审计、影响预览 |
| 状态不一致 | 试井被修改或撤销批准,下游校准值仍在使用 | 明确依赖关系与失效规则 |
| 上下文缺失 | WSO 缺少 Approved 试井或校准值 | 明确降级策略,界面上标明所用上下文 |
| 人工审批积压 | WTV 和 WMC 都有人工审批点,可能成为瓶颈 | 看板展示待处理数量(现有看板已有 Pending User Action) |
| 可追溯性 | 一个优化结论依赖哪次试井、哪版校准、哪套配置 | 结果中记录所用上下文的标识 |

## 7. 待向团队确认

1. WTM 与 WTV 的归属:WTM 在 Well Surveillance 下,WTV/WTE 在 WPE 下(见 [wpe-wso-surveillance.md](../domains/wpe-wso-surveillance.md)),与"同一条链路"的描述如何对应?
2. WTV 的人工审批触发条件是什么?哪些试井会自动通过?
3. 已批准的试井被修改后,状态与下游校准如何处理?
4. 校准值的版本、生效范围、过期或回滚规则是什么?
5. WSO 缺少试井或校准上下文时,如何降级?
6. WFC 配置的粒度(全局 / 资产 / 井 / 生产方式)与版本管理方式?
7. KPI Evaluation 和 Priority Management(见 well-model-management 的生命周期)属于哪个部分?
8. WTM 是否也受 WFC 配置控制?(原文只列了 WTV、WMC、WSO)

## 8. 下一步

- [ ] 与团队对齐第 7 节问题
- [ ] 补充各部分对应的页面、API 和数据对象(WELL_TEST、WELL_TEST_PERIOD 等已见于 [wpe-wso-surveillance.md](../domains/wpe-wso-surveillance.md))
- [ ] 把状态机(试井状态、校准状态)整理到 data-model/enums
