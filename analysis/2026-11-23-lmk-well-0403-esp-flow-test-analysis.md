# LMK-Well-0403 ESP Flow Test 数据分析

**日期:** 2026-11-23  
**状态:** Draft  
**关联模块:** Well Test Management、Model Calibration  
**相关文档:** [well-test-model-calibration-data-prep.md](../domain-knowledge/well-test-model-calibration-data-prep.md)、[esp-wells-monitoring.md](../domain-knowledge/production/esp-wells-monitoring.md)、[well-test-csv-mapping.md](../data-model/entities/well-test-csv-mapping.md)

## 1. 背景

来源:WPO "Detailed Information" 页面截图。LMK-Well-0403 的一次 ESP 24 小时 Flow Test(已 Approved)。数据含产量、井口压力、分离器参数与 ESP 运行参数,可用于判断当前产能、分析 ESP 状态,并为 Well Test Management 与 Model Calibration 提供基础数据。

## 2. 基本信息

| 项目                | 数据                                      |
| ----------------- | --------------------------------------- |
| Well Name         | LMK-Well-0403                           |
| Well Type         | Oil Producer                            |
| Well Test Type    | Flow Test                               |
| Production Method | ESP                                     |
| Status            | Approved                                |
| Start / End       | Jul 04, 2026 21:44 → Jul 05, 2026 21:44 |
| Duration          | 24 h                                    |
| Remarks           | ESP Product Test - II                   |
|                   |                                         |

## 3. 原始测试数据

| 类别  | 参数                          | 数值          | 单位            |
| --- | --------------------------- | ----------- | ------------- |
| 产量  | Liquid Rate                 | 1068.8      | stb/d         |
|     | Oil Rate                    | 293.92      | stb/d         |
|     | Water Rate                  | 774.88      | stb/d         |
|     | Total / Associated Gas Rate | 91.63       | Mscf/d        |
|     | Water Cut                   | 72.5        | %             |
| 地面  | THP                         | 384.93      | psia          |
|     | Choke Size                  | 64          | 1/64 in       |
|     | Separator Pressure          | 349.95      | psia          |
|     | Separator Temperature       | 154.6       | °F            |
| ESP | Intake Pressure (Pi)        | 1406.36     | psia          |
|     | Discharge Pressure (Pd)     | 2063.46     | psia          |
|     | Frequency                   | 46          | Hz            |
| 气液比 | Total GOR / Solution GOR    | 0.31 / 0.31 | scf/stb(单位存疑) |
|     | TGLR                        | 0.09        | scf/stb(单位存疑) |
| 空缺  | Water Salinity              | 无值          | ppm           |

## 4. 分析

### 4.1 产能与含水
- 液量 = 油 + 水:293.92 + 774.88 = 1068.80,数据自洽。
- Water Cut 72.5%,每 100 桶液约 27.5 桶油,属较高含水。高含水不等于产能差,需结合油藏压力、历史含水趋势、完井层段判断。

### 4.2 GOR 单位疑点(需核查)
- GOR = 91.63 × 1000 / 293.92 ≈ **311.7 scf/stb**,截图为 0.31,应是 **Mscf/stb** 却标成 scf/stb。
- TGLR = 91.63 / 1068.8 ≈ 0.0857 Mscf/stb ≈ **85.7 scf/stb**,截图为 0.09。
- 影响:PVT、IPR/VLP、模型校准。需核查 Total GOR、Solution GOR、TGLR 的单位定义与换算逻辑。

### 4.3 井口与分离器
- THP − Separator Pressure = 384.93 − 349.95 = 34.98 psi。要判断压降是否合理,还需管线压力测点和设备布置。
- Choke 64/64 in = 名义 1 英寸。需确认系统存的是实际开度、标称尺寸还是配置值。

### 4.4 ESP
- 泵压差 ΔP = 2063.46 − 1406.36 = **657.10 psi**。
- 46 Hz 本身无法判断是否在最佳效率区,还需:泵型号、级数、性能曲线、电机功率/电流、流体密度/粘度、气体处理能力。

## 5. 当前数据能回答什么

| 分析方向 | 能否分析 | 原因 |
|---|---|---|
| 当前日产油 / 液能力 | 可以 | 有 Oil / Liquid Rate |
| 含水率 | 可以 | 有 Water Cut |
| 气油比 | 需核查单位 | GOR 单位存疑 |
| ESP 泵压差 | 可以 | 有 Pi、Pd |
| ESP 最佳工况 | 数据不足 | 缺泵性能曲线 |
| IPR | 暂不能 | 缺油藏压力、流动井底压力 |
| VLP | 暂不能 | 缺井筒流体、管柱、温度 |
| Model Calibration | 需补充 | 缺油藏、PVT、井筒、历史测试 |

## 6. 做 IPR / VLP / Model Calibration 还需补充

- **油藏:** Reservoir Pressure、Reservoir Temperature、Productivity Index、完井信息
- **PVT:** Oil API、Water SG、Gas SG、Bubble Point、Solution GOR、Bo/Bw/Bg
- **井筒:** Tubing Size / Depth、TVD / MD、Completion Depth、Wellhead Temperature、Flowing Bottomhole Pressure
- **ESP:** Pump Model、Stages、Frequency、Pi、Pd、Pump Performance Curve

## 7. 结论与下一步

1. **生产表现:** 液 1068.8、油 293.92 stb/d,含水 72.5%。
2. **设备表现:** 46 Hz、泵压差约 657.10 psi,具备分析泵工作点的基础。
3. **数据质量:** GOR / Solution GOR / TGLR 单位需核实;缺 FBHP 与油藏压力,无法建立可靠 IPR。

这份数据只说明这口井**在某一工况下产了多少**,不能说明**最大产能**。

下一步:获取多个不同流量工况下的 Flowing Bottomhole Pressure,建立 IPR,结合 ESP 性能曲线与 VLP 确定实际工作点;由此从单次 Well Test 走向完整的 Well Surveillance、Well Test Validation 与 Model Calibration。
