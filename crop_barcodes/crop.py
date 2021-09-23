from dbr import *
import cv2
import numpy as np

def four_point_transform(image, pts):

    rect = np.array(pts, dtype = "float32")
    (tl, tr, br, bl) = rect
 
    # compute the width of the new image, which will be the
    # maximum distance between bottom-right and bottom-left
    # x-coordiates or the top-right and top-left x-coordinates
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))
 
    # compute the height of the new image, which will be the
    # maximum distance between the top-right and bottom-right
    # y-coordinates or the top-left and bottom-left y-coordinates
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))
 
    # now that we have the dimensions of the new image, construct
    # the set of destination points to obtain a "birds eye view",
    # (i.e. top-down view) of the image, again specifying points
    # in the top-left, top-right, bottom-right, and bottom-left
    # order
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype = "float32")
 
    # compute the perspective transform matrix and then apply it
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
    
    # return the warped image
    return warped

img = cv2.imread("IMG_20210922_174600-1.jpg")

dbr = BarcodeReader()
dbr.init_license("t0068MgAAABaPdihgo0ura46bBvXa/K+sCfupbVhYdDSY3AlEooBX/7ZSvLQVJmCnYzaJ8Xblhwt1G3hrI9hrklQDGgzvFp0=")
text_results = dbr.decode_buffer(img)

img_width = img.shape[1]
img_height = img.shape[0]

index = 0
for tr in text_results:
    index = index + 1
    points = tr.localization_result.localization_points
    angle =  tr.localization_result.angle
    cropped = four_point_transform(img, points)
    cv2.imshow(str(index),cropped)
    
        
cv2.waitKey()
cv2.destroyAllWindows()
    
