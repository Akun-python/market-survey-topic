from pathlib import Path
import pymupdf
pdfs=list(Path('2027年企业命题').rglob('选题说明.pdf')); bad=[]
for p in pdfs:
 d=pymupdf.open(p)
 if len(d)!=1 or 'a237658765' not in ''.join(x.get_text() for x in d): bad.append(str(p))
print(len(pdfs),'bad',len(bad)); assert len(pdfs)==320 and not bad
p=pdfs[0];pix=pymupdf.open(p)[0].get_pixmap(matrix=pymupdf.Matrix(1.2,1.2));pix.save('_gen/guidance_sample2.png')
