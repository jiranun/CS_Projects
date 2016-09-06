__author__ = 'Jiranun.J'

import numpy as np
import cv2
from pylab import *
import ConfigParser
import random
r = lambda: random.randint(0,255)

window_name_L = "Left Image"
window_name_R = "Right Image"
DEFAULT_IMG_FILE_L = "corridor-l.tiff"
DEFAULT_IMG_FILE_R = "corridor-r.tiff"
INIT_POINTS_FILE = ""

config = ConfigParser.RawConfigParser()
config.read('Asg4.config')

nConfigInitPoints = config.getint('ASG4', 'INIT_POINTS')
nInitPoints = max(8,nConfigInitPoints)

L_init_points=[]
R_init_points=[]
L_point_left = nInitPoints
R_point_left = nInitPoints
alreay_init = False
F = np.array([])
exit_the_program = False


if len(sys.argv) == 4:
    original_image_L = cv2.imread(sys.argv[1])
    original_image_R = cv2.imread(sys.argv[2])
    INIT_POINTS_FILE = sys.argv[3]
elif len(sys.argv) == 3:
    original_image_L = cv2.imread(sys.argv[1])
    original_image_R = cv2.imread(sys.argv[2])
else:
    original_image_L = cv2.imread(DEFAULT_IMG_FILE_L)
    original_image_R = cv2.imread(DEFAULT_IMG_FILE_R)


def restart_all():
    global img_L, img_R, L_init_points, R_init_points, L_point_left, R_point_left, alreay_init, nInitPoints
    img_L = original_image_L.copy()
    img_R = original_image_R.copy()
    L_init_points=[]
    R_init_points=[]
    L_point_left = nConfigInitPoints
    R_point_left = nConfigInitPoints
    nInitPoints = nConfigInitPoints
    alreay_init = False
    print "Please click",nInitPoints,"corresponding points on left and right images."


def clear_images():
    global img_L, img_R
    img_L = original_image_L.copy()
    img_R = original_image_R.copy()


clear_images()


if INIT_POINTS_FILE != "":
    f = open(INIT_POINTS_FILE,'r')
    nPoints = 0
    for line in f:
        p = line.rstrip('\n').split()
        nPoints += 1
        L_init_points.append((float(p[0]),float(p[1])))
        R_init_points.append((float(p[2]),float(p[3])))

    if nPoints >= 8:
        nInitPoints = nPoints
        L_point_left = 0
        R_point_left = 0
        alreay_init = True
    else:
        restart_all()
else:
    restart_all()


def draw_line(p, side):
    global F, img_L, img_R
    rand_color = (r(),r(),r())

    if side == 'right':
        line = np.dot(F.T,p)
        [a,b,c] = line
        line_angle = np.arctan(b/a)

        if np.abs(line_angle) < 1.:
            for y in range(img_R.shape[0]):
                x = int(np.round((-c-b*y)/a))
                if x in range(img_R.shape[1]):
                     cv2.ellipse(img_R, (x,y), (0,0), 0, 0, 360, rand_color, 2)
        else:
            for x in range(img_R.shape[1]):
                y = int(np.round((-c-a*x)/b))
                if y in range(img_R.shape[0]):
                     cv2.ellipse(img_R, (x,y), (0,0), 0, 0, 360, rand_color, 2)

        cv2.ellipse(img_L, (int(p[0]),int(p[1])), (1,1), 0, 0, 360, rand_color, 2)

    else :
        line = np.dot(F,p)
        [a,b,c] = line
        line_angle = np.arctan(b/a)

        if np.abs(line_angle) < 1.:
            for y in range(img_L.shape[0]):
                x = int(np.round((-c-b*y)/a))
                if x in range(img_L.shape[1]):
                     cv2.ellipse(img_L, (x,y), (0,0), 0, 0, 360, rand_color, 2)
        else:
            for x in range(img_L.shape[1]):
                y = int(np.round((-c-a*x)/b))
                if y in range(img_L.shape[0]):
                     cv2.ellipse(img_L, (x,y), (0,0), 0, 0, 360, rand_color, 2)

        cv2.ellipse(img_R, (int(p[0]),int(p[1])), (1,1), 0, 0, 360, rand_color, 2)


# mouse callback function
def mouse_callback_L(event,x,y,flags,param):
    global img_L, L_init_points, L_point_left, R_point_left, alreay_init
    if event == cv2.EVENT_LBUTTONDOWN:
        if not alreay_init:
            if L_point_left > 0:
                L_init_points.append((float(x),float(y)))
                cv2.ellipse(img_L, (x,y), (1,1), 0, 0, 360, 0, 2)
                cv2.putText(img_L, str(nInitPoints+1-L_point_left),
                            (x,y-4), cv2.FONT_HERSHEY_PLAIN, 1.0, (0,0,0), 1)
                L_point_left -= 1

            if L_point_left == 0 and R_point_left == 0:
                alreay_init = True
        else:
            draw_line(np.array([float(x),float(y),1.]),'right')


# mouse callback function
def mouse_callback_R(event,x,y,flags,param):
    global img_R, R_init_points, L_point_left, R_point_left, alreay_init
    if event == cv2.EVENT_LBUTTONDOWN:
        if not alreay_init:
            if R_point_left > 0:
                R_init_points.append((float(x),float(y)))
                cv2.ellipse(img_R, (x,y), (1,1), 0, 0, 360, 0, 2)
                cv2.putText(img_R, str(nInitPoints+1-R_point_left), (x,y-4), cv2.FONT_HERSHEY_PLAIN, 1.0, (0,0,0), 1)
                R_point_left -= 1

            if  L_point_left == 0 and R_point_left == 0:
                alreay_init = True
        else:
            draw_line(np.array([float(x),float(y),1.]),'left')


cv2.namedWindow(window_name_L)
cv2.setMouseCallback(window_name_L,mouse_callback_L)
cv2.namedWindow(window_name_R)
cv2.setMouseCallback(window_name_R,mouse_callback_R)

while not exit_the_program:

    while not alreay_init:

        cv2.imshow(window_name_L, img_L)
        cv2.imshow(window_name_R, img_R)

        key = cv2.waitKey(1)
        if key == ord('h'):
            print "Number of init points could be configured in Asg4.config"
            print "Special key :"
            print "\t<ESC>: quit the program"
            print "\t'r' - restart setting corresponding points"
            print "\t'h' - help"
        if key == ord('r'):
            restart_all()
            break
        if key == 27:
            exit_the_program = True
            break

    if not alreay_init:
        continue

    # normalize points
    mean_L = (np.average([x for (x,y) in L_init_points]), np.average([y for (x,y) in L_init_points]))
    var_L = (var([x for (x,y) in L_init_points]), var([y for (x,y) in L_init_points]))
    norm_left_points = np.array([ ((p[0] - mean_L[0])/var_L[0],(p[1] - mean_L[1])/var_L[1]) for p in L_init_points], np.float32)
    v_mat = np.array([[1./var_L[0],0.,0.],[0.,1./var_L[1],0.],[0.,0.,1.]])
    m_mat = np.array([[1.,0.,-mean_L[0]],[0.,1.,-mean_L[1]],[0.,0.,1.]])
    M_L = np.dot(v_mat, m_mat)

    mean_R = (np.average([x for (x,y) in R_init_points]), np.average([y for (x,y) in R_init_points]))
    var_R = (var([x for (x,y) in R_init_points]), var([y for (x,y) in R_init_points]))
    norm_right_points = np.array([ ((p[0] - mean_R[0])/var_R[0],(p[1] - mean_R[1])/var_R[1]) for p in R_init_points], np.float32)
    v_mat = np.array([[1./var_R[0],0.,0.],[0.,1./var_R[1],0.],[0.,0.,1.]])
    m_mat = np.array([[1.,0.,-mean_R[0]],[0.,1.,-mean_R[1]],[0.,0.,1.]])
    M_R = np.dot(v_mat, m_mat)

    # build Fundamental matrix (F') by init points by normalized points
    A = np.array([[xl*xr, xl*yr, xl, yl*xr, yl*yr, yl, xr, yr, 1.]
                  for ((xl,yl),(xr,yr)) in zip(norm_left_points, norm_right_points)])
    U, D, VT = np.linalg.svd(A)
    F_p = VT[-1,:]
    F_p = np.array([[F_p[0],F_p[1],F_p[2]],[F_p[3],F_p[4],F_p[5]],[F_p[6],F_p[7],F_p[8]]])

    # Enforcing rank 2 contraint F'
    U, D, VT = np.linalg.svd(F_p)
    D[np.argmin(D)] = 0
    F_p = np.dot(U,np.dot(np.diag(D),VT))

    # Compute F from F'
    F = np.dot(M_L.T, np.dot(F_p, M_R))

    clear_images()

    #Find Epipoles
    U, D, VT = np.linalg.svd(F.T)
    last_col_u = U[:,-1]
    e_r = (int(np.round(last_col_u[0]/last_col_u[2])),int(np.round(last_col_u[1]/last_col_u[2])))
    last_col_v = VT[-1,:]
    e_l = (int(np.round(last_col_v[0]/last_col_v[2])),int(np.round(last_col_v[1]/last_col_v[2])))

    print "Estimated Fundamental Matrix : "
    print F
    print "The coordinates of the left epipole :", e_r
    print "The coordinates of the right epipole :", e_l

    # drawing epipoles
    cv2.ellipse(img_R, e_r, (2,2), 0, 0, 360, (255,255,255), 4)
    cv2.ellipse(img_L, e_l, (2,2), 0, 0, 360, (255,255,255), 4)
    cv2.ellipse(img_R, e_r, (1,1), 0, 0, 360, (0,0,255), 2)
    cv2.ellipse(img_L, e_l, (1,1), 0, 0, 360, (0,0,255), 2)

    while not exit_the_program:

        cv2.imshow(window_name_L, img_L)
        cv2.imshow(window_name_R, img_R)

        key = cv2.waitKey(1)
        if key == ord('h'):
            print "<ESC>: quit the program"
            print "'r' - re-init points"
            print "'c' - clear images"
            print "'e' - draw epipoles"
            print "'h' - help"
        if key == ord('r'):
            restart_all()
            break
        if key == ord('c'):
            clear_images()
        if key == ord('e'):
            cv2.ellipse(img_R, e_r, (2,2), 0, 0, 360, (255,255,255), 4)
            cv2.ellipse(img_L, e_l, (2,2), 0, 0, 360, (255,255,255), 4)
            cv2.ellipse(img_R, e_r, (1,1), 0, 0, 360, (0,0,255), 2)
            cv2.ellipse(img_L, e_l, (1,1), 0, 0, 360, (0,0,255), 2)
        if key == 27:
            exit_the_program = True
            break