# -*- coding: utf-8 -*-
"""
示例：市场调查报告常用图表代码（对照 SK5 的代码模板）
运行：python example_charts.py
依赖：matplotlib, numpy（可选 sklearn；本文件不强制）
输出：./output/*.png（300 dpi）
"""

import os
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

OUT = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(OUT, exist_ok=True)

mpl.rcParams.update({
    "font.sans-serif": ["SimHei", "Microsoft YaHei", "Noto Sans CJK SC"],
    "axes.unicode_minus": False,
    "figure.dpi": 120,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "font.size": 10,
    "axes.titlesize": 12,
    "axes.labelsize": 10,
    "legend.fontsize": 9,
    "figure.figsize": (6.4, 4.0),
})
PALETTE = ["#4C72B0", "#DD8452", "#55A868", "#C44E52", "#8172B3"]


def bar_chart():
    """单变量分布：样本性别构成（排序条形 + 数值标签）"""
    labels = ["男", "女"]
    vals = [812, 861]
    fig, ax = plt.subplots(figsize=(5.2, 3.6))
    bars = ax.bar(labels, vals, color=PALETTE[0], width=0.55)
    for b, v in zip(bars, vals):
        ax.annotate(f"{v}人\n({v/sum(vals):.1%})",
                    (b.get_x() + b.get_width() / 2, v),
                    ha="center", va="bottom", fontsize=9)
    ax.set_ylabel("人数（人）")
    ax.set_title("样本性别构成")
    ax.set_ylim(0, max(vals) * 1.15)
    ax.spines[["top", "right"]].set_visible(False)
    fig.savefig(os.path.join(OUT, "fig_01_gender.png"))
    plt.close(fig)


def radar_chart():
    """多指标画像：四类消费者雷达图"""
    dims = ["认知", "接受", "支付", "推广", "信任"]
    angles = np.linspace(0, 2 * np.pi, len(dims), endpoint=False).tolist()
    angles += angles[:1]
    groups = {
        "忠诚型": [4.2, 4.5, 3.9, 4.1, 4.3],
        "沉睡型": [3.1, 2.8, 2.5, 2.9, 3.0],
        "迷茫型": [2.2, 3.0, 2.1, 2.4, 2.6],
    }
    fig, ax = plt.subplots(figsize=(5.4, 5.0), subplot_kw=dict(polar=True))
    for i, (name, vals) in enumerate(groups.items()):
        v = list(vals) + [vals[0]]
        ax.plot(angles, v, "o-", lw=1.5, label=name, color=PALETTE[i])
        ax.fill(angles, v, alpha=0.08, color=PALETTE[i])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(dims)
    ax.set_ylim(0, 5)
    ax.set_title("四类消费者画像（均值，1–5 分）")
    ax.legend(loc="upper right", bbox_to_anchor=(1.28, 1.12))
    fig.savefig(os.path.join(OUT, "fig_02_radar.png"))
    plt.close(fig)


def cluster_scatter():
    """聚类可视化：二维簇散点（示意：可直接换成 t-SNE/PCA 坐标）"""
    rng = np.random.default_rng(42)
    centers = [(1, 1), (5, 5), (1, 5), (5, 1)]
    fig, ax = plt.subplots(figsize=(5.6, 4.4))
    for i, c in enumerate(centers):
        x = rng.normal(c[0], 0.6, 60)
        y = rng.normal(c[1], 0.6, 60)
        ax.scatter(x, y, s=14, alpha=0.75, label=f"类别{i+1}", color=PALETTE[i])
    ax.set_xlabel("维度 1")
    ax.set_ylabel("维度 2")
    ax.set_title("K-means 聚类结果（t-SNE 降维示意）")
    ax.legend(markerscale=1.5)
    fig.savefig(os.path.join(OUT, "fig_03_cluster.png"))
    plt.close(fig)


def forecast_line():
    """时序预测：实际值 + 预测值 + 预测区间"""
    years = np.array([2016, 2017, 2018, 2019, 2020, 2021, 2022])
    actual = np.array([5.0, 5.6, 6.3, 7.1, 8.0, 9.0, 10.1])
    pred_years = np.array([2021, 2022, 2023])
    pred = np.array([8.9, 10.0, 11.2])
    lower, upper = pred - 0.7, pred + 0.7
    fig, ax = plt.subplots(figsize=(6.4, 4.0))
    ax.plot(years, actual, "o-", color=PALETTE[0], label="实际值")
    ax.plot(pred_years, pred, "s--", color=PALETTE[1], label="预测值")
    ax.fill_between(pred_years, lower, upper, alpha=0.15, color=PALETTE[1])
    ax.set_xlabel("年份")
    ax.set_ylabel("面积（亿平方米）")
    ax.set_title("行业销售面积预测（GM(1,1) 示意）")
    ax.legend()
    ax.spines[["top", "right"]].set_visible(False)
    fig.savefig(os.path.join(OUT, "fig_04_forecast.png"))
    plt.close(fig)


def heatmap():
    """关联矩阵：灰色关联度热力图"""
    labels = ["人口", "均价", "收入", "面积"]
    mat = np.array([
        [1.00, 0.72, 0.81, 0.66],
        [0.72, 1.00, 0.58, 0.63],
        [0.81, 0.58, 1.00, 0.71],
        [0.66, 0.63, 0.71, 1.00],
    ])
    fig, ax = plt.subplots(figsize=(5.0, 4.2))
    im = ax.imshow(mat, cmap="RdBu_r", vmin=0.5, vmax=1.0)
    ax.set_xticks(range(len(labels)), labels)
    ax.set_yticks(range(len(labels)), labels)
    for i in range(len(labels)):
        for j in range(len(labels)):
            ax.text(j, i, f"{mat[i, j]:.2f}", ha="center", va="center", fontsize=9)
    fig.colorbar(im, ax=ax, label="关联度")
    ax.set_title("需求影响因素灰色关联度")
    fig.savefig(os.path.join(OUT, "fig_05_heatmap.png"))
    plt.close(fig)


if __name__ == "__main__":
    bar_chart()
    radar_chart()
    cluster_scatter()
    forecast_line()
    heatmap()
    print("已生成：", os.listdir(OUT))
