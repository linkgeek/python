# -*- coding: utf-8 -*-
import cv2
import pytesseract
import numpy as np


class ImageTableOCR(object):

    # 初始化
    def __init__(self, ImagePath):
        # 读取图片
        self.image = cv2.imread(ImagePath, 1)
        # 把图片转换为灰度模式
        self.gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

    # 横向直线检测
    def HorizontalLineDetect(self):

        # 图像二值化
        ret, thresh1 = cv2.threshold(self.gray, 240, 255, cv2.THRESH_BINARY)
        # 进行两次中值滤波
        blur = cv2.medianBlur(thresh1, 3)  # 模板大小3*3
        blur = cv2.medianBlur(blur, 3)  # 模板大小3*3

        h, w = self.gray.shape

        # 横向直线列表
        horizontal_lines = []
        for i in range(h - 1):
            # 找到两条记录的分隔线段，以相邻两行的平均像素差大于120为标准
            if abs(np.mean(blur[i, :]) - np.mean(blur[i + 1, :])) > 120:
                # 在图像上绘制线段
                horizontal_lines.append([0, i, w, i])
                # cv2.line(self.image, (0, i), (w, i), (0, 255, 0), 2)

        horizontal_lines = horizontal_lines[1:]
        # print(horizontal_lines)
        return horizontal_lines

    #  纵向直线检测
    def VerticalLineDetect(self):
        # Canny边缘检测
        edges = cv2.Canny(self.gray, 30, 240)

        # Hough直线检测
        minLineLength = 500
        maxLineGap = 30
        lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 100, minLineLength, maxLineGap).tolist()
        lines.append([[13, 937, 13, 102]])
        lines.append([[756, 937, 756, 102]])
        sorted_lines = sorted(lines, key=lambda x: x[0])

        # 纵向直线列表
        vertical_lines = []
        for line in sorted_lines:
            for x1, y1, x2, y2 in line:
                # 在图片上绘制纵向直线
                if x1 == x2:
                    # print(line)
                    vertical_lines.append((x1, y1, x2, y2))
                    # cv2.line(self.image, (x1, y1), (x2, y2), (0, 0, 255), 2)

        return vertical_lines

    # 顶点检测
    def VertexDetect(self):
        vertical_lines = self.VerticalLineDetect()
        horizontal_lines = self.HorizontalLineDetect()

        # 顶点列表
        vertex = []
        for v_line in vertical_lines:
            for h_line in horizontal_lines:
                vertex.append((v_line[0], h_line[1]))

        # print(vertex)

        # 绘制顶点
        for point in vertex:
            cv2.circle(self.image, point, 1, (255, 0, 0), 2)

        return vertex

    # 寻找单元格区域
    def CellDetect(self):
        vertical_lines = self.VerticalLineDetect()
        horizontal_lines = self.HorizontalLineDetect()

        # 顶点列表
        rects = []
        for i in range(0, len(vertical_lines) - 1, 2):
            for j in range(len(horizontal_lines) - 1):
                rects.append((vertical_lines[i][0], horizontal_lines[j][1], \
                              vertical_lines[i + 1][0], horizontal_lines[j + 1][1]))

        # print(rects)
        return rects

    # 识别单元格中的文字
    def OCR(self):
        rects = self.CellDetect()
        thresh = self.gray

        # 特殊字符列表
        special_char_list = ' `~!@#$%^&*()-_=+[]{}|\\;:‘’，。《》/？ˇ'
        for i in range(20):
            rect1 = rects[i]
            DetectImage1 = thresh[rect1[1]:rect1[3], rect1[0]:rect1[2]]

            # Tesseract所在的路径
            pytesseract.pytesseract.tesseract_cmd = 'C://Program Files (x86)/Tesseract-OCR/tesseract.exe'
            # 识别数字（每行第一列）
            text1 = pytesseract.image_to_string(DetectImage1, config="--psm 10")
            print(text1, end='-->')

            # 识别汉字（每行第二列）
            rect2 = rects[i + 20]
            DetectImage2 = thresh[rect2[1]:rect2[3], rect2[0]:rect2[2]]
            text2 = pytesseract.image_to_string(DetectImage2, config='--psm 7', lang='chi_sim')
            text2 = ''.join([char for char in text2 if char not in special_char_list])
            print(text2, end='-->')

            # 识别汉字（每行第三列）
            rect3 = rects[i + 40]
            DetectImage3 = thresh[rect3[1]:rect3[3], rect3[0]:rect3[2]]
            text3 = pytesseract.image_to_string(DetectImage3, config='--psm 7', lang='chi_sim')
            text3 = ''.join([char for char in text3 if char not in special_char_list])
            print(text3)

    # 显示图像
    def ShowImage(self):
        cv2.imshow('AI', self.image)
        cv2.waitKey(0)
        # cv2.imwrite('E://Horizontal.png', self.image)


ImagePath = '../../data/image/cp.png'
imageOCR = ImageTableOCR(ImagePath)
imageOCR.OCR()
