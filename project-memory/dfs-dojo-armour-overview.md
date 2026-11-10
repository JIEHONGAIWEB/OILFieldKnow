# DFS Dojo Armour:项目介绍与能力地图

**来源:** 项目 README(2026-11-10 收录,内容以该仓库 README 为准,后续版本以仓库为准)
**类型:** 相关产品/项目参考(非 WPO 本身,但与 "WPO Agent-Native" 想法高度相关)
**GitLab:** `ds365ai/DFSDEV/apps/06-dfs-dojo/dfs-dojo-armour`(镜像:`.../dfs-dojo-armour/app`、`/web`)
**关联仓库:** `dfs-dojo-widget-library`(组件库)、`dfs-dojo-nextgen-testing`(测试与模拟器)

> Related: [WPO Agent-Native 机会分析](../analysis/2026-11-10-wpo-agent-native-opportunity-analysis.md)、
> [WPO 引入 MCP](../analysis/2026-11-10-wpo-mcp-requirement-analysis.md)、
> [ADR-0002 数据驱动图表分层](../architecture-decision/0002-data-driven-chart-layering.md)。

## 1. 一句话

**DFS Dojo Armour** 是 DFS Dojo 的下一代:一个 **React Web 应用 + Node API**,**每个客户本地(on-premises)安装一次**。用户通过 DecisionSpace 的 Keycloak(Halliburton 标准)或客户自己的身份提供方(Okta、Entra ID 等)登录。

核心理念:**Dojo = 一块多人实时协作的画布(canvas)**,上面放"组件(widget)",组件之间用连线(wire)传数据;**AI 可以在画布上直接添加、设置、连线组件**,而且每次改动都可列出、可撤销、可要求逐项确认。

## 1.1 真正的价值(总结)

> 一句话:**它不是又一个图表看板,而是一个"让 AI 在受控边界内,用现成积木替用户搭界面、接数据、并可随时撤销"的可落地范式,而且已经做到可私有化交付的产品级。**

**价值 1:证明了"AI 操作界面"可以安全落地**
AI 不生成代码,只在白名单组件里增删改、连线、绑定数据;每轮改动可列出、可一键撤销、可逐项确认。这解决了 Agent 最大的顾虑——不可控。

**价值 2:把"数据接入"和"界面搭建"解耦**
管理员一次性配好数据源(PI、Web API、SQL、Excel/CSV、资产模型),之后用户和 AI 只面对"标签(tag)"和"表"。换数据源不改页面,换井只换 `{well}`。**接入成本在管理员,使用成本接近零。**

**价值 3:权限贯穿到 AI**
数据源有读者组;AI 以**提问者的权限**读数据,读不到会明说。企业场景里"AI 不会越权"是上线的前提,这里已经做了。

**价值 4:经验可沉淀、可复用**
模板 + 变量 + 资产模型 = 一次搭好的页面可以套到另一口井、另一个 FPSO。这是"流程沉淀与复用"的现成底座。

**价值 5:油气领域内置,不是通用 BI 换皮**
Arps 递减预测(P10/P50/P90)、GOR/含水率/BS&W/60°F 体积公式、ISA-101 控制室外观、ISA-5.1 的 70 个 P&ID 符号、井-FPSO 资产树、跳闸/通讯中断事件。领域语义已经在组件和公式里。

**价值 6:企业级交付能力**
本地部署、离线安装、OIDC 单点登录(兼容 Keycloak/Okta/Entra)、审计日志、统一加密密钥存储、非 root + 只读文件系统容器、OpenShift 适配、备份/恢复/升级命令。能直接进客户机房。

**价值 7:工程方法值得借鉴**
契约单一来源(zod)、迁移只增不改、Mock AI 做确定性测试、"读取而不执行"(公式、路径语法、SVG 清理)、组件库独立仓库发布。

**需要清醒看待的边界:**
- 目前是**单副本**;多副本是后续步骤。
- 偏**实时监控与可视化**,不负责创建业务数据(如 WPO 的模型上传、调度任务)。
- 数据库连接器仅 PostgreSQL,OPC UA、SQL Server、Oracle、MySQL 未做。
- 第 6 步尚未开始;第 4、5 步仍在进行。
- 以上均来自 README 的描述,实际成熟度需看代码和 `docs/roadmap.md`。

## 2. 为什么对我们重要

它已经把 [WPO Agent-Native 分析](../analysis/2026-11-10-wpo-agent-native-opportunity-analysis.md) 里讨论的几个想法**做成了现实的产品形态**,可以作为参考实现:

| 我们分析中的想法 | Dojo Armour 中的对应 |
| --- | --- |
| 5.3 动态界面运行引擎(Agent 操作前端) | AI 在画布上增删改组件、连线、设属性;组件库 + 属性 Schema + 协议 |
| 5.3 组件注册表 | Widget Library(`widget-protocol` / `widget-sdk` / `widgets` / `widget-views`),可在 Settings 控制哪些类型可用 |
| 5.2 AI 选图并说明原因 | "AI as a designer":按表格形状选图表并解释 |
| 5.3 动作可撤销/可确认 | 每轮改动列表 + 即时 Undo;**Ask for approval** 模式逐项 Apply / Skip |
| 5.5 流程沉淀与复用 | **模板**(Templates):选中组件保存为模板,"井"参数化为 `{well}`,可换井复用;Dojo 变量与链接 `?var-well=B-2` |
| 5.2 数据发现 | 标签浏览器 + AI 的 `find_tags` / `list_queries` / `read_table` 等工具 |
| 7 权限与数据范围 | "Who reads what":按数据源的读者组控制,AI 以**提问者的权限**读取,读不到会明说 |
| 7 审计 | 内置审计日志(数据库) |
| 7 评估/测试 | Mock AI(`mock:` 指令)可确定性地测试画布工具,不依赖真实模型 |
| 5.3 事件回传 | 点击组件下钻、联动;用户选择可作为后续对话上下文 |

## 3. 技术栈与架构

| 部分 | 技术 |
| --- | --- |
| Web | React 19、Vite、TanStack Router/Query、Tailwind v4、Material UI(使用 Tecton 主题,`@webframework/*`,仅在 `shared/design-system` 导入) |
| Server | Fastify 5(Node 22),API 在 `/api` 下 |
| 实时协作 | Hocuspocus(画布 WebSocket)、光标/在线状态、事件总线 |
| 数据库 | PostgreSQL 18 + pgvector(客户自备时 ≥ 14);Kysely;迁移文件只增不改 |
| 契约 | `packages/contracts`:zod schema,服务端校验 + 前端校验响应(单一事实来源) |
| 其他包 | `app-sdk`(App 屏幕与 Armour 页面之间的桥)、`create-armour-app`(第三方 App 模板与合规检查) |
| 图表 | 组件由 Widget Library 提供(ECharts 等),通过 GitLab npm registry 引入 |
| 国际化 | `react-i18next`,字符串在 `apps/web/src/i18n/locales` |
| 安全 | OIDC(授权码 + PKCE)、HttpOnly Cookie 会话(空闲/绝对超时)、CSP(页面只加载自身文件,可离线)、容器非 root + 只读文件系统 + 丢弃所有 capabilities |

服务拆分(生产风格栈):`web`(nginx,代理 `/api`)、`app`(API,仅内部)、`migrate`(迁移后退出)、`postgres`(`database` profile)。

**关键约束:** 当前 **app 只能 1 个副本**——打开的画布驻留在所连接的那个实例里;误开两个也不会丢数据(通过数据库合并),多副本留待后续步骤。

## 4. 路线与进度(六步,前三步已完成)

| 步骤 | 内容 | 状态 |
| --- | --- | --- |
| 1 基础 | OIDC 登录/登出、会话、角色(`admin`/`member`,来自 IdP 的组)、审计日志、应用外壳 | 已完成 |
| 2 Dojo 与实时画布 | 共享给人/组、多人同时编辑、光标、撤销、版本、回收站;组件连线;Dojo 的聊天(画布上或停靠) | 已完成 |
| 3 Dojo 中的 AI | 聊天问答、AI 操作画布(含撤销/逐项确认)、Settings 里接入 Claude 与模型、`/` 命令、聊天导航与书签、问题附件 | 已完成 |
| 4 配置 | 每人设置(资料/主题/区域与单位/AI 指令与提示词);管理员设置(组织、人员与组、策略与限额、组件类型、安装页、密钥存储与轮换) | 部分完成 |
| 5 组件与数据 | 组件属性与阈值、实时数据、趋势与分析、仪表、分析图表、表格与事件、计算、流程图、地图、下钻/模板、显示模式、AI 设计师;以及连接器框架 | 大部分完成 |
| 6 | 见 `docs/roadmap.md` | 未开始 |

详细计划:`docs/step-2-plan.md` … `docs/step-5-plan.md`、`docs/step-5-part-b-plan.md`。

## 5. 能力地图

### 5.1 组件(Widget)

| 类别 | 内容 |
| --- | --- |
| 数值与仪表 | Value、Radial gauge、Linear gauge(bullet)、Level(罐/鼓)、Status light(严重时闪烁)、Analog indicator(ISA-101)、Sparkline、Progress、KPI 卡(带趋势线,与前一天/周对比) |
| 趋势 | Trend:多笔(pen)、分 panel/lane、状态与事件、设定值/输出、限值;缩放/平移/导航条;光标 A/B 统计;Dojo 时间范围与 Marker |
| 趋势分析 | 条件(如 "A-1 GOR above 1,800 for 10 minutes")高亮区间;Find similar(找相似区间);What moved with it(关联标签);叠加对比(日/班/区间);预期带(expected band);保存 View |
| 分析图 | Waterfall、Donut(其余并入 Other)、Scatter(直线/抛物线/指数/对数拟合 + R²)、Histogram/箱线图、Pareto |
| 运营与预测 | Heatmap、State timeline、Sankey(流量)、**Decline curve(Arps 递减:指数/双曲/调和,P10/P50/P90 预测)** |
| 表格与事件 | Table v2(分组/合计/徽章/按标签实时/按井成行,虚拟滚动),Event list(跳闸、通讯中断、存疑,可联动趋势) |
| 告警 | Alerts:按阈值生成卡片,标签带最近一小时小线 |
| 计算 | Calculation:电子表格式公式,44 个函数(时间加权平均、变化率、**GOR、含水率、BS&W、净油、60°F 体积**等);虚拟标签;公式语言为应用自有,**从不当代码执行** |
| 过程图形 | P&ID 风格,70 个按 ISA-5.1 绘制的符号,ISA-101 灰度;泵/罐/阀随状态变化,管道按流体着色并动态流动;可编辑、协作绘制;管理员可上传自有 SVG 符号(会清理可执行内容) |
| 地图 | Field map:井/FPSO/平台/管汇、井到 FPSO 的连线,按状态着色、按数值定大小,经纬度或场区坐标,或叠加场区图片 |
| 其他 | Group、Note(Markdown)、Pick(变量选择)、Slider/Toggle(what-if)、Time range、Query、Number/Math 等 |

通用能力:每个组件的属性分组(Data/Display/Series/Axes/Thresholds/Format/Card)、复制/粘贴样式、阈值与状态集合、ISA-101 **Control room look**、**Display mode**(整屏、实时,适合控制室大屏,`?display=true`)、导出 PNG/SVG/CSV。

### 5.2 数据与连接器(Settings → Data)

| 数据源 | 说明 |
| --- | --- |
| 模拟油田 | 2 个 FPSO、12 口生产井(带 ESP)、4 口注入井、分离器与外输线,按时间计算,所有人一致 |
| Dojo 数据源协议 v2 | HTTP + WebSocket,客户可自写适配器 |
| **PI System** | 通过 PI Web API;服务账号 Basic(仅 HTTPS)或 Bearer;按名称通配搜索 PI Point;历史取 plot values;统计用 PI 自身时间加权摘要;事件帧模板映射为跳闸/通讯中断/存疑 |
| Web API | API key/Bearer/Basic/OAuth client credentials;查询是路径 + 参数;用自有路径语法取行(如 `data.items[*]`),**读取不执行**;分页(链接/游标/页码),最多 5,000 行 |
| PostgreSQL | 查询为单条 SELECT,命名参数由驱动绑定,只读事务 + 超时 + 5,000 行上限;标签也可由 SQL 定义。SQL Server / Oracle / MySQL 待做 |
| Excel / CSV | 上传工作簿与 CSV(每文件 20 MB、每表 50,000 行、最多 10 个文件);表头定义列名与单位(如 `Oil (bbl)`);时间 + 数值表自动成为标签;重传覆盖且保留 ID |
| **资产模型(Asset model)** | 油田树:Field → FPSO → 井;每个资产的指标可为数据源标签或标签公式;作为数据源 `asset:A-1.oil_rate`;可从 CSV 或 PI AF 导入(导入前预览新增/变更/保留);OPC UA 待驱动 |

要点:
- **Tables from sources**:管理员在数据源页写查询(含参数、列单位、缓存时长),可试跑;**Query 组件**读取并作为表格传给任何图表/表格/计算;AI 用 `list_queries`、`read_table` 读取。
- **Who reads what**:管理员指定每个数据源的读者组;每个人只读到自己有权的标签、历史、统计、事件、查询;共享 Dojo 里无权读的组件显示锁标;**AI 以提问者的权限读取**。
- **资产模型的好处**:模板写成 `asset:{well}.oil_rate`,无论标签在哪个数据源,换井即复用。

### 5.3 AI 能力

| 能力 | 说明 |
| --- | --- |
| 聊天 | Dojo 内问答,所有成员实时可见;`/` 命令:`/share` `/rename` `/version` `/undo` `/new` `/widget` `/help`(不经 AI 直接执行);个人提示词可在 `/` 后选用 |
| 画布工具 | 添加/设置/连线组件;每轮改动列出,**Undo 立即撤销**;**Ask for approval** 模式下每项等待 Apply/Skip |
| AI 设计师 | 如 "a control-room page for FPSO A" 一次生成页面:标题、分区(Group)、按行排列的组件、标签、阈值、连线、风格;为表格选图并说明原因;让组件风格一致;设置时间范围并标注趋势;为另一口井放置模板;给 Calculation 写公式前先校验 |
| 数据工具 | `find_tags`、`list_queries`、`read_table`;趋势分析用 `read_span`、`find_spans`、`find_similar`、`find_related` |
| 附件 | 每个问题最多 5 个文件、每个 20 MB;图片/PDF(模型支持时)原样读取,Word/Excel/CSV/文本按文本读取 |
| 模型 | Settings 中管理员接入 Claude,并指定哪些组可用哪些模型、设默认 |
| 个人指令 | 每人自己的 AI 指令,仅用于自己的提问 |
| Mock AI | 无提供方时的占位 AI,用 `mock:` 指令确定性触发行为(如 `mock: page FPSO A`、`mock: trend A-1 rate`、`mock: fail/decline/busy/stall/long/markdown`、`mock: add note`、`mock: read`、`mock: remove`),用于测试 |

### 5.4 管理与运维

- **Settings(管理员)**:AI 模型、组织(名称/Logo/默认区域与单位)、人员与组(含停用并立即结束其会话)、策略与限额(Dojo 对外开放程度、AI/文件限额、会话时长、API 限流,立即生效)、组件类型开关、Data、Assets、Symbols、Installation(健康检查、密钥存储与轮换、环境)。
- **密钥**:AI 提供方的 key、数据源 token 用 `SECRETS_KEY` 加密,存放在统一的密钥存储中,**不再回显**;环境变量里只保留启动必需项。
- **安装**:`deploy/armour` 命令(`init` `check` `load` `start` `stop` `status` `logs` `backup` `restore` `upgrade`)、`deploy/INSTALL.md`、`deploy/schema.sql`(供客户 DBA 建表)。支持联网与离线安装;`armour check` 检查设置、数据库、密钥、IdP 与上传卷。
- **OpenShift / Kubernetes**:两个镜像以任意 UID(组 0)运行、只读根文件系统,适配 `restricted-v2`;app 端口 4302(`/api/health`、`/api/health/ready`),web 端口 8080(`/healthz`);迁移用同一镜像 `node dist/index.js migrate` 作为 Job;`TRUST_PROXY=uniquelocal`;上传卷需持久化并备份。

## 6. 开发与交付

| 项 | 说明 |
| --- | --- |
| 前置 | Docker + Compose(推荐 rootless);Node 22(`nvm use`);`@webframework` scope 的 npm 凭据(`~/.npmrc`,镜像构建以 BuildKit secret 读取,不进镜像层) |
| 启动 | `npm install` → `npm run dev`(Compose Watch 热更新),访问 `http://localhost:4202`;必须使用 `localhost`(它是 `PUBLIC_URL`,IdP 回调地址) |
| 管理员 | 在 `.env` 的 `AUTH_ADMIN_GROUPS` 指定自己所在的组,首次启动时写入数据库;之后在 Settings → People and groups 管理 |
| 检查 | `npm run lint` / `typecheck` / `test` / `build` / `format` / `ci`;服务端测试跑在内存 PGlite 上,无需容器;依赖模拟器的测试在 testing 仓库 |
| 流水线 | GitLab CI:check、ShellCheck、镜像构建、扫描(密钥/SAST/Dockerfile/依赖);`dev`/`master` 推镜像;`vX.Y.Z` 标签生成发布包和镜像文件;`dev`→`dfsdojo-dev`、`master`→`dfsdojo`(tiger 的 Kubernetes) |
| 分支 | `dev`(默认,工作分支,走 MR)、`master`(已发布,从 `dev` 合并并打标签);紧急修复从 `master` 拉分支再合回 `dev` |
| 发布 | `npm run release:version -- X.Y.Z` → 更新 CHANGELOG → `dev` 合并 `master` → 打标签 `vX.Y.Z`;发布包 `npm run release:package -- X.Y.Z`,测试 `npm run test:release` |

## 7. 约定(给 AI 助手与开发者)

- UI 用 Material UI + Tecton 主题;布局用 Tailwind;Tecton 只能在 `shared/design-system` 导入,不改写其组件样式。
- 图标用 Tecton 自带(`TectonIconName`)。
- 对话框用 `shared/components/dialog`。
- API 的输入输出**只在 `packages/contracts` 定义一次**,服务端与前端都据此校验。
- zod 只从 contracts 或组件库协议/SDK 引入(CSP 禁止编译式校验);页面与组件中禁止直接 `import zod`(ESLint)。
- 组件在独立仓库 `dfs-dojo-widget-library` 中修改和发布,本仓库通过 GitLab npm registry 升级版本;发布前可 `npm link` 试用。
- 服务端只加载组件的 manifest 和英文文案;只有页面加载视图。
- 前端 HTTP 统一走 `shared/data-access/api-client.ts`;服务端状态用 TanStack Query,客户端状态用 Zustand(导出 hooks 与 actions,不直接导出 store)。
- 数据库变更 = 新增迁移文件并登记到 `migrator.ts`;**已发布的迁移不得修改**。
- API 路由在 `onRequest` 校验会话,保证无会话一律 401。
- 服务端测试共用 PGlite 单连接:事务内要通过事务对象查询;写请求的测试串行发送,不用 `Promise.all`。
- 用户可见字符串放 i18n locale;测试文件与被测文件同目录;缺少 locale 字符串、未被 `mockApi` 应答的请求都会让测试失败;`renderApp` / `renderWithProviders` 是异步的,须 await。

## 8. 对 WPO Agent 想法的借鉴与差异

**可借鉴:**
1. **画布 + 组件 + 连线** 是"动态界面引擎"的一个成熟形态;AI 通过**工具调用**改画布,而不是生成代码(与我们 5.3 倾向 L1+L2 一致)。
2. **每轮改动可列出、可撤销、可逐项确认**,直接对应我们的"确认卡/可回滚"要求。
3. **以提问者权限读取**数据,不因 AI 而放大权限。
4. **模板 + 变量(`{well}`)+ 资产模型** 是"流程可复用"的现成做法:把一次成功的页面保存为模板,换井即用。
5. **Mock AI** 提供确定性测试,可借鉴为我们的评估集与重放回归基础。
6. **公式语言不当代码执行**、**路径语法只读取不执行**、**SVG 清理**:统一的"不执行不可信内容"原则,可直接用于 VizSpec / UI Schema 的校验。
7. **契约单一来源(zod)**、**迁移不可改**、**密钥统一加密存储**,是值得对齐的工程规范。

**差异 / 需要评估:**
- Dojo 的数据入口是 PI、Web API、SQL、文件、资产模型;WPO 的数据入口是 WSO/WPO REST 接口。要做 WPO Agent,需要新增一个"WPO 数据源"连接器,或用 MCP 暴露 WPO 接口。
- Dojo 偏**实时数据可视化与监控**;WPO 偏**油井性能分析与优化(IPR/泵/气举/Dynacard)**。性能曲线、梯度图、Dynacard 等 **WPO 特有的组件** Dojo 的组件库不一定已有,需要评估是新增组件还是复用 WPO 现有图表。
- Dojo 是**每客户本地安装的独立产品**;WPO 的 Agent 是否要嵌入 WPO 现有前端(Angular),还是通过 Dojo 承载,是一个架构选择(见待确认问题)。
- Dojo 当前单副本、写操作主要围绕画布,**不直接创建 WPO 业务数据(模型上传、调度任务)**。

## 8.1 优化空间

> 说明:AI **已经能驱动动态界面**(例如一句话生成整页控制室页面),只是限定在组件库的边界内。下面是**根据 README 推断**的空间,不是 README 明说的缺陷,需对照代码和 `docs/roadmap.md` 核实。

### A. AI 驱动界面的能力边界

| 现状 | 优化空间 |
| --- | --- |
| 只能用库里已有的组件类型 | 没有"组合出新组件"的机制。可让 AI 把几个组件组合为可复用的复合组件,或提出"缺哪种组件"的需求草稿,而不是只能近似替代 |
| 通过工具调用逐个修改画布 | 可先产出整页的声明式描述(Schema),预览和校验后整体应用,更易 diff、回放、评审 |
| 一次对话是"提问→改画布" | 未见页面随用户操作持续演化的机制(如用户点了某口井,AI 顺势调整整页) |
| 模板由人选中并保存 | 可让 AI 把一次成功对话主动提炼为模板,并自动参数化 |
| 布局靠 Group + 按行排列 | 缺少按屏幕尺寸、角色、数据量自适应的布局规则 |

### B. AI 在数据侧还做不到的

- **数据发现偏被动**:AI 能 `find_tags`、`list_queries`,但数据源与查询需管理员先配置;AI 不能提出"需要接这个接口",也不能根据样例响应推荐字段映射。
- **以只读和改画布为主**:不创建 WPO 那样的业务数据(模型上传、调度任务)。
- **缺评估闭环**:Mock AI 测的是工具链是否正常,不是"AI 搭出的页面好不好、对不对";缺页面质量评分与黄金样例。
- **口径解释**:图上数值是否自动带出口径和来源,README 未提。

### C. 工程层面

- 单副本,画布驻留在所连的 app 实例中。
- 连接器缺 OPC UA、SQL Server、Oracle、MySQL。
- 组件库与应用分仓,改一个组件要发版再升级,迭代链路长。
- 性能预算与无障碍检查是第 5 步的目标,是否完成需看代码。

### D. 对 WPO 最现实的几条

1. 补一个 **WPO 数据源**(Web API 连接器或 MCP),先让 Dojo 读到 WSO 数据。
2. 补 **WPO 特有组件**:IPR、Pump、Gas Lift、Dynacard、梯度图。
3. 让 AI 把成功的分析对话**提炼成带 `{well}` 的模板**,并叠加[分析 5.5](../analysis/2026-11-10-wpo-agent-native-opportunity-analysis.md) 的泛化测试。
4. 给 AI 搭的页面建**评估集**:选对图了吗、数对吗、口径带上了吗。

## 9. 待确认

1. Dojo Armour 与 WPO 的关系:是并列产品、可集成,还是 WPO 的 Agent 将构建在 Dojo 之上?
2. Widget Library 是否可被 WPO 前端(Angular)复用,还是只在 Dojo(React)中使用?
3. 是否计划为 Dojo 增加 WPO 数据源连接器(或 MCP 连接)?
4. WPO 特有图表(IPR/Pump/Gas Lift/Dynacard/梯度图)是否会纳入组件库?
5. Dojo 的模板/变量/资产模型机制,能否作为"流程沉淀与复用验证"(分析 5.5)的底座?

## 10. 参考

- 项目 README 与 `docs/roadmap.md`、`docs/step-2…5-plan.md`
- 组件参考:`dfs-dojo-widget-library/docs/catalog.md`
- 安装指南:`deploy/INSTALL.md`
- 仓库内相关:[WPO Agent-Native 机会分析](../analysis/2026-11-10-wpo-agent-native-opportunity-analysis.md)
