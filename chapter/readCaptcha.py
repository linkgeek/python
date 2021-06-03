import cv2 as cv
import pytesseract
from PIL import Image


def recognize_text(image):
    # 边缘保留滤波  去噪
    dst = cv.pyrMeanShiftFiltering(image, sp=10, sr=150)
    # 灰度图像
    gray = cv.cvtColor(dst, cv.COLOR_BGR2GRAY)
    # 二值化
    ret, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)
    # 形态学操作   腐蚀  膨胀
    erode = cv.erode(binary, None, iterations=2)
    dilate = cv.dilate(erode, None, iterations=1)
    cv.imshow('dilate', dilate)
    # 逻辑运算  让背景为白色  字体为黑  便于识别
    cv.bitwise_not(dilate, dilate)
    cv.imshow('binary-image', dilate)
    # 识别
    test_message = Image.fromarray(dilate)
    text = pytesseract.image_to_string(test_message)
    print(f'识别结果：{text}')


#src = cv.imread(r'./captcha01.png')
src = cv.imread(r'G:/working/sucai/captcha02.png')
cv.imshow('input image', src)
recognize_text(src)
cv.waitKey(0)
cv.destroyAllWindows()