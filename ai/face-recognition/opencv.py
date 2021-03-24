import cv2 as cv

image = cv.imread('../../data/ciyun.png')


cv.imshow('image', image)

cv.waitKey(0)

# cv.destroyAllWindows()
