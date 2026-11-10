# frontend testing

前端技术测试规范，聚焦单元测试（Unit Test）可执行基线。

## 专项需求文档

- [min-max-range-unit-test-requirements.md](min-max-range-unit-test-requirements.md) — 最小值/最大值可为空场景的单元测试需求（仅最小值、仅最大值、双边界、双空默认态）。

## 目标

- 保证核心业务逻辑在重构与需求迭代中行为稳定。
- 尽早发现边界值、空值、单位换算、条件分支回归问题。
- 为代码评审与提测提供可验证依据。

## 适用范围

- 组件中的纯业务函数与转换函数（transformer / mapper）。
- service 的业务分支逻辑（不依赖真实后端）。
- state 层 reducer / selector / effect 的关键分支。
- 配置驱动规则（如阈值、规则表、映射表）解析逻辑。

## 不建议作为单元测试主体

- 第三方库本身行为（ECharts/PrimeNG 内部实现）。
- 需要完整页面联动才能验证的流程（应放集成或 E2E）。

## 建议命令

- 全量单测：`npm run test`
- Angular CLI：`ng test --watch=false --browsers=ChromeHeadless`
- 指定项目：`ng test <project-name> --watch=false --browsers=ChromeHeadless`

说明：以仓库实际 scripts 与 workspace project 名为准。

## 用例设计基线

每个核心规则或函数，至少包含以下用例：

- 正常路径：命中主流程。
- 边界值：等于阈值、临界点前后。
- 异常路径：`null`/`undefined`/非数值/空数组。
- 兜底路径：配置缺失、字段缺失、转换失败。

## 断言粒度建议

- 优先断言“业务结果”，避免过度依赖内部实现细节。
- 单个测试只验证一个核心行为，失败定位要清晰。
- 对浮点计算使用容差断言（避免精度噪声）。

## 文件组织建议

- 被测文件：`xxx.ts`
- 对应测试：`xxx.spec.ts`
- 与被测文件同目录，便于变更同步维护。

示例：

- `libs/wso/.../wso-detail-table-exception.util.ts`
- `libs/wso/.../wso-detail-table-exception.util.spec.ts`

## PR 合入前检查

- 新增/修改业务规则是否同步补充单测。
- 关键分支是否覆盖（正向、边界、反向）。
- 是否存在“只改配置不补测试”的情况。
- 单测是否可在 CI 头less模式稳定执行。

## 与文档联动

- 业务规则来自文档时（如规则书/字段映射），测试命名建议包含 Rule ID 或规则名称，保证可追溯。
- 规则变更应在同一变更集中同时更新：实现 + 单测 + 文档。
