---
name: address-requirement-completion-ratio
description: "分析一个地址的需求总量、完成量与完成比例，并输出可核对的结果与风险提示。"
argument-hint: "地址是什么？需求清单数据从哪里来（文件/API/文本）？"
user-invocable: true
---

# 地址需求完成比例分析

基于单个地址的需求数据，计算需求总量、已完成量、未完成量和完成比例，并输出可验证结论。

## When to Use

- 需要快速评估某个地址的需求执行情况。
- 需要在周报或验收前给出完成率。
- 需要识别该地址的交付风险（例如逾期需求占比高）。

## Inputs

- 地址标识（例如：深圳南山科技园A栋3层，或 addressId）。
- 需求明细（至少包含需求唯一标识与状态）。
- 可选字段：截止时间、优先级、负责人、更新时间。
- 状态映射规则（例如 Done/Closed 视为完成）。

## Status Mapping

默认完成状态集合：

- done
- closed
- completed
- 已完成
- 已关闭

默认未完成状态集合：

- todo
- pending
- open
- in_progress
- blocked
- 待处理
- 处理中
- 已阻塞

若用户提供了团队自定义状态映射，以用户映射为准。

## Procedure

1. 过滤地址范围。
- 仅保留 address 与输入地址匹配的数据。
- 无匹配数据时，输出 0 统计并标记 TODO：确认地址字段值是否一致。

2. 去重与清洗。
- 按需求唯一标识去重。
- 对空状态记为 unknown，并在结果中单独统计。

3. 计算核心指标。
- 需求总量 = total
- 已完成量 = completed
- 未完成量 = total - completed
- 完成比例 = completed / total
- 当 total = 0 时，完成比例定义为 0%

4. 输出结构化结果。
- 地址
- total
- completed
- remaining
- completionRatio
- unknownStatusCount
- 状态分布摘要

5. 给出风险与建议。
- remaining > 0 时给出推进建议。
- unknownStatusCount > 0 时提示先补齐状态字典。

## Formula

$$
completionRatio =
\begin{cases}
0, & total = 0 \\
\frac{completed}{total}, & total > 0
\end{cases}
$$

## Output Format

- 地址：<address>
- 需求总量：<total>
- 已完成：<completed>
- 未完成：<remaining>
- 完成比例：<xx.xx%>
- unknown 状态数：<unknownStatusCount>
- 状态分布：<status1=count1, status2=count2, ...>
- 结论：<一句话结论>
- TODO：<待确认项，若无则写“无”>

## Quality Checks

- 样本过滤仅包含目标地址。
- 分母为 0 时不报错。
- 百分比格式统一为两位小数。
- 所有统计可从原始需求明细反查。

## Example

输入：

- 地址：A园区-1号楼
- 需求：10 条，其中 done 6 条，in_progress 2 条，todo 1 条，unknown 1 条

输出：

- 地址：A园区-1号楼
- 需求总量：10
- 已完成：6
- 未完成：4
- 完成比例：60.00%
- unknown 状态数：1
- 状态分布：done=6, in_progress=2, todo=1, unknown=1
- 结论：该地址需求完成率为 60.00%，仍有 4 条未完成，建议优先处理 in_progress 与 unknown。
- TODO：确认 unknown 状态定义与归类规则。
