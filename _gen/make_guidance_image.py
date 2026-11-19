from PIL import Image,ImageDraw,ImageFont
font=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',24)
text='正大杯全程指导（不代做）：a237658765'
b=font.getbbox(text); w=b[2]+20; h=40
im=Image.new('RGBA',(w,h),(255,255,255,0)); d=ImageDraw.Draw(im); d.text((10,5),text,font=font,fill=(120,120,120,255)); im.save('_gen/guidance_text.png'); print(w,h)
