import json
from pathlib import Path
root=Path(__file__).resolve().parent.parent; gen=root/'_gen'
patches=[]
for p in sorted(gen.glob('award_patch_E*.json')):
    patches.extend(json.loads(p.read_text(encoding='utf-8-sig')))
by={x['id']:x['title_main'] for x in patches}
assert len(by)==320 and len(set(by.values()))==320
for i in range(1,9):
    code=f'E{i:02d}'; p=gen/(code+'.json'); rows=json.loads(p.read_text(encoding='utf-8-sig')); assert len(rows)==40
    for r in rows:
        r['title_main']=by[r['id']]; r['full_title']=f'“{r["title_main"]}”——{r["title_sub"]}'
    p.write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('applied',len(by))
