# AI Agent 自然语言驱动 Model Management / Model Scheduler

**日期:** 2026-11-10
**状态:** Draft(想法探索阶段,待与团队对齐)
**负责人:**

> Related: [AI Agent + Model Management + Scheduler 知识说明](../domain-knowledge/ai-agent-model-driven-optimization.md)、
> [well-model-management.md](../domain-knowledge/well-model-management.md)、
> [requirements-index.md](requirements-index.md)、
> [趋势探索(analysis)](../analysis/2026-11-10-ai-agent-trend-exploration-analysis.md)。

## 背景

目前 Model Management 与 Model Scheduler 需要用户在多个页面间切换、填写较复杂的表单:上传模型文件、创建 Task、选择类型/时间/Model/Well 等。操作路径长,对新用户不友好。

希望引入 AI Agent + 自然语言交互,让用户用业务语言描述需求,由 AI 完成参数提取、校验与配置生成,用户只做确认。

## 目标

用户不再手动操作多个页面和复杂表单,而是通过对话描述业务需求,由 AI 协助完成整个工作流:**上传模型 → 创建任务 → 结果反馈**。

## 场景

### 场景 1:Model Management — 拖拽上传
1. 用户把 Model 文件(如 Prosper 模型)拖拽到 Chatbox。
2. 系统自动识别文件类型并上传。
3. 对话框反馈:**模型信息**(名称、类型、关联井等可解析信息)和**上传结果**(成功/失败及原因)。

### 场景 2:Model Scheduler — 自然语言创建 Task
用户用自然语言说明:
- 想创建什么**类型的 Task**;
- **什么时候执行**(一次性/周期);
- 使用哪个 **Model**;
- 关联哪口 **Well**。

AI 需要:
1. 理解需求并**提取参数**;
2. **检查必要信息**,缺失时追问;
3. **生成任务配置**供用户确认。

用户确认后,任务创建与结果反馈由系统自动完成。

示例:"每天早上 6 点用 Well-0032 的 Prosper 模型跑一次工作点分析,结果发给我。"

```
自然语言 → 意图识别 → 参数抽取(Task 类型/时间/Model/Well)
        → 必填校验(缺失则追问) → 生成 Task 配置草稿
        → 用户确认 → 创建 Task → 执行 → 结果回传到对话
```

## 用户故事
- As a 生产工程师, I want to 拖拽模型文件到对话框完成上传, so that 不用进入多个页面填表。
- As a 生产工程师, I want to 用一句话描述任务, so that AI 帮我生成 Scheduler 配置,我只需确认。
- As a 生产工程师, I want to 在对话中收到任务执行结果, so that 无需再去其他页面查看。

## 验收标准(初稿)
- [ ] Chatbox 支持文件拖拽,并识别模型文件类型,拒绝不支持的格式。
- [ ] 上传后返回模型信息摘要与成功/失败状态。
- [ ] 能从自然语言中提取 Task 类型、执行时间、Model、Well。
- [ ] 必填信息缺失时主动追问,而不是猜测。
- [ ] 创建前展示任务配置供用户确认/修改;**未确认不创建**。
- [ ] 任务完成后在对话中反馈结果(成功/失败/关键输出)。

## 关键设计考量(待讨论)
- **Human-in-the-loop**:创建/修改任务、覆盖已有模型等写操作必须经用户确认。
- **歧义处理**:Model/Well 名称模糊匹配时给出候选让用户选择。
- **权限与审计**:Agent 以当前用户权限操作,记录操作日志。
- **复用现有 API**:Agent 通过工具调用现有 Model Management / Scheduler 接口,避免另建一套逻辑。
- **边界**:此方案解决"模型驱动的任务自动化",不等于对现场设备的实时闭环控制(见知识文档)。

## 待向团队确认的问题
1. 团队是否也有类似的产品想法?
2. 是否已在探索 AI Agent 与 Model Management / Model Scheduler 的集成?
3. 是否已有相关技术方案、Prototype 或正在推进的实现?
4. Chatbox 的承载位置(全局悬浮 / 各模块内嵌)与 Agent 后端选型。

> 当前知识库中**未检索到**团队已有相关规划、方案或原型的记录,以上问题需向团队确认后回填。

## 超出范围
- 对现场控制系统/设备的实时闭环控制。
- Model 本身的校准算法改动。
