import pytesseract
from PIL import Image

import tesserocr

im = Image.open('ying_shu.png')
print(pytesseract.image_to_string(im))
im1 = Image.open('ying_jianti.png')
print(pytesseract.image_to_string(im1, lang='chi_sim'))
im2 = Image.open('fanti.png')
print(pytesseract.image_to_string(im2, lang='chi_tra'))