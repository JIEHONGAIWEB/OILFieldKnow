# ESP Production Summaries — 后端接口字段与计算逻辑

> 接口:`POST wpo/wells/esp-production-summaries`(WSO Overview 的 KPI 卡片数据源)。
> 本文说明**后端**读取哪些数据、对每个字段做了什么运算。前端调用侧见
> [wso-v1-overview-api.md](wso-v1-overview-api.md),全部 WSO 接口清单见
> [wso-api-list.md](wso-api-list.md),业务含义见
> [oil-rate-kpis.md](../../domain-knowledge/production/oil-rate-kpis.md)。
>
> **来源**:`wpo-prodoptimization-service`,分析于 2026-11-16。
>
> | 层 | 文件 |
> |---|---|
> | Controller | `ESPOverviewController.getProductionSummary` |
> | Service | `service/ESPOverviewService.java` → `getProductionSummary`、`getEspProductionSummaryOutput`、`getUptimeFactor` |
> | DTO | `dto/esp/overview/ESPProductionSummaryInput` / `ESPProductionSummaryOutput` / `ESPProductionSummaryDiffRatio` |
>
> **未覆盖**:mapper SQL(`getOilRateWso`、`getOpportunityOilPotential`)、
> `UnitAwareResponseUtils` 的换算实现、`businessService` / `alarmService` 的下游接口,均未读取,
> 下文涉及这些处的描述标注为推测。

## 1. 请求

只有 **POST**,路径 `…/wpo/wells/esp-production-summaries`,`Content-Type: application/json`。

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `wellIds` | `List<Integer>` | 是 | 要汇总的井 ID |
| `date` | `String` | 否 | `MM/dd/yyyy`。不传则取**昨天** |

> ⚠️ **与前端文档不一致,待确认**:[wso-v1-overview-api.md](wso-v1-overview-api.md) 和
> [wso-feature.md](../../frontend/pages/wso-feature.md) 把这个接口记为 `GET`
> (参数 `wellIds`、`date`、`timezone`)。后端搜索整个 `src/main`,该路径只在
> `ESPOverviewController` 里定义了一次,方法是 `@POST`,请求体 DTO 也**没有 `timezone`**。
> 需要核对前端实际调用方式,或是否有网关 / 其他版本做了转换。

## 2. 处理流程

```
getProductionSummary(wellIds, date)
 ├─ specifiedDate = date 为空 ? 昨天 : parse(date)
 ├─ current  = getEspProductionSummaryOutput(wellIds, specifiedDate)
 ├─ previous = getEspProductionSummaryOutput(wellIds, specifiedDate - 1 天)
 └─ current / previous 任一为 null → 直接返回 current(没有 diffRatio)
    否则 current.calculateChange(previous) → 填充 diffRatio
```

### 2.1 单日汇总 `getEspProductionSummaryOutput`

**第 1 步:给井分类。**
调用 `businessService.wellStatusLatestPost`,类型 `Condition`,取指定日期的最新状态,按 `wellStatusLabel` 分组:

| 分组 | 条件 | 用途 |
|---|---|---|
| 流动井 | `Flowing` | 产量、潜力、试井、分配、开井率 |
| 未流动井 | `Not Flowing` | 关井损失(shut-in) |
| SRP 井 | 流动井中生产方式为 `SRP` | 产油量单独走 SRP 数据 |

这一步抛异常或没有任何状态时,**当天返回 `null`**(并不报错,异常只记日志)。

**第 2 步:并行取数。** 用 `TaskGroup` 同时执行 9 个任务。流动井 / 未流动井列表为空时,对应任务返回 `null`。

| 任务 | 数据来源 | 关键条件 |
|---|---|---|
| `oilRateDao` | `espOverviewMapper.getOilRateWso` | 流动井,只保留 `days == 0` |
| `oilPotentialDao` | `espOverviewMapper.getOpportunityOilPotential` | 流动井 |
| `wellTestFlowMeasurementDao` | `getWellTestFlowMeasurementsLastest` | 流动井,Flow Test,最新 1 条 |
| `gasLiftWellTestFlowMeasurementDao` | `getGasLiftWellTestFlowMeasurementsLastest` | 流动井 |
| `oilShutInDao` | `businessService.getLostVolumesPost` | 未流动井,产品 Oil,reportingFlow `Production`,limit 1 |
| `gasShutInDao` | 同上 | 未流动井,产品 Gas |
| `rateAllocDaoTask` | `businessService.wellProductionSummary` | 流动井,`Allocated`,按日,fromDate = toDate = 当天 |
| `uptimeTask` | `businessService.entityDailyVolumes` | 流动井,产品 Oil + Gas,`Allocated`,按日 |
| `srpWellTask` | `alarmService.getSRPWrapper` | SRP 井 |

**第 3 步:汇总成字段。** 结果对象先用 14 个字段初始化为 `0.0`,再按下表覆盖。

## 3. 输出字段与运算

所有求和都先把 `null` 当作 `0.0`。`UnitField` 列是该字段的单位参数类型。

| 输出字段 | 单位参数 | 取值逻辑 |
|---|---|---|
| `oilRateWso` | OIL_RATE | **SRP 井**:`Σ(SRP.oilRate × 开井率)`;**其余流动井**:`Σ(oil_rate × 开井率)`;两者相加 |
| `gasRateWso` | GAS_RATE | 对 `oilRateDao` 里**所有**流动井(含 SRP 井):`Σ(gas_rate × 开井率)` |
| `gasLiftRateWso` | GAS_LIFT_RATE | `Σ gas_lift_rate`(**不乘开井率**) |
| `oilPotentialWso` | OIL_RATE | `oilRateWso + Σ oil_gain` |
| `gasPotentialWso` | GAS_RATE | `gasRateWso + Σ gas_gain` |
| `oilRateWt` | OIL_RATE | 试井结果中产品为 Oil 的 `Σ rate` |
| `gasRateWt` | GAS_RATE | 试井结果中产品为 Gas 的 `Σ rate` |
| `gasLiftRateWt` | GAS_LIFT_RATE | 气举试井 `Σ rate` |
| `shutInWellPotential` | OIL_RATE | 未流动井 `Σ lostVolume`(Oil) |
| `gasShutInWellPotential` | GAS_RATE | 未流动井 `Σ lostVolume`(Gas) |
| `oilRateAlloc` | OIL_RATE | 分配产量 `Σ oilVolume` |
| `gasRateAlloc` | GAS_RATE | 分配产量 `Σ gasVolume` |
| `diffRatio` | — | 见第 4 节 |

> WSO = Well Stream Oil,WT = Well Test,含义见 [oil-rate-kpis.md](../../domain-knowledge/production/oil-rate-kpis.md)。

### 开井率(uptime factor)

`getUptimeFactor(uptimeDao, wellId, product)` = 该井、该产品当天的 `upTime / 24.0`;
列表为空、`wellId` 为空或查不到该井时,按 **1.0** 处理(即默认全天在产)。

### 取值的前置条件

- `oilRateWso`、`gasRateWso`、`gasLiftRateWso` 以及随后对 Potential 的初始化,**只在** `oilRateDao` 或 SRP 数据非空时才执行。
- `oilPotentialWso` / `gasPotentialWso` 先被设为对应的 Rate,再叠加 `oil_gain` / `gas_gain`。若上面的条件不成立,它们从 `0.0` 起叠加。
- 单位换算:字段上的 `@UnitField(parameterCode=…)` 配合 `UnitAwareResponseUtils.buildNormalResponse`,**推测**用于按用户单位偏好换算输出,未验证。

## 4. 变化率 `diffRatio`

```
diffRatio = (当天值 − 前一天值) / 当天值 × 100
```

- **分母是当天值**,不是前一天值(DTO 的 Schema 描述也写作 `(current-yesterday)/current * 100`)。
- 当天值为 `null` 或 `0`,或前一天值为 `null` → 结果 `null`。
- 经 `DoubleFormatter.format` 格式化;`-0.0` 归一为 `0.0`。
- JSON 输出格式 `0.00`,单位参数 `RATIO`。

| 有变化率的字段 | 没有变化率的字段 |
|---|---|
| `oilRateWso`、`oilPotentialWso`、`oilPotentialNso`、`gasRateWso`、`gasPotentialWso`、`gasPotentialNso`、`gasLiftRateWso`、`gasLiftOptimizedWso`、`gasLiftOptimizedNso`、`oilRateAlloc`、`gasRateAlloc` | `oilRateWt`、`gasRateWt`、`gasLiftRateWt`、`shutInWellPotential`、`gasShutInWellPotential`(相关代码在 DTO 中被注释掉) |

## 5. 代码阅读中发现的问题(待业务确认)

以下是读代码时的观察,未确认是否为有意设计。

| # | 现象 | 影响 |
|---|---|---|
| 1 | `oilPotentialNso`、`gasPotentialNso`、`gasLiftOptimizedWso`、`gasLiftOptimizedNso` 在本接口里**从不赋值**,恒为初始值 `0.0` | 返回固定的 0;它们的 `diffRatio` 恒为 `null`(当天值为 0) |
| 2 | `oilRateNso`、`gasRateNso`、`gasLiftRateNso` 及其 `*DiffRatio` **从不赋值** | 序列化后为 `null` / 缺省 |
| 3 | 油、气对 SRP 井口径不同:`oilRateWso` 把 SRP 井单独用 SRP 数据;`gasRateWso` 却遍历全部流动井 | SRP 井的气量来自 mapper 而不是 SRP 数据,是否合理需确认 |
| 4 | `gasLiftRateWso` 不乘开井率,油、气都乘 | 三个 Rate 口径不统一 |
| 5 | 前一天汇总失败(返回 `null`)时,不报错也不提示,只是没有 `diffRatio` | 调用方无法区分"无变化率"和"前一天取数失败" |
| 6 | 开井率查不到时默认 `1.0` | 缺失开井数据的井会按全天在产计入,可能高估 |

## 6. 后续可补充

- [ ] mapper SQL:`getOilRateWso`、`getOpportunityOilPotential` 读取的表和过滤条件。
- [ ] `UnitAwareResponseUtils` 的实际换算规则。
- [ ] 核对前端到底用 GET 还是 POST 调用该接口(见第 1 节)。
- [ ] 与业务确认第 5 节各项是否有意。
