# 长期维护项目与文档地址台账

更新时间：2026-11-12
维护主题：维护长久

## 1. 维护范围

- 维护长久-知识图谱：JIEHONGAIWEB/OILFieldKnow
- 维护长久-项目建设：JIEHONGAIWEB/systemWholePerson
- 自动化测试：JIEHONGAIWEB/AutoUITest
- 维护长久-长期目标：跨项目文档化、标准化、可追踪化

## 2. 项目地址与文档地址

| 维护方向 | 仓库标识 | 项目地址 | 文档地址（当前） | 文档地址（建议） | 备注 |
|---|---|---|---|---|---|
| 维护长久-知识图谱 | JIEHONGAIWEB/OILFieldKnow | https://github.com/JIEHONGAIWEB/OILFieldKnow | https://github.com/JIEHONGAIWEB/OILFieldKnow#readme | https://github.com/JIEHONGAIWEB/OILFieldKnow/tree/main/docs | 作为知识图谱与文档中枢 |
| 维护长久-项目建设 | JIEHONGAIWEB/systemWholePerson | https://github.com/JIEHONGAIWEB/systemWholePerson | https://github.com/JIEHONGAIWEB/systemWholePerson#readme | https://github.com/JIEHONGAIWEB/systemWholePerson/tree/main/docs | 作为系统建设与落地项目(本地 react-app,详见 [system-whole-person-react-app-overview.md](system-whole-person-react-app-overview.md)) |
| 自动化测试 | JIEHONGAIWEB/AutoUITest | https://github.com/JIEHONGAIWEB/AutoUITest | https://github.com/JIEHONGAIWEB/AutoUITest#readme | https://github.com/JIEHONGAIWEB/AutoUITest/tree/main/docs | 作为自动化测试能力建设 |

### 2.1 运行环境地址

| 名称 | 地址 | 环境 | 备注 | 加入日期 |
|---|---|---|---|---|
| Harmony UI（DFS Dojo，dev） | https://harmony-ui-dfsdojo-dev.tiger.dazlmkengdev02.ienergycloud.solutions/ | Tiger dev（域名中含 dazlmkengdev02） | Harmony 前端入口；相关背景见 [dfs-dojo-armour-overview.md](dfs-dojo-armour-overview.md)、[subsurface-studio-harmony-showcase.md](subsurface-studio-harmony-showcase.md)、[dfs-ai-assistant-overview.md](dfs-ai-assistant-overview.md) | 2026-11-12 |

> 用途和访问权限根据域名名称推断，尚未打开核实；需要登录与否、对应的负责人，见第 5 节待补充项。

## 3. 长期目标（书面化）

- 目标一：项目资料统一入口
  - 三个项目统一维护 README 与 docs 目录入口，避免信息分散。
- 目标二：文档结构标准化
  - 统一最小文档集合：README、架构说明、开发指南、测试指南、发布记录。
- 目标三：交付过程可追踪
  - 每个项目维持变更记录（feature history）与问题记录（bug knowledge）。
- 目标四：自动化与质量提升
  - 在 AutoUITest 体系中沉淀可复用测试场景，并回链到业务文档。

## 4. 维护建议节奏

- 每周：核对仓库地址、文档入口是否有效。
- 每双周：更新一次目标完成情况与风险。
- 每月：输出一次跨项目维护报告（进展、风险、下月重点）。

## 5. 待补充项

- 各仓库实际 docs 根路径与发布地址（如 GitHub Pages / 内部门户）。
- 各项目负责人、维护人、评审人名单。
- 统一文档版本号规则与归档规则。
- 运行环境地址（如 Harmony UI dev）的用途、访问方式（是否需登录/VPN）、负责人，以及是否有对应的 test/prod 地址。
