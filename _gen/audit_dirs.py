import json
from pathlib import Path
base=Path('2027年企业命题')
for cdir in sorted(p for p in base.iterdir() if p.is_dir() and p.name.startswith('E0')):
 code=cdir.name[:3]
 rows=json.loads((Path('_gen')/(code+'.json')).read_text(encoding='utf-8-sig'))
 expect={r['id']+'_'+r['full_title'] for r in rows}
 actual={p.name for p in cdir.iterdir() if p.is_dir()}
 print(code,'expected',len(expect),'actual',len(actual),'stale',len(actual-expect),'missing',len(expect-actual),'docx',len(list(cdir.rglob('选题说明.docx'))),'pdf',len(list(cdir.rglob('选题说明.pdf'))))
 for x in sorted(actual-expect)[:2]: print('  stale',x)
