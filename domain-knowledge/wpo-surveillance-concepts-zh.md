# WPO 领域知识 — 监控与性能

> 英文原文：[wpo-surveillance-concepts.md](wpo-surveillance-concepts.md)

WPO 应用的业务背景知识。

## 产品家族

- **WPO — Well Performance Optimization（油井性能优化）**：优化油井的产量表现。
- **WPE — Well Performance Evaluation（油井性能评估）**：评估每口井相对其模型的表现，并反映模型质量（Good / Moderate / Bad / 无模型）。
- **WSO — Well Surveillance Optimization（油井监控优化）**：优化监控工作流程。
- **Well Surveillance（油井监控，核心）**：持续监测油井及设备的健康状态。

## 关键分析

### Run Life Analysis（RLA，运行寿命分析）
研究井下设备（例如 ESP — Electric Submersible Pump，电潜泵）在失效前的运行时长。KPI 包括 **AERL**（Average Estimated Run Life，平均估算运行寿命）、**MEANTIME**（平均故障间隔时间）、失效次数以及置信区间。接口前缀为 `/well-equipment-results`，服务名为 `wellsurv-app-runlifeanalysis`。

### Survival Analysis（生存分析）
对设备进行统计学失效建模：
- **生存曲线（Survival curve）**：设备在时间 *t* 之后仍存活的概率。
- **风险曲线（Hazard curve）**：时间 *t* 时的瞬时失效率。
- **Weibull（威布尔）** 变体（`weibullSurvival`、`wellbullHazard`）使用威布尔分布拟合失效数据。

接口为 `/survival-hazards`。

### Well Test Management（井测试管理）
**井测试（Well Test）** 用于测量油井在 **井测试周期（Well Test Period）** 内的各项流量。用于验证和校准井模型，涉及 WTV（Well Test Validation，井测试验证）与 WMC（Well Model Calibration，井模型校准）。业务对象为 `WELL_TEST`、`WELL_TEST_PERIOD`。

### Model Quality（模型质量）
每口井的生产模型被评为 `Good`（良好）/ `Moderate`（一般）/ `Bad`（差），或标记为 `Wells without Model`（无模型井）。在 WPE 概览页（`/wells/model-qualities`）中展示。

## PDM 与业务对象

后端为 **PDM（Petroleum Data Management，石油数据管理）**。领域数据以 **业务对象（Business Objects, BO）** 的形式对外提供，通过通用的 `BOQuery` 进行查询（参见 `data-model/entities/pdm-boquery.md`）。业务对象的属性带有 `unitPolicy`（单位策略），用于控制单位换算。这一点非常关键：油田数据同时混用公制与英制单位，并且对时区敏感（产量速率按每日 / 每小时计）。
