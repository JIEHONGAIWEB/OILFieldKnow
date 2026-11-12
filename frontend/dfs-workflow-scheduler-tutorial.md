# DFS Workflow Scheduler 教程说明

**来源：** DECISION SPACE® DIGITAL FIELD SOLVER®(DFS)官方教程 *Workflow Scheduler*
**链接：** https://dfs-ng20.tiger.dazlmkengdev02.ienergycloud.solutions/docs/Tutorial/workflow_scheduler/
**状态：** 摘要说明(基于页面内容整理)

## 概述

Workflow Scheduler(工作流调度器)用于管理工作流**如何运行、何时运行**。已发布(Published)的工作流可以:

- **按需触发**(手动运行);
- **按计划触发**(一次性或周期性);
- **由事件触发**(通过 API)。

## 功能说明

### 1. 创建一次性任务(One-time Task)

1. 在工作流列表中基于某个工作流创建任务;或点击 **Create New Task** 后选择工作流。
2. 填写 **Task Name** 和 **Description**。
3. 填写 **Trigger Date** 和 **Time**。
4. 跳过 Rules 和 Notification 步骤，直接创建。
5. 任务出现在 **Single Run** 标签页，右侧面板显示其设置。
6. 切换到 **History** 查看运行实例。

### 2. 创建周期性任务(Recurrent Task)

1. 同上，基于工作流创建任务，填写 Task Name 和 Description。
2. **Trigger Type:** 可选 Sub-daily、Daily、Weekly、Monthly。
3. **触发设置(以 Daily 为例):**
   - 每隔 N 天在固定时间运行;或
   - 在某个时间段内按固定间隔运行，例如 16:00–17:00 每 10 分钟一次。
   - 可选择在时间段结束时停止所有运行中的任务，以释放 license。
4. **Rules — 已有实例运行时的处理方式:**
   1. 不启动新实例(默认)
   2. 并行启动新实例
   3. 停止现有实例
5. **Rules — 超时(Timeout):** 设置超时时间，运行超过预期时间的实例会被停止。
6. **Rules — 删除旧实例(26.0.00 及以上版本):**
   - 删除超过 # 天的旧实例;或
   - 实例数量超过 # 时删除旧实例。
7. **Notification:** 选择一个或多个用户，或输入一个或多个邮箱地址，在所选状态出现或时间间隔结束时接收通知。
8. **Entity selection(26.0.00 及以上版本):** 为任务选择实体(entity)。所选实体保存在运行实例目录下的 `entity.json` 中，工作流可读取使用。
9. 实例按计划运行，可查看历史和日志。

### 3. 查看历史(History)

- 运行中或运行后均可打开实例历史。
- 点击带下划线的状态可查看运行日志，日志可下载。
- 如需按状态筛选(例如所有失败的实例)，打开 **All History**。

### 4. 运行 / 停止任务

- 计划任务按设定时间自动运行，也可**手动运行**。
- 运行中的任务可以**停止**。

### 5. 停止实例

- 可停止所有排队中和运行中的实例，也可只停止选中的实例。

### 6. 禁用任务(Disable)

- 禁用后任务暂时不再触发，需要时可重新启用。

### 7. 事件触发(Event Trigger)

除时间计划外，任务也可通过 API 由事件触发。

- **Endpoint:** `{service address}/scheduler/tasks/{task-id}/instances`
- 如果工作流有输入参数(例如 UWI、test ID)，在请求体(request body)中传入，执行时会设置到工作流中。
- 事件触发**推荐使用一次性任务**。Task ID 可在 **General Information** 中找到。
- 触发后在 History 和日志中查看实例。
- **示例:** 在 "well test validation" 审批通过时，触发模型校准(model calibration)工作流。

## 关键概念速查

| 概念 | 说明 |
| --- | --- |
| Task | 基于已发布工作流创建的调度任务 |
| Instance | 任务每次运行产生的实例 |
| Single Run | 一次性任务所在的标签页 |
| Trigger Type | 周期类型: Sub-daily / Daily / Weekly / Monthly |
| Rules | 并发处理、超时、旧实例清理等运行规则 |
| Notification | 状态变化或时间间隔结束时通知用户/邮箱 |
| Entity selection | 选定实体并写入 `entity.json`(26.0.00+) |
| Event Trigger | 通过 API 触发任务实例 |

## 使用注意事项

- 只有**已发布**的工作流才能被调度。
- 默认在已有实例运行时**不启动新实例**，避免重复运行;需要并发时才选择并行。
- 周期任务建议设置超时，并在时间段结束时停止任务以释放 license。
- 删除旧实例与 Entity selection 需要 **26.0.00 及以上版本**。
- 事件触发优先使用一次性任务，并记录好 Task ID。
- 官方页面未给出实例状态的完整列表，也未列出限制条件，本文不做额外推断。
