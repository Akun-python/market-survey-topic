# 市调大赛结构方程模型模板：仅示范模型声明与报告字段，不含真实数据。
# 运行前：确认题项方向、缺失编码、样本量、理论路径和许可证/版本。
# install.packages("lavaan")
library(lavaan)

data <- read.csv("analysis_ready_demo.csv")

model <- '
  # 测量模型：每个反映性潜变量至少三个题项
  trust =~ trust1 + trust2 + trust3
  usefulness =~ useful1 + useful2 + useful3
  purchase =~ buy1 + buy2 + buy3

  # 结构模型：这是关联路径假设，不自动代表因果
  usefulness ~ a*trust
  purchase ~ b*usefulness + cprime*trust
  indirect := a*b
  total := cprime + (a*b)
'

fit <- sem(
  model, data=data, estimator="MLR", missing="fiml",
  se="bootstrap", bootstrap=5000, fixed.x=FALSE
)

# 交付前须报告：样本N、缺失/权重、估计器、版本、载荷、CR/AVE、区分效度，
# chisq/df、CFI、TLI、RMSEA及CI、SRMR、路径β/SE/p/95%CI、R²、间接效应CI。
summary(fit, standardized=TRUE, fit.measures=TRUE, rsquare=TRUE)
parameterEstimates(fit, standardized=TRUE, ci=TRUE)
fitMeasures(fit, c("chisq","df","cfi","tli","rmsea","srmr"))
