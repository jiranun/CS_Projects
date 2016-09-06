__author__ = 'Jiranun.J'

import cv2
import numpy as np
from pylab import *

CALIBRATION_TARGET_IMG_FILE = "calibration_target.jpg"
OBJECT_POINTS_FILE = 'object_points.txt'
CORRESPONDENCE_FILE = 'correspondence_file.txt'

# mouse callback function
def mouse_callback(event,x,y,flags,param):
    global original_img, amt_marked_point, obj_pnts_file, correspondence_file
    if event == cv2.EVENT_LBUTTONDOWN:
        if (amt_marked_point < amt_of_obj_points):
            cv2.circle(original_img, (x, y), 2, (100,0,100), 2)
            cv2.putText(original_img, str(amt_marked_point+1), (x,y-4), cv2.FONT_HERSHEY_PLAIN, 1.0, (100,0,100), 1)
            amt_marked_point += 1
            corresponding_points = obj_pnts_file.readline().rstrip('\n')
            corresponding_points += ' '+str(x)+' '+str(y)+'\n'
            correspondence_file.write(corresponding_points)


if len(sys.argv) == 3:
    OBJECT_POINTS_FILE = sys.argv[1]
    original_img = cv2.imread(sys.argv[2])
    amt_of_obj_points = np.sum(1 for line in open(OBJECT_POINTS_FILE))
    obj_pnts_file = open(OBJECT_POINTS_FILE,'r')
    # Check if the image can be read
    if original_img is None:
        print "ERROR :", sys.argv[2], "can not be read. Use \"" + CALIBRATION_TARGET_IMG_FILE + "\" instead!"
        # get default image instead
        original_img = cv2.imread(CALIBRATION_TARGET_IMG_FILE)
else:
    original_img = cv2.imread(CALIBRATION_TARGET_IMG_FILE)
    amt_of_obj_points = np.sum(1 for line in open(OBJECT_POINTS_FILE))
    obj_pnts_file = open(OBJECT_POINTS_FILE,'r')

amt_marked_point = 0
correspondence_file = open(CORRESPONDENCE_FILE,'w')

cv2.namedWindow('image')
cv2.setMouseCallback('image',mouse_callback)

while(1):
    img = original_img.copy()
    h = img.shape[0]/20

    if (amt_marked_point < amt_of_obj_points):
        txt_amt_points = "Point : "+str(amt_marked_point+1)+"/"+str(amt_of_obj_points)
    else:
        txt_amt_points = "All "+str(amt_of_obj_points)+" points have been marked. Press <ESC> to exit the program."

    cv2.putText(img, txt_amt_points, (5,h), cv2.FONT_HERSHEY_PLAIN, 1.0, (125,125,125), 2)
    cv2.imshow('image',img)

    key = cv2.waitKey(20)
    if key == ord('h'):
        print "<ESC>: quit"
        print "'o' - print the object points text filename"
        print "'h' - help"
    if key == ord('o'):
        print "Object points filename is", OBJECT_POINTS_FILE
    if key == 27:
        break

obj_pnts_file.close()
correspondence_file.close()
cv2.destroyAllWindows()