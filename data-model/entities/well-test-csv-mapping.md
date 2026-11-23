# Well Test CSV → DSPDM 表映射(WELL TEST 表组)

> 场景:一份单井测试 CSV(1 口井、10 个 `test_point`),需要写入 DSPDM。
> 结论:**不能放进一张表**,应落到 WELL TEST 表组的 4 张表。

```
WELL TEST → WELL TEST PERIOD → WELL TEST MEASUREMENT
                             → WELL TEST FLOW MEASUREMENT
```

## 1. 每张表放什么

| 表                                                            | 存放内容                                                           | 本 CSV 产生的行数            |
| ------------------------------------------------------------ | -------------------------------------------------------------- | ---------------------- |
| **WELL TEST**(`WELL_TEST`)                                   | 测试头:井、开始/结束时间、时长、类型、设备                                         | 1                      |
| **WELL TEST PERIOD**(`WELL_TEST_PERIOD`)                     | 测试作业的每个时段,`TEST_PERIOD` 为序号                                    | 10(每个 `test_point` 一行) |
| **WELL TEST MEASUREMENT**(`WELL_TEST_MEASUREMENT`)           | 压力、油嘴、GOR、含水,每个测量一行(`MEASUREMENT` + `MEASUREMENT_VALUE` + UOM) | 约 90(每点 9 行)           |
| **WELL TEST FLOW MEASUREMENT**(`WELL_TEST_FLOW_MEASUREMENT`) | 各产品产量(`PRODUCT` + `RATE` + `RATE_UOM`)                         | 40(每点 4 行)             |

未建议 `WELL TEST ALLOCATION FACTOR`:CSV 中没有分配数据。

## 2. 列映射

| CSV 列 | 目标 | 备注 |
|---|---|---|
| `well_id` | WELL TEST `ASSOCIATED_OBJECT_ID` + `R_REPORTING_ENTITY_KIND_ID`(井) | 必填。"WELL-001" 不是 DSPDM ID;现有井为 LMK-Well-0001…0030,ID 6415–6444 |
| `test_datetime`(首/末) | WELL TEST `START_DATE`(必填)、`END_DATE` | |
| `test_datetime`(每行) | WELL TEST PERIOD `PERIOD_START_DATE`;子表的 `START_DATE`/`END_DATE`(子表必填) | |
| `test_point` | `TEST_PERIOD`(整数,必填) | 直接对应 |
| `test_duration_hr` | WELL TEST `TEST_DURATION`(hrs) | period 上也有 |
| `lift_type`(ESP) | 无专用字段 | 可放 WELL TEST `REMARK` 或 `WELL_TEST_NAME` |
| `tubing_head_pressure_bar` | MEASUREMENT = **Tubing Pressure** | |
| `casing_head_pressure_bar` | MEASUREMENT = **Casing Pressure** | |
| `flowing_bottomhole_pressure_bar` | MEASUREMENT = **Bottom Hole Pressure**(或 **Flowing Pressure**) | 需二选一 |
| `pump_discharge_pressure_bar` | MEASUREMENT = **Pump Discharge Pressure** | |
| `pump_intake_pressure_bar` | MEASUREMENT = **Pump Intake Pressure** | |
| `reservoir_pressure_bar` | MEASUREMENT = **Reservoir Pressure** | |
| `choke_size_64ths_in` | MEASUREMENT = **Choke Size**(1/64 in) | 与参考表单位一致 |
| `gor_scf_stb` | MEASUREMENT = **Gas Oil Ratio**(scf/stb) | 与参考表单位一致 |
| `water_cut_pct` | MEASUREMENT = **BS&W Percent**(%) | 近似;无 "Water Cut" 项,BS&W 最接近 |
| `oil_rate_stb_d` | FLOW MEASUREMENT,`PRODUCT`=Oil,`RATE`,`RATE_UOM`=stb/d | |
| `water_rate_stb_d` | FLOW MEASUREMENT,`PRODUCT`=Water | |
| `gas_rate_mscf_d` | FLOW MEASUREMENT,`PRODUCT`=Gas,`RATE_UOM`=Mscf/d | |
| `liquid_rate_stb_d` | FLOW MEASUREMENT,`PRODUCT`=Liquid | 可跳过(= 油 + 水) |

测量名与产品名来自 `R MEASUREMENT`(已标记用于 well test)和 `R REPORTING PRODUCT`,均实时读取。

## 3. 入库前需确认的问题

1. **井身份**:`WELL-001` 无匹配。对应哪口现有井(LMK-Well-00xx)?还是需要先创建?
2. **压力单位**:CSV 为 bar,参考单位为 `psia`。选择:转换(×14.5038,假设为绝压),或在 `MEASUREMENT_VALUE_UOM` 中直接存 bar。
3. **时间**:各行间隔 2 小时,但 `test_duration_hr` 全为 24,无法确定每个 period 的 `END_DATE`。取"开始 + 24h"还是"下一测试点时间"?
4. **测试类型**:是否从 `R WELL TEST TYPE` 设置 `WELL_TEST_TYPE`?看起来像 multirate 或 choke-sweep 测试。
5. **`liquid_rate` 是否保留**?水含量是真实 water cut 还是 BS&W?
6. **时区**:测试日期(2026-10)没问题,是否设置 `TIMEZONE`(如 GMT+08:00)?

## 4. 写入顺序(`POST /save`)

1. 先保存 1 条 **WELL TEST**,得到 `WELL_TEST_ID`。
2. 再保存 10 条 **WELL TEST PERIOD**(需 `WELL_TEST_ID`),得到 `WELL_TEST_PERIOD_ID`。
3. 最后保存 **MEASUREMENT** 与 **FLOW MEASUREMENT**(需 period ID)。

每个请求体在写入前先给用户确认。先回答问题 1–3 即可开始构造 payload。
