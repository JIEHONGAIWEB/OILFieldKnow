# AI Agent + Model Management + Scheduler:模型驱动优化 vs 实时闭环控制

说明 AI Agent 结合 **Model Management**(井模型库)与 **Model Scheduler**(任务调度)能做什么,以及它与"真正的实时闭环控制"的边界。

> Related: [well-model-management.md](well-model-management.md)(井模型治理)、
> [wpo-surveillance-concepts-zh.md](wpo-surveillance-concepts-zh.md)(WPO/WPE/WSO 概念)。

## AI Agent 的能力链路

1. **理解用户意图** — 把自然语言需求解析为优化目标(如"提高某井产量""降低气举注气量")。
2. **查询井模型** — 在 Model Management 中查找对应井的 Prosper 模型。
3. **获取实时生产数据** — 从 SCADA / Historian 取压力、温度、产量、注气量、含水等。
4. **运行 Prosper 模型** — 以最新数据驱动模型计算。
5. **分析 IPR、VLP 和 Workpoint** — 节点分析:IPR(油藏流入)与 VLP(井筒流出)的交点即工作点。
6. **计算优化参数** — 如气举注气量、油嘴开度、ESP 频率等推荐值。
7. **创建 Model Scheduler 任务** — 把计算/执行安排为定时或周期任务。
8. **持续跟踪生产效果** — 执行后对比产量、模型预测与实测,评估收益。

```
用户意图 → 找井模型 → 取实时数据 → 跑 Prosper → IPR/VLP/Workpoint
        → 计算优化参数 → 创建 Scheduler 任务 → 跟踪生产效果 ──┐
              ▲                                              │
              └──────────── 偏差大则重新校准/再优化 ────────────┘
```

## 关键区别:模型驱动优化 ≠ 实时闭环控制

| 维度 | Model Management + Scheduler + AI Agent | 真正的实时闭环控制 |
| --- | --- | --- |
| 解决的问题 | **模型驱动的生产优化和任务自动化** | 自动、持续地把优化结果作用于现场设备 |
| 输出 | 推荐参数、计划任务、效果跟踪报告 | 直接下发的控制指令 |
| 执行方 | 通常由工程师确认后执行(human-in-the-loop) | 控制系统自动执行 |
| 时间尺度 | 分钟~天级(调度周期) | 秒~分钟级 |
| 额外依赖 | 模型、数据接口、调度器 | 见下 |

**真正的实时闭环控制还需要连接:**

- **现场控制系统**(SCADA / DCS / PLC / RTU)— 能写入设定值。
- **执行设备**(气举注气阀、油嘴/节流阀、ESP 变频器等)。
- **反馈数据链路**(传感器 → 历史库 → 模型/Agent 的低延迟回路)。
- 配套的安全约束、限幅、权限审批、异常回退与审计。

## 要点总结

- 当前能力 = **"建议 + 调度 + 跟踪"** 的闭环**流程**,闭环中的"执行"环节仍依赖人或外部系统。
- 做到实时闭环需补齐控制侧写入、设备执行与反馈回路,并解决安全与合规问题。
- 持续跟踪的结果应回流到模型校准(见 [well-model-management.md](well-model-management.md) 的 Model KPI),保证模型可信。

## Glossary

| Term | Meaning |
| --- | --- |
| IPR | Inflow Performance Relationship,油藏流入动态 |
| VLP | Vertical Lift Performance,井筒垂直管流(流出)曲线 |
| Workpoint | IPR 与 VLP 交点,即当前工作点 |
| Model Scheduler | 按计划/周期运行模型计算或任务的调度模块 |
| Closed-loop control | 感知→决策→自动执行→反馈的自动控制回路 |
