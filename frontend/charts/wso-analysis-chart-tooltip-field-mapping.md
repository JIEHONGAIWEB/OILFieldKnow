# WSO Well Analysis — 图表 Tooltip 字段映射

> 来源: `C:/Users/h224847/code/EEE-WPO/wpo-11-06-02/wpo-app/docs/wso/overview/ANALYSIS_CHART_TOOLTIP_FIELD_MAPPING.md`
>
> 目的: 说明 Well Analysis 各图表 Tooltip 展示项对应的后端 API 字段来源。

## 1. 适用范围

本映射适用于以下 Well Analysis 图表类型:

- INFLOW PERFORMANCE CURVE
- GL PERFORMANCE CURVE
- PUMP PERFORMANCE CURVE
- VLP/IPR PLOT
- GRADIENT PLOT

## 2. 数据链路总览

### 2.1 图表主数据 API（按图表）

- INFLOW PERFORMANCE CURVE
  - API: `getInflowPerformance`
  - Endpoint: `/wpo/wells/{wellId}/optimizations/performances/iprperformance`
- GL PERFORMANCE CURVE
  - API: `getGasLiftPerformance`
  - Endpoint: `/wpo/wells/{wellId}/optimizations/performances/gas-lift`
- PUMP PERFORMANCE CURVE
  - API: `getPumpPerformance`
  - Endpoint: `/wpo/wells/{wellId}/optimizations/performances/pump`
- VLP/IPR PLOT
  - API: `getVlpIprPerformance`
  - Endpoint: `/wpo/wells/{wellId}/optimizations/performances/inflow`
- GRADIENT PLOT
  - API: `getGradientPlot`
  - Endpoint: `/wpo/wells/{wellId}/optimizations/gradient-plots`

### 2.2 Tooltip 二次补数 API

- API: `getAnalysisParameters`
- Endpoint: `/wpo/wells/{wellId}/optimizations/analysis-parameters?date=...&timezone=...`
- 匹配结构:
  - `currentParameters`
  - `opportunityParametersMap`
  - `historicalParametersMap`
  - `optimumParametersMap`

Tooltip 实际展示数据:

- `mergedData = pointData + resolvedDataFromAnalysisParameters`
- 同名字段时，resolved 补数数据优先于原始点数据。

## 3. Tooltip 字段映射（按图表）

## 3.1 PUMP PERFORMANCE CURVE

### A. 主数据点字段（extractor）

- `liquidRate` <- `liquidRate | liquid_rate | flowRate`
- `oilRate` <- `oilRate`
- `waterRate` <- `waterRate`
- `frequency` <- `frequency | pumpFrequency`
- `fthp` <- `fthp | whp`
- `date` <- `date`
- `oilGain` <- `oilGain`

### B. Tooltip 展示取值回退顺序

- Liquid Rate: `liquidRateSurface -> pumpLiquidRate -> liquidRate -> "-"`
- Oil Rate: `oilRate -> "-"`
- Water Rate: `waterRate -> "-"`
- Oil Gain: `oilGain -> "-"`
- Frequency: `pumpFrequency -> frequency -> "-"`
- THP: `whp -> fthp -> pressure -> "-"`

## 3.2 GL PERFORMANCE CURVE

### A. 主数据点字段（extractor）

- `gasLiftRate` <- `gas_lift_rate | gasLiftRate | glir`
- `oilRate` <- `oil_rate | oilRate`
- `gasRate` <- `gas_rate | gasRate`
- `waterRate` <- `water_rate | waterRate`
- `pressure` <- `pressure | fthp`
- `fthp` <- `fthp`
- `date` <- `analysis_date | analysisDate | date`
- `oilGain` <- `oil_gain | oilGain`

### B. Tooltip（curve point, `isCurvePoint=true`）

- Title: `THP: fthpName`
- GLIR: `gasLiftRate -> glir -> value[0]`
- Oil Rate: `oilRate -> value[1]`

### C. Tooltip（scatter point）

- Liquid Rate: `liquidRateSurface -> pumpLiquidRate -> liquidRate -> "-"`
- Oil Rate: `oilRate -> data.value[1] -> "-"`
- Water Rate: `waterRate -> "-"`
- Oil Gain: `oilGain -> "-"`
- GLIR: `gasLiftRate -> glir -> data.value[0] -> "-"`
- THP: `whp -> fthp -> pressure -> "-"`

## 3.3 INFLOW PERFORMANCE CURVE

### A. 主数据点字段（extractor）

- 曲线点坐标:
  - 气井: `x = gasRate`, `y = pressure`
  - 油井: `x = oilRate`, `y = pressure`
- 散点补充字段:
  - `gasRate`, `liquidRate`, `oilRate`, `waterRate`, `pressure`, `fthp`, `date`, `oilGain`, `gasGain`

### B. Tooltip（curve point, `isCurvePoint=true`）

- 气井:
  - Associate Gas Rate: `gasRate | liquidRate | value[0]`
  - Pressure: `pressure | value[1]`
- 油井:
  - Oil Rate: `oilRate | liquidRate | value[0]`
  - Pressure: `pressure | value[1]`

### C. Tooltip（scatter point, 气井）

- Associate Gas Rate: `gasRate -> data.value[0] -> "-"`
- Water Rate: `waterRate -> "-"`
- Gas Gain: `gasGain -> "-"`
- THP: `whp -> fthp -> pressure -> "-"`

### D. Tooltip（scatter point, 油井）

- Liquid Rate: `liquidRateSurface -> pumpLiquidRate -> liquidRate -> data.value[0] -> "-"`
- Oil Rate: `oilRate -> "-"`
- Water Rate: `waterRate -> "-"`
- Oil Gain: `oilGain -> "-"`
- THP: `whp -> fthp -> pressure -> "-"`

## 3.4 VLP/IPR PLOT

### A. 主数据点字段（extractor）

- x 字段:
  - 气井: `gasRate`
  - 其他: `liquidRate`
- y 字段: `pressure`

### B. Tooltip 展示项

- ESP: `Rate(value[0])`, `Pressure(value[1])`
- 气井: `Associate Gas Rate(value[0])`, `Pressure(value[1])`
- 其他: `Liquid Rate(value[0])`, `Pressure(value[1])`

该图 Tooltip 主要读取点坐标值，不依赖 analysis-parameters 补数对象。

## 3.5 GRADIENT PLOT

### A. 主数据点字段（extractor）

- 通用坐标: `[pressure, depth]`

### B. Tooltip 展示项

- Pressure: `value[0]`
- Depth: `value[1]`

该图 Tooltip 主要读取点坐标值，不依赖 analysis-parameters 补数对象。

## 4. analysis-parameters 匹配主键规则

Tooltip 补数是否命中，依赖点上的 identity 字段:

- `currentId`
- `opportunityId`
- `historicalId`
- `optimumId`
- `sourceId`（兜底）

匹配成功后从以下结构读取:

- `currentParameters`
- `opportunityParametersMap[pointId]`
- `historicalParametersMap[pointId]`
- `optimumParametersMap[pointId]`

## 5. 单位显示规则

Tooltip 单位文本通过 `withUnit(...)` 统一生成:

- `resolveUnitLabel(getUnit, unitCode, fallbackUnit)`
- 若 `getUnit(unitCode)` 为空，则回退到 `fallbackUnit`

示例:

- Oil Rate: `unitCode = oil_rate`，回退 `bopd`
- Pressure: `unitCode = pressure`，回退 `ksc`

## 6. 代码入口索引

- Tooltip 构建入口:
  - `buildAnalysisTooltipOption`
  - `libs/wso/src/lib/features/well-analysis/components/analysis-chart/core/transformers/parts/analysis-chart-tooltip.builder.ts`

- 主图表数据 API 路由:
  - `getAnalysisChartLoader`
  - `libs/wso/src/lib/features/well-analysis/components/analysis-chart/core/loaders/analysis-chart.loaders.ts`

- API 定义:
  - `AnalysisChartService`
  - `libs/wso/src/lib/features/well-analysis/servies/analysis-chart.service.ts`

- Tooltip 补数解析:
  - `resolveTooltipDataFromAnalysisParameters`
  - `libs/wso/src/lib/features/well-analysis/components/analysis-chart/analysis-chart.component.ts`

- analysis-parameters 选中 opportunity 映射:
  - `resolveSelectedOpportunityFromAnalysisParameters`
  - `libs/wso/src/lib/features/well-analysis/components/analysis-chart/parts/common/detail/analysis-chart-selected-opportunity.util.ts`