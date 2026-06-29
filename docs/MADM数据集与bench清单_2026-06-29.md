# 智能 MADM/MCDA 数据集与 bench 清单

日期：2026-06-29  
目的：围绕“不要再做没有外部基准的 online reviews 产品排序”，整理文献中可被改造成有标签、多准则分级/排序/偏好学习任务的数据来源，并给出适配判断。  
原则：优先看数据是否可获得、标签是否能作为 bench、任务是否仍然有 MCDA/MADM 味道，而不是只看方法名称是否“AI”。

## 1. 先给结论

当前文献给出的信号比较清楚：更适合我们继续深挖的不是“在线评论产品最终排名”，而是“有 assignment examples / ordered classes / external ranking 的多准则 sorting 或 preference learning”。原因是这类任务天然能做训练/测试划分、accuracy、F-score、Kendall tau、0/1 loss、AUC 等检验，审稿人更容易看到方法到底好在哪里。

最适合我们做长期调研和论文切口的场景，按当前证据排序如下：

| 优先级 | 场景 | 结论 |
|---:|---|---|
| 1 | 公开 monotone classification / MCS benchmark suite | 最稳的 benchmark 底座。数据公开、标签明确、已有文献使用，适合做第一层方法验证，但应用故事偏弱。 |
| 2 | 机构评价：Polish research units / research unit evaluation | 决策学味道强、公开数据、官方等级标签，比 QS 更像真正 MCDA 应用。非常值得作为主应用或第二案例。 |
| 3 | 大学排名/大学分级：QS、BCUR、THE 等 | 老师给过方向，数据好拿，本地已有 QS 2020/2022/2026；适合作为应用案例，但不能把 QS 当绝对真值，只能当“外部榜单监督信号”。 |
| 4 | Wine quality / car / CPU / medical screening 等有序质量分级 | 数据最容易获得，bench 很清楚；风险是容易被看成普通 ML，需要强调“ordered classes + interpretable MCDA constraints”。 |
| 5 | Credit rating / bankruptcy / bank failure / firm financial state rating | bench 强、决策味道强；但公开数据与财务字段处理要再核，且容易进入金融风控文献竞争区。 |
| 6 | Incremental / active preference elicitation 的小型真实决策案例 | 前沿感强，适合方法创新；但很多数据集是小规模或从既有文献生成 assignment，数据公开性不如前几类。 |
| 7 | Dynamic/context-dependent preference learning | 很新，但更靠近推荐系统、用户行为和动态偏好；若没有可靠行为数据，不宜作为当前主线。 |
| 8 | Online reviews / consumer preference / human preference experiment | 暂不建议作为主线。评论数据已有积累，但最终排序缺外部客观 bench；人类实验成本高。 |

推荐的验证结构不是单一场景，而是“双层 bench”：

1. 第一层：用公开 MCS benchmark suite 做方法硬验证，证明模型不是只在某个榜单上有效。
2. 第二层：用机构评价或大学分级做应用案例，讲清楚它为什么是多准则决策问题。
3. 避免只做 QS。只做 QS 容易被质疑为“复现商业排名”；但 QS 作为第二案例是可以的。

## 2. 大表：文献中的数据集与 bench

证据状态：

- A：本地全文或官方数据页已核到关键细节。
- B：DOI/摘要/官方元数据已核，全文数据细节尚未完全核。
- C：候选线索，仍需下载全文或确认数据可得性。

| 状态 | 场景/任务 | 代表文献 | 数据集与来源 | 自建/公开 | 规模 | 准则/属性 | 标签/bench | 文献验证方式 | 数据获取难度 | 适配判断 |
|---|---|---|---|---|---:|---|---|---|---|---|
| A | 大学多准则 sorting：QS 2020 五等级 | Liu et al., EJOR 2020, DOI: [10.1016/j.ejor.2020.04.013](https://doi.org/10.1016/j.ejor.2020.04.013)；本地 PDF `1-s2.0-S0377221720303465-main.pdf` | QS World University Ranking 2020；论文脚注给出 TopUniversities 入口；本地有 `大学排名2020.csv` | 公开榜单，本地已存 | 500 所大学用于实验；本地 CSV 有 1300 行原始抓取 | 6 个 QS 指标：citation per faculty、international students、international faculty、faculty/student、employer reputation、academic reputation | 按 QS 排名区间构造 5 个有序等级：[1,100] 到 [401,500] | 70% reference/training，30% test，重复随机划分 100 次；Top-N accuracy、Kendall tau | 低 | 适合作为应用案例。优势是老师方向一致、数据好拿；风险是 QS 是商业榜单，不能当绝对真值。 |
| A | 智能 ELECTRE III 阈值学习：QS 2022/2026 | 本地“An intelligent ELECTRE III model based on neural networks with threshold detection” | QS World University Rankings 2022；本地 `大学排名2022.csv`、`大学排名2026多了几个属性.xlsx`；QS 官方 methodology 页面列出当前指标与权重 | 公开榜单，本地已存 | 论文使用 top 500；训练 350、测试 150；本地 2026 xlsx 为 509 行、12 列 | QS 2022 六指标；2026 本地数据增加 IRN、employment outcomes、sustainability、international student diversity 等 | QS 官方排名作为真实排序/benchmark；训练 q/p/v 阈值使 ELECTRE 排名接近真实排名 | ranking accuracy、Kendall rank correlation；与 VIKOR、TODIM、传统 ELECTRE III、linear regression、linear NN、MLP 对比 | 低 | 可作为“传统优序法参数智能化”直接样板。但如果继续做，应把任务改成“阈值/偏好结构学习”，而不是泛泛说 AI+MADM。 |
| A | 中国大学分级：BCUR 2018 | Liu et al., EJOR 2019, DOI: [10.1016/j.ejor.2019.01.058](https://doi.org/10.1016/j.ejor.2019.01.058)；本地 PDF `1-s2.0-S0377221719300931-main.pdf` | Best Chinese Universities Ranking 2018，论文给出 ShanghaiRanking 链接 | 公开榜单，需重新核下载入口 | 600 所中国大学 | 4 个维度：teaching and learning、research、social service、internationalization | 按综合得分分成 5 类，每类 120 所；Cl5 最好、Cl1 最差 | accuracy、precision、recall、F-score；与 UTADIS 对比；同时做仿真实验检验 criteria/classes/noise | 中 | 比 QS 更贴中国语境，但数据入口要重新抓。适合做“大学/机构分级”的补充案例。 |
| A | Polish research units 官方机构评价 | Liu et al., INFORMS JOC 2020, DOI: [10.1287/ijoc.2020.0977](https://doi.org/10.1287/ijoc.2020.0977)；数据在 [ijoc-data/research-unit-evaluation](https://github.com/ijoc-data/download/tree/master/research-unit-evaluation) | Polish Ministry of Science and Higher Education 2017 研究单位评价；INFORMS JOC GitHub 提供 `PLS.csv` | 公开数据 | 993 个单位，分五个学科子集：HS 282、NZ 218、SI 286、TA 99、NJN 108 | 4 个 gain criteria：scientific activity、scientific potential、material effects、remaining effects | 4 个有序等级：low、medium、good、extraordinary | 各学科子集 70/30 划分；classification accuracy；解释 criteria weights 与 interactions | 低 | 很适合。它比 QS 更像真实多准则机构评价，且数据公开、标签清楚。建议优先核并下载。 |
| A | 9 个公开 monotone classification benchmark | Liu et al., INFORMS JOC 2020；数据在 [ijoc-data/monotone-classification-problems](https://github.com/ijoc-data/download/tree/master/monotone-classification-problems)；Martyn & Kadziński EJOR 2023 也属于同一 benchmark 生态 | UCI、WEKA、Den Bosch 等整理后的 MCS benchmark；GitHub 直接提供 CSV | 公开数据 | 9 个数据集：DBS 120、CPU 209、BCC 278、MPG 392、ESL 488、MMG 830、ERA 1000、LEV 1000、CEV 1728 | 4-8 个 criteria；GitHub 已标准化为 [0,1] gain type | 有序 classes；class index 越大越偏好 | accuracy、precision、recall、F-measure；与 UTADIS、Choquet sorting 等比较 | 很低 | 最适合做“硬 bench”。缺点是应用故事分散，建议作为方法验证第一层，不单独作为论文应用主叙事。 |
| B | Deep preference learning for MCDA | Martyn & Kadziński, EJOR 2023, DOI: [10.1016/j.ejor.2022.06.053](https://doi.org/10.1016/j.ejor.2022.06.053)；PDF 线索已核 | 大概率使用上述多个 MCS benchmark，学习 threshold-based sorting model 参数 | 公开/半公开 | 需全文逐表核对 | MCDA scores：OWA、additive value、Choquet、ideal/anti-ideal distance、Net Flow Scores 等 | assignment examples | AUC、0/1 loss 等；与 MCDA/ML baseline 比较 | 低到中 | 方法很关键。它说明“深度学习”不是替代 MCDA，而是学习 MCDA sorting model 参数。需要全文精读。 |
| B | Red/wine quality 有序质量分级 | Li, Zhang & Pedrycz, Omega 2025, DOI: [10.1016/j.omega.2024.103219](https://doi.org/10.1016/j.omega.2024.103219)；UCI [Wine Quality](https://archive.ics.uci.edu/dataset/186/wine%2Bquality) | UCI Wine Quality；红白 vinho verde 酒，physicochemical tests 到 sensory quality score | 公开数据，CC BY 4.0 | UCI 页面主表显示 4898 个 white-wine 实例、11 个输入特征；常用 red-wine 子集为 1599 条 | 11 个物理化学属性：fixed acidity、volatile acidity、citric acid 等 | quality score 0-10；ordered and imbalanced | 分类/回归；Omega 文献用于 non-monotonic MCS 与 PLNN/PLFMNN | 很低 | 适合作为非单调偏好学习的可复现实验。但应用故事偏普通 ML，需要和 MCDA 约束强绑定。 |
| A | Car evaluation / CPU / MPG / Breast cancer / Mammographic 等 | INFORMS JOC 2020 的 benchmark suite；UCI/WEKA 原始来源 | GitHub 已清洗为 MCS 格式；UCI 也有原始数据，如 [Car Evaluation](https://archive.ics.uci.edu/dataset/19/car%2Bevaluation)、[Wine Quality](https://archive.ics.uci.edu/dataset/186/wine%2Bquality) | 公开数据 | 单个数据集 120-1728 | 车辆、CPU、患者筛查等多属性 | 有序等级或二分类标签 | 分类指标；与 UTADIS/Choquet/其他 PL 方法对比 | 很低 | 适合做 benchmark 扩展。不要把每个都写成应用创新，作为实验矩阵即可。 |
| C | Credit rating / firm financial state rating | Li et al., arXiv 2024 / EJOR 2025, DOI 线索：EJOR 2024.11.047；arXiv: [2409.02760](https://arxiv.org/abs/2409.02760) | 文献用 existing literature 的 credit rating / firm financial state rating 示例；来源包括 Guo et al. 2019、Despotis & Zopounidis 1995、Ghaderi et al. 2017 | 不确定，需全文追溯 | 需核 | 财务指标，多准则 | 信用等级/财务状态等级 | active/incremental preference elicitation；accuracy、cost saving rate | 中到高 | 决策味道强，bench 强，但数据来源要追。可作为中期候选，不宜现在就锁主线。 |
| B | Incremental active preference elicitation 的 9 个小型真实决策矩阵 | Li et al., arXiv 2024 / EJOR 2025, arXiv [2409.02760](https://arxiv.org/html/2409.02760v1) | Buses、Environmental zones、Students、Couple's embryos、Suppliers、Nanomaterials、Storage location、Research units HS1EK、Research units NZ1M | 来自既有文献；公开性待核 | 48-93 个 alternatives；4-8 criteria | transport、environment、education、medical reproduction、supplier、nanomaterial、storage、research units | 该文为构造实验会生成 category assignments，不全是天然外部标签 | accuracy、cost saving rate；比较 question selection strategies | 中 | 前沿，但数据小且部分标签是生成的。适合做“交互式 elicitation”副线，不适合作为我们当前第一主线。 |
| B | Constructive preference elicitation：research units | Liang et al., Information Fusion 2025, DOI: [10.1016/j.inffus.2024.102926](https://doi.org/10.1016/j.inffus.2024.102926) | 57 个 research units，4 个 criteria；真实研究单位案例 | 未核数据公开 | 57 | 4 criteria | DM preference / pairwise question setting | estimate-then-select strategy；减少 DM 认知负担 | 中到高 | 方法前沿、样本小。可作为“如何减少专家标注成本”的理论参照，不建议当主数据源。 |
| B | Attention network + interacting criteria MCS | Gao, Zhang & Yu, Information Fusion 2026, DOI: [10.1016/j.inffus.2025.103443](https://doi.org/10.1016/j.inffus.2025.103443) | 摘要称使用 real-world datasets；具体数据集需全文核 | 未核 | 未核 | monotonic blocks 学 marginal value functions；attention 捕捉 pairwise interaction | assignment examples | real-world datasets + numerical experiments | 中 | 方法方向很贴近“智能化 MCDA”，但数据细节未核。作为前沿方法文献优先下载。 |
| A | Temporal criteria preference learning：用户价值分级 | Li et al., EJOR 2025 / arXiv [2309.12620](https://arxiv.org/abs/2309.12620)；本地 PDF `li_etal_2025_temporal_criteria_preference_learning_arxiv.pdf` | 中国某大型互联网公司 MOBA 手游用户行为数据 | 私有数据 | 3080 用户；2023-04-30 到 2023-05-30；24 个时间点 | 购买金额、购买频次、在线时长、登录频次 | 2023-05-24 到 2023-05-30 累计游戏内购买是否大于 0；高价值用户 47% | 10-fold CV；precision、recall、F-score、accuracy；与 SVM、LR、RF、MLP、RNN/GRU/LSTM、MCDA baseline 比较 | 高 | 论文很强，但数据不可得。除非有合作数据，否则只能作为方法参照。 |
| C | Dynamic preference learning：动态决策环境 ranking | Zhao et al., EJOR 2025/2026, DOI: [10.1016/j.ejor.2025.08.008](https://doi.org/10.1016/j.ejor.2025.08.008) | practical application in military context + computational experiments | 未核公开 | 未核 | 动态多准则 ranking | DM evolving preferences | state space model；与 state-of-the-art PL methods 对比 | 高 | 新但抽象，真实数据难拿。更适合后期理论拓展，不适合当前落地。 |
| B | Dynamic/context-dependent user preference | Ru et al., INFORMS JOC 2026, DOI: [10.1287/ijoc.2023.0372](https://doi.org/10.1287/ijoc.2023.0372)；代码数据仓库 [INFORMSJoC/2023.0372](https://github.com/INFORMSJoC/2023.0372) | real-world Amazon data，cell phones and accessories 等；仓库关联软件和数据 | 仓库公开，但需核数据完整性 | 未核 | item/content/user behavior/context | user preference / recommendation outcome | scalability、interpretability、predictive performance against baselines | 中 | 接近推荐系统和在线评论，数据可能可得，但和我们想避开的 consumer preference 边界很近。暂不主推。 |
| A | Online reviews 产品排序 | 大量 2017-2025 online reviews + MCDM 文献；本地已有 PConline/产品排序类 PDF | 平台评论、情感、评分、销量、评论数、平台排名等 | 多为自建抓取 | 通常可抓，但复现实验难 | aspect sentiment、价格、评论数、销量等 | 常用销量/评论数/平台排序/一致性作为弱 benchmark | 与 TOPSIS/VIKOR/TODIM/均值排序一致性；case explanation | 中 | 不建议做主线。数据不难，bench 最弱，容易自说自话。除非改成“评论特征预测外部标签”，否则风险高。 |
| C | Human preference experiment / pairwise choice | Jiang et al. 2025, arXiv [2504.14938](https://arxiv.org/abs/2504.14938) 等 | 人类受试者做 pairwise comparison，可能结合 response time、attention、eye-tracking | 自建实验 | 例如 40 名受试者级别 | 产品属性、套餐属性、行为信号 | 受试者偏好/选择作为 ground truth | preference reconstruction accuracy | 高 | bench 很干净，但实验成本高、伦理/招募麻烦。当前不现实。 |

## 3. 对“QS 排名方向”的判断

QS 方向不是不能做。文献中至少有两种已经成型的做法：

1. EJOR 2020 把 QS 2020 top 500 转成五个有序等级，并用 70/30 划分测试 sorting 模型。
2. 本地智能 ELECTRE III 文献用 QS 2022/2026 做阈值学习和排名复现。

但 QS 的问题也很明确：

- QS 排名不是自然真值，而是商业排名机构自己的加权体系。
- QS 指标中包含 reputation survey，审稿人可能认为这不是客观质量标签。
- 如果方法目标只是“更接近 QS”，贡献容易变成拟合既有榜单。

因此，QS 更适合作为第二应用案例，而不是唯一 bench。比较稳的写法是：

> 使用 QS/BCUR 等公开大学排名作为外部监督信号，构造有序分级任务，检验模型能否在保留 MCDA 可解释结构的同时，从历史 assignment/ranking examples 中学习偏好参数。

这比“我们预测大学真实好坏”更稳。

## 4. 对“换掉 online reviews”的判断

如果按 bench 强度和数据现实性来看，online reviews 不适合作为下一条主线。它最大的问题不是数据没有，而是最后的排序无法被强验证：

- 用评论排序产品，本身就是用主观评论生成主观结果。
- 用销量、价格、评论数、平台榜单做外部标签，这些变量也受曝光、营销、库存、品牌、平台机制影响。
- 只证明和 TOPSIS/VIKOR/TODIM/均值法相近，只能说明没有排得离谱，不能证明更优。
- 用个案解释差异，容易被认为是事后解释。

如果必须保留在线评论资产，建议把它降级为输入模态，而不是最终任务：

| 可保留方式 | bench 怎么来 | 风险 |
|---|---|---|
| 评论文本抽取 criteria/sentiment，然后预测外部标签 | 例如退货风险、投诉等级、质量等级、官方缺陷召回、销量区间等 | 需要能拿到外部标签 |
| 评论作为产品属性补充，加入 QS/机构/质量类任务不可行，这条不建议硬拼 | 无自然对应 | 容易回到自说自话 |
| 做人类偏好实验，让受试者基于评论摘要选择 | 人类选择是 ground truth | 实验成本高 |

## 5. 更像论文切口的三条路线

### 路线 A：Benchmark-first 的智能 MCS 方法

任务：从 assignment examples 中学习 MCDA sorting model 的参数、阈值、边际价值函数、criteria interactions 或 non-monotonic preference。

数据组合：

- 主 bench：9 个 monotone classification problems。
- 应用案例：Polish research units 或 QS/BCUR。
- 可选：Wine quality / car / medical screening 作为 non-monotonic 或 ordered classification 扩展。

优点：bench 最强，实验说服力最好。  
风险：需要方法上真有增量，不能只是套 NN。

### 路线 B：机构/大学评价的可解释偏好学习

任务：把大学/机构评价从固定加权排名改成可学习、可解释、有约束的 MCDA sorting/ranking。

数据组合：

- Polish research units：官方机构分级，四准则，四类。
- QS/BCUR：外部榜单分级或排序。
- 2026 QS 本地数据：新增可持续、就业、国际研究网络等属性，可做跨年泛化。

优点：和老师方向贴合，应用叙事强。  
风险：如果只拟合榜单，会被质疑；必须加公开 benchmark 做第一层验证。

### 路线 C：非单调/交互 criteria 的偏好学习

任务：传统 MCDA 常假设准则单调、独立，但真实任务中可能存在非单调和交互；用结构化 ML/NN 学习这些关系。

数据组合：

- Wine quality：非单调很自然，例如某些化学指标过高过低都不好。
- INFORMS JOC benchmark：有 interactions 的模型对比。
- Information Fusion 2026 attention network 文献作为前沿方法参照。

优点：方法创新点比“学权重”更实。  
风险：需要讲清楚为什么这仍是 MCDA，而不是普通神经网络分类。

## 6. 当前最该继续核的文献/数据

优先级 1：

- INFORMS JOC 2020 的两个 GitHub 数据目录：`research-unit-evaluation` 和 `monotone-classification-problems`。这两个最可能直接进入实验。
- Martyn & Kadziński, EJOR 2023, Deep preference learning for MCDA。需要全文核数据、baseline、指标。
- Omega 2025 non-monotonic MCS。需要全文核到底用了 red wine、stock/hotel 还是多组 real-world data，因为摘要入口存在差异。

优先级 2：

- Information Fusion 2026 attention network MCS。需要核 real-world datasets 名称和是否可得。
- EJOR 2025 incremental preference elicitation。需要核 credit rating / firm financial state rating 数据来源是否可公开复现。
- QS 2026 本地数据清洗：确认列、排名、缺失值、是否能和 2020/2022 形成跨年泛化。

## 7. 文献和数据入口

- Liu et al. (2020), INFORMS JOC, Data-driven preference learning with interacting criteria: [10.1287/ijoc.2020.0977](https://doi.org/10.1287/ijoc.2020.0977)
- INFORMS JOC research-unit-evaluation data: [GitHub](https://github.com/ijoc-data/download/tree/master/research-unit-evaluation)
- INFORMS JOC monotone-classification-problems data: [GitHub](https://github.com/ijoc-data/download/tree/master/monotone-classification-problems)
- Liu et al. (2020), EJOR, valued assignment examples: [10.1016/j.ejor.2020.04.013](https://doi.org/10.1016/j.ejor.2020.04.013)
- Liu et al. (2019), EJOR, non-monotonic criteria: [10.1016/j.ejor.2019.01.058](https://doi.org/10.1016/j.ejor.2019.01.058)
- Martyn & Kadziński (2023), EJOR, deep preference learning: [10.1016/j.ejor.2022.06.053](https://doi.org/10.1016/j.ejor.2022.06.053)
- Li et al. (2025), Omega, non-monotonic MCS: [10.1016/j.omega.2024.103219](https://doi.org/10.1016/j.omega.2024.103219)
- UCI Wine Quality dataset: [UCI](https://archive.ics.uci.edu/dataset/186/wine%2Bquality)
- Li et al. (2024/2025), incremental preference elicitation: [arXiv 2409.02760](https://arxiv.org/abs/2409.02760)
- Gao et al. (2026), Information Fusion, attention network MCS: [10.1016/j.inffus.2025.103443](https://doi.org/10.1016/j.inffus.2025.103443)
- QS World University Rankings methodology: [TopUniversities](https://www.topuniversities.com/world-university-rankings/methodology)
- Ru et al. (2026), dynamic/context-dependent preference learning: [10.1287/ijoc.2023.0372](https://doi.org/10.1287/ijoc.2023.0372), data/code [GitHub](https://github.com/INFORMSJoC/2023.0372)
