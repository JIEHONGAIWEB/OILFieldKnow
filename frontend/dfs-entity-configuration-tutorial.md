# DFS Entity Configuration 教程说明

**来源：** DECISION SPACE® DIGITAL FIELD SOLVER®(DFS)官方教程 *Entity Configuration*
**链接：** https://dfs-ng20.tiger.dazlmkengdev02.ienergycloud.solutions/docs/Tutorial/entity_configuration/
**状态：** 摘要说明(基于页面内容整理)
**相关文档：** [Global Settings 教程说明](dfs-global-settings-tutorial.md)、[User Interfaces 教程说明](dfs-user-interfaces-tutorial.md)

## 概述

Entity Configuration(实体配置)用于由管理员**把实体(井, wells)分配给具体应用**。

- 该功能适用于 **on-premises(本地部署)** 环境，由 License 控制并发用户数和实体数。
- 所有应用中**已启用的实体总数**受 License 上限约束。

## 功能说明

### 1. 添加新实体(Add New Entities)

- 可将 **PDM** 中的井添加到应用。
- 已添加的井**不会再出现**在添加列表中。
- 列表支持**排序、搜索**，并可**按油田(field)过滤**。

### 2. 启用/禁用实体(Enable/Disable Entities)

- 已添加的井可以启用或禁用。
- 点击 **Enable/Disable Wells** 按钮后，会出现 **Save Changes** 按钮。

## 操作流程

1. 在 PDM 井列表中使用排序、搜索或 field 过滤找到目标井并添加；
2. 点击 **Enable/Disable Wells** 修改井的状态；
3. 点击 **Save Changes** 保存生效。

## 规则与限制

| 项目 | 说明 |
| --- | --- |
| License 上限 | 所有应用中已启用实体总数受 License 限制 |
| 适用环境 | License 控制仅适用于 on-premises |
| 去重 | 已添加的井不在添加列表中显示 |

## 与其他设置的关系

- 页面侧边栏将 *Global Settings* 与 *User Interfaces* 并列为独立页面，原文**未说明**三者的关联。
- 按整理者理解(推断)：[Global Filter](dfs-global-settings-tutorial.md) 决定应用的过滤层级(含 Well 层级)，而 Entity Configuration 决定哪些具体的井可被应用使用。

## 开发/管理注意事项

- 启用井数量受 License 限制，批量启用前先确认剩余额度。
- 修改启用状态后必须点击 **Save Changes**，否则不生效。
- 页面未说明哪些角色可执行这些操作，需以实际 Users and Roles 配置为准。
- 页面仅提到“实体(井)”，未描述其他实体类型(如 Facility)是否同样适用。
