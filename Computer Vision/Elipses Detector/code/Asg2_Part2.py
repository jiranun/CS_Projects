__author__ = 'Jiranun.J'

import numpy as np
import cv2
from pylab import *
from numpy.linalg import eigh
import random
r = lambda: random.randint(0,255)

window_name = "ASG2 Part 2 : Ellipse Fitting"
DEFAULT_IMG_FILE = "ellipse.jpg"
FACTOR = 15.

class CEllipse:
    def __init__(self, centerx, centery, rad1, rad2, angle):
        self.center = (centerx,centery)
        self.axes = (rad1,rad2)
        self.angle = angle

    def getInfo(self):
        return self.center, self.axes, self.angle

def findEllipseCenter(l):
    a, b,c,d,f,g = l[0], l[1]/2, l[2], l[3]/2, l[4]/2, l[5]
    num = b*b-a*c
    x0=(c*d-b*f)/num
    y0=(a*f-b*d)/num
    return x0, y0

def findEllipseradius(l):
    a,b,c,d,f,g = l[0], l[1]/2, l[2], l[3]/2, l[4]/2, l[5]
    up = 2*(a*f*f+c*d*d+g*b*b-2*b*d*f-a*c*g)
    down1=(b*b-a*c)*( (c-a)*np.sqrt(1+4*b*b/((a-c)*(a-c)))-(c+a))
    down2=(b*b-a*c)*( (a-c)*np.sqrt(1+4*b*b/((a-c)*(a-c)))-(c+a))

    res1=np.sqrt(up/down1)
    res2=np.sqrt(up/down2)
    return res1, res2

def findEllipseRotation(l):
    a,b,c,d,f,g = l[0], l[1]/2, l[2], l[3]/2, l[4]/2, l[5]
    theta=(0.5*np.arctan(2*b/(a-c)))*180.0/np.pi
    return theta

if len(sys.argv) == 2:
    original_image = cv2.imread(sys.argv[1])
    # Check if the image can be read
    if original_image is None:
        print "ERROR :", sys.argv[1], "can not be read. Use \"" + DEFAULT_IMG_FILE + "\" instead!"
        # get default image instead
        original_image = cv2.imread(DEFAULT_IMG_FILE)
else:
    original_image = cv2.imread(DEFAULT_IMG_FILE)

gray = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray,(5,5),1)

if (np.average(gray) > 130):
    TEXT_COLOR = (0,0,0)
    TRESH_TYPE = cv2.THRESH_BINARY_INV
else:
    TEXT_COLOR = (255,255,255)
    TRESH_TYPE = cv2.THRESH_BINARY


ret1,thresh = cv2.threshold(gray,200,255,TRESH_TYPE)
kernel = np.ones((5,5),np.uint8)
thresh = cv2.dilate(thresh,kernel,iterations = 1)

contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
max_contour = max(contours, key=len)

amt_of_ellipses = 0
ellipses = []

if contours and len(max_contour) > 3:
    for contour in contours:
        if len(contour) < 3:
            continue;

        x = np.array([p[0][0] for p in contour])
        y = np.array([p[0][1] for p in contour])

        xmean = x.mean()
        ymean = y.mean()
        x -= xmean
        y -= ymean
        x /= FACTOR
        y /= FACTOR

        x = x[:,np.newaxis]
        y = y[:,np.newaxis]

        D =  np.hstack((x*x, x*y, y*y, x, y, np.ones_like(x)))
        S = np.dot(D.T,D)

        if np.linalg.det(S) == 0:
            continue;

        C = np.zeros([6,6])
        C[0,2] = C[2,0] = -2; C[1,1] = 1

        invSC = np.dot(inv(S), C)

        E, V =  eig(invSC)
        n = np.argmin(E)
        l = V[:,n]

        center_x, center_y = findEllipseCenter(l)
        rad1, rad2 = findEllipseradius(l)
        angle = findEllipseRotation(l)

        center_x = int(np.round(center_x*FACTOR + xmean))
        center_y = int(np.round(center_y*FACTOR + ymean))
        rad1 = int(np.round(rad1 * FACTOR))
        rad2 = int(np.round(rad2 * FACTOR))

        e = CEllipse(center_x, center_y, rad1, rad2, angle)
        ellipses.append(e)
        amt_of_ellipses += 1

    i = 0
    while True:

        output_img = original_image.copy()
        h = output_img.shape[0]/20
        e = ellipses[i].getInfo()
        center = e[0]
        rad = e[1]
        angle = e[2]

        cv2.ellipse(output_img, center, rad, angle, 0, 360, (r(),r(),r()),3)
        cv2.ellipse(output_img, center, (1,1), 0, 0, 360, (r(),r(),r()),5)

        cv2.putText(output_img, "** "+str(amt_of_ellipses)+" ellipse(s) found. **", (5,h), cv2.FONT_HERSHEY_PLAIN, 1.0, TEXT_COLOR,1)
        cv2.putText(output_img, "Ellipse : "+str(i+1), (5,2*h), cv2.FONT_HERSHEY_PLAIN, 1.0, TEXT_COLOR,1)
        cv2.putText(output_img, "Center : ("+str(center_x)+","+str(center_y)+")", (5,3*h), cv2.FONT_HERSHEY_PLAIN, 1.0, TEXT_COLOR)
        cv2.putText(output_img, "Axes : ("+str(rad1)+","+str(rad2)+")", (5,4*h), cv2.FONT_HERSHEY_PLAIN, 1.0, TEXT_COLOR)
        cv2.putText(output_img, "Angle : "+str(angle), (5,5*h), cv2.FONT_HERSHEY_PLAIN, 1.0, TEXT_COLOR)

        cv2.imshow("ASG2 Part2 : Ellipse Fitting"+str(amt_of_ellipses), output_img)

        i = ( i + 1 ) % amt_of_ellipses
        key = cv2.waitKey()
        if key == ord('h'):
            print "<ESC>: quit"
            print "'h' - help"
            print "'any key' - show next ellipse"
        if key == 27:
            break

# When everything done, release the capture
cv2.destroyAllWindows()