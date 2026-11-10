# Pipeline 改用 Production configuration 打包后再做安全扫描

**日期:** 2026-11-10
**状态:** 沟通中(待确认 pipeline 修改方 / 扫描对象)
**负责人:**

## 背景 / 问题

当前安全扫描(Xray)扫描的是 **Dev 环境下打包**的产物,因此扫描报告里的部分问题出现在 **devDependencies** 中,并不代表生产环境实际存在的风险,干扰判断。

## 想法

调整前端 pipeline,让它在 **Production configuration** 下 build,再对该产物做安全扫描,从而更准确地反映生产环境真实的安全问题。调整后再查看扫描报告,看还有哪些问题需要优化。

## 当前线索

- 对 dev 分支打包时,目前参数选项是打包 production configuration,然后对该包做安全扫描;需确认能否通过 job 的某个选项选择生产/开发包。
- 观察:该 job 的 build 步骤中,`ng build` 后面**没有** `--configuration production`。→ 很可能是 dev 包的直接原因(待验证)。
- 建议改法(待验证):在 build 命令加 `--configuration production`(或使用 `npm run build -- --configuration production` / 对应的 build script)。

## 待确认问题

1. Xray 扫描的压缩文件与仓库/制品库中的 **SHA-256** 序列有无对应关系?目的:确认**当前扫描的到底是哪个压缩包**。
2. pipeline 里是否已有选项可切换 production / development configuration?
3. 打包产物(production)中是否仍包含 devDependencies 的内容?(production build 通常只打包被引用的代码,但需看扫描是否基于 `package.json`/lock 文件而非产物。)

## 沟通进展

| 对象 | 内容 | 状态 |
| --- | --- | --- |
| 俊杰 | 昨天已沟通;他目前工作安排仍在 WPO,会来修改 pipeline | 等待今天是否有更新,有则反馈 |
| Yiming | 咨询是否之前修改过前端 pipeline 的打包配置 | 待回复 |
| Dingjing | 咨询是否可通过选项选择 prod/dev 打包;并指出 `ng build` 缺少 `--configuration production` | 待回复 |
| Eric | 咨询 Xray 扫描的压缩文件与 SHA-256 的关系,定位被扫描的包 | 待回复 |

## 下一步

- [ ] 确认 pipeline 中 `ng build` 实际命令并加上 `--configuration production`。
- [ ] 重新打包并触发扫描,拿到新的扫描报告。
- [ ] 通过 SHA-256 核对被扫描的压缩包即为 production 包。
- [ ] 对比新旧报告,梳理剩余需优化的问题。

## 备注

若 Xray 是按依赖清单(lock 文件)扫描而非产物内容,即使改为 production build,devDependencies 仍可能出现在报告中;这时需要在扫描侧过滤 dev 依赖(如仅扫描 production 依赖),应在拿到报告后判断。
