# DFS Unit System 教程说明

**来源：** DECISION SPACE® DIGITAL FIELD SOLVER®(DFS)官方教程 *Unit System*
**链接：** https://dfs-ng20.tiger.dazlmkengdev02.ienergycloud.solutions/docs/Tutorial/unit_system/
**状态：** 摘要说明(基于页面内容整理)

## 概述

Unit System(单位制)功能用于让页面显示的数值单位符合用户习惯。支持:

- **US Oil Field**(美国油田单位制);
- **SPE Preferred Metric**(SPE 推荐公制);
- **自定义单位制**:每个租户(tenant)仅一个。

用户可以添加并启用新的单位。

## 界面元素

| 元素 | 说明 |
| --- | --- |
| 页内目录 | 跳转到 Unit System Setting、Unit Convertion Table、Unit System Apply to Applications(页面原文拼写为 Convertion) |
| 单位制界面 | 显示可用单位制及各参数的单位 |
| Clone | 复制现有单位制(US Oil Field 或 SPE Preferred Metric)作为起点 |
| Apply 按钮 | 激活所选单位制,已应用的单位制以**绿点**标记 |
| 添加参数视图 | 向自定义单位制添加新参数 |
| Delete | 删除自定义单位制中新增的参数 |
| Unit Convertion Table | 列出 DSIS 单位,可启用或新增单位 |

## 功能说明

### 1. 设置单位制(Unit System Setting)

1. Clone 现有的 US Oil Field 或 SPE Preferred Metric;
2. 把各参数的单位改为用户偏好的单位;
3. 点击 **Apply** 生效。

### 2. 自定义单位

- 在自定义单位制中修改参数的单位;
- 面向项目中的客户界面,可**添加新参数**,不再需要的参数可**删除**。

### 3. 单位换算表(Unit Convertion Table)

- 启用 DSIS 单位集中生产工作常用的单位;
- 需要时启用更多单位;
- 也可以新增单位。

### 4. 在应用中使用(Unit System Apply to Applications)

按**参数代码(parameter code)**获取单位,再将数值从源单位换算为目标(已应用)单位。

## 开发者服务(前端 / 后端)

| 方法 | 作用 |
| --- | --- |
| `getCurrentParameters$()` | 以流的方式返回当前模板的系统参数 |
| `getCurrentParameterByCode()` | 读取系统参数,可读全部或按代码读取单个 |
| `getUnitsByType$()` | 按基础单位类型分组,以流的方式返回可用单位 |
| `convert()` | 在单位间换算,支持单个值、数组、批量实体(**关键方法**) |

## 权限

页面未说明谁可以 Apply、Clone 或编辑单位制,权限请参见 **Users and Roles**。

## 限制

- 每个租户只允许**一个**自定义单位制;
- 默认只启用 DSIS 单位集中的一部分;
- PDM 中的数据以 **US Oil Field** 单位存储,使用其他单位制时必须换算;
- 页面未说明校验规则、单位级限制,也未说明内置单位制能否直接编辑(从描述看应通过 Clone 使用)。

## 关键概念速查

| 概念 | 说明 |
| --- | --- |
| Unit system | 一组参数单位的命名集合(US Oil Field、SPE Preferred Metric 或自定义) |
| Parameter code | 应用中检索参数单位所用的标识 |
| Base unit type | 组织可用单位的分组依据 |
| Source / Target unit | 换算的"从"和"到"单位 |
| Template system parameters | 当前模板的参数 |
| DSIS | 单位来源集合 |
| PDM | 数据存储,使用 US Oil Field 单位 |
| Tenant | 自定义单位制所属的客户范围 |

## 开发注意事项

- 展示数值前先按参数代码取目标单位,再用 `convert()` 从源单位换算;
- 假定存储值为 US Oil Field 单位(PDM),显示和写回时都要考虑换算;
- 每个租户仅一个自定义单位制,修改会影响该租户全部用户;
- 需要的单位若未启用,先在 Unit Convertion Table 中启用或新增。
