# 开源工具链总纲（Open Source Stack）

> **配套**：本仓库 `skills/` 下 8 个 SKILL 的**工具实现层**。每个 SKILL.md 的"开源工具链"一节指向这里；本文给安装命令、最小可运行代码、无 SPSS 团队的 GUI 替代方案。
>
> **立场**：开源工具由**团队自己跑数据、出图表**；脚本与工具版本请进附录，便于评审核验与复现。

## 一、环境与可复现

```bash
# Python（推荐 3.10+）
python -m venv .venv
.venv\Scripts\activate            # Windows
pip install pandas numpy scipy statsmodels scikit-learn factor_analyzer \
            pingouin semopy jieba snownlp gensim pyLDAvis wordcloud \
            matplotlib seaborn yellowbrick pyreadstat jupyter
pip freeze > requirements.txt     # 锁定版本，脚本进附录

# R（可选，抽样/复杂设计更全）
install.packages(c("sampling", "survey", "RDS", "psych", "lavaan", "semTools", "FactoMineR", "randomForest"))
```

## 二、分阶段工具矩阵

| 阶段 | 开源工具 | 用途 | 安装/入口 |
|---|---|---|---|
| 文献 | Zotero + Better BibTeX | 文献管理、GB/T 7714 条目导出 | zotero.org（免费） |
| 文献检索 | OpenAlex / Crossref API | 外文文献线索（开放数据） | `pip install openalex` 或网页 |
| 抽样 | Python `numpy.random` | PPS 随机落点、简单随机 | pip |
| 抽样 | R `sampling` / `RDS` | PPS/分层整套函数、受访者驱动抽样 | R CRAN |
| 复杂设计 | R `survey` | 设计效应、权重、复杂抽样置信区间 | R CRAN |
| 问卷平台 | LimeSurvey | 开源问卷部署（GPL） | limesurvey.org |
| 问卷平台 | KoboToolbox / ODK Collect | 公益/田野调查（含离线） | kobotoolbox.org |
| 信效度 | `factor_analyzer` | KMO、Bartlett、EFA 载荷 | pip |
| 信效度 | `pingouin` | Cronbach α、ICC | pip |
| SEM | `semopy`（Python）/ `lavaan`（R） | 结构方程、Bootstrap 中介 | pip / CRAN |
| 统计 | `scipy.stats` / `statsmodels` | 卡方、Friedman、ANOVA、Logit/有序/LNM | pip |
| 聚类 | `scikit-learn` | KMeans、CH/轮廓系数、t-SNE、随机森林 | pip |
| 选簇可视化 | `yellowbrick` | KElbowVisualizer（CH/肘部自动标） | pip |
| 文本 | `jieba` + `snownlp`/`cnsenti` | 分词、中文情感 | pip |
| 主题 | `gensim` + `pyLDAvis` | LDA 主题模型与交互可视化 | pip |
| 词云 | `wordcloud` | 词云（须指定中文字体） | pip |
| 图表 | `matplotlib`+`seaborn` / `plotly` | 统计图、交互图（静态导出 kaleido） | pip |
| 高级图型 | Apache ECharts | 桑基/水波/玫瑰/和弦（Web 导出） | echarts.apache.org |
| 网络图 | Gephi / draw.io | 共现网络、SEM 路径、SWOT 图 | gephi.org / draw.io |
| 报告 | `pandoc` + LaTeX / `quarto` / `typst` | Markdown 统一排版导出 | pandoc.org |
| Word | `python-docx` + LibreOffice | 套模板生成 docx、命令行转 PDF | pip / libreoffice.org |
| GUI 替代 SPSS | jamovi / JASP / GNU PSPP | 信效度、回归、方差（图形界面） | jamovi.org / jasp-stats.org |
| 甘特 | GanttProject | 进度图 | ganttproject.biz |
| 版本管理 | `git` | 每章一提交、可回滚 | git-scm.com |

## 三、最小可运行代码（对照 SK2–SK5 直接改）

### 1. 样本量计算（SK2）

```python
from math import ceil
z, pi, e, deff, rate = 1.96, 0.25, 0.05, 1.8, 0.90
n0 = z**2 * pi * (1 - pi) / e**2      # 288
n = ceil(n0 * deff)                   # 519
send = ceil(n / rate)                 # 577（报告按此上浮）
```

### 2. PPS 抽样落点（SK2）

```python
import numpy as np, pandas as pd
df = pd.DataFrame({"unit": ["熊口", "浩口", "龙湾"], "pop": [13127, 15654, 9011]})
df["cum"] = df["pop"].cumsum()
rng = np.random.default_rng(42)
for _ in range(5):                    # 抽 5 次，放回
    r = rng.integers(1, df["cum"].iloc[-1] + 1)
    hit = df[df["cum"] >= r].iloc[0]["unit"]
    print(r, "->", hit)
```

### 3. 信度 α 与 KMO/Bartlett（SK3）

```python
import pandas as pd, pingouin as pg
from factor_analyzer.factor_analyzer import calculate_kmo, calculate_bartlett_sphericity

items = df[[f"q{i}" for i in range(1, 8)]]     # 一个潜变量的题
alpha = pg.cronbach_alpha(data=items)[0]       # 目标 ≥0.7
kmo_all, kmo_model = calculate_kmo(items)      # kmo_model ≥0.6
chi2, p = calculate_bartlett_sphericity(items) # p <0.05
```

### 4. 卡方、Friedman、ANOVA（SK4-L2）

```python
from scipy import stats
chi2, p, dof, _ = stats.chi2_contingency(pd.crosstab(df["group"], df["buy"]))
chi2_f, p_f = stats.friedmanchisquare(*[df.loc[df["type"] == k, "score"] for k in sorted(df["type"].unique())])
f, p_a = stats.f_oneway(*[df.loc[df["g"] == k, "v"] for k in sorted(df["g"].unique())])
```

### 5. K-means + CH/轮廓系数选簇（SK4-L3）

```python
from sklearn.cluster import KMeans
from sklearn.metrics import calinski_harabasz_score, silhouette_score
X = df[["v1", "v2", "v3"]].values
for k in range(2, 7):
    m = KMeans(n_clusters=k, n_init=10, random_state=42).fit(X)
    print(k, round(calinski_harabasz_score(X, m.labels_), 1),
          round(silhouette_score(X, m.labels_), 3))   # CH 最大 + 轮廓系数结合定 k
```

### 6. Logistic / 有序 Probit / 无序多分类（SK4-L4）

```python
import statsmodels.api as sm
logit = sm.Logit(y_binary, sm.add_constant(X)).fit()      # 二元
ord = sm.OrdinalModel(y_ord, X, distr="probit").fit()     # 有序 Probit（statsmodels ≥0.14）
mnl = sm.MNLogit(y_multi, sm.add_constant(X)).fit()       # 无序多分类（消费者类型识别）
logit.summary()  # 系数/标准误/伪 R²；H-L 拟合优度可用 sklearn 分箱手算（Logistic 诊断）
```

### 7. SEM（SK4-L4，semopy）

```python
import semopy
model = """
PU =~ q1 + q2 + q3
PE =~ q4 + q5 + q6
INT =~ q7 + q8 + q9
INT ~ PU + PE
"""
sm_ = semopy.Model(model)
sm_.fit(df_subset)
print(semopy.inspect(sm_))          # 估计值/SE/p
print(semopy.calc_stats(sm_))       # RMSEA/CFI/TLI，对照 χ²/df<3 等阈值
```

### 8. Bootstrap 中介效应（SK4-L4）

```python
import pingouin as pg
pg.mediation_analysis(data=df, x="trust", m="peu", y="intention", seed=42)
# 输出含 a、b、c、c' 与 Bootstrap 95% CI（区间不含 0 = 中介显著）
```

### 9. LDA 主题 + pyLDAvis（SK4-L5）

```python
import jieba, pyLDAvis.gensim_models as vis
from gensim.corpora import Dictionary
from gensim.models import LdaModel
tokens = [jieba.lcut(t) for t in comments]
dic = Dictionary(tokens); corpus = [dic.doc2bow(t) for t in tokens]
lda = LdaModel(corpus, num_topics=4, id2word=dic, passes=10)
p = vis.prepare(lda, corpus, dic); pyLDAvis.save_html(p, "lda.html")
```

### 10. 中文情感（SK4-L5）

```python
from snownlp import SnowNLP
score = SnowNLP(comment).sentiments      # 0–1，>0.5 偏正面
```

### 11. IPA 重要度-满意度象限图（SK4-L4 / SK5）

```python
import matplotlib.pyplot as plt
plt.scatter(imp, sat, s=40)                # imp/sat 各为指标均值向量
plt.axhline(sat.mean(), color="gray", ls="--"); plt.axvline(imp.mean(), color="gray", ls="--")
for i, lab in enumerate(labels): plt.annotate(lab, (imp[i], sat[i]))
# 左上=重点改进，右下=维持现状（IPA 标准四象限）
```

### 12. GM(1,1) 灰色预测（SK4-L6，numpy 手写）

```python
import numpy as np
def gm11(x, n=3):
    x, acc = np.asarray(x, float), [float(x[0])]
    z = (np.cumsum(x)[:-1] + np.cumsum(x)[1:]) / 2
    B = np.column_stack([-z, np.ones(len(z))]); Y = x[1:]
    a, b = np.linalg.lstsq(B, Y, rcond=None)[0]
    for k in range(1, len(x) + n):
        x1 = (x[0] - b / a) * np.exp(-a * (k - 1)) + b / a
        acc.append(x1 - (x[0] - b / a) * np.exp(-a * (k - 2)) if k > 1 else x[0])
    return np.round(acc[len(x):], 2)       # 后 n 期预测
```

### 13. 词频条形 + 词云（SK5）

```python
import matplotlib.pyplot as plt
from collections import Counter
from wordcloud import WordCloud
cnt = Counter(jieba.lcut(full_text))[:20]
plt.bar(*zip(*cnt.items())); plt.xticks(rotation=45); plt.show()   # 主证据
wc = WordCloud(font_path=r"C:\Windows\Fonts\simhei.ttf", max_words=150,
               background_color="white", width=1200, height=800)
wc.generate_from_frequencies(dict(cnt)); wc.to_file("fig_wordcloud.png")  # 辅助
```

## 四、GUI 替代（无 SPSS 也能全流程）

| 环节 | 工具 | 说明 |
|---|---|---|
| 问卷 | LimeSurvey / KoboToolbox | 自建问卷、导出 CSV/SPSS、记录时长与 IP |
| 信效度/回归/方差 | jamovi、JASP、GNU PSPP | 开源图形界面；jamovi 有 SEM 模块（semlj） |
| SEM/CFA | JASP-SEM / R(lavaan) | 拟合指标齐全 |
| 抽样/复杂设计 | R(survey/sampling) | RStudio 开源桌面版 |
| 文献 | Zotero | 与 Word 插件联动引用 |
| 排版 | Pandoc/Quarto/Typst | Markdown → PDF/Word |

## 五、开源许可

- **许可**：numpy/pandas/matplotlib/scikit-learn 为 BSD，statsmodels 为 BSD，semopy/因子分析器为 MIT 系，LimeSurvey/PSPP/GanttProject 为 GPL，ECharts 为 Apache-2.0。商用与参赛均可，但须保留出处与许可声明习惯。
- **引用**：方法章节写明软件与版本（如"SEM 采用 Python semopy 2.x 拟合"），附录放脚本——这是评审"方法科学、过程可溯"的加分项。
- **数据规范**：原始数据脱敏后存 `data/`，脚本存 `code/`，图表存 `figures/`，报告引用相对路径；git 提交留痕。
- **可复现**：分析脚本进附录，注明运行环境、数据说明与工具版本。