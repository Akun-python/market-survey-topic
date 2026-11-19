#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""生成 2027 年企业命题的总 README 与各企业 README。"""
import json
from collections import OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = ROOT / "2027年企业命题"
GEN = ROOT / "_gen"

COMPANIES = [
    ("E01", "益普索", "🥇", "blueviolet"),
    ("E02", "问卷网", "📋", "blue"),
    ("E03", "同方知网", "📚", "green"),
    ("E04", "格远数智赋能", "🧑‍🎓", "orange"),
    ("E05", "汇辽集团", "🏗️", "brown"),
    ("E06", "酷冷保温", "❄️", "cyan"),
    ("E07", "神启数据", "📊", "purple"),
    ("E08", "中健国康", "😴", "teal"),
]

INFO = {
    "E01": {
        "intro": "益普索（Ipsos）为本届企业命题方之一，共发布 5 个命题，覆盖快消产品创新、爆款研究、银发营养、AI 短剧与 AI 问答媒介研究。选题须落到具体品类、具体人群与具体决策环节，产出可直接支撑品牌与平台决策的数据。",
        "rules": [
            "命题 1｜产品创新与品牌定位：大学生智能手表购买过程、使用习惯与评价、品牌态度、理想功能与营销方案设计；城市限北京、上海、武汉，渠道聚焦线上电商，对标苹果/华为/小米。",
            "命题 2｜爆款研究：从销量与社媒角度定义爆款，提炼品类趋势、竞争机会、渠道与沟通策略；品类自选（食品、饮料、小家电、化妆品等），单题建议只做一个品类。",
            "命题 3｜银发营养与主食健康化：中老年人群细分（活力自理/半失能/失能失智）、主食健康化场景（控糖、控脂、吞咽困难、易烹易食）、益海嘉里产品线覆盖与空白、子女代购与适老包装。",
            "命题 4｜AI 短剧 U&A：知晓率、观看率与频率时长、场景与平台、题材偏好、与真人短剧的迁移、AI 生成在意程度、商业模式接受度（广告解锁、品牌定制、电商带货、付费订阅、周边）、1–3 年趋势。",
            "命题 5｜媒介研究·AI 问答：AI 搜索使用行为、对 AI 答案的信任与影响因素、品牌被 AI 提及/推荐对认知与购买意愿的影响、AI 推荐与 KOL/广告的说服力对比、商业内容边界与 GEO 策略。",
        ],
    },
    "E02": {
        "intro": "问卷网命题聚焦“AI 如何改变市场研究并为企业创造价值”，研究对象为用研者（高校、企业、事业单位的市场研究/用户研究从业者），鼓励混合研究方法并建议研究者自身走查全流程。",
        "rules": [
            "研究设计变化：自主设计 vs AI 设计、问卷与指标生成质量、抽样与配额建议。",
            "研究对象与研究方式变化：数字人受访者、AI 主持/访谈、焦点小组的 AI 化。",
            "信息模式变化：问卷 + VOC（舆情/用户声音）+ 多模态（文字/声音/图片/视频）。",
            "研究成果变化：AI 分析报告的可信度、洞察深度、决策采纳率。",
            "采纳与治理：用研者的信任、组织采纳障碍、数据安全、AI 使用披露与伦理。",
        ],
    },
    "E03": {
        "intro": "同方知网命题为“数智中国：经济社会关键维度测度与实地调查研究”，属统计数据分析类，鼓励使用中国经济社会大数据研究平台、AI 知数、CNKI AI、AI Pat+ 与产业通等工具，将宏观测度与实地调查结合。",
        "rules": [
            "大语言模型统计数据问答准确性测评（宏观经济指标幻觉率）。",
            "AI 赋能社会科学研究的嵌入度测度与高校科研人员使用现状。",
            "人工智能对岗位结构的影响测度与青年就业者职业适应。",
            "数智消费新图景：消费数字化统计测度与 Z 世代“智能+”消费。",
            "银发浪潮遇上 AI：老龄化现状与智慧养老服务需求。",
            "生育支持政策强度的省际测度与育龄青年生育意愿。",
            "省域共同富裕水平测度与低收入家庭增收路径。",
            "县域经济高质量发展水平测度与特色产业带动效应。",
            "产业链专利布局与技术竞争态势（AI Pat+ 数据）。",
            "自主拟定题目（可落到具体省、市、县）。",
        ],
    },
    "E04": {
        "intro": "格远数智赋能命题为“青年发展主题调查”，下设青年心理健康、青年就业创业、青年人工智能应用与数字素养三个子选题，要求衔接“十五五”规划支持青年发展专节、国发〔2025〕11 号“人工智能+”行动与国卫医政发〔2026〕8 号社会心理服务体系方案，按“本地前期研究—全国统一采集—数据深化应用”三阶段推进。",
        "rules": [
            "子选题①青年心理健康：压力新表现、服务可及性与使用成效、供需适配判断。",
            "子选题②青年就业创业：灵活就业与慢就业新形态、支持政策落地成效、青年获得感。",
            "子选题③青年 AI 应用与数字素养：素养水平测度、能力结构短板、提升支持体系适配。",
            "数据口径：优先参与“全国一张卷”统一问卷，保证跨省可比；可先做本省基线预调研。",
            "成果导向：形成可报送团中央及省市有关单位的调研报告与分项判断。",
        ],
    },
    "E05": {
        "intro": "汇辽集团（安徽汇辽新型装饰材料有限公司）命题聚焦装配式住宅的国内外市场发展阶段与具体需求，企业立足长三角、辐射全国并逐步打开海外市场。选题须回答“装配式住宅是否成为主流趋势、需求群体与产品类型是什么、企业如何应对”。",
        "rules": [
            "发展阶段与趋势：国内外装配式住宅的政策推进节奏、渗透率与主流技术体系。",
            "需求群体：房企、施工总包、设计院、政府/园区、家装与自建房农户的差异化需求。",
            "产品类型：预制混凝土构件、钢结构、模块化建筑及围护材料的选型偏好。",
            "海外市场：东南亚、中东、欧洲、北美等区域的准入标准、认证与渠道模式。",
            "企业应对：成本、供应链、运维与本地化生产布局建议。",
        ],
    },
    "E06": {
        "intro": "酷冷保温命题为“产品终端用户体验洞察与口碑转化路径研究”，产品为金属面聚氨酯夹芯板、金属面聚氨酯冷库门、金属面岩棉夹芯板，服务冷链冷库围护系统，重点回答新兴场景空间、海外区域标准、满意度与口碑、原材料成本、采产销存数据五个问题。",
        "rules": [
            "国内新兴场景：医药冷链、预制菜加工、生鲜中转仓、特种恒温库、粮库、储能温控仓等。",
            "海外区域差异：防火等级、保温指标、板型结构、认证要求、交付模式。",
            "终端满意度：保温性能、板面平整度、封边气密性、交付周期、技术支持、资料报审、售后响应。",
            "成本与采购：黑白料、彩钢卷、岩棉、包边型材的价格波动与锁价、替代、库存策略。",
            "采产销存数据：信息断点诊断、岗位数据需求与数字化建设优先级。",
        ],
    },
    "E07": {
        "intro": "神启数据命题聚焦 AI 调研工具的“买方”——中小微企业与个体经营者，研究其市场信息获取困境及对 AI 问卷、AI 访谈机器人、AI 数据分析报告的认知、需求与付费意愿，要求数据能落到具体价格区间与人群差异。",
        "rules": [
            "现状与痛点：信息渠道、成本、频次、满意度，验证“做不起、不会做、找不到人”真伪。",
            "认知与信任：是否知道 AI 能做调研、对 AI 访谈与分析的信任边界。",
            "付费意愿：按次、订阅、按报告三种计费方式的心理价位与预算归属。",
            "决策路径：谁决策、通过什么渠道触达、什么话术有效。",
            "客群差异：中小微企业主与个体经营者、不同行业与区域的需求差异。",
        ],
    },
    "E08": {
        "intro": "中健国康命题围绕健康睡眠产品（DeepZi 智能助眠家纺）与搜搜商盟电商平台，发布睡眠产品消费行为、DeepZi 品牌健康度、平台品牌影响力与渠道体验、内容电商转化优化 4 个选题，关注都市白领、Z 世代、银发家庭的睡眠痛点差异与“种草—体验—转化—复购”链路。",
        "rules": [
            "选题①睡眠产品消费行为与购买意愿：痛点分层、决策要素、价格敏感度、线下睡眠馆体验、复购与推荐。",
            "选题②DeepZi 品牌健康度：认知与联想、品牌升级迁移、科技信任与溢价、竞品区隔。",
            "选题③搜搜商盟平台品牌影响力与渠道体验：平台认知、商户入驻、线上线下联动、获客成本。",
            "选题④内容电商转化与营销优化：种草—转化—复购链路、详情页数据可视化、直播话术、退货与信任机制。",
        ],
    },
}


def load(code):
    p = GEN / f"{code}.json"
    return json.loads(p.read_text(encoding="utf-8-sig")) if p.exists() else []


def company_readme(code, name, icon, color):
    rows = load(code)
    buckets = OrderedDict()
    for r in rows:
        buckets.setdefault(r["company_bucket"], []).append(r)
    lines = []
    lines.append(f'<p align="center">')
    lines.append(f'  <img src="https://img.shields.io/badge/{code}_{name}-{icon}-{color}?style=for-the-badge" alt="{code}_{name}"/>')
    lines.append(f'  <img src="https://img.shields.io/badge/选题数-{len(rows)}-success?style=for-the-badge" alt="{len(rows)}题"/>')
    lines.append(f'  <img src="https://img.shields.io/badge/企业命题-第17届-blue?style=for-the-badge" alt="第17届"/>')
    lines.append(f'</p>')
    lines.append("")
    lines.append(f"# {icon} {code}_{name}")
    lines.append("")
    lines.append(f"> 📌 选题档案：{len(rows)} 题，对应 {name} 第 17 届企业命题原文（`references/第十七届赛制资料/附加1：企业命题.xlsx`）。")
    lines.append(f"> 每个选题目录内含 `选题说明.pdf` 与 `_topic.txt` 速览；DOCX 和水印 PDF 不在本目录保留。")
    lines.append("")
    lines.append("## 一、命题要求摘要")
    lines.append("")
    lines.append(INFO[code]["intro"])
    lines.append("")
    for rule in INFO[code]["rules"]:
        lines.append(f"- {rule}")
    lines.append("")
    lines.append("## 二、选题清单")
    lines.append("")
    lines.append("| 编号 | 选题 | 命题子方向 |")
    lines.append("|---|---|---|")
    for r in rows:
        lines.append(f"| **{r['id']}** | [{r['full_title']}](<{r['id']}_{r['full_title']}>) | {r['company_bucket']} |")
    lines.append("")
    lines.append("## 三、命题覆盖度")
    lines.append("")
    lines.append("| 命题子方向 | 题数 | 编号 |")
    lines.append("|---|---:|---|")
    for bucket, items in buckets.items():
        ids = "、".join(x["id"].replace(code + "-", "") for x in items)
        lines.append(f"| {bucket} | {len(items)} | {ids} |")
    lines.append("")
    lines.append("## 四、使用说明")
    lines.append("")
    lines.append("- 编号规则：`" + code + "-NN`，与企业命题原文的子方向一一对应；目录名 = 编号 + 全标题。")
    lines.append("- 选题目录内 `_topic.txt` 为速览版（对象/变量/假设/可行性/来源），`选题说明.pdf` 供选题审阅；参赛须另行完成正式调研报告。")
    lines.append("- 参赛前须按官方附件 3 排版、附件 5 附 AI 使用说明，报告正文不超过 65 页，且任何一页不得出现学校与指导教师信息。")
    lines.append("- 企业命题赛提交截止：2027-03-29 12:00（每校最多 3 份，须附附件 2 参赛承诺书）。")
    lines.append("")
    lines.append("> 证据核验提示：档案中的 ✅ 为官方/权威来源，🔶 为行业报告或媒体线索，参赛前须下载原文核对；具体数据以官方最新发布为准。")
    return "\n".join(lines) + "\n"


def root_readme(codes):
    total = 0
    stats = []
    for code, name, icon, color in COMPANIES:
        if code not in codes:
            continue
        rows = load(code)
        total += len(rows)
        stats.append((code, name, icon, color, len(rows)))

    lines = []
    lines.append('<p align="center">')
    lines.append('  <img src="https://img.shields.io/badge/2027年企业命题-8家企业-blueviolet?style=for-the-badge" alt="2027年企业命题"/>')
    lines.append(f'  <img src="https://img.shields.io/badge/选题总数-{total}-success?style=for-the-badge" alt="{total}题"/>')
    lines.append('  <img src="https://img.shields.io/badge/第17届-企业命题赛-orange?style=for-the-badge" alt="第17届"/>')
    lines.append('</p>')
    lines.append("")
    lines.append("# 🏭 2027 年企业命题选题库（第 17 届企业命题赛）")
    lines.append("")
    lines.append(f"> 依据 `references/第十七届赛制资料/附加1：企业命题.xlsx` 的 8 家企业命题原文，逐企业拆解为可直接参赛的选题，共 **{total}** 题。")
    lines.append("> 每题一个目录，仅保留 `选题说明.pdf` 与 `_topic.txt` 速览；选题风格与 `正大杯最新选题/` 既有题库一致（一个题目两个研究点、五段式档案）。")
    lines.append("")
    lines.append("## 一、企业目录")
    lines.append("")
    lines.append("| 编号 | 企业 | 选题数 | 命题方向 | 入口 |")
    lines.append("|---|---|---:|---|---|")
    direction = {
        "E01": "快消产品创新 / 爆款 / 银发营养 / AI 短剧 / AI 问答",
        "E02": "AI 如何改变市场研究（面向用研者）",
        "E03": "数智中国：经济社会关键维度测度",
        "E04": "青年发展（心理 / 就业创业 / AI 素养）",
        "E05": "装配式住宅国内外市场需求",
        "E06": "冷链围护系统终端体验与口碑",
        "E07": "中小微企业 AI 调研工具付费意愿",
        "E08": "健康睡眠产品与电商平台转化",
    }
    for code, name, icon, color, n in stats:
        lines.append(f"| {code} | {icon} **{name}** | {n} | {direction[code]} | [{code}_{name}](<{code}_{name}/README.md>) |")
    lines.append("")
    lines.append("## 二、命题赛规则速查（第 17 届）")
    lines.append("")
    lines.append("- **选题方式**：可自主选题，也可选企业命题；选企业命题的团队与自主选题团队一起参加校赛、角逐省赛名额。")
    lines.append("- **国赛直通名额**：益普索选题 30 个，其他企业选题各 3 个（按各选题提交报告数量适当调整）。")
    lines.append("- **提交截止**：2027-03-29 12:00 前在竞赛系统提交，每校最多 3 份；材料为报告 + 附件 2 参赛承诺书，逾期视同不参加。")
    lines.append("- **评审方式**：企业命题赛为报告评审，2027-04-10 前完成。")
    lines.append("- **报告要求**：正文 ≤65 页（超页系统拒收），正文与附录分开；按附件 3 排版；任何一页不得出现参赛校与指导教师信息；中国地图须用附件 4 最新版。")
    lines.append("- **合规要求**：查重率 >20% 取消成绩与资格，>40% 视为学术不端并官网通报；使用 AI 须遵循附件 5 并提交 AI 附录。")
    lines.append("")
    lines.append("## 三、编号与文件规范")
    lines.append("")
    lines.append("- 编号：`E01`–`E08` 对应 8 家企业，`E01-01`～`E08-40` 为企业内序号，与企业命题子方向一一对应。")
    lines.append("- 目录名：`编号_全标题`，全标题格式为 `“主标题”——副标题`，副标题含两个研究点。")
    lines.append("- 精简交付：每题只保留 `选题说明.pdf`（无水印，选题审阅版）和 `_topic.txt`；不保留 DOCX 或水印版 PDF。")
    lines.append("- 速览：`_topic.txt` 汇总对象、变量、假设、可行性、参考来源与命题呼应。")
    lines.append("")
    lines.append("## 四、选题使用建议")
    lines.append("")
    lines.append("1. 先按企业命题方向筛 3–5 个候选，核对本校可获得的企业/商户样本渠道（如酷冷需工程商名单、神启需中小微企业主社群）。")
    lines.append("2. 用 `_topic.txt` 快速比对两个研究点是否都可测量，再打开 docx 补全抽样方案与问卷。")
    lines.append("3. 报名企业命题后须加入对应企业官方沟通群（格远、神启等命题在原文中指定了联系人），按企业口径统一问卷。")
    lines.append("4. 与企业命题原文冲突时，以 `references/第十七届赛制资料/` 中的官方附件为准。")
    lines.append("")
    lines.append("> 证据核验提示：档案中 ✅ 为官方/权威来源，🔶 为行业报告或媒体线索，参赛前须下载原文核对；数据以官方最新发布为准。")
    return "\n".join(lines) + "\n"


def build(codes=None):
    codes = codes or [c for c, _, _, _ in COMPANIES]
    for code, name, icon, color in COMPANIES:
        if code not in codes:
            continue
        cdir = BASE / f"{code}_{name}"
        cdir.mkdir(parents=True, exist_ok=True)
        (cdir / "README.md").write_text(company_readme(code, name, icon, color), encoding="utf-8")
    (BASE / "README.md").write_text(root_readme(codes), encoding="utf-8")
    print("readme built")


if __name__ == "__main__":
    build()
