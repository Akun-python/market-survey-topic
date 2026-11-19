#!/usr/bin/env python
"""检验 8 家企业选题 JSON 的结构、覆盖、重复与标题公式。"""
import json
import re
from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GEN = ROOT / "_gen"
EXISTING_ROOT = ROOT / "正大杯最新选题"
FIELDS = {
    "id", "title_main", "title_sub", "full_title", "company_bucket", "industry",
    "project_type", "stage", "region", "object", "variables", "h1", "h2",
    "basis", "feasibility", "sources", "fit_note",
}
COMPANIES = ["益普索", "问卷网", "同方知网", "格远数智赋能", "汇辽集团", "酷冷保温", "神启数据", "中健国康"]
INDUSTRIES = {p.name for p in EXISTING_ROOT.iterdir() if p.is_dir()}
EXISTING = [topic.name.split("_", 1)[-1] for industry in EXISTING_ROOT.iterdir()
            if industry.is_dir() for topic in industry.iterdir() if topic.is_dir()]
ERRORS, WARNINGS = [], []
ALL = []


def normalized(text):
    return re.sub(r"[\s，。；：‘’“”《》\-—、（）()]+", "", text)


for n, company in enumerate(COMPANIES, 1):
    code = f"E{n:02d}"
    path = GEN / f"{code}.json"
    if not path.exists():
        WARNINGS.append(f"{code}: 尚未生成数据文件")
        continue
    try:
        rows = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        ERRORS.append(f"{code}: JSON 读取失败 {exc}")
        continue
    if len(rows) != 40:
        ERRORS.append(f"{code}: 题数 {len(rows)}，预期 40")
    buckets = Counter()
    for i, row in enumerate(rows, 1):
        rid = row.get("id", "?")
        if rid != f"{code}-{i:02d}":
            ERRORS.append(f"{rid}: 编号顺序错误：应为 {code}-{i:02d}")
        missing = FIELDS - row.keys()
        if missing:
            ERRORS.append(f"{rid}: 缺失字段 {sorted(missing)}")
            continue
        blank = [key for key in FIELDS if not str(row[key]).strip()]
        if blank:
            ERRORS.append(f"{rid}: 空字段 {blank}")
        if row["full_title"] != f"“{row['title_main']}”——{row['title_sub']}":
            ERRORS.append(f"{rid}: 全标题拼接不一致")
        if not re.search(r"与|及|和|、", row["title_sub"]):
            WARNINGS.append(f"{rid}: 副标题未清楚出现双研究点连接词")
        if not row["title_sub"].endswith(("研究", "调查", "测度", "评估")):
            WARNINGS.append(f"{rid}: 副标题不以研究/调查/测度/评估结尾")
        if len(row["title_main"]) > 19 or len(row["title_sub"]) > 45:
            WARNINGS.append(f"{rid}: 标题过长：{len(row['title_main'])}/{len(row['title_sub'])}")
        if row["industry"] not in INDUSTRIES:
            ERRORS.append(f"{rid}: 未知行业 {row['industry']}")
        if len([v for v in re.split(r"[,，、；;]", row["variables"]) if v.strip()]) < 5:
            WARNINGS.append(f"{rid}: 变量少于五项")
        for k in ("h1", "h2"):
            if "待验证" not in row[k]:
                WARNINGS.append(f"{rid}: {k} 未标待验证")
        if "✅" not in row["basis"] and "🔶" not in row["basis"]:
            WARNINGS.append(f"{rid}: 选题依据未标来源状态")
        dirname = f"{rid}_{row['full_title']}"
        if len(str(ROOT / '2027年企业命题' / f'{code}_{company}' / dirname / '选题说明_水印版.pdf')) >= 250:
            ERRORS.append(f"{rid}: 路径过长（Windows）")
        title = normalized(row["full_title"])
        same = [x for x in EXISTING if normalized(x) == title]
        if same:
            ERRORS.append(f"{rid}: 与旧题库完全同题 {same[0]}")
        buckets[row["company_bucket"]] += 1
        ALL.append(row)
    print(code, company, len(rows), "命题覆盖", dict(buckets))

normtitles = [normalized(row["full_title"]) for row in ALL]
for title, count in Counter(normtitles).items():
    if count > 1:
        ERRORS.append(f"新题库重复标题：{title}（{count} 次）")

for i, row in enumerate(ALL):
    for other in ALL[i + 1:]:
        ratio = SequenceMatcher(None, normalized(row["title_sub"]), normalized(other["title_sub"])).ratio()
        if ratio >= 0.87:
            WARNINGS.append(f"相似副标题：{row['id']} / {other['id']}，相似度 {ratio:.2f}")

print(f"总数 {len(ALL)}；错误 {len(ERRORS)}；警告 {len(WARNINGS)}")
for label, items in (("ERROR", ERRORS), ("WARN", WARNINGS)):
    for item in items[:60]:
        print(f"[{label}] {item}")
    if len(items) > 60:
        print(f"[{label}] 其余 {len(items) - 60} 条省略")
raise SystemExit(1 if ERRORS else 0)
