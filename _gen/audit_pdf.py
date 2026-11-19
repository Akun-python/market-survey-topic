from pathlib import Path
import pymupdf,collections
root=Path('2027年企业命题'); bad=[]; counts=collections.Counter(); total=0
for company in root.iterdir():
 if not company.is_dir() or not company.name.startswith('E0'): continue
 for topic in company.iterdir():
  if not topic.is_dir(): continue
  if not all((topic/name).exists() for name in ('_topic.txt','选题说明.docx','选题说明.pdf','选题说明_水印版.pdf')):
   bad.append(str(topic)); continue
  p=pymupdf.open(topic/'选题说明.pdf'); w=pymupdf.open(topic/'选题说明_水印版.pdf')
  counts[(p.page_count,w.page_count)]+=1;total+=1
  if p.page_count!=w.page_count or any(not pg.get_text().strip() for pg in p):bad.append(str(topic))
print('topics',total,'pages',dict(counts),'bad',len(bad))
for p in bad[:15]:print(p)
