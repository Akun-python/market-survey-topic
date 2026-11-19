import json
from pathlib import Path
from collections import Counter
root=Path(__file__).resolve().parent.parent
gen=root/'_gen'
patches=[]
for p in sorted(gen.glob('prefix_patch_E*.json')):
    patches.extend(json.loads(p.read_text(encoding='utf-8-sig')))
by={x['id']:x['title_main'] for x in patches}
assert len(by)==320 and len(set(by.values()))==320
for code in [f'E{i:02d}' for i in range(1,9)]:
    p=gen/f'{code}.json'; rows=json.loads(p.read_text(encoding='utf-8-sig'))
    assert len(rows)==40
    for row in rows:
        assert row['id'] in by
        row['title_main']=by[row['id']]
        row['full_title']=f'“{row["title_main"]}”——{row["title_sub"]}'
    p.write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('updated',len(by),'titles')
