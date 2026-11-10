# 最小值/最大值范围校验 单元测试需求

## 1. 背景与目标

本需求用于统一范围输入控件在“最小值/最大值可为空”前提下的业务语义，并形成可执行的单元测试基线，避免前后端和测试口径不一致。

## 2. 总体规则

- 默认状态：最小值与最大值均不预填（为空）。
- 任一边界为空时，不应把空值当作 0 参与比较。
- 数值比较前，输入需通过数值合法性校验。

## 3. 业务语义（核心场景）

### 3.1 只填写最小值，最大值为空

期望行为：

- 所有有效数值必须大于或等于最小值。
- 语义可表示为：value >= min。

示例：

- min = 10, max = 空
- value = 9 -> 不通过
- value = 10 -> 通过
- value = 100 -> 通过

### 3.2 最小值为空，只填写最大值

期望行为：

- 所有有效数值必须小于或等于最大值。
- 语义可表示为：value <= max。

示例：

- min = 空, max = 50
- value = 49.9 -> 通过
- value = 50 -> 通过
- value = 50.1 -> 不通过

### 3.3 最小值和最大值都填写

期望行为：

- 所有有效数值必须落在区间内。
- 语义可表示为：min <= value <= max。

示例：

- min = 10, max = 20
- value = 9.9 -> 不通过
- value = 10 -> 通过
- value = 15 -> 通过
- value = 20 -> 通过
- value = 20.1 -> 不通过

### 3.4 最小值和最大值都为空（默认）

期望行为：

- 不施加范围限制。
- 若仅校验范围条件，则任意有效数值均通过。

### 3.5 数据集语义边界（新增）

约定：`dataMax` 表示当前待筛选数据集合中的最大值。

- 当输入最小值 > dataMax（且 max 为空或 >= min）时：
  - 范围条件本身合法，但不会命中任何数据（结果为空）。
- 当输入最大值 > dataMax（且 min 为空）时：
  - 上限约束对当前数据集不产生额外过滤效果（不因 max 过大而误过滤）。
- 当输入最小值 = 最大值时：
  - 退化为“精确值匹配”语义，仅允许 `value = min = max` 通过。

## 4. 异常与边界规则

- min > max：配置/输入非法，应直接返回校验失败并给出明确错误标识。
- 非数值输入：应判定为无效输入，不进入范围比较。
- 空字符串、null、undefined：按“未填写边界”处理，不应隐式转为 0。
- 浮点比较：建议统一精度策略（例如保留固定小数位后比较）。

## 5. 单元测试用例矩阵（最小集合）

| 场景 | min | max | value | 预期 |
| --- | --- | --- | --- | --- |
| 仅最小值-小于下限 | 10 | 空 | 9 | fail |
| 仅最小值-等于下限 | 10 | 空 | 10 | pass |
| 仅最小值-大于下限 | 10 | 空 | 11 | pass |
| 仅最大值-小于上限 | 空 | 50 | 49 | pass |
| 仅最大值-等于上限 | 空 | 50 | 50 | pass |
| 仅最大值-大于上限 | 空 | 50 | 51 | fail |
| 双边界-小于下限 | 10 | 20 | 9 | fail |
| 双边界-等于下限 | 10 | 20 | 10 | pass |
| 双边界-区间中值 | 10 | 20 | 15 | pass |
| 双边界-等于上限 | 10 | 20 | 20 | pass |
| 双边界-大于上限 | 10 | 20 | 21 | fail |
| 双空-默认态 | 空 | 空 | 999 | pass |
| 非法区间 | 20 | 10 | 15 | fail |
| 数据集边界-最小值大于数据最大值 | 101 | 空 | dataMax=100 时任意 value | fail（结果为空） |
| 数据集边界-最大值大于数据最大值 | 空 | 200 | dataMax=100 时 value=100 | pass |
| 双边界相等-命中精确值 | 10 | 10 | 10 | pass |
| 双边界相等-非精确值 | 10 | 10 | 9/11 | fail |

## 6. 建议测试结构

- 建议被测函数签名：validateRange(value, min, max)
- 建议断言输出：
  - valid: boolean
  - reason: optional（如 RANGE_MIN_EXCEEDED / RANGE_MAX_EXCEEDED / INVALID_RANGE）

示例测试分组：

- describe: only min provided
- describe: only max provided
- describe: both provided
- describe: both empty
- describe: invalid input and invalid range

## 7. 验收标准

- 上述最小用例矩阵全部通过。
- 关键边界（等于 min、等于 max、min > max）均有明确断言。
- 不允许出现“空边界被当作 0”导致的误判。
- 需求变更时，同步更新：实现 + 单测 + 本需求文档。

## 8. 可直接复用的 spec 用例骨架

以下模板可直接粘贴到 `*.spec.ts`，将 `validateRange` 替换为实际函数。

    // min-max-range.spec.ts
    // 请替换导入路径
    // import { validateRange } from './range-validator';

    describe('validateRange', () => {
      describe('only min provided', () => {
        it('fails when value < min', () => {
          const result = validateRange(9, 10, undefined);
          expect(result.valid).toBeFalse();
          expect(result.reason).toBe('RANGE_MIN_EXCEEDED');
        });

        it('passes when value = min', () => {
          const result = validateRange(10, 10, undefined);
          expect(result.valid).toBeTrue();
        });

        it('passes when value > min', () => {
          const result = validateRange(11, 10, undefined);
          expect(result.valid).toBeTrue();
        });
      });

      describe('only max provided', () => {
        it('passes when value < max', () => {
          const result = validateRange(49, undefined, 50);
          expect(result.valid).toBeTrue();
        });

        it('passes when value = max', () => {
          const result = validateRange(50, undefined, 50);
          expect(result.valid).toBeTrue();
        });

        it('fails when value > max', () => {
          const result = validateRange(51, undefined, 50);
          expect(result.valid).toBeFalse();
          expect(result.reason).toBe('RANGE_MAX_EXCEEDED');
        });
      });

      describe('both min and max provided', () => {
        it('fails when value < min', () => {
          const result = validateRange(9, 10, 20);
          expect(result.valid).toBeFalse();
        });

        it('passes when value = min', () => {
          const result = validateRange(10, 10, 20);
          expect(result.valid).toBeTrue();
        });

        it('passes when value is between min and max', () => {
          const result = validateRange(15, 10, 20);
          expect(result.valid).toBeTrue();
        });

        it('passes when value = max', () => {
          const result = validateRange(20, 10, 20);
          expect(result.valid).toBeTrue();
        });

        it('fails when value > max', () => {
          const result = validateRange(21, 10, 20);
          expect(result.valid).toBeFalse();
        });
      });

      describe('both empty (default)', () => {
        it('passes for any valid number', () => {
          const result = validateRange(999, undefined, undefined);
          expect(result.valid).toBeTrue();
        });
      });

      describe('invalid range', () => {
        it('fails when min > max', () => {
          const result = validateRange(15, 20, 10);
          expect(result.valid).toBeFalse();
          expect(result.reason).toBe('INVALID_RANGE');
        });
      });

      describe('dataset-boundary semantics', () => {
        it('returns no match when min is greater than dataset max', () => {
          const data = [10, 30, 60, 100];
          const filtered = data.filter((v) => validateRange(v, 101, undefined).valid);
          expect(filtered.length).toBe(0);
        });

        it('does not over-filter when max is greater than dataset max', () => {
          const data = [10, 30, 60, 100];
          const filtered = data.filter((v) => validateRange(v, undefined, 200).valid);
          expect(filtered).toEqual([10, 30, 60, 100]);
        });

        it('acts as exact match when min equals max', () => {
          const data = [9, 10, 11];
          const filtered = data.filter((v) => validateRange(v, 10, 10).valid);
          expect(filtered).toEqual([10]);
        });
      });

      describe('invalid numeric input', () => {
        it('fails when value is NaN', () => {
          const result = validateRange(Number.NaN, 10, 20);
          expect(result.valid).toBeFalse();
          expect(result.reason).toBe('INVALID_VALUE');
        });

        it('treats empty boundaries as undefined, not zero', () => {
          const result = validateRange(1, undefined, undefined);
          expect(result.valid).toBeTrue();
        });
      });
    });

说明：

- 若当前实现只返回 boolean，可先断言 true/false；后续建议补 reason 字段提升可诊断性。
- 若存在浮点精度风险，建议增加临界值用例（如 0.1 + 0.2 场景）并采用容差断言。
