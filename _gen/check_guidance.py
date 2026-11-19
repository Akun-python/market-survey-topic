from pathlib import Path
import pymupdf
pdfs=list(Path('2027年企业命题').rglob('选题说明.pdf')); bad=[]
for p in pdfs:
 d=pymupdf.open(p); txt=''.join(pg.get_text() for pg in d)
 if 'a237658765' not in txt or len(d)!=1: bad.append(str(p))
print('pdfs',len(pdfs),'bad',len(bad)); print('sample_tail',repr(''.join(pymupdf.open(pdfs[0])[0].get_text().splitlines()[-2:])))
assert len(pdfs)==320 and not bad
