__author__ = 'Jiranun.J'

import numpy as np
import cv2
from pylab import *
from numpy.linalg import eigh

window_name = "ASG2 Part 1 : Movement detection"

cap = cv2.VideoCapture(0)
# Capture frame-by-frame
ret, frame = cap.read()
frame=cv2.flip(frame,1)
last_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    frame=cv2.flip(frame,1)

    current_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    current_frame = cv2.GaussianBlur(current_frame,(5,5),1)

    # Find the difference between last frame and current frame
    diff_of_frames = cv2.absdiff(last_frame, current_frame)
    ret1,thresh_diff_of_frames = cv2.threshold(diff_of_frames,20,255,0)
    kernel = np.ones((10,10),np.uint8)
    thresh_diff_of_frames = cv2.dilate(thresh_diff_of_frames,kernel,iterations = 1)

    # Find the edge of image by using canny detection
    edge_img = cv2.Canny(current_frame, 40, 10)

    # Find the intersection of the difference between frames and the edge (marked_edge_img)
    marked_edge_img = cv2.bitwise_and(thresh_diff_of_frames, edge_img)

    # Find the contours of the marked_edge_img
    contours, hierarchy = cv2.findContours(marked_edge_img.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        # If contours exists, choose the largest contour
        max_contour = max(contours, key=len)


        ######################## This part doesn't work ######################
        # Find the curvatures of points in contour
        # curvatures_vectors = [max_contour[i-1]-2.*max_contour[i]+max_contour[i+1] for i in range(1,len(max_contour)-1)]
        # curvatures = [np.sqrt(v[0][0]**2.+v[0][1]**2.) for v in curvatures_vectors]
        # max_curv = max(curvatures)
        # min_curv = min(curvatures)
        # contour_groups = []
        # finger_amt = 0
        # curv_state = 0 # O : Finding finger tip , 1 : Finding fingers bridge
        # start_p = 0
        # for i in range(1,len(max_contour)-1):
        #     curvature_vector = max_contour[i-1]-2.*max_contour[i]+max_contour[i+1] # Prob 3 : curvature calculation correct?
        #     curvature = np.sqrt(curvature_vector[0][0]**2.+curvature_vector[0][1]**2.) # Prob 4 : no negative value
        #
        #     if curv_state == 0 and max_curv - curvature < 1.:
        #         curv_state = 1
        #     elif curv_state == 1 and curvature - min_curv < 1.:
        #         curv_state = 2
        #     elif curv_state == 2 and max_curv - curvature < 1.:
        #         curv_state = 0
        #         contour_groups.append(max_contour[start_p:i+1])
        #         start_p = i+1
        #         finger_amt += 1
        # contour_groups.append(max_contour[start_p:len(max_contour)])
        #
        #
        # #Ellipse Fitting
        # C = np.array([[ 0, 0, -2, 0, 0, 0 ],
        #      [ 0, 1, 0, 0, 0 ,0 ],
        #      [-2, 0, 0, 0, 0, 0 ],
        #      [ 0, 0, 0, 0, 0, 0 ],
        #      [ 0, 0, 0, 0, 0, 0 ],
        #      [ 0, 0, 0, 0, 0, 0 ]])
        #
        #
        # data = np.array([[p[0][0]**2, p[0][0]*p[0][1], p[0][1]**2, p[0][0], p[0][1], 1] for p in max_contour])
        # S = np.dot((data.T),data)
        # invSC = np.dot(inv(S),C)
        #
        # eig_vals, eig_vectors = eigh(invSC)
        #
        # n = np.argmin(eig_vals)
        # result_vector = V[:,n]
        #
        # a = result_vector[0]
        # b = result_vector[1]
        # c = result_vector[2]
        # d = result_vector[3]
        # e = result_vector[4]
        # f = result_vector[5]
        ######################################################################


        cv2.drawContours(current_frame, [max_contour], 0, (0,0,0), 3)

        cv2.imshow("ASG2 Part 1 : Largest contour", current_frame)

    cv2.imshow(window_name, marked_edge_img)
    last_frame = current_frame

    key = cv2.waitKey(1)
    if key == ord('h'):
        print "There are 2 windows which show Movement detection and Largest contour"
        print "<ESC>: quit"
        print "'h' - help"

    if key == 27:
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()