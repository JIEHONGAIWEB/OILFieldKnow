# Shared 组件维护性评估（com-chart / com-map）

日期：2026-11-26  
评估范围：

1. `libs/shared/src/lib/components/com-chart`
2. `libs/shared/src/lib/components/com-map`

---

## 评分模型（总分 100）

- 模块边界清晰度（20）
- 依赖方向与耦合度（20）
- 一致性与命名规范（15）
- 类型安全与可演进性（15）
- 复杂度可控性（20）
- 错误处理与可观测性（10）

---

## 总览结论

| 模块 | 分数 | 结论 |
| --- | ---: | --- |
| `com-chart` | **81** | 基础能力封装完整、扩展性好，主要问题是 store 选择器弱类型。 |
| `com-map` | **75** | 工程化拆分较好（builder/handler/util），但 map SDK 适配层 `any/unknown` 较多。 |

---

## 1) com-chart（81/100）

### 优点

- 组件职责清晰：输入 `options` + 卡片动作 + 图表渲染，边界明确。
- 可维护设计较好：  
  - `parts` 拆分（actions/export/types）  
  - `ResizeObserver` + 生命周期清理，避免尺寸抖动导致首帧异常。  
- 考虑了 MFE 主题注册隔离（模块内注册标记）：
  - `com-chart.component.ts:38`
  - `com-chart.component.ts:41`
  - `com-chart.component.ts:47`

### 风险点

- `Store<any>` 与 `select('userPreferences' as any)` 弱类型：
  - `com-chart.component.ts:62`
  - `com-chart.component.ts:317`
- 主题来源依赖全局 store key 字符串，后续状态模型调整时脆弱。

### 子项评分

- 模块边界清晰度：17/20
- 依赖方向与耦合度：16/20
- 一致性与命名规范：13/15
- 类型安全与可演进性：11/15
- 复杂度可控性：16/20
- 错误处理与可观测性：8/10

---

## 2) com-map（75/100）

### 优点

- 分层结构良好：`builders / handlers / utils / types`，职责分离优于单体组件。
- 性能与稳定性处理较细：  
  - 输入签名去重（`buildRenderInputKey`）  
  - 异步渲染版本号防止过期写回  
  - map style 未就绪时延迟重试。  
  参考：
  - `com-map.component.ts:218`
  - `com-map.component.ts:266`
  - `com-map.component.ts:323`
- 交互链路可维护：`selection` 映射逻辑独立在 handler 中。

### 风险点

- SDK 适配层存在 `any`，边界类型不够强：
  - `utils/com-map-render.util.ts:136`
  - `utils/com-map-render.util.ts:137`
  - `utils/com-map-render.util.ts:239`
- 公共类型中存在 `unknown` 与宽索引签名，调用方需要反复判型：
  - `com-map.types.ts:6`
  - `com-map.types.ts:16`
  - `com-map.types.ts:25`

### 子项评分

- 模块边界清晰度：16/20
- 依赖方向与耦合度：14/20
- 一致性与命名规范：12/15
- 类型安全与可演进性：10/15
- 复杂度可控性：15/20
- 错误处理与可观测性：8/10

---

## 改进空间（优先级）

### P0

1. 为 `com-chart` 的 store 读取增加 typed selector（替代 `any`/字符串 key）。
2. 为 `com-map-render.util.ts` 建立最小 map/view 适配接口，逐步移除关键路径 `any`。

### P1

1. 收敛 `ComMapContext` 与 `ComMapWellInfo` 的 `unknown` 字段，建立稳定 DTO。
2. 为 `com-map` 的重试分支（style not ready）补监控计数，区分“瞬态未就绪”与“持续失败”。

### P2

1. 抽取共享的 map SDK adapter 层，降低组件对第三方 SDK 变更敏感度。
2. 在 `components/index.ts` 旁增加简短契约文档，明确 `com-chart/com-map` 输入输出约束与兼容策略。

