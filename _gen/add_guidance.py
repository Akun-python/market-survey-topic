from pathlib import Path
import pymupdf
pdfs=list(Path('2027年企业命题').rglob('选题说明.pdf'))
assert len(pdfs)==320
font='C:/Windows/Fonts/simhei.ttf'
text='正大杯全程指导（不代做）：a237658765'
for i,p in enumerate(pdfs,1):
    doc=pymupdf.open(p)
    for page in doc:
        box=pymupdf.Rect(page.rect.x0+36,page.rect.y1-42,page.rect.x1-36,page.rect.y1-18)
        page.insert_textbox(box,text,fontfile=font,fontsize=8,color=(0.48,0.48,0.48),align=pymupdf.TEXT_ALIGN_CENTER,overlay=True)
    tmp=p.with_suffix('.pdf.tmp')
    doc.save(tmp,garbage=3,deflate=True)
    doc.close()
    tmp.replace(p)
print('watermarked',len(pdfs),text)
