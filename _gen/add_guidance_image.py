from pathlib import Path
import pymupdf
img=str(Path('_gen/guidance_text.png').resolve()); pdfs=list(Path('2027年企业命题').rglob('选题说明.pdf')); assert len(pdfs)==320
for p in pdfs:
 d=pymupdf.open(p)
 for page in d:
  r=pymupdf.Rect(page.rect.x0+36,page.rect.y1-44,page.rect.x1-36,page.rect.y1-15)
  page.insert_image(r,filename=img,keep_proportion=True,overlay=True)
 tmp=p.with_suffix('.pdf.tmp'); d.save(tmp,garbage=3,deflate=True);d.close();tmp.replace(p)
print('updated',len(pdfs))
