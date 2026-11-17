# VLP 与 IPR 曲线计算

> 适用范围：油井生产分析、Well Test Management、Model Calibration。
> 相关：[operating-point.md](operating-point.md)（工作点的决策应用）、[well-test-model-calibration-data-prep.md](well-test-model-calibration-data-prep.md)（IPR / VLP 所需输入数据）、[ai-agent-model-driven-optimization.md](ai-agent-model-driven-optimization.md)（Workpoint 在 Agent 流程中的位置）。

## 1. 核心目标

找到**油藏供液能力**与**井筒举升能力**之间的平衡点（Operating Point，工作点），从而预测油井在当前生产条件下能够达到的产量。

这是油井生产分析、试井管理和模型校准中最基础的计算之一。

## 2. IPR 与 VLP 分别解决什么问题

| 曲线 | 全称 | 研究的问题 | 主要输入 |
|---|---|---|---|
| **IPR** | Inflow Performance Relationship（地层流入性能曲线） | 地层能以多大能力向井筒提供流体？ | 地层压力、流体性质、PI（生产指数）、Skin 等 |
| **VLP** | Vertical Lift Performance（垂直举升性能曲线） | 要把一定产量的流体举升到地面，井底需要多大压力？ | 井深、油管尺寸、流体性质、井口压力、含水率等 |

简单理解：

- **IPR**：地层能提供多少油？
- **VLP**：井筒能把多少油输送到地面？

## 3. 为什么需要两条曲线

油井生产既不完全由地层决定，也不完全由井筒决定，需要同时满足：

1. 地层有足够能量把流体推入井筒。
2. 井筒有足够举升能力把流体输送到地面。

因此两条曲线需要放在同一张图中比较。

## 4. 曲线形态与工作点

- 横坐标：Production Rate（产量）
- 纵坐标：Bottomhole Pressure（井底压力，BHP / FBHP）
- **IPR 曲线**：产量增加，井底流压通常下降。
- **VLP 曲线**：产量增加，所需井底流压通常上升。

两条曲线的交点即 **Operating Point（工作点 / 预测工作点）**，对应该条件下的稳定生产状态。

## 5. 示例（仅为原理演示）

假设某口井：Reservoir Pressure = 200 bar，Wellhead Pressure = 20 bar，其他流体与井筒参数已确定。

> 以下为简化的演示数据，并非真实油井计算结果。

| Production Rate (m³/d) | IPR：井底流压 (bar) | VLP：所需井底流压 (bar) |
|---|---|---|
| 10 | 170 | 80 |
| 20 | 140 | 110 |
| 30 | 110 | 140 |
| 40 | 80 | 170 |

读数规律：

- 产量 10 时，地层提供的流压大于井筒所需压力，流体可以被举升。
- 产量 40 时，地层提供的流压小于井筒所需压力，无法维持该产量。
- 两条曲线在约 **25 m³/d** 处相交，因此模型预测工作点约为 **25 m³/d**。

## 6. 在 Model Calibration 中的作用

假设：

| 指标 | 实际试井 | 模型预测 |
|---|---|---|
| Oil Rate | 20 m³/d | 28 m³/d |
| FBHP | 120 bar | 105 bar |

两者存在偏差，工程师需要检查：

**IPR 方面**

- Reservoir Pressure 是否准确？
- Productivity Index 是否合理？
- Skin Factor 是否准确？
- PVT 数据是否正确？

**VLP 方面**

- Tubing Diameter 是否正确？
- Wellhead Pressure 是否准确？
- Water Cut 是否准确？
- Gas-Liquid Ratio 是否准确？
- 人工举升设备参数是否正确？

通过调整合理的模型参数、重新计算 IPR / VLP 曲线，使模型工作点尽可能贴近实际试井数据。

> **注意**：不能为了让曲线吻合而随意调参。调整应结合独立测量数据和工程约束，避免过度校准。

## 7. 业务价值

| 应用场景 | IPR / VLP 能解决的问题 |
|---|---|
| Well Test Analysis | 判断实际生产状态与模型预测是否一致 |
| Model Calibration | 校准油藏和井筒模型参数 |
| Production Forecast | 预测不同条件下的产量 |
| Production Optimization | 寻找更合理的生产参数 |
| Artificial Lift Optimization | 分析 ESP、Gas Lift 等举升方案 |
| What-if Analysis | 模拟改变井口压力、泵频率等参数后的生产变化 |

## 8. 业务逻辑链路

```
Reservoir & Well Data（PVT、Reservoir Pressure、Wellbore、Lift Parameters）
        │
        ├── IPR Calculation（地层流入曲线）
        └── VLP Calculation（井筒举升曲线）
                │
        IPR + VLP Curve Intersection
                │
        Operating Point（工作点）
                │
Production Analysis & Optimization（产量预测、模型校准、生产优化）
```

## 9. 软件功能区分

| 功能 | 含义 |
|---|---|
| Calculate IPR | 计算地层流入能力 |
| Calculate VLP | 计算井筒举升能力 |
| Calculate IPR & VLP | 通过两条曲线交点预测油井工作状态 |
| Calibrate Model | 利用实际试井数据验证并调整模型参数 |

`IPR/VLP` 计算不只是生成两张曲线图，而是为模型校准、产量预测和生产优化提供数学基础。

## 10. 术语对照

| 英文 | 中文 | 说明 |
|---|---|---|
| IPR | 地层流入性能曲线 | 油藏向井筒供液能力 |
| VLP | 垂直举升性能曲线 | 井筒举升所需压力 |
| Operating Point / Workpoint | 工作点 | IPR 与 VLP 的交点 |
| BHP / FBHP | 井底流压 | 流动井底压力 |
| PI | 生产指数 | 单位压差下的产液能力 |
| Skin | 表皮系数 | 近井地带的附加压降 |
