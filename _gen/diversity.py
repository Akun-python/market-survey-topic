import json,collections
from pathlib import Path
for p in sorted(Path('_gen').glob('E0?.json')):
 r=json.loads(p.read_text(encoding='utf-8-sig'))
 cols={k:len(set(x[k] for x in r)) for k in ('title_sub','object','variables','h1','h2','feasibility','basis','sources','fit_note')}
 print(p.stem,cols)
