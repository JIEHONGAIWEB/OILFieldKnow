# WSO Detail Table Exception Rulebook

## 1. 目的

- 定义明细表异常高亮规则的唯一事实来源（single source of truth）。

## 2. 适用范围

- 当前模块中 WSO Overview 明细表（detail table）的异常高亮。

### 2.1 关键表头含义（石油业务语义）

针对明细表常见列 `OIL RATE_WSO`、`OIL RATE_WT`、`OIL RATE_ALLOC`，业务含义如下：

- `OIL RATE_WSO`（Well Stream Oil）
  - 含义：井口混合产物流中的油相产量（井流中的油），用于反映当前生产状态。
  - 常见来源：在线监测/实时生产链路。
  - 典型用途：看“现在产了多少油”。

- `OIL RATE_WT`（Well Test）
  - 含义：单井在测试工况下通过测试分离器得到的实测产油率。
  - 常见来源：井测作业结果（非连续时序，按测试频次刷新）。
  - 典型用途：作为单井真实性能基准，用于模型校准与偏差核对。

- `OIL RATE_ALLOC`（Allocation）
  - 含义：在多井共管/共站场景下，将总量按算法分摊后的单井归属产量。
  - 常见来源：分摊算法（结合井测、压力、工况、历史趋势等）。
  - 典型用途：看“这口井应被记账多少产量”。

判读要点：

- `WT` 更接近“单井实测真值”，但时效性受测试频次影响。
- `WSO` 更接近“当前运行态势”，通常时效性更强。
- `ALLOC` 是“归属口径”，用于群井共享管网时的核算与对账。
- 三者不要求完全相等；偏差本身是监控信号，常用于触发异常分析（工况变化、计量偏差、分摊参数漂移等）。

单位说明：

- 常见单位为 `m3/d` 或 `bbl/d`（BOPD）。
- 比较阈值前需确保单位一致；如存在单位换算失败，应禁用对应阈值比较规则。

源码位置：

- `libs/wso/src/lib/features/wso-overview/components/detail-table/wso-detail-table/parts/wso-detail-table-detail.config.ts`
- `libs/wso/src/lib/features/wso-overview/components/detail-table/wso-detail-table/parts/wso-detail-table-exception.util.ts`

## 3. 规则引擎语义

### 3.1 规则类型

- value：当字段值命中配置的 values 列表时高亮。
- lessThan：当当前值严格小于阈值时高亮。
- greaterThan：当当前值严格大于阈值时高亮。

### 3.2 阈值计算

- 生效阈值 = 基准值 + offset。

基准值来源：

- 固定阈值字段 `threshold`
- 对比字段值 `compareField`

### 3.3 数值解析行为

- 数值规则仅在对比双方都可解析为有限数字（finite number）时执行。

### 3.4 边界行为

- 等于阈值时，不命中 `lessThan` 或 `greaterThan`。

### 3.5 高亮样式

- 命中单元格使用异常背景色与文本色变量。

### 3.6 范围边界（最小值 / 最大值，默认为空）

- 默认状态：最小值与最大值均不预填（为空）；空值不视为 0 参与比较。
- 仅填写最小值（max 为空）：所有有效数值必须 `value >= min`，小于 min 不通过，等于或大于 min 通过。
- 仅填写最大值（min 为空）：所有有效数值必须 `value <= max`，大于 max 不通过，等于或小于 max 通过。
- 同时填写最小值和最大值：所有有效数值必须落在区间内，`min <= value <= max`，低于 min 或高于 max 均不通过。
- 两者都为空：不施加范围限制，任意有效数值通过。
- `min > max` 为非法输入，直接判定校验失败。
- 完整的边界示例与单元测试矩阵见 [min-max-range-unit-test-requirements.md](../testing/min-max-range-unit-test-requirements.md)。

## 4. 规则 ID 约定

格式：

- `WSO-[Chart]-[Domain]-[NNN]`

示例：

- `WSO-RTC-OIL-001`
- `WSO-RTC-GAS-001`
- `WSO-GL-ALL-001`
- `WSO-ESP-ALL-001`

图例：

- RTC = Rate Comparison
- RGC = Reservoir Guideline Compliance
- GL = Gas Lift Performance Exception
- ESP = ESP System Performance

## 5. 规则目录

## 5.1 RTC: OIL_RATE_COMPARISON

| Rule ID | Field | Expression | Boundary Example |
|---|---|---|---|
| WSO-RTC-OIL-001 | flowingStatus | value in [Not Flowing] | Not Flowing: highlighted; Flowing: not highlighted |
| WSO-RTC-OIL-002 | oilRateWsoProChangeRatio | value > 0 | -0.1: not highlighted; 0: not highlighted; 0.1: highlighted |
| WSO-RTC-OIL-003 | oilRateWtProChangeRatio | value > 0 | -0.1: not highlighted; 0: not highlighted; 0.1: highlighted |
| WSO-RTC-OIL-004 | oilRateAllocProChangeRatio | value > 0 | -0.1: not highlighted; 0: not highlighted; 0.1: highlighted |

说明：

- 当 `productionType` 被识别为气井类型时，选择 RTC gas 规则集。
- 对于 `productionType = SRP`，会移除 `oilPotential` 列；上述异常规则不变。

## 5.2 RTC: GAS_RATE_COMPARISON

| Rule ID | Field | Expression | Boundary Example |
|---|---|---|---|
| WSO-RTC-GAS-001 | gasRateWsoProChangeRatio | value > 0 | -0.1: not highlighted; 0: not highlighted; 0.1: highlighted |
| WSO-RTC-GAS-002 | gasRateWtProChangeRatio | value > 0 | -0.1: not highlighted; 0: not highlighted; 0.1: highlighted |
| WSO-RTC-GAS-003 | gasRateAllocProChangeRatio | value > 0 | -0.1: not highlighted; 0: not highlighted; 0.1: highlighted |

## 5.3 FLOWING_STATUS

| Rule ID | Field | Expression | Boundary Example |
|---|---|---|---|
| WSO-FS-ALL-001 | label | value in [Not Flowing] | Not Flowing: highlighted; Others: not highlighted |

## 5.4 RGC: RESERVOIR_GUIDELINE_COMPLIANCE (Oil)

| Rule ID | Field | Expression | Boundary Example |
|---|---|---|---|
| WSO-RGC-OIL-001 | fbhpWso | value < bubblePoint | value=bp: not highlighted; value<bp: highlighted |
| WSO-RGC-OIL-002 | wcWt | value > previousWcWt | value=prev: not highlighted; value>prev: highlighted |

## 5.5 RGC: RESERVOIR_GUIDELINE_COMPLIANCE (Gas)

| Rule ID | Field | Expression | Boundary Example |
|---|---|---|---|
| WSO-RGC-GAS-001 | liquidLoading | value in [true] | true: highlighted; false: not highlighted |

## 5.6 GL: GL_PERFORMANCE_EXCEPTION

常量：

- GL offset = 99.9758214885342 Mscf/d

| Rule ID | Field | Expression | Boundary Example |
|---|---|---|---|
| WSO-GL-ALL-001 | gasLiftRate | value > optimumGasLiftRate + 99.9758214885342 | value=upper: not highlighted; value>upper: highlighted |
| WSO-GL-ALL-002 | gasLiftRate | value < optimumGasLiftRate - 99.9758214885342 | value=lower: not highlighted; value<lower: highlighted |
| WSO-GL-ALL-003 | multiPointDescription | value in [Yes] | Yes: highlighted; No: not highlighted |

单位说明：

- 若可进行单位换算，offset 会转换到当前显示单位。
- 若单位换算失败，该列基于 offset 的规则将被禁用。

## 5.7 ESP: ESP_SYSTEM_PERFORMANCE

| Rule ID | Field | Expression | Boundary Example |
|---|---|---|---|
| WSO-ESP-ALL-001 | motorEfficiencyUpper | value < 90 | 89.9: highlighted; 90: not highlighted |
| WSO-ESP-ALL-002 | motorLoadUpper | value > 95 | 95: not highlighted; 95.1: highlighted |
| WSO-ESP-ALL-003 | pumpOperationUpper | value in [Upthrust, Downthrust] | Upthrust: highlighted; Normal: not highlighted |
| WSO-ESP-ALL-004 | pumpWearFactorUpper | value > 20 | 20: not highlighted; 20.1: highlighted |
| WSO-ESP-ALL-005 | gvf | value > 30 | 30: not highlighted; 30.1: highlighted |

## 5.8 无异常规则的图表

- PROD_LOSS
- OIL_GAIN_POTENTIAL
- GAS_GAIN_POTENTIAL
- SRP_PERFORMANCE

## 6. 治理

## 6.1 变更流程

1. 在 detail-table 代码中更新规则配置。
2. 在同一变更集中同步更新本规则书。
3. 确认阈值方向与边界行为的业务语义。
4. 补充阈值两侧（正向、等于、反向）的测试用例。

## 6.2 评审检查清单

- Rule ID 存在且唯一。
- 字段与图表映射正确。
- 边界示例已同步更新。
- 对于基于 offset 的规则，已注明单位换算说明。

## 6.3 单元测试（技术实现）

### 6.3.1 测试目标

- 验证规则类型语义正确：`value`、`lessThan`、`greaterThan`。
- 验证阈值计算正确：`effectiveThreshold = base + offset`。
- 验证边界行为正确：等于阈值不命中大小比较规则。
- 验证异常输入兜底：非数值、空值、缺失 compareField 时不误高亮。
- 验证单位换算失败策略：offset 规则被禁用而非错误命中。

### 6.3.2 建议测试文件

- `wso-detail-table-exception.util.spec.ts`
  - 重点覆盖：规则命中判定函数、阈值解析函数、单位换算分支。
- `wso-detail-table-detail.config.spec.ts`
  - 重点覆盖：规则配置完整性（Rule ID 唯一、字段存在、图表映射正确）。

建议与被测文件同目录放置，便于规则变更时同步维护。

### 6.3.3 最小用例矩阵

每条规则至少覆盖以下 3 组输入：

- 正向命中样例（应高亮）。
- 边界相等样例（不应高亮）。
- 反向不命中样例（不应高亮）。

示例（以 `value > 0` 为例）：

- `-0.1` -> 不高亮
- `0` -> 不高亮
- `0.1` -> 高亮

示例（以 `value in [Not Flowing]` 为例）：

- `Not Flowing` -> 高亮
- `Flowing` -> 不高亮

### 6.3.4 GL offset 规则专项

针对 `WSO-GL-ALL-001/002`，至少包含：

- 上下阈值边界点（等于上限/下限）不高亮。
- 略高于上限、略低于下限时高亮。
- 单位换算成功时按换算后 offset 判定。
- 单位换算失败时，该列 offset 规则禁用（不命中）。

### 6.3.5 配置质量校验（建议）

- Rule ID 全局唯一。
- `field` 在对应数据模型中可访问。
- 使用 `compareField` 的规则必须能读取到 compare 值。
- 同一图表规则集不得出现语义冲突（例如同字段同条件重复定义）。

### 6.3.6 覆盖率建议

- 规则引擎核心分支覆盖率建议不低于 90%。
- 新增或修改规则时，必须同时补充对应单元测试。
- 缺少测试的规则变更不应合入主分支。

## 6.4 版本记录

- v1.1 (2026-11-06)
  - 文档调整为英文单语版本。
- v1.0 (2026-11-06)
  - 初始双语层级规则书。
  - 包含 RTC、FS、RGC、GL、ESP 规则集。