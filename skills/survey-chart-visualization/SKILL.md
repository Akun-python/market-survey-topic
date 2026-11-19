---
name: survey-chart-visualization
title: 绘图（图表可视化）规范
description: 用于为市场调查报告制作规范图表——按数据形态选择图型、中文字体与统一色板、Python 代码模板（条形/雷达/t-SNE/预测/词云/热力图）、图题表题与来源注、编号与图表清单管理。
layer: 贯穿层（分析→报告）
rubric: [报告文本 20, 数据分析与结论 30]
depends_on: [survey-data-analysis]
feeds: [survey-report-writing]
---

# SK5 绘图规范：让图表成为"证据"而不是"装饰"

> **本版整合说明**：本 Skill 吸收 MIT 许可的 Superpowers `brainstorming` 与 `verification-before-completion` 的工作原则，但不复制其正文。前者对应“先明确图表使命与受众，再选择图型”；后者对应“提交前以新鲜命令验证图表、来源、字体、分辨率与引用”。原始参考实现和许可证见 [`../_third_party/README.md`](../_third_party/README.md)。

> **一句话**：每张图只讲一件事；图的使命是「**替文字说话**」——评委扫一眼就知道你想让他看到什么、数据从哪来、是否可信。

## 一、定位与适用场景

- **用在报告哪里**：全文图表（描述统计、差异对比、画像、模型结果、舆情、预测）。
- **用在什么阶段**：SK4 每产出一组结果即可出图，贯穿分析与报告写作。
- **不适用**：数据尚未清洗/口径未定 —— 先定口径再画图，避免返工。

## 一点五、开画前的图表设计卡（先想清楚，再写代码）

每张图先填写以下六项；缺一项时先回到问卷/分析口径，不直接开画：

| 项目 | 必填内容 |
|---|---|
| 观众与决策 | 谁看图、看完要做什么决策 |
| 一句话主张 | 这张图只证明一个什么问题（不得写成结论性因果，除非有相应设计） |
| 数据口径 | 分母、加权、缺失值、时间窗、分组基数 |
| 图型理由 | 为什么这种图比替代图更适合；明确不采用何种误导性图型 |
| 证据边界 | 描述/差异/关联/因果/预测能支持到哪一级 |
| 来源与版本 | 问卷题号、数据文件、提取日期、处理脚本或表格位置 |

设计卡应先进入图表清单，主张、口径和证据边界发生变化时重新审阅；不要为了“好看”调整数据比例、截断坐标轴或把关联改写为因果。

## 二、输入清单

| 输入 | 具体要求 |
|---|---|
| 分析结果 | 频数/均值/系数/聚类中心/时间序列（结构化表或 DataFrame） |
| 图表清单 | 先列"图 1–图 N 要讲什么"，再逐张实现 |
| 中文字体 | 本机可用：`SimHei` / `Microsoft YaHei`（Windows）或 `Noto Sans CJK SC` |
| 配色约定 | 全报告 ≤5 色（建议莫兰迪/色盲友好色板，如 `viridis`、`Okabe-Ito`） |

## 三、标准步骤

### 第 1 步｜先定"图表清单"，再写代码
按章节列出：`图/表编号 → 讲什么 → 数据来源 → 对应结论`。没有归属的图不画。

### 第 2 步｜选对图（按数据形态）

| 数据形态 / 目的 | 推荐 | 慎用/禁用 |
|---|---|---|
| 单类别占比（构成） | 排序条形图、环形图 | 3D 饼图、饼图 >6 类 |
| 等级/有序分布 | 百分比堆叠条形图 | 饼图 |
| 连续变量分布 | 直方图 + 箱线图 | 柱状图硬套 |
| 两组以上均值比较 | 分组条形图、箱线图、误差棒 | 无误差信息的裸均值 |
| 多指标画像 | 雷达图（3–8 维） | 雷达图维度 >10 |
| 两连续变量关系 | 散点图 + 拟合线 | 折线（x 非时序时） |
| 聚类结果 | PCA/t-SNE 散点（按簇着色） | 强制二维原始变量散点 |
| 时序趋势/预测 | 折线 + 预测区间（阴影） | 双 Y 轴滥用 |
| 文本高频词 | 词频条形图（主）+ 词云（辅） | 只有词云无统计 |
| 区域差异 | 分级设色地图（choropleth） | 地图无图例 |
| 指标关联矩阵 | 热力图、桑基图 | 3D 柱状 |
| 流程/路径类（用户旅程、转化） | 桑基图（多层级流向） | 无标注的复杂流向图 |
| 单指标对比层级 | 水波图、玫瑰图（等角度变半径） | 3D 饼图 |
| 满意度优先改进 | IPA 象限散点图（重要度 × 满意度） | 无线阈值线的裸散点 |

### 第 3 步｜统一视觉规范（全报告一套）

```python
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.rcParams.update({
    "font.sans-serif": ["SimHei", "Microsoft YaHei", "Noto Sans CJK SC"],
    "axes.unicode_minus": False,      # 负号显示
    "figure.dpi": 120,                # 屏幕
    "savefig.dpi": 300,               # 导出
    "savefig.bbox": "tight",
    "font.size": 10,
    "axes.titlesize": 12,
    "axes.labelsize": 10,
    "legend.fontsize": 9,
    "figure.figsize": (6.4, 4.0),
})

PALETTE = ["#4C72B0", "#DD8452", "#55A868", "#C44E52", "#8172B3"]  # ≤5 色
```

- **图题在图下**、**表题在表上**（中文期刊与大赛惯例，三篇报告均如此）；
- 图/表内文字不倾斜、不旋转（除非坐标轴标签）；
- 数据来源注：图下 `数据来源：×××（年份）` 或 `注：……`；
- 导出 PNG（300 dpi）+ PDF（矢量）各一份，Word 引用 PNG。

### 第 4 步｜常用图代码模板

**① 条形图（带数值标签，最常见的描述统计图）**

```python
vals = [...]; labels = [...]
fig, ax = plt.subplots(figsize=(7, 3.8))
bars = ax.bar(labels, vals, color=PALETTE[0], width=0.6)
for b, v in zip(bars, vals):
    ax.annotate(f"{v}", (b.get_x() + b.get_width()/2, v), ha="center", va="bottom", fontsize=9)
ax.set_ylabel("人数（人）"); ax.set_title("样本性别构成")
for s in ("top", "right"):          # 兼容旧版 matplotlib，勿用 spines[[...]]
    ax.spines[s].set_visible(False)
plt.savefig("fig_01_gender.png", dpi=300); plt.close()
```

**② 雷达图（用户画像）**

```python
import numpy as np
dims = ["认知", "接受", "支付", "推广", "信任"]
angles = np.linspace(0, 2*np.pi, len(dims), endpoint=False).tolist()
angles += angles[:1]
fig, ax = plt.subplots(figsize=(5, 5), subplot_kw=dict(polar=True))
for i, (name, vals) in enumerate(groups.items()):
    v = list(vals) + [vals[0]]
    ax.plot(angles, v, label=name, color=PALETTE[i]); ax.fill(angles, v, alpha=0.08)
ax.set_xticks(angles[:-1]); ax.set_xticklabels(dims)
ax.legend(loc="upper right", bbox_to_anchor=(1.25, 1.1))
plt.savefig("fig_03_radar.png", dpi=300); plt.close()
```

**③ t-SNE / PCA 聚类散点图**

```python
from sklearn.manifold import TSNE
xy = TSNE(random_state=42).fit_transform(X_scaled)
for k in sorted(set(labels)):
    m = labels == k
    plt.scatter(xy[m, 0], xy[m, 1], s=12, alpha=0.7, label=f"类别{k+1}", color=PALETTE[k])
plt.xlabel("t-SNE 维度 1"); plt.ylabel("t-SNE 维度 2"); plt.legend()
plt.savefig("fig_05_tsne.png", dpi=300); plt.close()
```

**④ 折线 + 预测区间（GM(1,1)/回归对比）**

```python
ax.plot(years, actual, "o-", color=PALETTE[0], label="实际值")
ax.plot(years_pred, pred, "s--", color=PALETTE[1], label="预测值")
ax.fill_between(years_pred, lower, upper, alpha=0.15, color=PALETTE[1])
ax.set_xlabel("年份"); ax.set_ylabel("面积（亿平方米）"); ax.legend()
plt.savefig("fig_06_forecast.png", dpi=300); plt.close()
```

**⑤ 词云（仅作辅助，必须配词频条形图）**

```python
from wordcloud import WordCloud
wc = WordCloud(font_path=r"C:\Windows\Fonts\simhei.ttf",   # Linux/macOS 用 Noto Sans CJK 路径
               background_color="white", width=1200, height=800,
               max_words=150, colormap="viridis")
wc.generate_from_frequencies(freq_dict)
wc.to_file("fig_07_wordcloud.png")
```

**⑥ 热力图（灰色关联度矩阵、交叉关注）**

```python
import seaborn as sns
sns.heatmap(mat, annot=True, fmt=".2f", cmap="RdBu_r", cbar_kws={"label": "相关系数"})
plt.tight_layout(); plt.savefig("fig_04_heatmap.png", dpi=300); plt.close()
```

**⑦ SEM 路径图**：matplotlib 画路径成本高，优先用 **draw.io / PowerPoint / yEd** 画矢量图，再导出 PNG；图上标注路径系数（含显著性星号）。

### 第 5 步｜图注写法（评委视线停留处）

每图配 **2–3 句**解读：**展示什么 → 关键对比/异常 → 对研究结论的含义**，不重复图题。

> 示例："图 5 显示，受访者的认知集中在'一知半解'，占比 41.2%；与'基本不了解'合计超过六成，说明概念普及仍停留在浅层，为后文宣传策略提供依据。"

### 第 6 步｜编号与目录

- 图 1、图 2……（全文连续）或 图 3-1（按章）——二选一，全文统一；
- 正文先引后现："如图 5 所示"——不要让图先出现再解释；
- 图目录/表目录与正文编号严格一致（评审会核对）。

## 四、产出模板

**图表清单表**（开工前填）：

| 编号 | 类型 | 讲什么 | 数据来源 | 对应结论 | 章节 |
|---|---|---|---|---|---|
| 图 1 | 条形图 | 样本性别构成 | 问卷 Q1 | — | 5.1 |

**导出规范**：`fig_0x_主题.png`（300 dpi）放入 `figures/`，与 `.md` 引用路径一致。

## 五、验收标准（逐条打勾）

- [ ] 每张图有明确使命，且至少有一句正文引用它
- [ ] 图题在图下、表题在表上；图注 2–3 句
- [ ] 全部图有来源注（数据来源/注）
- [ ] 配色 ≤5 色、色板统一；无 3D 饼图、无滥用双 Y 轴
- [ ] 字号在导出图内 ≥8 pt；中文字无乱码、负号正常
- [ ] 导出 ≥300 dpi PNG（+ 矢量 PDF 更佳）
- [ ] 编号连续、图目与正文一致
- [ ] 坐标轴有单位、图例清晰、数据标签不重叠

## 五点五、完成前的证据验证门（必须实际运行）

完成声明前，不凭肉眼或“代码执行成功”直接宣称合格。对本次交付的实际图表重新执行核验并保留记录：

1. **数据检查**：数值与清洗后的分析表逐项比对；比例核对分母/权重、百分比合计与四舍五入误差；误差线注明标准差、标准误或置信区间，不可互换。
2. **文件检查**：确认 PNG 可读、尺寸与 `dpi` 元数据符合要求；PDF 若导出，确认文件存在且可打开。演示数据文件名/图注显式带“示例”，严禁冒充调查成果。
3. **字体检查**：抽看中文、负号、图例、超长标签和图边缘，不得出现方框、裁切、覆盖；PDF 文本提取失败时以渲染图复核。
4. **报告映射**：每张图均能在正文找到首次引用、图号、图题、来源、口径说明和对应结论；文件名与图表清单一致。
5. **失败处理**：任一项失败即记录问题与修复动作，重跑同一验证；没有全量通过结果不得写“已完成”。

可执行的本仓库示例验证命令：`python skills/survey-chart-visualization/examples/example_charts.py`；统计图验收细则见 [`references/图表证据与验收.md`](references/图表证据与验收.md)。

## 六、报告呈现要求

- 分析章图表密度：**每 1–2 页 1 张图表**，全报告 30–50 张为宜（过多 → 像 PPT；过少 → 无证据）；
- 关键结论必须有图（如聚类画像雷达图、SEM 路径图、预测对比图）；
- 词云仅作辅助；正文提及数字时与图一致。

## 七、常见坑

1. **Excel 默认样式直接贴**（灰底粗边、倾斜标签）→ 一眼业余。
2. **彩虹配色**（bar 每根不同色）→ 色盲不友好且无意义。
3. **3D 饼图/3D 柱**：面积失真，评审反感。
4. **图无来源**：图表数据无法追溯。
5. **词云当主证据**：只有云没有数。
6. **中文乱码/负号变成方块**：忘设字体。
7. **图注只写"如图"**：等于浪费最有说服力的版面。
8. **编号跳号**（图 4 后直接图 6）→ 目录对不上。
9. **双变量散点硬连线**（x 非时间）→ 误导。

## 八、开源工具链（完整命令见 `OPEN_SOURCE_STACK.md`）

- **主绘图**：`matplotlib` + `seaborn`（统计图）；`plotly`（交互，静态导出用 kaleido）；
- **高级图型**：Apache `ECharts`（开源的桑基图/水波图/玫瑰图/和弦图，Web 端导出 PNG/SVG）；
- **网络/路径**：Gephi（共现网络）、draw.io（SEM 路径图、SWOT 矩阵）、Inkscape（矢量后期）；
- **聚类选簇**：`yellowbrick` KElbowVisualizer（自动标注 CH 曲线与肘部）；
- **主题可视化**：`gensim` + `pyLDAvis`（LDA 交互页）；
- **词云**：`wordcloud`（务必指定系统中文字体路径：Windows `C:\Windows\Fonts\simhei.ttf`，Linux/macOS 用 Noto Sans CJK）；
- **论文风样式**：`SciencePlots`（pip install SciencePlots）配合中文 rcParams；
- **输出**：统一导出 300 dpi PNG + 矢量 PDF，`figures/` 目录 + 相对路径引用。

## 九、写法要点（对照历届获奖作品自检）

高分作品的图表通常具备以下特征：

1. 每张图有明确使命，正文先引后现，图注 2–3 句解读（不只写"如图"）；
2. 图型匹配数据形态：占比用排序条形/环形、画像用雷达、聚类用 t-SNE 散点、预测用折线+阴影区间、文本用词频条形（词云仅辅助）；
3. 进阶图型可选：桑基图（流程）、水波/玫瑰图（单指标对比）、IPA 象限图（满意度改进）、成分载荷图、轮廓系数选簇图；
4. 统一色板 ≤5 色、中文字体与负号正常、≥300 dpi 导出（另存矢量 PDF）；
5. 图题在图下、表题在表上、来源注齐全，编号与图目/表目严格一致；
6. 全报告图表密度约每 1–2 页 1 张，关键结论必有图支撑。

> 历届获奖作品可从大赛官方渠道自行获取对照；本 skill 不附带、不显示具体作品。

## 十、Word 文件交付（必做）

每次完成本 Skill，必须生成 `研究题目_图表报告.docx`，按报告章节顺序内嵌实际图表，并为每张图表提供编号、图/表题、数据来源、口径注释、2–3 句发现解读和对应研究结论。图源 PNG（≥300 dpi）与矢量 PDF 可另附，但不能用素材目录或 Markdown 代替 Word 成果。图表未有真实数据时交付标注为演示的样式样稿，不伪称实证结果。依 `../WORD_DELIVERY.md` 检查清晰度、分页、图注和来源。

## 开源工作流整合（MIT 参考）

本 Skill 结合 MIT 许可 Superpowers 的 `brainstorming`、`writing-plans`、`systematic-debugging` 与 `verification-before-completion` 方法参考（原始副本和归属见 [`../_third_party/README.md`](../_third_party/README.md)）。以下原则已按本阶段本地化，不替代当届官方赛制：

- **图表设计与验收工作流**：先填写图表设计卡，明确受众、一句话主张、分母、图型理由和证据边界；生成后重新核验数据、字体、来源、尺寸、图号和正文映射。完整细则见本目录 references/图表证据与验收.md。
- **完成证据**：交付前保留来源/版本、输入输出文件、运行命令或审校记录；任何“完成/有效/显著/代表性”表述都要有可复查证据。
- **失败处理**：若检查失败，记录复现步骤、最小修复和复测结果；不得只依赖代理或作者口头确认。

## 科研严谨性补充：图表不可越过数据边界

- 图表清楚标注估计量、分母、权重、缺失处理、误差线含义、样本量和调查时期；小样本或不稳定估计不能用视觉精度掩盖。
- 坐标轴、零点、排序和颜色规则须在比较图中保持一致；截轴、面积编码、双轴和地图分级需在图注说明理由并做误导风险检查。
- 统计显著不等于实质重要；图下解读同时写方向、效应大小和不确定性，不能用“明显/显著”替代数字。


## 市调大赛比赛格式与评分对接

本 Skill 的最终成果须同时符合 [`../COMPETITION_REPORT_STANDARD.md`](../COMPETITION_REPORT_STANDARD.md) 与当届官方附件；该文件按第17届本科组整理，届次变化时重新核对。交付前把本阶段产出填入“评分证据链”：对应评分板块、报告位置、数据/文献/实施证据、局限和待核验项。

- **报告格式**：正文与附录分开；正文包含标题页、摘要页、目录页和正文；最终PDF正文页数、匿名、地图、查重、AI附录等按当届通知验收。
- **证据纪律**：不把模拟/占位/未核验数字作为实证结果；每个结论、图表、引用和建议都有可回链来源。
