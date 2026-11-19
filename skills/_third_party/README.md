# 第三方开源 Skill 归属与整合说明

本目录保存经许可证核验的开源 Agent Skill 参考实现；原文件不替代仓库本地化 Skill。

## 来源与版本

- **Superpowers**：<https://github.com/obra/superpowers>
- 固定提交：`22f0b463e7a5e579904dd6211a520321035526f7`
- 许可证：MIT License，完整文本见 [`superpowers/LICENSE`](superpowers/LICENSE)

## 收录模块与本地整合

| 原模块 | 适配的市调大赛 Skill | 吸收原则 |
|---|---|---|
| `brainstorming/` | 选题、背景、框架、问卷、绘图 | 先明确受众、研究问题、口径、非目标和验收标准，再产出 |
| `writing-plans/` | 框架、问卷、分析、报告 | 把研究任务拆成可验证步骤，写清输入、输出、依赖、风险和检查点 |
| `systematic-debugging/` | 问卷、数据分析、绘图、报告 | 先复现问题、收集证据、定位机制，再做最小修复，避免猜改 |
| `verification-before-completion/` | 全部 9 个 Skill | 完成声明必须有新鲜证据：来源、数字、文件、渲染和引用逐项核验 |

仓库自有的绘图证据卡详见 [`../survey-chart-visualization/references/图表证据与验收.md`](../survey-chart-visualization/references/图表证据与验收.md)。

## 许可证边界

上述模块以参考副本形式保留，复制/分发时保留 MIT 版权和许可文本。仓库自己的 Skills 是本地化原创工作流，不声称第三方项目为官方市调大赛规则，也不把第三方文本或工具输出当成调查证据。
