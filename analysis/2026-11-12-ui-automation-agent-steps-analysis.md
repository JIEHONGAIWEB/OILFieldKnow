# UI 自动执行 + Agent Steps:Model Management / Scheduler 的实现方案与机会

**日期:** 2026-11-12
**状态:** Draft(想法阶段,基于仓库现有文档推导,待与团队对齐)
**关联需求:** [REQ-20261110 AI Agent + Model Management / Scheduler](../feature-history/REQ-20261110-ai-agent-model-management-scheduler.md)
**关联模块:** Model Management、Scheduler(Model Scheduler)

> Related: [WPO Agent-Native 机会分析](2026-11-10-wpo-agent-native-opportunity-analysis.md)(API 优先、动态界面引擎,本文不重复)、
> [WPO 引入 MCP](2026-11-10-wpo-mcp-requirement-analysis.md)、
> [DFS Workflow Scheduler 教程](../frontend/dfs-workflow-scheduler-tutorial.md)。
> 本文只回答一个问题:**让 Agent 直接操作真实界面("UI 自动执行"),并把过程以"Agent Steps"展示出来,有哪些做法、机会在哪。**

## 1. 要解决什么

REQ 的痛点:Model Management 和 Scheduler 需要在多个页面间切换、填写较长的表单(上传模型,创建 Task:类型/时间/Model/Well/规则/通知)。

"UI 自动执行"的含义:**用户说一句话,Agent 在真实界面上替用户点、填、选,用户看得见每一步,并在关键步骤确认。**

它与已有文档的区别:

| 路线 | Agent 怎么做事 | 用户看到什么 | 文档 |
| --- | --- | --- | --- |
| API 优先 | 直接调接口,结果在对话里展示 | 对话 + 确认卡 | [Agent-Native](2026-11-10-wpo-agent-native-opportunity-analysis.md) |
| **UI 自动执行(本文)** | 操作真实页面:打开表单、预填、点击 | 界面本身在动,每步可见 | 本文 |

两者不是二选一:UI 自动执行适合"需要用户看着、校对、保留原有界面"的场景。

## 2. Agent Steps 是什么

把 Agent 的一次任务拆成**可见、可控、可回放的步骤列表**,而不是一个黑盒的"处理中"。

```
用户:每天早上 6 点用 Well-0032 的 Prosper 模型跑一次工作点分析
 │
 ├─ Step 1  理解意图          提取:类型=工作点分析,周期=每天 06:00,Model=Prosper,Well=Well-0032   ✔
 ├─ Step 2  校验参数          Model/Well 是否存在、是否匹配;缺失则追问                              ✔
 ├─ Step 3  打开 Scheduler    导航到 Create New Task                                                ✔
 ├─ Step 4  选择工作流         选中对应的工作流                                                      ✔
 ├─ Step 5  填写基本信息       Task Name / Description                                               ✔
 ├─ Step 6  设置触发           Trigger Type = Daily,时间 06:00                                       ✔
 ├─ Step 7  设置规则/通知      已有实例处理方式、超时、通知对象                                       ✔
 ├─ Step 8  ⏸ 等待用户确认     展示最终配置,用户点"确认创建"(写操作,必须停)                          ⏸
 ├─ Step 9  提交               点击创建                                                              
 └─ Step 10 验证               任务出现在列表,右侧设置与预期一致;失败则回报原因                      
```

每个 Step 建议包含:

| 字段 | 说明 |
| --- | --- |
| 类型 | `navigate` / `fill` / `select` / `upload` / `click` / `wait` / `verify` / `confirm` |
| 目标 | 哪个页面、哪个控件(语义名,不是坐标) |
| 前置条件 | 进入前页面应处于的状态(例如表单已打开) |
| 后置验证 | 做完后应观察到什么(例如字段值已变化、列表出现新行) |
| 风险等级 | 只读 / 可撤销写 / 不可撤销写(后者必须用户确认) |
| 状态与耗时 | 待执行 / 执行中 / 成功 / 失败 / 跳过 |
| 证据 | 截图或页面状态快照,用于回放和审计 |

**价值:** 可见(用户信任)、可停(随时接管)、可重试(失败从某一步继续)、可回放(调试和审计)、可沉淀(成功的步骤序列可参数化为流程,见 Agent-Native 5.5)。

## 3. 实现方案(从稳到灵活)

### 方案 A:应用内语义动作(推荐主线)

前端暴露一组**语义化动作**,Agent 调用动作,而不是模拟鼠标。

```
Agent ──► 动作总线 ──► 页面组件
          openCreateTask({ workflow, name })
          setTrigger({ type: 'daily', time: '06:00' })
          selectModel({ id })  selectWell({ id })
          uploadModel({ file })
          submit()   ← 写动作,强制确认
```

- 与 Agent-Native 文档的 L1 动作总线是同一个思路:动作有名称、参数 Schema、权限等级。
- 表单通过**预填(prefill)**完成:Agent 填好,用户看着界面,点确认。
- 优点:稳定(不依赖 DOM 结构)、可校验、可审计、与手动操作走同一条代码路径。
- 缺点:需要前端改造,每个页面要登记动作;Module Federation 的各 remote 需各自接入(见 [ADR-0001](../architecture-decision/0001-module-federation-remote.md))。

#### 方案 A 能实现吗?怎么实现?

**能。** 这是前端里很常见的"命令模式 + 服务注册"做法,不依赖任何特殊技术,Angular(本项目栈,见 [coding-standards](../coding-standards/README.md))直接可做。工作量主要在"给每个页面登记动作",而不是引擎本身。

> 说明:仓库里只有文档,没有前端源码;下面的代码是示意,具体要按真实组件调整。

**核心结构:一个全局的动作注册服务**

```typescript
// agent-action.registry.ts(示意)
type Risk = 'read' | 'write-reversible' | 'write-irreversible';

interface AgentAction<P = unknown, R = unknown> {
  name: string;                    // 例如 'scheduler.setTrigger'
  description: string;             // 给模型看的说明
  paramsSchema: JsonSchema;        // 参数校验
  risk: Risk;                      // 写操作分级
  handler: (params: P) => Promise<ActionResult<R>>;
}

@Injectable({ providedIn: 'root' })
export class AgentActionRegistry {
  private actions = new Map<string, AgentAction>();
  register(a: AgentAction) { this.actions.set(a.name, a); return () => this.actions.delete(a.name); }
  list() { return [...this.actions.values()]; }          // → 自动生成给模型的工具清单
  async run(name: string, params: unknown) {
    const a = this.actions.get(name);
    if (!a) return fail('ACTION_NOT_AVAILABLE');         // 页面没打开 → 告诉 Agent 先导航
    if (!validate(a.paramsSchema, params)) return fail('INVALID_PARAMS');
    return a.handler(params as never);
  }
}
```

**页面组件进入时注册,离开时注销**(所以 Agent 只能看到当前页面可用的动作):

```typescript
// scheduler-task-wizard.component.ts(示意)
ngOnInit() {
  this.unregister = [
    this.registry.register({
      name: 'scheduler.setTrigger',
      description: '设置任务触发方式',
      risk: 'write-reversible',            // 只改表单,没提交,可撤销
      paramsSchema: TRIGGER_SCHEMA,
      handler: async (p) => {
        this.form.get('trigger')!.patchValue(p);   // 用户立刻在界面上看到变化
        return ok({ summary: `Daily ${p.time}` });
      },
    }),
    // ...其他动作
  ].flat();
}
ngOnDestroy() { this.unregister.forEach(fn => fn()); }
```

**关键点:Agent 不能直接提交,只能"请求提交"**

```typescript
this.registry.register({
  name: 'scheduler.requestSubmit',
  risk: 'write-irreversible',
  handler: async () => {
    const confirmed = await this.confirmCard.open(this.form.value); // 用户点击才返回 true
    if (!confirmed) return fail('USER_CANCELLED');
    return this.service.createTask(this.form.value);                // 真正的提交只发生在用户点击之后
  },
});
```

即使模型被诱导,它能做的最坏情况也是"弹出一个确认卡",真正的写入必须由用户点击触发。

**怎么让 Agent 知道有哪些动作:** `registry.list()` 自动转成工具定义(名称 + 描述 + 参数 Schema),所以新增一个动作不需要改 Agent 侧代码。

**Module Federation(见 [ADR-0001](../architecture-decision/0001-module-federation-remote.md)):** 注册服务放在 host 或共享库里,配置为 singleton shared;各 remote(Model Management、Scheduler)用同一个实例注册自己的动作。

#### 丰富的例子

**例 1:Scheduler 创建每日任务(完整的动作序列)**

用户:"每天早上 6 点用 Well-0032 的 Prosper 模型跑一次工作点分析,结果发给我。"

| # | Agent 调用 | 参数 | 界面上用户看到 | 返回 |
| --- | --- | --- | --- | --- |
| 1 | `nav.goto` | `{ route: "scheduler/new-task" }` | 跳转到创建任务页 | `ok` |
| 2 | `scheduler.selectWorkflow` | `{ query: "工作点分析" }` | 工作流下拉被选中 | `ok` 或 `AMBIGUOUS` + 候选列表 |
| 3 | `scheduler.setBasicInfo` | `{ name: "Well-0032 Daily Operating Point", description: "..." }` | 名称、描述被填入 | `ok` |
| 4 | `scheduler.setTrigger` | `{ type: "daily", everyDays: 1, time: "06:00" }` | Trigger Type 切到 Daily,时间 06:00 | `ok` |
| 5 | `scheduler.setRules` | `{ whenRunning: "skip", timeoutMin: 30 }` | 规则区域被填好(`skip` = 不启动新实例,默认值) | `ok` |
| 6 | `scheduler.setNotification` | `{ users: ["me"], on: ["failed", "completed"] }` | 通知对象被选中 | `ok` |
| 7 | `scheduler.setEntities` | `{ wells: ["Well-0032"] }` | 实体被选中;若版本低于 26.0.00 则返回 `NOT_SUPPORTED` 并跳过 | `ok` / `NOT_SUPPORTED` |
| 8 | `scheduler.requestSubmit` | — | **弹出确认卡**,展示完整配置 | 用户确认后 `ok { taskId }` |
| 9 | `scheduler.verifyCreated` | `{ taskId }` | 列表出现新任务,右侧设置展开 | `ok` + 与预期的差异(应为空) |

**例 2:歧义处理——名称不唯一时不猜**

```json
// Agent 调用
{ "action": "scheduler.selectModel", "params": { "query": "Prosper" } }

// 返回
{
  "ok": false,
  "code": "AMBIGUOUS",
  "message": "找到 3 个匹配的模型",
  "candidates": [
    { "id": "m-101", "name": "Prosper_Well-0032_v3", "updated": "2026-11-05" },
    { "id": "m-102", "name": "Prosper_Well-0032_v2", "updated": "2026-10-12" },
    { "id": "m-188", "name": "Prosper_Well-0040",    "updated": "2026-11-01" }
  ]
}
```

Agent 把候选列在对话里让用户选,而不是随便挑一个。选完再调用 `selectModel({ id: "m-101" })`。

**例 3:Model Management 拖拽上传**

| # | Agent 调用 | 说明 |
| --- | --- | --- |
| 1 | `model.inspectFile` (只读) | 读取文件名、扩展名、大小;识别类型,不支持的格式直接返回 `UNSUPPORTED_TYPE` |
| 2 | `model.checkDuplicate` (只读) | 查同名/同井是否已有模型 |
| 3 | `model.fillUploadForm` | 预填名称、类型、关联井等可解析的信息 |
| 4 | `model.requestUpload` | 若有重复,确认卡展示"新旧对比"(风险为不可撤销写);无重复也要确认 |
| 5 | `model.verifyUploaded` | 列表出现新模型、状态正常;失败时返回原因 |

**例 4:运维类动作(简单、高频)**

| 用户说 | 动作 | 风险 |
| --- | --- | --- |
| "暂停 Well-0032 那个日任务" | `scheduler.disableTask({ taskId })` | 可撤销写,可免确认或轻确认 |
| "现在跑一次" | `scheduler.runNow({ taskId })` | 写操作,确认 |
| "停掉所有排队中的实例" | `scheduler.stopInstances({ scope: "queued" })` | 不可撤销写,强制确认,展示影响数量 |
| "上次为什么失败?" | `scheduler.openHistory({ taskId, status: "failed" })` + `scheduler.readLog({ instanceId })` | 只读 |

**例 5:出错时返回结构化信息,Agent 才能自己恢复**

```json
{ "ok": false, "code": "ACTION_NOT_AVAILABLE", "hint": "先调用 nav.goto 打开创建任务页" }
{ "ok": false, "code": "INVALID_PARAMS",       "details": [{ "path": "time", "msg": "需为 HH:mm" }] }
{ "ok": false, "code": "NOT_SUPPORTED",        "hint": "当前版本不支持 Entity selection,可跳过" }
{ "ok": false, "code": "PERMISSION_DENIED" }
{ "ok": false, "code": "USER_CANCELLED" }
```

**例 6:动作清单(建议的命名空间)**

| 命名空间 | 动作示例 |
| --- | --- |
| `nav.*` | `goto`、`back`、`openTab` |
| `scheduler.*` | `selectWorkflow`、`setBasicInfo`、`setTrigger`、`setRules`、`setNotification`、`setEntities`、`requestSubmit`、`verifyCreated`、`runNow`、`disableTask`、`stopInstances`、`openHistory`、`readLog` |
| `model.*` | `inspectFile`、`checkDuplicate`、`fillUploadForm`、`requestUpload`、`verifyUploaded`、`search` |
| `agent.*` | `showSteps`、`askUser`(追问/选候选)、`highlight`(高亮用户应关注的控件) |

**实现成本估算(粗略):**

| 部分 | 工作量 |
| --- | --- |
| 注册服务 + 参数校验 + 工具清单导出 | 小(一次性) |
| Steps 面板(列表、状态、暂停/接管) | 小到中 |
| 确认卡 | 小 |
| 每个动作 | 小(多数是 `patchValue` + 校验 + 返回结果) |
| Scheduler 向导约 8–10 个动作,Model 上传约 5–6 个 | 合计中等 |
| 真正的难点 | 动作与现有表单校验、权限、版本差异(如 26.0.00+)保持一致 |

**需要先确认才能落地:** 页面是否用 Reactive Forms(`patchValue` 最顺)、表单是否被拆成多个组件、Chatbox 与页面是否在同一个 Angular 应用里(决定能否共享注册服务)。如果 Chatbox 是外部工具,则要加一层 postMessage 或 WebSocket 桥接。

### 方案 B:DOM / 无障碍树自动化(Playwright / 页面内 Agent)

Agent 读取页面的无障碍树或 DOM,按角色和名称找到控件并操作(类似 Playwright MCP、浏览器扩展、页面内脚本)。

- 优点:**几乎不用改前端**,对任意现有页面都能工作,最快做 PoC。
- 缺点:
  - 依赖控件名称和结构,UI 改版容易失效;
  - PrimeNG 等组件库的下拉、日期选择、虚拟滚动控件需要专门适配;
  - iframe / Shadow DOM / 远程模块可能读不到;
  - 需要在用户浏览器里运行或远程控制浏览器,权限和安全边界要想清楚。
- 改善办法:给关键控件加稳定的 `data-testid` 或 `aria-label`,这也顺带改善测试和无障碍。

### 方案 C:视觉 / Computer-use(截图 + 坐标)

Agent 看截图,决定点哪里、输入什么。

- 优点:**最通用**,不依赖页面实现,能操作任何界面(包括 canvas、第三方控件)。
- 缺点:慢、贵、易错(点偏、识别错);分辨率、主题、缩放都会影响;难做精确校验。
- 定位:**兜底方案**,只用于 A、B 都覆盖不到的地方。

### 方案 D:API 直连(无界面)

见 Agent-Native 文档。Scheduler 已有 **事件触发 API**(`{service address}/scheduler/tasks/{task-id}/instances`,见 [Scheduler 教程](../frontend/dfs-workflow-scheduler-tutorial.md)),运行已有任务可以不经过界面。

### 对比

| 维度 | A 语义动作 | B DOM/无障碍树 | C 视觉 | D API 直连 |
| --- | --- | --- | --- | --- |
| 稳定性 | 高 | 中 | 低 | 高 |
| 前端改造 | 需要 | 少(加 testid) | 无 | 无 |
| 速度/成本 | 快、便宜 | 中 | 慢、贵 | 最快 |
| 用户可见性 | 高 | 高 | 高 | 低(需另做展示) |
| 覆盖面 | 仅已登记页面 | 多数 Web 页面 | 任何界面 | 仅有 API 的能力 |
| 写操作可控性 | 高 | 中 | 低 | 高 |
| 适合 | 核心流程(创建 Task、上传) | PoC、长尾页面 | 兜底 | 批量、无需看界面 |

### 推荐:分层降级

```
语义动作(A) ──失败/未覆盖──► DOM 自动化(B) ──失败──► 视觉(C) ──失败──► 停下,交给用户
        └── 不需要看界面的步骤直接走 API(D)
```

每一步用哪一层,在 Step 里记录,便于统计哪一层最常失败、该补哪些动作。

## 4. 对 Model Management 的机会

> Model Management 的具体页面和字段在仓库里没有详细记录,下面是基于 REQ 描述的推断,需对照实际界面确认。

| 步骤 | UI 自动执行怎么做 | 机会 |
| --- | --- | --- |
| 拖拽模型文件到 Chatbox | `upload` 步骤:识别文件类型,调用上传动作(或填入上传控件) | 省去进入页面、选文件、填元数据 |
| 解析模型信息 | Agent 读取名称、类型、关联井等,在步骤里展示 | 上传前就能发现类型不对、关联井缺失 |
| 同名/覆盖 | 命中已有模型时停在确认步骤,展示前后对比 | 防止误覆盖(不可撤销写,必须确认) |
| 上传结果 | `verify`:列表出现新模型,状态正确 | 失败原因直接回报,不用用户自己找 |
| 批量上传 | 多文件逐个生成步骤,可部分成功、部分重试 | 比逐个点表单省得多 |

## 5. 对 Scheduler 的机会

Scheduler 的任务创建是**多步向导**,最适合 Agent Steps(字段来自 [Scheduler 教程](../frontend/dfs-workflow-scheduler-tutorial.md)):

| 向导部分 | 字段 | 自动化要点 |
| --- | --- | --- |
| 基本信息 | Task Name、Description | 按规则自动生成命名,用户可改 |
| 触发 | 一次性(Date/Time)或周期(Sub-daily / Daily / Weekly / Monthly)及其细项 | 自然语言转触发设置;"每天 6 点"→ Daily + 06:00;时间区间内按间隔运行也能表达 |
| Rules | 已有实例处理(默认不启动新实例 / 并行 / 停止现有)、超时、删除旧实例(26.0.00+) | 给出默认值并说明;改成"并行"这类有风险的选择要提示 |
| Notification | 用户或邮箱,状态触发 | 从"结果发给我"推出当前用户 |
| Entity selection(26.0.00+) | 实体,写入 `entity.json` | 从 Well 推出实体;版本不支持时跳过并说明 |

其他机会:

- **创建后验证**:任务出现在 Single Run 或周期列表,右侧设置与预期逐项比对,不一致就报告。
- **运行后跟进**:到 History 查看实例,失败时打开日志并总结原因(日志可下载)。
- **运维类操作**:Run / Stop / Disable / 停止指定实例,这些是简单、高频的动作,很适合语义动作。
- **事件触发**:对已有的一次性任务,Agent 直接走 API 触发,不必操作界面。
- **批量**:"给这 20 口井各建一个同样的任务"——UI 里是 20 遍向导,Agent 是 20 组步骤,可并行校验后统一确认。

## 6. 风险与对策

| 风险 | 对策 |
| --- | --- |
| Agent 点错或填错 | 每步有后置验证;写操作前展示最终配置;错了可从某一步重试 |
| 越权 / 误操作 | 以当前用户权限执行;写操作强制确认;动作分级 |
| 界面改版导致失效 | 优先语义动作;DOM 层用稳定标识;有回归测试 |
| 用户与 Agent 同时操作 | 执行时锁定界面或明确提示"Agent 正在操作",用户可一键接管 |
| 提示注入(文件名、井名里夹指令) | 工具层独立校验;写操作只接受结构化参数 |
| 慢与成本 | 能走 API/语义动作就不用视觉;步骤可缓存 |
| 审计 | 保存每次的步骤、参数、证据;Agent 的操作要有"由 Agent 执行"的标识 |
| 版本差异 | 如 Scheduler 的部分选项需 26.0.00+,步骤要先检测能力再决定是否出现 |

## 7. 建议路线

| 阶段 | 内容 | 退出标准 |
| --- | --- | --- |
| 0 梳理 | 画出 Model Management 上传、Scheduler 创建 Task 的真实页面流程和字段;决定语义动作清单 | 动作清单评审通过 |
| 1 Steps 展示 + 只读 | 做 Steps 面板;先支持"导航、查询、解释"这类只读步骤 | 步骤可见、可暂停、可回放 |
| 2 表单预填(方案 A) | Scheduler 创建 Task 向导预填 + 确认;Model 上传 | 未确认不提交;结果可验证 |
| 3 DOM 兜底(方案 B) | 用无障碍树覆盖未登记的页面;关键控件补 testid | 失败可自动降级或交还用户 |
| 4 流程沉淀 | 成功的步骤序列参数化,做泛化测试(见 Agent-Native 5.5) | 至少 1–2 个流程被他人复用 |
| 5 批量与主动 | 批量创建、失败任务巡检与提醒 | 误报可接受 |

**先做什么:** Scheduler 创建 Task 向导的预填 + 确认。它步骤多、字段清晰、有现成的验证点,收益最容易看见。

## 8. 待向团队确认

1. Model Management / Scheduler 的前端是否都在同一应用内?各自是独立的 remote 吗?(决定语义动作怎么接入)
2. 页面控件是否已有稳定的 `data-testid` / `aria-label`?
3. Chatbox 与页面是同一前端内的组件,还是外部工具?(决定能不能直接调用动作总线)
4. 用户是否需要"看着界面动",还是只看对话里的 Steps 就够?
5. 哪些写操作必须确认?覆盖已有模型、删除、并行运行等是否都算?
6. 步骤记录与截图的保存期限、审计要求?
7. 版本差异(例如 26.0.00 之前后)如何检测?
8. 是否已有团队在做类似的原型?(仓库里没有记录)

## 9. 结论

- **方向成立:** Scheduler 和 Model Management 都是"长表单 + 多步骤 + 有明确验证点"的典型场景,适合 UI 自动执行。
- **主线:** 应用内语义动作 + Agent Steps 面板;DOM 自动化做兜底和 PoC;视觉只做最后手段;不需要看界面的操作走 API。
- **Agent Steps 是核心体验:** 它把"AI 在做什么"变成可见、可停、可重试、可审计的步骤,是用户敢让 Agent 去点确认的前提。
- **下一步:**
  - [ ] 与团队对齐第 8 节问题
  - [ ] 画出 Scheduler 创建 Task 的真实页面流程和语义动作清单
  - [ ] 做一个 Steps 面板 + 预填的最小原型
