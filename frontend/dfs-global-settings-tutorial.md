# DFS Global Settings 教程说明

**来源：** DECISION SPACE® DIGITAL FIELD SOLVER®(DFS)官方教程 *General Settings*
**链接：** https://dfs-ng20.tiger.dazlmkengdev02.ienergycloud.solutions/docs/Tutorial/global_settings/
**状态：** 摘要说明(基于页面内容整理)
**相关文档：** [DFS User Interfaces 教程说明](dfs-user-interfaces-tutorial.md)

## 概述

Global Settings 是基于 DFS 底座构建的**所有应用共享的全局设置**，包含三部分：

1. Global Filter(全局过滤器)
2. General Settings(通用设置)
3. Workflow Engine Integration(工作流引擎集成)

## 功能说明

### 1. Global Filter(全局过滤器)

- **作用范围：** 按**应用**配置，在**租户级别**生效，因此可针对不同客户定制。
- **配置步骤：**
  1. 从下拉框选择应用；
  2. 选择可用的实体层级(entity levels)；
  3. (可选)选择组织层级(org hierarchy)；
  4. 如 PDM 中已有数据，可预览已配置层级及其数据；
  5. 结果符合预期后点击 **Apply**。
- **实体规则：**
  - 添加 **Facility** 时必须选择设施类型(facility type)；
  - 添加 **Well** 时可选择 Well Type 和 Production Method；
  - 层级可调整顺序，但选了 **Well** 则它必须是**最后一级**；
  - 并非所有层级之间都有父子关系，无关系时会出现警告；
  - 显示名称(display name)可编辑。

### 2. General Settings(通用设置)

| 设置项 | 说明 |
| --- | --- |
| Date format | 日期格式，应用于各应用的 UI |
| Logo | 可上传一个 Logo，供需要在报告中展示 Logo 的应用使用 |
| Production Time | 设置 ETL 导入每日数据的时间 |

### 3. Workflow Engine Integration(工作流引擎集成)

- **权限：** 主要面向工作流设计者，**仅 master tenant 可用**。
- **包含内容：**
  - 工作流引擎链接；
  - 用于工作流调试的 tenant JSON；
  - 工作流可请求的服务列表。
- **添加服务：** 新服务对**所有工作流**立即可用，无需逐个工作流配置。
- **健康检查：** 如指定了 health check endpoint，访问 UI 时会检查其状态。

## 与 User Interfaces 的关系

- General Settings 中的**日期格式**会作用于各应用 UI。
- **Global Filter** 的配置决定各应用数据视图的过滤层级。
- 这些全局设置本身属于 Admin Panel 的 **Settings** 菜单；该菜单下的设置链接/设置模块，其添加方式与权限（在 Users and Roles 中以同名条目维护）见 [User Interfaces 教程](dfs-user-interfaces-tutorial.md) 第 5 节。
- 原页面仅提供指向 User Interfaces 的链接，未进一步说明二者关系，以上关联为整理时的推断。

## 关键概念速查

| 概念 | 说明 |
| --- | --- |
| Global Filter | 按应用、按租户配置的实体层级过滤 |
| Entity level | 过滤层级，如 Facility、Well；Well 必须最后 |
| Org hierarchy | 可选的组织层级 |
| PDM | 预览层级数据所依赖的数据源 |
| Production Time | ETL 每日数据导入时间 |
| Master tenant | 可使用 Workflow Engine Integration 的超级租户 |

## 开发注意事项

- Global Filter 预览依赖 PDM 中已有数据。
- 选择 Well 层级时务必放在最后，并为 Facility 指定类型。
- Workflow Engine Integration 只在 master tenant 可见，普通租户无需关注。
- 页面未描述除 master tenant 限制外的角色权限细节，需以实际 Users and Roles 配置为准。
