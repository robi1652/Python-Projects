import math
import numpy as np
import scipy
from skimage import filters
from skimage.measure import label
from skimage import morphology
import utils


def find_gradient(img):
    vert = filters.sobel_v(img)
    hori = filters.sobel_h(img)
    return np.subtract(vert, hori)

def find_barcode(img):    
    t = 25
    teed = filters.threshold_local(img, t)
    gradients = abs(find_gradient(teed))
    gradients = gradients * 255.0 / gradients.max()    
    blurred = filters.gaussian(gradients)
    thresholded = np.copy(blurred)
    thresholded[thresholded > 65] = 255
    thresholded[thresholded <= 65] = 0    
    closed = morphology.binary_closing(thresholded, morphology.disk(5))
    final = np.zeros([len(closed), len(closed[0])], dtype=np.uint8)
    final[closed == True] = 255
    final[closed == False] = 0
    return final

def getLargestCC(img):
    connComps = label(img)
    largestCC = connComps == np.argmax(np.bincount(connComps.flat)[1:])+1
    return largestCC

def getBarcode(original, connected):
    shape = connected.shape
    height = shape[0]
    width = shape[1]
    top = height
    bottom = 0
    left = width
    right = 0
    for i in range(width):
        for j in range(height):
            if connected[j][i] == 0:
                continue
            else:
                if j < top:
                    top = j
                if j > bottom:
                    bottom = j
                if i < left:
                    left = i
                if i > right:
                    right = i                
    barcodeWidth = right - left
    #barcodeHeight = bottom - top
    #for z in range(barcodeWidth):
    #   for x in range(1):
    #        original[top - x][left + z] = 0
    #        original[bottom + x][left + z] = 0
    #for c in range(barcodeHeight):
    #   for v in range(1):
    #        original[top + c][left - v] = 0
    #       original[top + c][right + v] = 0
            
    #utils.show_image(original)

    startingY = top + ((bottom-top)/2)
    startingY = int(startingY)    
    code = np.array(barcodeWidth)    
    for a in range(barcodeWidth):
        curr = original[startingY][left + a]
        code = np.append(code, curr)  

    code[code > 87] = 255
    code[code <= 87] = 0   

    count = 0
    for q in range(len(code)):
        if code[q] == 255:
            count = count+1
        else:
            break
    code = code[count:]
    return code

def readBarcode(barcode):
    a = 0
    currSegment = []
    final = []
    flipped = False
    bar1 = 0
    bar2 = 0
    bar3 = 0
    barNum = 0
    for q in range(len(barcode)):
        index = q
        while barcode[index] == barcode[index+1]:
            if barNum == 0:
                bar1 = bar1 + 1
            elif barNum == 1:
                bar2 = bar2 + 1
            elif barNum == 2:
                bar3 = bar3 + 1
            index = index + 1
        if barNum == 0:
            bar1 = bar1 + 1
        elif barNum == 1:
            bar2 = bar2 + 1
        elif barNum == 2:
            bar3 = bar3 + 1
            
        barNum = barNum + 1
        
        if barNum == 0:
            q = q + bar1
        elif barNum == 1:
            q = q + bar2
        elif barNum == 2:
            q = q + bar3
        else: 
            break

    primUnit = (bar1 + bar2 + bar3) / 3
    primUnit = int(round(primUnit))
    startIndex = primUnit * 3
#Reading the lines
    barcode = barcode[startIndex:]    
    print(barcode)    

    for i in range(0, len(barcode), 7*primUnit):
        if len(final) == 6:
            i = i + (3*primUnit)
        if len(final) == 12:
            break
        for h in range(0, 7*primUnit, primUnit):
            try:
                currSegment.append(barcode[i+h])
            except:
                break
            
        if not final:
            if currSegment[0] == 0:
                flipped = True
        
        if currSegment == [255, 255, 0, 0, 255, 255, 0]:
            #Number is 1
            final.append(1)
            flipped = False
        elif currSegment == [255, 255, 0, 255, 255, 0, 0]:
            #number is 2
            final.append(2)
        elif currSegment == [255, 0, 0, 0, 0, 255, 0]:
            #number is 3
            final.append(3)
        elif currSegment == [255, 0, 255, 255, 255, 0, 0]:
            #number is 4
            final.append(4)
        elif currSegment == [255, 0, 0, 255, 255, 255, 0]:
            #number is 5
            final.append(5)
        elif currSegment == [255, 0, 255, 0, 0, 0, 0]:
            #number is 6
            final.append(6)
        elif currSegment == [255, 0, 0, 0, 255, 0, 0]:
            #number is 7
            final.append(7)
        elif currSegment == [255, 0, 0, 255, 0, 0, 0]:
            #number is 8
            final.append(8)
        elif currSegment == [255, 255, 255, 0, 255, 0, 0]:
            #number is 9
            final.append(9)
        elif currSegment == [255, 255, 255, 0, 0, 255, 0]:
            #number is 0
            final.append(0)
        elif currSegment == [0, 0, 255, 255, 0, 0, 255]:
            #number is 1 - right side
            final.append(1)
            flipped = True
        elif currSegment == [0, 0, 255, 0, 0, 255, 255]:
            #number is 2 - right side
            final.append(2)
        elif currSegment == [0, 255, 255, 255, 255, 0, 255]:
            #number is 3 - right side
            final.append(3)
        elif currSegment == [0, 255, 0, 0, 0, 255, 255]:
            #number is 4 - right side
            final.append(4)
        elif currSegment == [0, 255, 255, 0, 0, 0, 255]:
            #number is 5 - right side
            final.append(5)
        elif currSegment == [0, 255, 0, 255, 255, 255, 255]:
            #number is 6 - right side
            final.append(6)
        elif currSegment == [0, 255, 255, 255, 0, 255, 255]:
            #number is 7 - right side
            final.append(7)
        elif currSegment == [0, 255, 255, 0, 255, 255, 255]:
            #number is 8 - right side
            final.append(8)
        elif currSegment == [0, 0, 0, 255, 0, 255, 255]:
            #number is 9 - right side
            final.append(9)
        elif currSegment == [0, 0, 0, 255, 255, 0, 255]:
            #number is 0 - right side
            final.append(0)
        else:
            a = a
            #print('broke')
            final.append('broke')
        #print(currSegment)
        currSegment = []
        
    if flipped == True:
        final.reverse()

    return final
                
        
        
    
imgPath = r'C:\Users\Blake\Desktop\Vision\Lab 6\images\easy.jpg'
img = utils.read_image_as_bw(imgPath)
img = np.rot90(img, 3)
barcode = find_barcode(img)  
connComp = getLargestCC(barcode)
bar = getBarcode(img, connComp)
print(readBarcode(bar))



