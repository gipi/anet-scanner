'''
Simple program to stitch together images captured with a microscope
'''
import os
import sys

import cv2
import imutils
import numpy as np


def load_images(start, end, directory='shoots/', fmt='frame_%02d_%02d.png', size=None):
	'''
	Return a list of OpenCV images loaded from a directory.
	
	start and end are couples indicating the interval for the x, y ranges.
	'''
	images = []
	for x in xrange(start[0], end[0] + 1):
		images_y = []
		for y in xrange(start[1], end[1] + 1):
			filepath = os.path.join(directory, fmt % (x, y))
			if not os.path.exists(filepath):
				raise Exception('%s doesnt exist' % filepath)
			image = cv2.imread(filepath)
			images_y.append(image if not size else imutils.resize(image, size))

		images.append(images_y)

	return images

def image_create(width, height):
	return np.zeros((height,width,3), np.uint8)

if __name__ == '__main__':
	start = int(sys.argv[1]), int(sys.argv[2])
	end   = int(sys.argv[3]), int(sys.argv[4])
	deltaX = int(sys.argv[5])
	deltaY = int(sys.argv[6])

	print locals()

	size = 400

	images = load_images(start, end, size=size)

	columns = (end[0] - start[0] + 1)
	rows    = (end[1] - start[1] + 1)
	print 'creating canvas with shape (%d, %d)' % (columns, rows)
	#canvas  = image_create(images[0][0].shape[1]*columns, images[0][0].shape[0]*rows)
	canvas  = image_create(size*columns, size*rows)

	# take the first image as standard size
	shape = images[0][0].shape

	for idx_x in xrange(end[0], start[0] - 1, -1):
		images_row = images[idx_x]
		for idx_y in xrange(end[1], start[1] - 1, -1):
			src = images_row[idx_y]
			#M = cv2.getRotationMatrix2D((0, 0), -4, 1)
			#src = cv2.warpAffine(src, M, (src.shape[1], src.shape[0]))
			print 'shape at %d %d: (%d, %d)' % (idx_x, idx_y, shape[0], shape[1])
			#import ipdb;ipdb.set_trace()
			x = idx_x*shape[1] + deltaX * idx_y
			if x < 0: x= 0
			y = canvas.shape[0] - (idx_y + 1)*(shape[0]) + idx_y*deltaY

			canvas[y:y + shape[0], x:x + shape[1]] = src

	# https://stackoverflow.com/questions/13538748/crop-black-edges-with-opencv
	gray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
	_, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)

	_img, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	cnt = contours[0]
	x, y, w, h = cv2.boundingRect(cnt)

	crop = canvas[y:y+h ,x:x+w]

	cv2.imshow('Editing window', crop)
	cv2.waitKey(0)
