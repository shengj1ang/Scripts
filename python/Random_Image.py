import random
import PIL
from PIL import Image #生成图片
from PIL import ImageDraw #控制图片内容
from PIL import ImageFont #控制字体样式

def random_color(): #生成一个0-255的三位数组 用以控制背景颜色
    return (random.randint(0,255),random.randint(0,255),random.randint(0,255))

def random_crop(): 
    #  (left, upper, right, lower)
    left=random.randint(0,412)
    upper=random.randint(0,412)
    right=left+100
    lower=upper+100
    return (left,upper,right,lower)
    #return(100,100,200,200)


def draw_random_image(filename):
    image = Image.new('RGB',(512,512),random_color()) #生成一个图片(模式，图片尺寸，颜色（用之前调好的随机颜色就好）)
    pixels = image.load()
    for i in range(image.size[0]):
        for j in range(image.size[1]):
            pixels[i,j] = random_color()
    draw=ImageDraw.Draw(image) #生成一个编辑对象 可以对image对象添加各种属性 实际是对刚才生成的image对象做编辑


    #draw有很多功能
    # draw.text() 往里面添加文本
    # draw.line() 往里面添加线
    # draw.point() 往里添加噪点
    #font=ImageFont.truetype("blog/static/font/kumo.ttf",size=32) #字体样式（字体样式文件（ttf）的django路径，尺寸）
    temp=[] #生成的随机字符串的列表
    for i in range(5): #生成随机字符
    
        #random_num = str(random.randint(0, 9))
        #random_low_alpha = chr(random.randint(97, 122))
        #random_upper_alpha = chr(random.randint(65, 90))
        #random_char = random.choice([random_num, random_low_alpha, random_upper_alpha])
        #draw.text((24 + i * 36, 0), random_char, random_color(), font=font) #生成字体（位置，字符，颜色，字体）
        #temp.append(random_char)

        # 噪点噪线
        width = 512
        height = 512
        for i in range(256):
            x1 = random.randint(0, width)
            x2 = random.randint(0, width)
            y1 = random.randint(0, height)
            y2 = random.randint(0, height)
            draw.line((x1, y1, x2, y2), fill=random_color())  # 画线((起始点xy坐标，终止点xy坐标),颜色)

        for i in range(256):
            draw.point([random.randint(0, width), random.randint(0, height)], fill=random_color())  # 画点(([点坐标]),颜色)
            x = random.randint(0, width)
            y = random.randint(0, height)
            draw.arc((x, y, x + 4, y + 4), 0, 90, fill=random_color())  # 画弧((起始点xy坐标，终止点xy坐标),弧度的起始，弧度的终止，颜色)
    after_crop=image.crop(random_crop()) 
    #after_resize = after_crop.resize((512, 512),Image.ANTIALIAS)
    after_resize = after_crop.resize((256, 256))
    with open(filename,"wb") as f:
        after_resize.save(f,"png")

    '''
    from io import BytesIO
    f = BytesIO() #在内存中开辟一块动态地址
    image.save(f,"png") #图片对象保存 （地址，格式）
    data = f.getvalue() #获取之前内存地址中的文件内容
    f.close() #管理内存 不占地

    valid_str="".join(temp) #生成的随机字符串的拼接 为和用户输入内容做比对用
    print("valid_str",valid_str)'''


#https://www.cnblogs.com/flashpoint3/p/8832624.html


for i in range(1,3):
    print(i)
    filename=str(i)+".png"
    draw_random_image(filename)
    