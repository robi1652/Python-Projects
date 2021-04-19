import utils
import numpy as np
import sys

fileName = sys.argv[1]

oldArray = utils.read_image_as_bw(fileName)
newArray = np.copy(oldArray)

shape = oldArray.shape
height = shape[0]
width = shape[1]

for i in range(height):
    for j in range(width):
        newArray[i][j] = oldArray[-i][j]
        

outPath = 'images/output/' + fileName

utils.show_image(newArray)
utils.save_bw_image(newArray, outPath)
