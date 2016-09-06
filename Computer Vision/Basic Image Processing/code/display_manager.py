__author__ = 'Jiranun.J'

import cv2
import numpy as np
from pylab import *

window_name = "myfile.jpg"
resize_factor = 1.0
original_image = np.zeros((100, 100, 3), np.uint8)  # initialize blank image
current_image = original_image
bw_image = np.zeros((100, 100), np.uint8)


def setWindowName(strWinName):
    global window_name
    window_name = strWinName

def setWindowSizeFactor(factor):
    global resize_factor
    resize_factor = factor

def showResizedImage(img):
    global resize_factor
    # resized image will be shown only (NOT effect to the original image)
    cv2.imshow(window_name, cv2.resize(img, (int(img.shape[1] * resize_factor), int(img.shape[0] * resize_factor))))

def setOriginalImage(img):
    global original_image
    original_image = img

def setCurrentImage(img = None):
    global current_image, original_image
    if img is None:
        current_image = original_image
    else:
        current_image = img
    showResizedImage(current_image)

def saveCurrentImage():
    global current_image
    cv2.imwrite("out.jpg", current_image)

def makeGrayScaleByOpenCV():
    global original_image
    setCurrentImage(cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY))

def makeGrayScaleByManual():
    global original_image
    gImg = np.ones((original_image.shape[0], original_image.shape[1]), np.float32)
    for i in range(0, original_image.shape[0], 1):
        for j in range(0, original_image.shape[1], 1):

            # NTSC conversion formula
            gImg[i][j] = 0.587 * float(original_image[i][j][0]) \
                         + 0.144 * float(original_image[i][j][1]) \
                         + 0.299 * float(original_image[i][j][2])

    normalized_image = np.uint8((gImg[:,:] - gImg.min()) * 255.0 / (gImg.max() - gImg.min()))
    setCurrentImage(normalized_image)

def makeRGBChannelImage(ch):
    global original_image
    output_img = np.ones((original_image.shape[0], original_image.shape[1], 3), np.uint8)
    b, g, r = cv2.split(original_image)

    if ch == 0:
        output_img[:,:,0] = original_image[:,:,0]
    elif ch == 1:
        output_img[:,:,1] = original_image[:,:,1]
    else:
        output_img[:,:,2] = original_image[:,:,2]

    setCurrentImage(output_img)

def calGaussian(x,y,sigma):
    return np.exp( (-1.0) * (np.power(x, 2.0)+np.power(y, 2.0)) / (2.0 * np.power(sigma, 2.0)))

def getGuessienFilter(sigma):
    filter_size = sigma * 5
    middle_position = filter_size / 2
    kernel = array([[calGaussian( i-middle_position, j-middle_position, sigma )
                     for i in range(0, filter_size)] for j in range(filter_size - 1 , -1, -1)])
    return kernel[:,:]/kernel.sum()

def sliderHandlerForOpenCVSmoothing(sigma):
    global bw_image
    if sigma == 0:
        setCurrentImage(bw_image)
    else:
        sigma = (sigma - 1) * 2 + 1
        kernel = getGuessienFilter(sigma)
        setCurrentImage(cv2.filter2D(bw_image, -1, kernel))  # convolve the image


def smoothByOpenCV():
    global bw_image, original_image
    bw_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    setCurrentImage(bw_image)
    cv2.createTrackbar('Smooth (OpenCV)', window_name, 0, 5, sliderHandlerForOpenCVSmoothing)


def sliderHandlerForSmoothingConvolution(sigma):
    global bw_image
    if sigma == 0:
        setCurrentImage(bw_image)
    else:
        sigma = (sigma - 1) * 2 + 1
        middle_position = (sigma * 5) / 2
        kernel = getGuessienFilter(sigma)
        outputImg = np.ones((bw_image.shape[0], bw_image.shape[1]), np.uint8)
        # convolve the image - use middle_position to ignore the boundaries
        for i in range(middle_position, bw_image.shape[0] - middle_position, 1):
            for j in range(middle_position, bw_image.shape[1] - middle_position, 1):
                convolved_array = bw_image[i - middle_position: i + middle_position + 1,
                                  j - middle_position: j + middle_position + 1] * kernel
                outputImg[i][j] = convolved_array.sum()
        setCurrentImage(outputImg)


def smoothByManualConvolution():
    global bw_image, original_image
    bw_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    setCurrentImage(bw_image)
    cv2.createTrackbar('Smooth (Manual)', window_name, 0, 5, sliderHandlerForSmoothingConvolution)

def calGaussianDerivative(x, sigma):
    return ( (-x) / np.power(sigma, 2.0)) * np.exp( (-1.0) * np.power(x, 2.0) / (2.0 * np.power(sigma, 2.0)))


def getDerivativesofImage(isX):
    global original_image
    float_of_image = np.array(cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY), np.float32)
    if isX:
        kernel = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], np.float32)
    else:
        kernel = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]], np.float32)
    return cv2.filter2D(float_of_image, -1, kernel)

def showDerivativesofImage(isX):
    result = getDerivativesofImage(isX)
    normalized_image = np.uint8((result[:,:] - result.min()) * 255.0 / (result.max() - result.min()))
    setCurrentImage(normalized_image)


def showMagnitudeofGradient():
    Xderv_img = getDerivativesofImage(True)
    Yderv_img = getDerivativesofImage(False)

    gradient_magnitude = np.sqrt((np.power(Xderv_img[:,:], 2.0) + np.power(Yderv_img[:,:], 2.0)))
    normalized_image = np.uint8((gradient_magnitude[:,:] - gradient_magnitude.min()) * 255.0
                                / (gradient_magnitude.max() - gradient_magnitude.min()))
    setCurrentImage(normalized_image)


def sliderHandlerForVector(vector_pace):
    global original_image
    output_img = original_image.copy()
    Xderv_img = getDerivativesofImage(True)
    Yderv_img = getDerivativesofImage(False)
    vector_pace = (vector_pace + 2)
    vector_max_length = min(original_image.shape[0], original_image.shape[1]) * 0.05
    vector_length_factor = vector_max_length / np.max([np.sqrt((np.power(Xderv_img[:,:], 2.0) + np.power(Yderv_img[:,:], 2.0)))])
    for i in range(0, original_image.shape[1], vector_pace):
        for j in range(0, original_image.shape[0], vector_pace):
            vector = ( int(i + Xderv_img[j][i] * vector_length_factor), int(j + Yderv_img[j][i] * vector_length_factor) )
            cv2.line(output_img, (i,j), vector, (0,0,0))
            cv2.line(output_img, (i,j), (i,j), (0,0,255))
    setCurrentImage(output_img)


def addVectors():
    cv2.createTrackbar('Pace', window_name, 0, 15, sliderHandlerForVector)


def rotateHandler(degree):
    global bw_image
    angle = degree * np.pi
    rows = bw_image.shape[0]
    cols = bw_image.shape[1]
    matrix = cv2.getRotationMatrix2D((cols / 2, rows / 2), angle, 1)
    setCurrentImage(cv2.warpAffine(bw_image, matrix, (cols, rows)))

def rotateImage():
    global bw_image, original_image
    bw_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    setCurrentImage(bw_image)
    cv2.createTrackbar('Degree', window_name, 0, 125, rotateHandler)
