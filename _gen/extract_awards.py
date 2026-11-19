from pathlib import Path
import pymupdf, openpyxl
root=Path('references/获奖名单'); out=[]
for p in root.rglob('*'):
 try:
  if p.suffix.lower()=='.pdf':
   doc=pymupdf.open(p); text='\n'.join(pg.get_text() for pg in doc)
   out.append(f'### {p.name}\n{text[:12000]}')
  elif p.suffix.lower()=='.xlsx':
   wb=openpyxl.load_workbook(p,read_only=True,data_only=True)
   vals=[]
   for ws in wb.worksheets:
    for row in ws.iter_rows(values_only=True):
     line=' | '.join(str(x) for x in row if x is not None)
     if line: vals.append(line)
   out.append(f'### {p.name}\n'+'\n'.join(vals[:1000]))
 except Exception as e: print('ERR',p,e)
Path('_gen/award_titles_raw.txt').write_text('\n\n'.join(out),encoding='utf-8')
print('files',len(out),'chars',sum(map(len,out)))
