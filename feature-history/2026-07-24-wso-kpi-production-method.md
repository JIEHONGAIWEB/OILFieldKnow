# WSO Overview KPI「按 Production Method 动态加载」增强（2026-07-24）

> 范围：`wpo-app/libs/wso/src/lib/`（`configs/wso-kpi-card.config.ts`、
> `services/wso-mock-data.service.ts`、`components/wso-overview/`）
> 相关：ADR-0002（data-driven chart layering）、
> `frontend/ui-patterns/wso-kpi-by-production-method.md`（案例分析）。

## 背景

`libs/wso` 已用配置驱动方式按 Production Method（SF Oil / ESP / SF Gas / GL）加载
不同 KPI，但存在四个缺口：① 生产方式选择器未接线（`productionMethod` 实际固定为
`OILSF`）；② GL 误用 GAS 模板、缺注气 KPI 与双 Summary；③ 数值按数组下标硬映射；
④ `mapSummaryToCards()` 恒用 `oilRate*` 字段，Gas 方法会错显示油值。本次针对
①②③④ 做增强（③④已解决，②补齐 GL，①接入选择器）。

## 变更内容

### 1. 注册表替代静态 Record（OCP）
- 移除 `WSO_KPI_CARD_CONFIG: Record<...>`，改为 `Map` 支撑的
  `registerKpiSet(key, summaries)`；四种方法各自注册。新增井型/汇总无需改中心分支。
- 新增 `WsoKpiSummary { id, label, templates }`——一个方法可含多个 Summary。
- 新增 `getWsoKpiSummaries(method)`、`getWsoKpiCardTemplates(method, summaryId?)`。

### 2. GL 独立注气模板 + 双 Summary
- 新增 `GAS_INJECTION_KPI_CARDS`：Injection Gas Rate / Injection Pressure /
  Injection Temperature / Gas Consumption / Gas Lift Efficiency。
- `OILGL` 注册为 `[Oil Production Summary, Gas Injection Summary]`（其余方法单 Summary）。

### 3. 数值按 id 键控（去下标耦合）
- `WsoKpiCardTemplate` 增 `valueKey`（对应 API 字段）。
- Mock 值改为 `MOCK_KPI_VALUES: Record<id, number>`；`getKpiCards(method, summaryId)`。
- `mapSummaryToCards()` 改为按 `template.valueKey` 从 summary 取值，天然区分油/气
  （利用既有 `gasRateWso/Wt/Alloc/Nso` 字段）。

### 4. 生产方式选择器 + 汇总切换
- 组件加 `p-select` 绑定 `productionMethod`，`onProductionMethodChange()` →
  `productionMethod.set()`；切换时重置 `activeSummaryId` 为主 Summary。
- 加 `p-selectButton` 汇总切换，仅当方法有 >1 Summary（GL）时显示
  （`showSummaryToggle()`）。
- `effect()` 现同时响应 `productionMethod` 与 `activeSummaryId`。
- 组件 `imports` 增 `FormsModule`、`SelectModule`、`SelectButtonModule`。

## 验证
- 语言服务器对 4 个改动文件均无编译错误；无遗留 `WSO_KPI_CARD_CONFIG` 引用。
- PrimeNG `p-select` / `p-selectButton` 的运行时渲染需本地 `nx serve wso` 验证。

## 仍开放
- ESP 设备健康 KPI（Motor Current / PIP / Pump Efficiency）尚未建模。
- Gas Injection KPI 目前为 mock（后端 `WsoProductionSummary` 暂无注气字段）。
