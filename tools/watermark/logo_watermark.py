# logo 添加水印
from PIL import Image, ImageSequence
import os
import random

# 保存 logo 信息
img_logo = Image.open("logo.png")
img_logo_width, img_logo_height = img_logo.size
img_logo_pixels = dict()
for w in range(img_logo_width):
    for h in range(img_logo_height):
        c = img_logo.getpixel((w, h))
        if c != (0, 0, 0, 0):
            img_logo_pixels[(w, h)] = c[:3] + (125,)


# 混合颜色
def blendPixel(c1, c2):
    # print(c1,c2)
    a1 = 256 - c2[3]
    a2 = c2[3] - (a1 * c2[3]) / 256.0
    a = a1 + a2
    c = (
    int((a1 * c1[0] + a2 * c2[0]) / a), int((a1 * c1[1] + a2 * c2[1]) / a), int((a1 * c1[2] + a2 * c2[2]) / a), int(a))
    return c


# 处理一个
def dealOneImage(image, offX=None, offY=None):
    w, h = image.size
    offX = offX if offX else random.random();
    offY = offY if offY else random.random();
    # 如果图片尺寸小于水印图片，不加水印
    if w >= img_logo_width and h >= img_logo_height:
        top = int((w - img_logo_width) * offX)
        left = int((h - img_logo_height) * offY)
        for p, c in img_logo_pixels.items():
            p_x = (p[0] + top)
            p_y = (p[1] + left)
            image_c = image.getpixel((p_x, p_y))
            if (isinstance(image_c, tuple) and len(image_c) > 2):
                image.putpixel((p_x, p_y), blendPixel(image_c, c))
    return image;


# 处理文件
def dealOneFile(filePath):
    img_orign = Image.open(filePath)
    _, file_type = os.path.splitext(filePath)
    basename = os.path.basename(filePath)
    if file_type == '.gif':
        sequence = [];
        offX = random.random()
        offY = random.random()
        for f in ImageSequence.Iterator(img_orign):
            if len(sequence) % 2 == 0:
                offX = random.random()
                offY = random.random()
            sequence.append(dealOneImage(f.convert(), offX, offY))
        sequence[0].save(f'./output/{basename}', save_all=True, append_images=sequence[1:])
    else:
        image_out = (dealOneImage(img_orign))
        for x in range(2):
            image_out = (dealOneImage(image_out))
        image_out.save(f'./output/{basename}')


# 处理目录
def dealSrc(srcDir):
    picFiles = [os.path.join(srcDir, fn) for fn in os.listdir(srcDir) if fn.endswith(('.gif', '.jpg', '.png', '.jpeg'))]
    for filePath in picFiles:
        dealOneFile(filePath)


dealSrc('./input/')
