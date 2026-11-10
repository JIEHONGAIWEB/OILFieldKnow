# WPO 引入 MCP(Model Context Protocol):需求分析与探索方向

**日期:** 2026-11-10
**状态:** Draft(分析阶段,基于仓库现有文档推导,待与团队对齐)

> Related: [REQ-20261110 AI Agent + Model Management / Scheduler](../feature-history/REQ-20261110-ai-agent-model-management-scheduler.md)、
> [领域知识:模型驱动优化 vs 实时闭环控制](../domain-knowledge/ai-agent-model-driven-optimization.md)、
> [趋势探索](2026-11-10-ai-agent-trend-exploration-analysis.md)、
> [WSO API 清单](../api/rest/wso-api-list.md)。

> 说明:仓库中此前**没有** MCP 相关的规划或实现记录(检索无结果)。以下为基于现有 API/领域文档的分析与建议,不代表团队已有决定。

## 1. 背景与问题

REQ-20261110 希望让 AI Agent 用自然语言驱动 Model Management / Scheduler。Agent 要做事,必须有一种**标准、受控**的方式调用 WPO 的能力和数据。MCP 是把"工具(Tools)、资源(Resources)、提示(Prompts)"以统一协议暴露给 AI 客户端的方式,可作为 Agent 与 WPO 之间的接入层。

## 2. 目标

用 MCP 把 WPO 现有能力封装成 Agent 可调用的工具,做到:
- **复用现有 API**,不另建业务逻辑(与 REQ 的设计考量一致);
- **以当前用户权限调用**,可审计;
- **写操作需用户确认**(Human-in-the-loop)。

## 3. 需求分析

### 3.1 候选 MCP 能力(按风险分级)

| 类别 | 候选工具 | 依据(现有接口/文档) | 风险 |
| --- | --- | --- | --- |
| 只读-查询 | 查询 WSO 概览/KPI、Oil Rate 对比、Map、井状态 | [wso-api-list.md](../api/rest/wso-api-list.md) Overview 11 条 | 低 |
| 只读-分析 | 取 IPR / Pump / Gas Lift / Inflow 性能、Gradient、分析参数 | wso-api-list.md Analyze Chart 10 条 | 低 |
| 只读-模型 | 查询井模型库(按井/类型) | [well-model-management.md](../domain-knowledge/well-model-management.md) | 低 |
| 写-模型 | 上传模型文件 | REQ 场景 1 | 中(覆盖已有模型) |
| 写-调度 | 创建/修改/暂停 Scheduler Task | REQ 场景 2 | 中高 |
| 现场控制 | 下发设定值到设备 | 不在范围 | 高(明确排除) |

### 3.2 非功能需求
- **鉴权**:MCP Server 透传用户身份,按用户数据权限过滤(如井、资产范围)。
- **审计**:每次工具调用记录用户、参数、结果、时间。
- **确认机制**:写类工具返回"草稿",用户确认后才执行。
- **限流与超时**:避免 Agent 批量/循环调用拖垮后端。
- **契约稳定**:工具描述(名称、参数、返回)要清晰,字段口径与前端一致。

### 3.3 约束与风险
- 现有 API 文档大量"待补充"(Overview #4/5/6/8–11 的用途与契约缺失),**契约不全会直接限制可暴露的工具数量**。
- 微服务路由前缀(`api/router/wpo/wpoService/msp/v1/`)与 `wpoCommonService` 混用,需统一网关或在 MCP 层适配。
- 数据口径复杂(分摊算法、异常规则等,见 [wso-detail-table-exception-rulebook.md](../frontend/ui-patterns/wso-detail-table-exception-rulebook.md)),Agent 解读结果时可能误导,需附带口径说明。
- 提示注入:从用户上传文件/井名称等输入进入 Agent 上下文,需防止被诱导执行写操作。

## 4. 可探索的方向

### 方向 A:只读 MCP Server(建议起步)
把 WSO Overview / Analyze Chart 查询接口封装为只读工具。价值:最快验证"自然语言问数据";风险最低,无需确认机制。
- 产出:5–10 个只读工具 + 工具描述 + 示例问答。

### 方向 B:Model Management 工具化
上传、列表、详情、校验。验证 REQ 场景 1(拖拽上传)的后端接入。需明确文件格式识别、覆盖策略。

### 方向 C:Scheduler 任务草稿 + 确认
工具分两步:`draft_task`(校验并生成配置)→ `confirm_task`(用户确认后创建)。对应 REQ 场景 2,核心是**未确认不创建**。

### 方向 D:Resources / Prompts
- Resources:把知识库文档(领域概念、API 清单、异常规则)作为只读资源提供给 Agent,减少"瞎猜"。
- Prompts:沉淀"工作点分析""异常井排查"等标准提示模板。

### 方向 E:面向开发的 MCP(内部效率)
让开发 Agent 通过 MCP 访问本知识库、API 清单、设计稿,提升协作效率。与业务 MCP 相互独立,风险更低。

### 方向 F:评估与可观测
为工具调用建立测试集(问题 → 期望工具调用 → 期望结果),监控成功率、误用率和耗时。

## 5. 方案对比(初步)

| 方案 | 做法 | 优点 | 缺点 |
| --- | --- | --- | --- |
| 1. 独立 MCP Server 封装现有 REST | 新服务调用现有 API | 不改业务后端,上线快 | 多一层运维;鉴权需透传 |
| 2. 后端服务内置 MCP 端点 | 在现有微服务暴露 | 复用鉴权,链路短 | 侵入业务代码,发布耦合 |
| 3. 仅 Function Calling,不用 MCP | Agent 内部直接定义工具 | 最简单 | 与具体 Agent 绑定,难复用 |

**初步倾向:** 方案 1 + 方向 A 起步。

## 6. 建议路线

1. **第 0 步(准备)**:补全 `wso-api-list.md` 中"待补充"接口的契约,确认可暴露范围。
2. **第 1 步**:方向 A 只读 PoC,验证问答质量与鉴权透传。
3. **第 2 步**:方向 B/C,引入写操作与确认机制。
4. **第 3 步**:方向 D/F,沉淀知识资源与评估体系。

## 7. 待向团队确认

1. 团队是否已有 MCP / Agent 相关规划或原型?
2. Agent 客户端是谁(内置 Chatbox / 外部 Copilot 类工具)?决定 MCP 的部署形态。
3. 用户身份与数据权限如何透传到 MCP?
4. 哪些接口允许 Agent 调用,哪些必须人工确认?
5. 部署环境(内网/云)对外部模型调用的合规约束?

## 8. 结论与下一步
- [ ] 与团队对齐第 7 节问题
- [ ] 补全 API 契约(第 0 步)
- [ ] 选定 PoC 范围并立项为 REQ,再写入 [requirements-index.md](../feature-history/requirements-index.md)
