__author__ = 'Jiranun.J'

import display_manager as dpm

CURRENT_CHANNEL = 0  # 0:BLUE, 1:GREEN, 2:RED

def i():
    dpm.setCurrentImage()

def w():
    dpm.saveCurrentImage()

def g():
    dpm.makeGrayScaleByOpenCV()

def G():
    dpm.makeGrayScaleByManual()

def c():
    global CURRENT_CHANNEL
    dpm.makeRGBChannelImage(CURRENT_CHANNEL)
    CURRENT_CHANNEL = (CURRENT_CHANNEL + 1) % 3

def s():
    dpm.smoothByOpenCV()

def S():
    dpm.smoothByManualConvolution()

def x():
    dpm.showDerivativesofImage(True)

def y():
    dpm.showDerivativesofImage(False)

def m():
    dpm.showMagnitudeofGradient()

def p():
    dpm.addVectors()

def r():
    dpm.rotateImage()

def h():
    print "<ESC>: quit"
    print "'i' - reload image"
    print "'x' - save the current image into the file out.jpg"
    print "'g' - convert the image to grayscale by openCV function"
    print "'G' - convert the image to grayscale by manual convolution"
    print "'c' - cycle through the color channels"
    print "'s' - smooth the grayscale image by openCV function"
    print "'S' - smooth the grayscale image by manual convolution"
    print "'x' - convolve the grayscale image with an x derivative filter"
    print "'y' - convolve the grayscale image with an y derivative filter"
    print "'m' - show magnitude of the gradient"
    print "'p' - plot the gradient vectors of the image every N pixels"
    print "'r' - rotate the grayscale image"
    print "'h' - help"

