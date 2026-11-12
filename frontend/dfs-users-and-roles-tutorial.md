# DFS Users and Roles 教程说明

**来源：** DECISION SPACE® DIGITAL FIELD SOLVER®(DFS)官方教程 *Users and Roles*
**链接：** https://dfs-ng20.tiger.dazlmkengdev02.ienergycloud.solutions/docs/Tutorial/users_and_roles/
**状态：** 摘要说明(基于页面内容整理)

## 概述

用户权限通过 **Users and Roles** 进行控制：

- 权限(Permission)**分配给角色(Role)**，而不是直接分配给用户。
- 拥有某角色的用户自动获得该角色的全部权限。
- 这些权限决定用户能够访问哪些**菜单**以及**内部功能**。

## 与 User Interfaces 的关系

在 [User Interfaces](dfs-user-interfaces-tutorial.md) 中添加的菜单、设置项和帮助链接，其访问权限都在 Users and Roles 中配置：

- 菜单：默认由 **View 权限** 控制访问。
- Settings / Help：在 Users and Roles 中以**同名条目**添加或编辑权限。
- 权限名称来源于 solution manager 的 Permission API，在开发阶段预定义。

## 操作流程

### 1. 创建角色并配置权限

1. 在 Solutions 菜单中添加自定义可视化(Visualization)后，即可为角色设置对应权限。
2. 新建一个角色，例如 **Test Role**。
3. 点击 **Edit** 按钮，启用权限选择，勾选该角色需要的权限。
   - 教程示例：仅勾选 Admin panel 下的三个菜单。

### 2. 将用户分配到角色

有两种方式：

| 方式 | 操作 |
| --- | --- |
| A. 从角色出发 | 在角色的 **Member List** 右上角点击 **+** 按钮添加成员 |
| B. 从用户出发 | 打开 **User** 标签页，为单个用户分配角色 |

### 3. 验证

- 使用 Test 用户登录后，只能看到 Admin panel 下的三个菜单。
- 用户的可访问范围始终与其所属角色的权限一致。

## 关键概念速查

| 概念 | 说明 |
| --- | --- |
| Role(角色) | 权限的集合，是授权的基本单位 |
| Permission(权限) | 控制菜单/页面/内部功能的访问 |
| Member List | 角色下的成员列表，可在此添加用户 |
| User 标签页 | 按用户维度查看并分配角色 |
| View 权限 | 菜单默认的访问控制权限 |

## 开发与使用注意事项

- 新增自定义可视化或菜单后，需到 Users and Roles 中为相应角色勾选权限，否则用户看不到。
- 权限名称须与 User Interfaces 中的定义保持一致。
- 先建角色、配权限，再分配用户，最后用测试账号登录验证。
- 官方页面未给出 user / role / group / tenant 的正式定义，也未列出限制条件，本文不做额外推断。
