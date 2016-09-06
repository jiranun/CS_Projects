__author__ = 'Jiranun.J'

import cv2
import sys
import keys_manager as km
import display_manager as dpm


###### Global Variables #######
DEFAULT_IMG_FILE = "myfile.jpg"
MAXIMUM_SIDE_WIDTH = 1000


###### Get Image ######
window_name = DEFAULT_IMG_FILE

# check if image name is specified in command line
if len(sys.argv) == 2:
    original_image = cv2.imread(sys.argv[1])
    window_name = sys.argv[1]

    # Check if the image can be read
    if original_image is None:
        print "ERROR :", sys.argv[1], "can not be read. Use \"" + DEFAULT_IMG_FILE + "\" instead!"
        # get default image instead
        original_image = cv2.imread(DEFAULT_IMG_FILE)
        window_name = DEFAULT_IMG_FILE

# capture an image from the camera if image name is not specified
elif len(sys.argv) < 2:
    cap = cv2.VideoCapture(0)
    retval, original_image = cap.read()
    window_name = "From Your Camera"

# otherwise, get default image
else:
    original_image = cv2.imread(DEFAULT_IMG_FILE)

# Calculate resize factor in case image is too big to show
# resize factor will depend on MAXIMUM_SIDE_WIDTH
max_side = max(original_image.shape[0], original_image.shape[1])
if max_side > MAXIMUM_SIDE_WIDTH:
    dpm.setWindowSizeFactor(1.0 / (float(max_side) / float(MAXIMUM_SIDE_WIDTH)))

# Add image dimention to the window name
window_name = window_name + ' - ' + str(original_image.shape[1]) + 'x' + str(original_image.shape[0])

dpm.setOriginalImage(original_image)
dpm.setWindowName(window_name)
dpm.setCurrentImage()

# ensure that the image was read properly
if original_image is not None:
    while (True):

        key = cv2.waitKey(10)

        if key == ord('i'): km.i()
        if key == ord('w'): km.w()
        if key == ord('g'): km.g()
        if key == ord('G'): km.G()
        if key == ord('c'): km.c()
        if key == ord('s'): km.s()
        if key == ord('S'): km.S()
        if key == ord('x'): km.x()
        if key == ord('y'): km.y()
        if key == ord('m'): km.m()
        if key == ord('p'): km.p()
        if key == ord('r'): km.r()
        if key == ord('h'): km.h()
        if key == 27:
            cv2.destroyWindow(window_name)
            break
