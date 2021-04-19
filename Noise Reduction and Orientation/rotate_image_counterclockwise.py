import utils
import numpy as np
import sys

fileName = sys.argv[1]

oldArray = utils.read_image_as_bw(fileName)
shape = oldArray.shape
height = shape[0]
width = shape[1]
newArray = np.zeros([width, height], dtype=np.uint8)

for i in range(width):
    for j in range(height):
        newArray[i][height - j - 1] = oldArray[height - j - 1][width - i - 1]

outPath = 'images/output/' + fileName

utils.show_image(newArray)
utils.save_bw_image(newArray, outPath)

