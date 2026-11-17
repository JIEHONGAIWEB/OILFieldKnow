# Well Test Management 与 Model Calibration:数据准备清单

> 做试井管理(Well Test Management)和模型校准(Model Calibration)之前,用户需要准备哪些数据。
>
> **性质**:通用油气工程知识整理,面向 DFS / WPO 场景。**没有与 DFS 实际数据模型或接口逐项核对**,
> 字段是否已存在于系统、叫什么名字,需要另行确认。第四、五节的 Data Readiness Check 是**产品设计建议**,不是已实现的功能。
>
> 相关文档:
> [well-model-management.md](well-model-management.md)(看板:试井验证、校准、模型 KPI、测试优先级)·
> [well-model-kpi-rules.md](well-model-kpi-rules.md)(各举升类型的 KPI 规则)·
> [production/oil-rate-kpis.md](production/oil-rate-kpis.md)(WSO / WT / Alloc 口径)·
> [ai-agent-model-driven-optimization.md](ai-agent-model-driven-optimization.md)(AI Agent 与模型管理)。

## 0. 两个阶段的目标

| 阶段 | 目标 | 数据重心 |
|---|---|---|
| **Well Test Management** | 获取某口井在特定测试时间内的**真实**生产能力和流动状态 | 实测的产量、压力、测试信息、数据质量 |
| **Model Calibration** | 让模型预测的结果尽可能接近试井得到的真实结果 | 在试井数据之外,还要油藏、PVT、井筒、举升设备、历史生产、IPR/VLP 参数 |

例:模型预测日产油 25 m³/d,试井实测 20 m³/d,就需要检查模型参数,分析偏差来自哪里。

两者有联系但数据要求不同,见第三节对比。

---

## 一、Well Test Management 必须准备的数据

### 1. 基础井信息(Well Information)——必需

| 数据项 | 英文名称 | 说明 |
|---|---|---|
| 井名 | Well Name | 唯一标识油井 |
| 井号 | Well ID | 系统内部唯一 ID |
| 油田 | Field | 所属油田 |
| 区块 | Reservoir / Block | 所属区块 |
| 井类型 | Well Type | Oil / Gas / Water / Injector |
| 井状态 | Well Status | Producing / Shut-in / Suspended |
| 完井日期 | Completion Date | 完井时间 |
| 人工举升方式 | Lift Type | ESP / SRP / PCP / Gas Lift 等 |

用途:确定测试对象,并关联后续的生产数据和模型。

### 2. 试井测试基本信息(Well Test Information)——必需

| 数据项 | 英文名称 | 说明 |
|---|---|---|
| 测试编号 | Test ID | 每次试井的唯一标识 |
| 测试日期 | Test Date | 测试时间 |
| 开始时间 | Start Time | |
| 结束时间 | End Time | |
| 测试时长 | Test Duration | 持续测试时间 |
| 测试类型 | Test Type | Production Test / Build-up / Drawdown 等 |
| 测试设备 | Test Equipment | 测试分离器、流量计等 |
| 测试状态 | Test Status | Planned / In Progress / Completed / Validated |

> 同一口井可以有多次试井记录,所以 **Test ID 和时间信息**非常重要。

### 3. 生产测试数据(Production Test Data)——核心必需

这是 Well Test Management 最重要的数据。

| 数据项 | 英文名称 | 常见单位 |
|---|---|---|
| 油产量 | Oil Rate | m³/d 或 STB/d |
| 气产量 | Gas Rate | m³/d 或 MSCF/d |
| 水产量 | Water Rate | m³/d 或 STB/d |
| 液体产量 | Liquid Rate | m³/d |
| 含水率 | Water Cut | % |
| 气油比 | GOR | m³/m³ 或 scf/STB |
| 总液量 | Total Liquid Volume | m³ |
| 累计产油量 | Cumulative Oil | m³ 或 STB |

示例:一次 24 小时生产测试

| 参数 | 结果 |
|---|---|
| Oil Rate | 20 m³/d |
| Gas Rate | 2,000 m³/d |
| Water Rate | 5 m³/d |
| Liquid Rate | 25 m³/d |
| Water Cut | 20% |
| GOR | 100 m³/m³ |

关系:`Liquid Rate = Oil Rate + Water Rate`(前提是体积基准和计量条件一致);
示例中 Water Cut = 5 / 25 = 20%,GOR = 2000 / 20 = 100。

### 4. 压力和温度数据(Pressure & Temperature)——核心必需

| 数据项 | 英文名称 | 说明 |
|---|---|---|
| 井口压力 | Wellhead Pressure (WHP) | |
| 井口温度 | Wellhead Temperature (WHT) | |
| 油管压力 | Tubing Head Pressure (THP) | |
| 套管压力 | Casing Pressure | |
| 流压 | Flowing Bottomhole Pressure (FBHP) | 流动状态下井底压力 |
| 静压 | Shut-in Pressure / SBHP | 关井状态下的压力 |
| 地层压力 | Reservoir Pressure | |

要点:
- **常规生产测试**:至少需要可靠的产量、测试时间和对应的压力数据。
- **压力恢复测试(Pressure Build-up)**:还需要关井时间序列、压力恢复曲线、关井前的生产历史。
- **FBHP 没有直接测量值时**,可以按可靠的梯度数据或井筒模型估算,但必须标记为**计算值**,不能当作实测值。

### 5. 测试质量和验证(Quality Control)

| 数据项 | 英文名称 | 说明 |
|---|---|---|
| 数据来源 | Data Source | 测试分离器、传感器等 |
| 计量设备 | Measurement Device | 流量计、压力计 |
| 数据质量 | Data Quality | 数据是否可靠 |
| 测试有效性 | Test Validity | Valid / Invalid |
| 异常说明 | Comments | 记录测试异常 |
| 审核人 | Approved By | |

企业级试井管理需要这一部分:**不是所有上传的试井数据都能直接用于模型校准**。

---

## 二、Model Calibration 必须准备的数据

在 Prosper / WPO 这类油井建模和生产优化场景中,通常需要下面几类。

### 1. 油藏数据(Reservoir Data)——核心必需

| 数据项 | 英文名称 | 说明 |
|---|---|---|
| 地层压力 | Reservoir Pressure (Pr) | 当前地层压力 |
| 地层温度 | Reservoir Temperature | |
| 渗透率 | Permeability (K) | 储层流体通过能力 |
| 厚度 | Reservoir Thickness (H) | 有效储层厚度 |
| 孔隙度 | Porosity | |
| 表皮系数 | Skin Factor | 近井地带流动阻力 |
| 泡点压力 | Bubble Point Pressure (Pb) | 原油开始析气的压力 |
| 排水半径 | Drainage Radius | 井的有效泄流范围 |

描述油藏向井筒供液的能力。地层压力、流体性质、IPR 模型所需参数尤其重要。

### 2. 流体性质 PVT 数据——核心必需

PVT = Pressure、Volume、Temperature,描述油、气、水在不同压力温度下的物理性质。

| 数据项 | 英文名称 | 说明 |
|---|---|---|
| 原油密度 | Oil Density | |
| 天然气相对密度 | Gas Specific Gravity | 相对空气 |
| 原油体积系数 | Oil Formation Volume Factor (Bo) | 地层原油与地面原油的体积关系 |
| 天然气体积系数 | Gas Formation Volume Factor (Bg) | |
| 原油黏度 | Oil Viscosity | |
| 天然气黏度 | Gas Viscosity | |
| 水黏度 | Water Viscosity | |
| 泡点压力 | Bubble Point Pressure | |
| 溶解气油比 | Solution GOR (Rs) | 溶解在原油中的气体量 |

来源:通常是实验室 PVT 报告,也可以用经过验证的相关流体模型。

重要性:同样日产 20 m³ 的井,在不同的温度、压力和流体性质下,井筒流动状态可能完全不同。

### 3. 井筒和完井数据(Wellbore & Completion)——核心必需

| 数据项 | 英文名称 | 对模型的影响 |
|---|---|---|
| 井深 | Measured Depth (MD) | 静液柱压力 |
| 垂深 | True Vertical Depth (TVD) | |
| 油管内径 / 外径 | Tubing ID / OD | 流动压降 |
| 套管尺寸 | Casing Size | |
| 射孔深度 | Perforation Depth | 流入特征 |
| 完井层段 | Completion Interval | |
| 井斜数据 | Well Trajectory | 多相流动特征 |
| 井口设备 | Surface Equipment | |

### 4. 人工举升设备数据(Artificial Lift)——按井类型要求

不同举升类型要不同参数,**系统应按 Lift Type 自动要求对应参数**,不是每口井都要全部。

| 举升方式 | 需要准备的参数 |
|---|---|
| **ESP** 电潜泵 | 泵厂商/型号、下泵深度、泵频率(Hz)、级数、泵性能曲线、电机功率、吸入口压力、排出口压力 |
| **SRP** 抽油机/杆式泵 | 泵深、冲程长度、冲次(SPM)、泵径、抽油杆组合、泵充满度(Pump Fillage) |
| **Gas Lift** 气举 | 注气量、注气压力、气举阀深度、阀配置、阀开启压力、气举性能数据 |
| **PCP** 螺杆泵 | 泵型号、下泵深度、转速(RPM)、排量、扭矩、泵性能曲线 |

### 5. 历史生产数据(Production History)——强烈建议

| 数据项 | 英文名称 |
|---|---|
| 历史日产油 / 气 / 水 | Historical Oil / Gas / Water Rate |
| 历史含水率 | Historical Water Cut |
| 历史井口压力 / 油管压力 | Historical WHP / THP |
| 历史泵频率 | Historical Pump Frequency(ESP 等) |
| 开关井记录 | Production / Shut-in History |

单次试井只反映一个时间点。历史数据帮助判断:产量是否持续下降、地层压力是否降低、含水率是否升高、举升设备是否性能衰减、生产参数变化是否导致模型偏差。

### 6. IPR / VLP 模型参数

- **IPR**(Inflow Performance Relationship):地层向井筒供液的能力。
  常见参数:Reservoir Pressure、Productivity Index (PI)、Skin Factor、Bubble Point Pressure、Reservoir Permeability。
- **VLP**(Vertical Lift Performance):流体从井底沿井筒到地面的压力损失。
  常见参数:Tubing Diameter、Tubing Roughness、Well Depth、Fluid Properties、Water Cut、Gas-Liquid Ratio、Wellhead Pressure、Temperature Profile。

两条曲线的**交点是预测的工作点(Operating Point)**。校准的目的之一,就是使模型算出的工作点与实际试井数据匹配。

---

## 三、两个流程的数据要求对比

| 数据分类 | Well Test Management | Model Calibration |
|---|---|---|
| Well Information | 必需 | 必需 |
| Test ID / Test Date | 必需 | 关联试井记录 |
| Oil / Gas / Water Rate | 必需 | 必需 |
| WHP / THP | 重要 | 必需或有可靠替代数据 |
| FBHP | 视测试类型而定 | 强烈建议 |
| Pressure Build-up Data | 压恢测试必需 | 特定校准场景需要 |
| Reservoir Parameters | 视测试类型而定 | 必需或需要可靠估算 |
| PVT Data | 视测试类型而定 | 必需 |
| Wellbore Geometry | 视测试类型而定 | 必需 |
| Artificial Lift Parameters | 视测试类型而定 | 举升井必需 |
| Historical Production | 强烈建议 | 强烈建议 |
| IPR / VLP Parameters | 非必需 | 必需或由模型计算生成 |

「必需」要结合具体的测试类型、模型类型和软件采用的计算方法判断,**并不是每个试井任务都要填全部字段**。

---

## 四、产品设计建议:分阶段的数据准备检查(Data Readiness Check)

> 以下为设计建议,不是已实现功能。思路是**不让用户一次填完所有参数**。

| 步骤 | 内容 |
|---|---|
| 1. Select Well | 选择 Field、Well、Well Type、Lift Type,自动读取已有井信息 |
| 2. Prepare Well Test | 导入测试时间、Oil / Gas / Water Rate、WHP、THP 等 |
| 3. Validate Test Data | 检查数据完整性、单位、测试时长,以及压力与产量是否合理 |
| 4. Select Model | 关联 Prosper Model,检查 PVT、Reservoir、Wellbore、Artificial Lift 参数 |
| 5. Model Calibration | 用实际试井结果和模型预测结果对比,调整模型参数 |
| 6. Review Results | 查看校准前后误差、IPR/VLP 曲线、Operating Point,保存校准版本 |

### 自动检查清单示例

选择一口 ESP 井后,系统可以这样列出就绪情况(仅为交互示例,**不是真实井数据或真实校验结果**):

**Well: WELL-001 · Lift Type: ESP**

| 分组 | 数据项 | 状态 |
|---|---|---|
| Well Test Data | Well ID / Well Name | 已具备 |
| | Test Date / Duration | 已具备 |
| | Oil / Gas / Water Rate | 已具备 |
| | WHP / THP | 已具备 |
| | FBHP | 待补充 |
| Model Data | PVT Data | 已具备 |
| | Reservoir Pressure | 已具备 |
| | Wellbore Geometry | 已具备 |
| | ESP Pump Model | 已具备 |
| | Pump Performance Curve | 待补充 |
| | Historical Production | 待补充 |
| Calibration Readiness | | 待检查 |

---

## 五、业务设计思路:三类数据,三种处理方式

| 数据类型 | 来源 | 系统处理方式 |
|---|---|---|
| 基础数据 | Well Master / Well Configuration | 自动获取 |
| 实际测量数据 | Well Test / Production System | 导入或关联 |
| 模型参数 | Prosper Model / Reservoir Model | 自动读取,检查缺失项 |

这样用户不需要重复录入系统里已经存在的数据。

理想流程:

```
用户选择一口井
  → 系统自动获取已有数据
  → 检查缺失项
  → 用户补充必要数据
  → 验证试井数据
  → 关联模型
  → 执行 Calibration
```

### 对 AI Agent 工作流的意义

这是从传统油田软件走向 AI Agent 工作流的基础:Agent 不只是执行任务,还应该知道
**执行任务需要什么数据、哪些已经存在、哪些不可靠、下一步该向用户索取什么**。

## 六、后续可做

- [ ] 梳理 Well Test Management → Model Calibration → Model Validation → Production Optimization 的完整链路,明确每阶段的数据输入、处理逻辑和输出。
- [ ] 把上面的字段与 DFS / WPO 实际数据模型(`data-model/`)逐项对照,标出哪些已有、哪些缺失。
- [ ] 按各举升类型,与 [well-model-kpi-rules.md](well-model-kpi-rules.md) 的校准判据对齐。
