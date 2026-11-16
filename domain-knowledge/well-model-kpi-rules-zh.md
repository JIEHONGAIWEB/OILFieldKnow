# Well Model KPI(井模型 KPI)— 按举升类型的计算规则

WPO 工作流如何为每种井型评定 **Well Model KPI**(Excellent / Good / Average /
Poor / N/A)。该 KPI 衡量计算(模型)井况与实测井况的吻合程度。

> 相关文档:[well-model-management.md](well-model-management.md)(展示该 KPI 的看板)、
> [production/oil-rate-kpis.md](production/oil-rate-kpis.md)。英文版:
> [well-model-kpi-rules.md](well-model-kpi-rules.md)。

## 通用:液量/气量偏差分级

自然流井直接使用;ESP 和气举井则作为**回退方案**使用。

| 偏差(计算值 vs. 试井值) | Model KPI |
| --- | --- |
| ≤ 10% | Excellent(优) |
| > 10% 且 ≤ 15% | Good(良) |
| > 15% 且 ≤ 20% | Average(中) |
| > 20% | Poor(差) |

## 按井型

### 自然流油井(Natural Flow Oil Producer)
比较**计算液量**与**试井液量**,按上表偏差分级。

### 自然流气井(Natural Flow Gas Producer)
同样的偏差分级,比较**计算气量**与**试井气量**。

### ESP(电潜泵井)
当有实时**入口压力(Pi)**和**出口压力(Pd)**测量值时,比较 Pi、Pd 的计算值与实测值。
偏差按实时测量数据的波动程度来评估,以**标准差(SD)**表示——SD 越小,说明模型与实测越吻合。

**Pd 与 Pi 两者中较差的等级决定 Model KPI。**

每个压力先分档:≤ 1 SD → 1 级,1–2 SD → 2 级,2–3 SD → 3 级,> 3 SD → 4 级。
结果矩阵(表 4,ESP 模型质量 KPI 范围):

| Pd 偏差 \ Pi 偏差 | ≤ 1 SD | 1–2 SD | 2–3 SD | > 3 SD |
| --- | --- | --- | --- | --- |
| **≤ 1 SD** | Excellent | Good | Average | Poor |
| **1–2 SD** | Good | Good | Average | Poor |
| **2–3 SD** | Average | Average | Average | Poor |
| **> 3 SD** | Poor | Poor | Poor | Poor |

(区间边界:"1–2 SD"指 > 1 且 ≤ 2 SD,依此类推。)

**回退规则**
1. 没有有效的 Pi/Pd 对比,但存在有效的液量对比 → 使用液量偏差分级。
2. 没有新的实时测量数据 → 保留上一次计算出的 Well Model KPI。

### 气举井(Gas Lift)
当有有效的 **GLIP**(气举注入压力)测量值时,将计算 GLIP 与**前 24 小时评估窗口**内实时 GLIP
数据的波动(SD)进行比较。

| GLIP 偏差 | Model KPI |
| --- | --- |
| ≤ 1 SD | Excellent |
| > 1 SD 且 ≤ 2 SD | Good |
| > 2 SD 且 ≤ 3 SD | Average |
| > 3 SD | Poor |

**最小 SD 规则**:若实时 GLIP 数据的 SD **小于平均 GLIP 的 1%**,则改用**平均 GLIP 的 5%**
作为默认 SD(避免信号近乎平直的井被过度惩罚)。

**回退规则**:没有有效的 GLIP 对比,但存在有效的液量对比 → 使用液量偏差分级。

## 最终回退(所有井型)

若无法计算当前 KPI,有上一次 Well Model KPI 则**保留之**;否则显示 **N/A**。

## 决策流程(ESP / 气举)

```
实时 Pi/Pd(ESP)或 GLIP(气举)有效?
   ├─ 是 → 基于 SD 分级
   └─ 否 → 有有效的液量对比?
              ├─ 是 → 液量偏差分级
              └─ 否 → 有上一次 KPI? → 保留 : N/A
```

## 与看板通用表的说明

[well-model-management.md](well-model-management.md) 中列出了一张通用误差表
(< 5% / 5–10% / 10–20% / > 20%)。本页规则是按举升类型定义的工作流口径;两者不一致时,以本页为更详细的依据。
