import utils
import numpy as np
import sys

fileName = sys.argv[1]
outPath = sys.argv[2]
kInput = sys.argv[3]
kInput = int(kInput)

oldArray = utils.read_image_as_bw(fileName)
newArray = oldArray.copy()
shape = oldArray.shape
height = shape[0]
width = shape[1]
kBound = int(kInput/2)
kTotal = kInput^2

for i in range(height):
    for j in range(width):
        kernel = []
        for kV in range(kInput):
            for kH in range(kInput):
                try:    
                    kernel.append(oldArray[i - 1 + kV][j - 1 + kH])
                except:
                    continue
        newArray[i][j] = np.mean(kernel)
        
        
outPath = outPath + fileName[:-4] + '_clean.jpg'

utils.show_image(newArray)
utils.save_bw_image(newArray, outPath)


        