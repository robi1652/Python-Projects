import math
import numpy as np
import utils
import scipy
from scipy import signal

def gaussian_blur(img):
    kernel = np.array([[1, 2, 1],[2, 4, 2],[1, 2, 1]])
    kernel = kernel.astype(np.float)
    return signal.correlate2d(img, ((1/16)*kernel))

def mean_blur(img, n):
    kernel = np.ones([n, n])
    return signal.correlate2d(img, kernel)

def central_diff_edges_x_and_y(img):
    kernelX = [[-1,0,1]]
    kernelY = [[-1],[0],[1]] 
    X_edges = signal.correlate2d(img, kernelX, "same")
    Y_edges = signal.correlate2d(img, kernelY, "same")    
    return X_edges, Y_edges

def sobel_edges_x_and_y(img):
    kernelX = [[1,2,1],[0,0,0],[-1,-2,-1]]
    kernelY = [[-1,0,1],[-2,0,2],[-1,0,1]]
    X_edges = signal.correlate2d(img, kernelX)
    Y_edges = signal.correlate2d(img, kernelY)
    return X_edges, Y_edges

def compute_edge_magnitudes(X_edges, Y_edges):
    return np.sqrt(np.square(X_edges)+np.square(Y_edges))

def compute_edge_directions(X_edges, Y_edges):
    directions = np.arctan2(Y_edges, X_edges)
    directions = 45 * np.round(directions + 180/45)
    return np.rad2deg(directions)

def suppress_edges(edge_magnitudes, edge_direction):
    shape = edge_magnitudes.shape
    height = shape[0]
    width = shape[1]
    suppressed = np.copy(edge_magnitudes)
    for i in range(width):
        for j in range(height):
            mag = edge_magnitudes[j][i]
            dire = edge_direction[j][i]
            comp = 0
            if dire == 0.0:
                comp = edge_magnitudes[j][i+1]
            elif dire == 45.0:
                comp = edge_magnitudes[j+1][i+1]
            elif dire == 90.0:
                comp = edge_magnitudes[j+1][i]
            elif dire == 135.0:
                comp = edge_magnitudes[j+1][i-1]
            elif dire == 180.0:
                comp = edge_magnitudes[j][i-1]
            elif dire == 225.0:
                comp = edge_magnitudes[j-1][i-1]
            elif dire == 270.0:
                comp = edge_magnitudes[j+1][i]
            elif dire == 315.0:
                comp = edge_magnitudes[j-1][i+1]
            elif dire == 360.0:
                comp = edge_magnitudes[j][i+1]        
            if mag > comp:
                suppressed[j][i] = 0
            else:
                suppressed[j][i] = 1
    return suppressed

def find_edges(img, method, blur, t):
    if blur == 'gaussian3':
        img = gaussian_blur(img)
    elif blur.startswith("mean"):
        n = blur[4:]
        n = int(n)
        img = mean_blur(img, n)
        
    if method == 'sobel':
        X_edges, Y_edges = sobel_edges_x_and_y(img)
    elif method == 'central_difference':
        X_edges, Y_edges = central_diff_edges_x_and_y(img)
        
    magnitudes = compute_edge_magnitudes(X_edges, Y_edges)
    directions = compute_edge_directions(X_edges, Y_edges)
    img = suppress_edges(magnitudes, directions)
    magnitudes[img == 1] = 0
    magnitudes = magnitudes * (255.0 / magnitudes.max())
        
    threshImg = np.copy(magnitudes)
    threshImg[threshImg > t] = 255
    threshImg[threshImg < t] = 0            
    return threshImg

path = r'C:\Users\Blake\Desktop\Vision\Lab 4\images\input\Piano.jpg'
img = utils.read_image_as_bw(path)

img = find_edges(img, 'sobel', 'gaussian3', 40)

utils.show_image(img)

#savePath = path = r'C:\Users\Blake\Desktop\Vision\Lab 4\images\output\Piano_edges.jpg'
#utils.save_bw_image(img, savePath)