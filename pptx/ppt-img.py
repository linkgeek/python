from pptx import Presentation

from pptx.util import Inches

#img_path = '../data/img/china.png'  # 图片名称一定要对
img_path = 'https://www.baidu.com/img/PCtm_d9c8750bed0b3c7d089fa7d55720d6cf.png'  # 图片名称一定要对

prs = Presentation()
blank_slide_layout = prs.slide_layouts[6]
slide = prs.slides.add_slide(blank_slide_layout)

left = top = Inches(1)
pic = slide.shapes.add_picture(img_path, left, top)

left = Inches(5)
height = Inches(5.5)
slide.shapes.add_picture(img_path, left, top, height=height)

prs.save('../data/add_pic.pptx')
