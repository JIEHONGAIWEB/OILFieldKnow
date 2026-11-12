# DFS Model Manager 教程说明

**来源：** DECISION SPACE® DIGITAL FIELD SOLVER®(DFS)官方教程 *Model Manager*
**链接：** https://dfs-ng20.tiger.dazlmkengdev02.ienergycloud.solutions/docs/Tutorial/model_manager/
**状态：** 摘要说明(基于页面内容整理)

## 概述

Model Manager(模型管理器)用于管理 DFS 中的**资产模型**:新增、更新版本、下载、删除和恢复。

模型是由建模技术或第三方工具生成的文件或文件夹,例如:

- **NETool**:井(wells)模型;
- **Nexus**:油藏(reservoirs)模型;
- 机器学习工作流产出的模型。

模型用于支持**模拟(simulation)、预测(prediction)和优化(optimization)**。

## 界面元素

| 元素 | 说明 |
| --- | --- |
| 左侧导航菜单 | Overview、Features、Asset Surveillance、Model Manager、Workflow Designer、Workflow Scheduler、User Interfaces、Users and Roles、Entity Configuration、Unit System、General Settings、Release Notes |
| Add 按钮 | 打开窗口,选择 Modeling Technology 并上传文件 |
| 实体匹配面板 | 将上传的文件/子文件夹匹配到实体;先自动匹配,未匹配项手动处理。14.2 及以上版本支持 PDM 之外的实体来源下拉框 |
| Effective date / Description | 在点击 **Apply** 前填写 |
| 版本面板 | 按生效日期排序列出所有版本,可多选后下载或删除 |
| Upload Model | 为已有模型添加新版本 |
| Download / Delete | 下载到本地 PC / 确认后删除所选模型 |
| Deleted history | 列出已删除模型,可恢复 |
| Settings | 建模技术配置表单(技术名称、文件数量、实体类型),表格显示各技术的模型数量 |
| Edit Model / View Model | 仅 NETool 模型,且云环境已部署并配置 NETool Essential 时出现 |

## 功能说明

### 1. 添加模型

1. 点击 **Add**,选择 Modeling Technology;
2. 上传 `.zip` 文件(NETool 也可上传单个 `.ntlcase` 文件);
3. 将文件匹配到实体(自动 + 手动);
4. 填写 Effective date 和 Description,点击 **Apply**。

规则:

- 名称会转换为 UWI 或实体名称;
- 名称中不允许的字符 `\ / : * ? " < > |` 会被替换为下划线;
- 技术下已有模型时,新上传会作为**新版本**;
- 未匹配成功的文件会**上传失败**。

### 2. 文件校验(26.2.00 及以上版本)

- 文件扩展名必须是该建模技术允许的类型,且与文件实际内容一致;
- `.zip` 压缩包内的文件同样会被检查;
- 以下类别会被拒绝:Windows 可执行文件、安装包、脚本、Unix 可执行文件、Java 载体、移动端安装包、系统文件、带宏的 Office 文档。

### 3. 上传新版本

模型变更后,以新的 Effective date 上传新版本,历史版本保留在版本面板中。

### 4. 下载 / 删除 / 恢复

- **下载**:选择模型后下载到本地 PC;
- **删除**:选择一个或多个模型,确认后删除;
- **恢复**:在 Deleted history 中选择已删除模型进行恢复。

### 5. 新增建模技术(Settings)

- 填写技术名称;
- 选择文件数量:**单文件**或**多文件(文件夹)**;
- 选择实体类型(来自 PDM reporting entity types):well、wellbore、well completion、pool、zone、formation、field、network、equipment、facility、org unit 等。选择 **others** 表示无需实体匹配。

### 6. 查看 / 编辑 NETool 模型

选择 NETool 模型后,点击 **Edit Model** 或 **View Model**,在 NETool 中打开。

### 7. Workflow Designer 中的模型服务

Python 接口 `dfs.utils.ModelService`:

| 方法 | 作用 |
| --- | --- |
| `get_all_models` | 按实体类型、技术或实体列表过滤模型 |
| `get_all_versions` | 列出某模型 ID 的所有版本 |
| `simple_upload` / `upload` | 上传单文件,或复合模型(如 GAP IAM 的 `.gar` 文件) |
| `download` | 下载模型并返回本地路径 |

配置需要 `MODEL_SERVICE_URL` 及 token 设置(详见 Developer Documentation)。从 DFS 外部调用服务时可使用多租户 token 选项。

## 权限

页面未描述基于角色的权限,访问控制请参见 **Users and Roles** 页面。

## 限制

- 默认建模技术(如 NETool、Nexus)**不能编辑或删除**;
- 自定义技术仅在**没有关联模型**时才能编辑或删除;
- 自定义技术已有模型时,只能修改其扩展名;
- 实体匹配失败或校验失败的文件会被拒绝;
- 被禁止的文件类型/扩展名无法上传;
- NETool 编辑需要云环境中部署并配置 NETool Essential;
- 页面未说明文件大小限制或配额。

## 关键概念速查

| 概念 | 说明 |
| --- | --- |
| Modeling Technology | 建模技术(NETool、Nexus 等),决定允许的文件类型与实体类型 |
| Entity matching | 将模型文件与 PDM 实体(井、油藏等)关联 |
| Effective date | 模型版本的生效日期,版本按此排序 |
| Version | 同一模型的历史版本 |
| ModelService | Workflow Designer 中访问模型的 Python 接口 |

## 开发注意事项

- 上传前确认文件名与实体名/UWI 对应,避免匹配失败;
- 避免文件名含特殊字符,否则会被改写为下划线;
- 26.2.00 起注意扩展名与内容一致,压缩包内也会校验;
- 自定义技术在上传模型前确认配置,有模型后仅能改扩展名。
