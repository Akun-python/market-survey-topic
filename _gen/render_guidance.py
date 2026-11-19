import pymupdf
from pathlib import Path
p=next(Path('2027年企业命题').rglob('选题说明.pdf'))
d=pymupdf.open(p); pix=d[0].get_pixmap(matrix=pymupdf.Matrix(1.5,1.5),alpha=False); pix.save('_gen/guidance_sample.png'); print(p)
