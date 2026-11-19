import json
from pathlib import Path
import pymupdf
root=Path('2027年企业命题'); errors=[];n=0
for code,name in [('E01','益普索'),('E02','问卷网'),('E03','同方知网'),('E04','格远数智赋能'),('E05','汇辽集团'),('E06','酷冷保温'),('E07','神启数据'),('E08','中健国康')]:
 rows=json.loads(Path('_gen',code+'.json').read_text(encoding='utf-8-sig')); cdir=root/(code+'_'+name)
 actual={p.name for p in cdir.iterdir() if p.is_dir()}; expected={r['id']+'_'+r['full_title'] for r in rows}
 if actual!=expected: errors.append((code,'dir difference',len(actual-expected),len(expected-actual)))
 for r in rows:
  topic=cdir/(r['id']+'_'+r['full_title']);pdf=topic/'选题说明.pdf';txt=topic/'_topic.txt';n+=1
  if not pdf.exists() or not txt.exists() or list(topic.glob('*.docx')) or list(topic.glob('*水印*.pdf')): errors.append((r['id'],'files'));continue
  if r['full_title'] not in txt.read_text(encoding='utf-8'):errors.append((r['id'],'txt title'))
  d=pymupdf.open(pdf)
  if len(d)!=1:errors.append((r['id'],'pages',len(d)))
  # Word may wrap the heading across lines, so compare normalized text.
  ptext=''.join(d[0].get_text().split())
  if ''.join(r['title_main'].split()) not in ptext:errors.append((r['id'],'pdf prefix'))
print('topics',n,'errors',len(errors),'first',errors[:8])
assert n==320 and not errors
