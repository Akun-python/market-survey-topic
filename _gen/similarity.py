import json
from pathlib import Path
from difflib import SequenceMatcher

for p in sorted(Path(__file__).parent.glob('E0?.json')):
    rows = json.loads(p.read_text(encoding='utf-8-sig'))
    pairs = []
    for i, a in enumerate(rows):
        for b in rows[i+1:]:
            score = SequenceMatcher(None, a['title_sub'], b['title_sub']).ratio()
            if score >= 0.87:
                pairs.append((a['id'], b['id'], round(score, 2)))
    print(p.name, 'similar title pairs:', len(pairs), 'examples:', pairs[:10])
