#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""构建 2027 年企业命题选题库：以临时 DOCX 导出无水印 PDF 和索引。"""
import argparse
import json
import os
import sys
import time
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.shared import Emu, Pt

ROOT = Path(__file__).resolve().parent.parent
BASE = ROOT / "2027年企业命题"
GEN = ROOT / "_gen"

COMPANIES = [
    ("E01", "益普索"),
    ("E02", "问卷网"),
    ("E03", "同方知网"),
    ("E04", "格远数智赋能"),
    ("E05", "汇辽集团"),
    ("E06", "酷冷保温"),
    ("E07", "神启数据"),
    ("E08", "中健国康"),
]
CMAP = dict(COMPANIES)

INDUSTRIES = [
    "01_银发经济", "02_宠物经济", "03_人工智能与数字科技", "04_文化旅游与演艺",
    "05_体育健身与户外运动", "06_餐饮食品", "07_零售商业与消费新形态",
    "08_居住与城市更新", "09_汽车与出行", "10_金融保险与理财", "11_健康医疗",
    "12_教育与培训", "13_职场与新就业", "14_乡村振兴与县域经济",
    "15_绿色低碳与循环经济", "16_二次元与青年潮流", "17_美妆服饰与珠宝",
    "18_母婴育儿与家庭", "19_婚恋与社交", "20_传媒娱乐与数字内容",
    "21_公共治理与社会关怀",
]

EMU = 12700  # per pt


def set_run_font(run, size_pt, bold=False):
    run.font.name = "宋体"
    run.font.size = Pt(size_pt)
    run.bold = bold
    rpr = run._element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = rpr.makeelement(qn("w:rFonts"), {})
        rpr.append(rfonts)
    for attr in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
        rfonts.set(qn(attr), "宋体")


def add_para(doc, text, size, bold=False, align=None, after_pt=0.0):
    p = doc.add_paragraph()
    if align is not None:
        p.alignment = align
    p.paragraph_format.space_after = Pt(after_pt)
    run = p.add_run(text)
    set_run_font(run, size, bold)
    return p


def build_docx(row, company, out_path):
    doc = Document()
    sec = doc.sections[0]
    sec.page_width = Emu(7772400)
    sec.page_height = Emu(10058400)
    sec.left_margin = sec.right_margin = Emu(1143000)
    sec.top_margin = sec.bottom_margin = Emu(914400)

    style = doc.styles["Normal"]
    style.font.name = "宋体"
    style.font.size = Pt(11)
    style.element.rPr.rFonts.set(qn("w:eastAsia"), "宋体")

    add_para(doc, f"{row['id']}. {row['full_title']}", 15, True,
             WD_ALIGN_PARAGRAPH.CENTER, 6)
    add_para(doc, "正大杯选题档案 · 选题规范化（呆塔大师兄（微信：a237658765））", 9,
             False, WD_ALIGN_PARAGRAPH.CENTER, 10)

    add_para(doc, "一、选题定位", 13, True, after_pt=4)
    add_para(doc, f"项目类型：{row['project_type']}", 11, after_pt=3)
    add_para(doc, f"研究阶段：{row['stage']}", 11, after_pt=3)
    add_para(doc, f"建议地区：{row['region']}", 11, after_pt=3)
    add_para(
        doc,
        f"确定行业：{row['industry']}（选择理由：贴合{company}命题“{row['company_bucket']}”的"
        f"产品与场景，研究对象与样本渠道明确，可转化为问卷/访谈设计；参赛前仍须核对近三年获奖题目。）",
        11, after_pt=3)
    add_para(
        doc,
        f"所属企业命题：{company}·{row['company_bucket']}（{row['fit_note']}）",
        11, after_pt=3)
    add_para(doc, f"研究对象：{row['object']}", 11, after_pt=3)
    add_para(doc, f"核心问题/变量：{row['variables']}", 11, after_pt=3)

    add_para(doc, "二、生成假设（待验证）", 13, True, after_pt=4)
    add_para(doc, f"H1：{row['h1']}；H2：{row['h2']}", 11, after_pt=4)

    add_para(doc, "三、选题依据（信息时间范围：2025–2026）", 13, True, after_pt=4)
    add_para(doc, row["basis"], 11, after_pt=4)

    add_para(doc, "四、可行性提示", 13, True, after_pt=4)
    add_para(doc, row["feasibility"] + " 可进一步明确抽样框、样本量与问卷/访谈工具，形成完整调研方案。",
             11, after_pt=4)

    add_para(doc, "五、参考来源", 13, True, after_pt=4)
    add_para(doc, row["sources"], 11, after_pt=4)

    add_para(
        doc,
        "※ 检索状态说明：本档案基于 2025–2026 公开政策、行业报告与企业命题原文整理（部分来源未逐条联网复核）；"
        "✅=官方/权威来源线索，🔶=行业报告/媒体线索；所有来源和近三年获奖题目均须在参赛前逐一核验。", 
        9, after_pt=8)

    doc.core_properties.title = row["full_title"]
    doc.core_properties.author = "呆塔大师兄"
    doc.save(str(out_path))


def topic_txt(row, company):
    lines = [
        f"{row['id']}. {row['full_title']}",
        f"- **企业命题**：{company} · {row['company_bucket']}",
        f"- **对象**：{row['object']}",
        f"- **变量**：{row['variables']}",
        f"- **行业**：{row['industry']}",
        f"- **地域**：{row['region']}",
        f"- **阶段**：{row['stage']}",
        f"- **假设**：H1：{row['h1']}；H2：{row['h2']}",
        f"- **可行性**：{row['feasibility']}",
        f"- **参考来源**：{row['sources']}",
        f"- **命题呼应**：{row['fit_note']}",
    ]
    return "\n".join(lines) + "\n"


def dir_name(row):
    return f"{row['id']}_{row['full_title']}"


def load_rows(code):
    path = GEN / f"{code}.json"
    if not path.exists():
        return None
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    return data


def validate(code, rows):
    errs = []
    if len(rows) != 40:
        errs.append(f"{code}: expected 40 rows, got {len(rows)}")
    seen = set()
    for i, r in enumerate(rows):
        expect_id = f"{code}-{i + 1:02d}"
        if r.get("id") != expect_id:
            errs.append(f"{code}: row {i} id {r.get('id')} != {expect_id}")
        ft = r.get("full_title", "")
        if ft != f"“{r['title_main']}”——{r['title_sub']}":
            errs.append(f"{code}: full_title mismatch at {r.get('id')}")
        key = (r["object"].strip(), r["variables"].strip()[:60])
        if key in seen:
            errs.append(f"{code}: duplicate object+variables at {r['id']}")
        seen.add(key)
        if r["industry"] not in INDUSTRIES:
            errs.append(f"{code}: bad industry {r['industry']} at {r['id']}")
        for field in ("title_main", "title_sub", "object", "variables", "h1",
                      "h2", "basis", "feasibility", "sources", "fit_note",
                      "project_type", "stage", "region", "company_bucket"):
            if not str(r.get(field, "")).strip():
                errs.append(f"{code}: empty {field} at {r['id']}")
    return errs


def stage_docx(codes, force=False):
    total = 0
    for code in codes:
        rows = load_rows(code)
        if rows is None:
            print(f"[skip] {code}: no json")
            continue
        company = CMAP[code]
        cdir = BASE / f"{code}_{company}"
        cdir.mkdir(parents=True, exist_ok=True)
        for r in rows:
            tdir = cdir / dir_name(r)
            tdir.mkdir(exist_ok=True)
            docx_path = tdir / "选题说明.docx"
            if force or not docx_path.exists():
                build_docx(r, company, docx_path)
                total += 1
            txt_path = tdir / "_topic.txt"
            txt_path.write_text(topic_txt(r, company), encoding="utf-8")
    print(f"docx built: {total}")


def stage_pdf(codes, force=False):
    import win32com.client as win32
    word = win32.DispatchEx("Word.Application")
    word.Visible = False
    word.DisplayAlerts = 0
    # Word 会在关闭唯一文档时自动退出；保留空白文档维持 COM 会话。
    keeper = word.Documents.Add()
    converted = 0
    failures = []
    try:
        for code in codes:
            rows = load_rows(code)
            if rows is None:
                continue
            company = CMAP[code]
            cdir = BASE / f"{code}_{company}"
            for r in rows:
                tdir = cdir / dir_name(r)
                docx_path = (tdir / "选题说明.docx").resolve()
                pdf_path = (tdir / "选题说明.pdf").resolve()
                if not docx_path.exists():
                    continue
                if pdf_path.exists() and not force:
                    continue
                try:
                    if pdf_path.exists():
                        pdf_path.unlink()
                    doc = word.Documents.Open(str(docx_path), ReadOnly=True,
                                              AddToRecentFiles=False)
                    doc.ExportAsFixedFormat(
                        OutputFileName=str(pdf_path), ExportFormat=17,
                        OpenAfterExport=False, OptimizeFor=0, Range=0, Item=0,
                        IncludeDocProps=True, KeepIRM=True, CreateBookmarks=0,
                        DocStructureTags=True, BitmapMissingFonts=True,
                        UseISO19005_1=False)
                    doc.Close(False)
                    converted += 1
                    print(f"[pdf] {code} {r['id']} {r['title_main']}")
                except Exception as exc:  # noqa: BLE001
                    failures.append((r['id'], str(exc)))
                    print(f"[pdf-error] {code} {r['id']}: {exc}")
    finally:
        try:
            keeper.Close(False)
            word.Quit()
        except Exception:  # Word 可能已自动退出
            pass
    print(f"pdf converted: {converted}; failures: {len(failures)}")
    if failures:
        raise RuntimeError(f"PDF conversion failed for {len(failures)} topics: {failures[:4]}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", default="readme",
                    choices=["docx", "pdf", "readme"])
    ap.add_argument("--companies", default="")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()

    codes = [c for c, _ in COMPANIES]
    if args.companies:
        codes = [c.strip() for c in args.companies.split(",") if c.strip()]

    all_errs = []
    for code in codes:
        rows = load_rows(code)
        if rows is None:
            print(f"[warn] missing {code}.json")
            continue
        all_errs += validate(code, rows)
    if all_errs:
        print("VALIDATION ERRORS:")
        for e in all_errs:
            print(" -", e)
        sys.exit(1)

    if args.stage == "docx":
        stage_docx(codes, args.force)
    if args.stage == "pdf":
        stage_docx(codes, args.force)
        stage_pdf(codes, args.force)
        for code in codes:
            company = CMAP[code]
            for row in load_rows(code) or []:
                (BASE / f"{code}_{company}" / dir_name(row) / "选题说明.docx").unlink(missing_ok=True)
    if args.stage == "readme":
        import build_readme
        build_readme.build(codes)


if __name__ == "__main__":
    main()
