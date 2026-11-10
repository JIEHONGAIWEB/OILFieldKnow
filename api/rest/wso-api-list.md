# WSO API 清单(Overview + Analyze Chart)

> 汇总 WSO 相关接口的完整路径清单。详细请求/响应见
> [wso-v1-overview-api.md](wso-v1-overview-api.md),路由模式见
> [microservice-api.md](microservice-api.md)。
> 「用途」列仅在仓库已有文档能佐证时填写,其余为「待补充」。

## 1. Overview WSO

URL 模式:`api/router/wpo/wpoService/msp/v1/<endpoint>`(下表省略前缀 `api/router/wpo/wpoService/msp/v1/`)。

| # | Endpoint | 用途 | 已在详细文档中 |
| --- | --- | --- | --- |
| 1 | `wpo/wells/esp-production-summaries` | KPI 卡片(Oil/Gas Production Summary) | ✅ wso-v1-overview-api |
| 2 | `wpo/wells/esp/map` | Map view | ✅ |
| 3 | `wpo/wells/oil-rate-comparison` | Oil Rate Comparison 图 | ✅ |
| 4 | `wpo/wells/optimizations/aggregated-data-analyses` | 待补充 | ❌ |
| 5 | `wpo/wells/status/overview` | 待补充 | ❌ |
| 6 | `wpo/wells/performance/by-production-method` | 待补充(按生产方式) | ❌ |
| 7 | `wpo/well/reservoir-guideline-compliance` | Reservoir Guideline Compliance(POST) | ✅ |
| 8 | `wpo/wells/oil-gain-potential` | 待补充 | ❌ |
| 9 | `wpo/wells/esp-performances-system` | 待补充(ESP) | ❌ |
| 10 | `wpo/wells/pump-fillage/overview` | 待补充 | ❌ |
| 11 | `wpo/wells/gas-lift-performance-exception` | 待补充(Gas Lift) | ❌ |

> 注意:[wso-v1-overview-api.md](wso-v1-overview-api.md) 另记录了 Prod Loss / Production Losses
> 使用的 `wpoCommonService` 接口 `ws/operation-surveillance/wells/overview?type=losses`,
> 不在上面 11 条清单内。

## 2. Analyze Chart(Well Analysis)

| # | Endpoint | 用途 | 已在其他文档中 |
| --- | --- | --- | --- |
| 1 | `/wpo/wells/{wellId}/optimizations/performances/iprperformance` | IPR 性能 | 待补充 |
| 2 | `/wpo/wells/{wellId}/optimizations/performances/pump` | Pump 性能 | 待补充 |
| 3 | `/wpo/wells/{wellId}/optimizations/performances/gas-lift` | Gas Lift 性能 | 待补充 |
| 4 | `/wpo/wells/{wellId}/optimizations/performances/inflow` | Inflow 性能 | 待补充 |
| 5 | `/wpo/wells/{wellId}/optimizations/gradient-plots` | 梯度图 | [tooltip 字段映射](../../frontend/charts/wso-analysis-chart-tooltip-field-mapping.md) |
| 6 | `/wpo/wells/{wellId}/optimizations/analysis-parameters` | 分析参数(tooltip 补数) | [tooltip 字段映射](../../frontend/charts/wso-analysis-chart-tooltip-field-mapping.md) |
| 7 | `/wpo/srp/well/dynacard-acquisition-time` | Dynacard 采集时间(SRP) | 待补充 |
| 8 | `/wpo/srp/well/well-pump-dynacard/points` | Pump Dynacard 点数据(SRP) | 待补充 |
| 9 | `/wpo/srp/well/well-pump-dynacard/detail` | Pump Dynacard 详情(SRP) | 待补充 |
| 10 | `/wpo/wells/{wellId}/optimizations/data-analyses` | well-trend 交叉图 | [microservice-api.md](microservice-api.md) |

## 待办

- [ ] 补全 Overview #4/5/6/8–11 的用途、请求参数与响应契约。
- [ ] 补全 Analyze Chart 的 method、参数、响应与 micro-service 前缀(`wpoService`)。
- [ ] 对照 `wpo-app` 源码核对清单是否完整。
