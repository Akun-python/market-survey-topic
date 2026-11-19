from pathlib import Path
s=Path('_gen/award_titles_raw.txt').read_text(encoding='utf-8')
for term in ['第十六届本科组全国总决赛获奖公告.pdf','第十五届全国大学生市场调查与分析大赛（本科生总决赛）.pdf']:
 i=s.find('### '+term)
 if i<0:continue
 end=s.find('### ',i+4)
 t=s[i:end if end>=0 else None]
 print('\n#####',term,'\n',t[:8500])
