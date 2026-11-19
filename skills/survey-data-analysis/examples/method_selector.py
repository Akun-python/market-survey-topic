"""市调大赛数据分析方法选择演示：只提供候选及诊断，不运行真实分析。"""
from dataclasses import dataclass

@dataclass(frozen=True)
class Question:
    outcome: str  # continuous, binary, nominal, ordinal, count, text, time, none
    objective: str  # describe, compare, explain, predict, discover

    repeated: bool = False
    probability_sample: bool = False


def recommend(q: Question) -> tuple[str, str]:
    if q.outcome == "text":
        return "TF-IDF+人工编码/监督分类或LDA主题", "先核验采集权限、标注一致性、训练测试泄漏与错误案例"
    if q.outcome == "time":
        return "朴素季节基线+ETS/ARIMA", "按时间滚动回测，检查断点、MAE/RMSE与预测区间"
    if q.objective == "discover":
        return "PCA/聚类（K-means或混合型距离）", "缩放与k选择只在训练数据拟合，报告稳定性"
    if q.objective == "compare":
        if q.outcome == "continuous":
            return ("配对t或Wilcoxon" if q.repeated else "Welch t/ANOVA或秩检验", "报告分组N、效应量、区间与多重比较")
        return "χ²/Fisher或有序趋势检验", "核对期望频数、分母、效应量与区间"
    if q.objective == "explain" and q.outcome == "latent":
        return "理论模型→CFA→CB-SEM（lavaan/semopy）→Bootstrap中介/多组等值性", "先查载荷/CR/AVE/区分效度、拟合、Heywood和修模理论；横截面路径不自动等于因果"
    if q.outcome == "binary":
        return "Logistic回归", "检查分离、校准、OR及95%CI；关联不等于因果"
    if q.outcome == "ordinal":
        return "有序Logit/Probit", "检查比例优势假设、基准类别与边际效应"
    if q.outcome == "count":
        return "Poisson或负二项回归", "检查过度离散、零膨胀与暴露量offset"
    if q.outcome == "continuous":
        return "OLS/稳健回归", "检查异方差、共线性、影响点与效应区间"
    return "描述统计与数据质量审查", "先定估计对象、分母、抽样设计与缺失规则"


if __name__ == "__main__":
    for q in [Question("text", "discover"), Question("latent", "explain"), Question("binary", "explain"), Question("time", "predict")]: 
        print(q, "=>", recommend(q))
