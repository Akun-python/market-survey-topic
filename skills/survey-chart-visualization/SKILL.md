---
name: survey-chart-visualization
title: 绘图（图表可视化）规范
description: 用于为市场调查报告制作规范图表——按数据形态选择图型、中文字体与统一色板、Python 代码模板（条形/雷达/t-SNE/预测/词云/热力图）、图题表题与来源注、编号与图表清单管理。
layer: 贯穿层（分析→报告）
rubric: [报告文本 15, 分析与结论 25]
depends_on: [survey-data-analysis]
feeds: [survey-report-writing]
---

# SK5 绘图规范：让图表成为"证据"而不是"装饰"

> **一句话**：每张图只讲一件事；图的使命是「**替文字说话**」——评委扫一眼就知道你想让他看到什么、数据从哪来、是否可信。

## 一、定位与适用场景

- **用在报告哪里**：全文图表（描述统计、差异对比、画像、模型结果、舆情、预测）。
- **用在什么阶段**：SK4 每产出一组结果即可出图，贯穿分析与报告写作。
- **不适用**：数据尚未清洗/口径未定 —— 先定口径再画图，避免返工。

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