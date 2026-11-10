---
name: docs-update
description: '根据现有代码或配置改动更新 docs 文档。适用于功能变更后同步 implementation、architecture、runbooks、knowledge 等文档内容。'
argument-hint: '本次改动了什么？需要更新 docs 的哪个区域？'
user-invocable: true
---

# Docs Update

基于现有实现改动，产出准确、可验证的文档更新，确保文档与代码行为一致。

## When to Use

- 已有代码、配置或脚本改动，需要同步更新 docs。
- 功能行为有变化，需要刷新实现说明。
- runbook 或 architecture/knowledge 文档因最近提交而过期。

## Inputs

- 变更范围（工作区改动、暂存区差异或最近提交）。
- 目标文档区域（docs/architecture、docs/implementation、docs/knowledge、docs/runbooks、docs/requirements、docs/decisions）。
- 可选约束（读者对象、细节粒度、格式要求）。

## Procedure

1. 识别改动范围。
   - 提取受影响模块、行为变化、接口、配置项和运维影响。
2. 建立文档映射。
   - 在 docs/ 下定位最匹配的现有文档。
   - 若没有合适文件，允许在 docs/implementation/ 新建实现说明。
3. 编写文档更新。
   - 写清楚改了什么、为什么改。
   - 说明实现方式与关键边界条件。
   - 补充影响范围、兼容性和验证步骤。
4. 做一致性校验。
   - 核对路径、命令、配置名、术语是否与仓库一致。
   - 未确认信息使用 TODO 或 Open Question 标注，禁止臆测。
5. 输出交付摘要。
   - 列出更新文件。
   - 每个文件给出 3-5 条核心变更点。
   - 列出待确认事项。

## Decision Points

- 若无行为或接口变化，只做最小且聚焦的文档调整。
- 若改动跨多个模块，按文档域拆分更新，避免单篇混杂。
- 若信息不完整，优先显式 TODO，而不是猜测性描述。

## Quality Checks

- 文档能清晰回答：改了什么、为什么改、影响是什么、如何验证。
- 引用的路径、术语、命令、配置项可在仓库中定位。
- 仅修改本次变更相关内容。
- 不包含密钥、token、内部敏感信息。

## Output Format

- 更新文档文件列表。
- 每个文件 3-5 条关键更新点。
- 待确认问题或 TODO 列表。