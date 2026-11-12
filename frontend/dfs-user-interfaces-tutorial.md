# DFS User Interfaces 教程说明

**来源：** DECISION SPACE® DIGITAL FIELD SOLVER®(DFS)官方教程 *User Interfaces*
**链接：** https://dfs-ng20.tiger.dazlmkengdev02.ienergycloud.solutions/docs/Tutorial/user_interfaces/
**状态：** 摘要说明(基于页面内容整理)

## 概述

User Interfaces(用户界面)模块用于集成各应用的决策支持界面,并以**两级菜单**形式呈现,同时支持**权限控制**。

主要能力:

- **Module Federation 集成**(官方推荐):模块可无缝接入 DFS。
- **统一设置中心**:集中托管各应用的设置项。
- **帮助管理**:可配置帮助链接。

## 功能说明

### 1. 模块管理(Manage Modules)

- 仅 **master tenant** 用户可见,普通用户无需关注。
- 模块可以是:
  - **localhost 模块**:用于本地开发;
  - **已部署模块**:用于开发或生产环境。
- 添加流程:
  1. 选择 MFE Name,页面显示对应的 Remote Entry JavaScript;
  2. 填写 **Exposed Module**(在代码中定义);
  3. 指定唯一的 **Route Path**(DFS 中的访问路径);
  4. 如有子模块,填写以 `/` 开头的 **Secondary Route**(在模块代码中定义)。
- 模块可按订阅情况分配给不同租户的菜单。

### 2. 添加主菜单(Main Menu)

- 一级菜单可以是 **URL** 或 **Group**。
- 可上传图标或从已有图标库中选择。

### 3. 添加二级/三级菜单(Branches)

- 二级菜单可以是 **Module Federation** 模块或**通用 URL**。
- 默认使用 **View 权限** 控制访问;页面内如有细粒度控制,可额外添加权限。权限列表由 solution manager 的 Permission API 提供,在开发阶段预定义。
- 模块包含子模块时,Route Path 由文本框变为下拉列表。
- 通用 URL 可在二级 Group 下再建三级菜单。
- 刷新 DFS 后,所有菜单即可访问。

### 4. 固定到首页(Pin to Home Page)

- 菜单可配置描述、链接和图片,以卡片形式展示在首页。
- 点击卡片即可直接访问对应菜单。

### 5. 添加设置项(Settings)

- 可在 Admin Panel 的 Settings 菜单下添加设置链接或设置模块。
- 权限在 **Users and Roles** 中以同名条目添加/编辑。
- 设置模块应为**独立模块**,不带 secondary route,且模块之间不直接交换数据。

### 6. 添加帮助(Help)

- 可添加帮助链接,在页面右上角的问号图标中查看。
- 权限同样在 Users and Roles 中以同名条目维护。

### 7. 菜单排序与编辑

- 支持**拖拽排序**,可在各级之间移动、进入其他分支或一级菜单。
- 拖拽时可用背景色高亮可放置位置。
- 点击 **Edit** 可修改名称、URL 等信息;删除菜单会同时删除其下的分支。

**限制:**

- 二级、三级菜单不能提升为一级菜单。
- Module Federation 模块或内部页面不能作为三级菜单。

## 关键概念速查

| 概念 | 说明 |
| --- | --- |
| Module Federation | 微前端集成方式,官方推荐 |
| Remote Entry | 远程模块的入口 JavaScript |
| Exposed Module | 模块中对外暴露的组件 |
| Route Path / Secondary Route | 模块在 DFS 中的访问路径 / 模块内子路由(以 `/` 开头) |
| Permission | 页面级权限,来源于 solution manager 的 Permission API |
| Master tenant | 可管理模块并分配给各租户的超级租户 |

## 开发注意事项

- 本地开发使用 localhost 模块,正式环境使用已部署模块。
- 权限名称须在开发阶段预定义,并与 Users and Roles 中的配置保持一致。
- 设置模块保持独立,避免模块间直接耦合。
- 修改菜单后需刷新 DFS 才能生效。
