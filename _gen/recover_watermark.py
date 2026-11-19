import glob,pymupdf
from PIL import Image
p=glob.glob('正大杯最新选题/01_银发经济/1023_*/选题说明_水印版.pdf')[0]
d=pymupdf.open(p)
xref,mask,*_=d[0].get_images(full=True)[0]
pix=pymupdf.Pixmap(d,xref)
alpha=pymupdf.Pixmap(d,mask)
rgba=pymupdf.Pixmap(pix,alpha)
out='2027年企业命题/_assets/watermark.png'
rgba.save(out)
i=Image.open(out)
print(i.mode,i.getextrema(),i.getbbox())
