# USAGE
# python stitch.py --first images/bryce_left_01.png --second images/bryce_right_01.png 

# import the necessary packages
from pyimagesearch.panorama import Stitcher
import argparse
import imutils
import cv2

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-f", "--first", required=True,
	help="path to the first image")
ap.add_argument("-s", "--second", required=True,
	help="path to the second image")
ap.add_argument("-d", "--direction", choices=["h", "v"], required=True,
	help="direction of the images")
ap.add_argument("-o", "--output", help="path to the output image")
args = vars(ap.parse_args())

# load the two images and resize them to have a width of 400 pixels
# (for faster processing)
imageA = cv2.imread(args["first"])
imageB = cv2.imread(args["second"])
#imageA = imutils.resize(imageA, width=400)
#imageB = imutils.resize(imageB, width=400)

# stitch the images together to create a panorama
stitcher = Stitcher()
(result, vis) = stitcher.stitch([imageA, imageB], showMatches=True, horizontal=args["direction"] == "h")

# show the images
cv2.imshow("Image A", imageA)
cv2.imshow("Image B", imageB)
cv2.imshow("Keypoint Matches", vis)


# https://stackoverflow.com/questions/13538748/crop-black-edges-with-opencv
gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
_, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)

_img, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnt = contours[0]
x, y, w, h = cv2.boundingRect(cnt)

crop = result[y:y+h ,x:x+w]

cv2.imshow("Result", result)
cv2.imshow("Crop", crop)
cv2.waitKey(0)

if args["output"]:
    cv2.imwrite(args["output"], crop)
