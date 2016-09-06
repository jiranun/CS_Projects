__author__ = 'Jiranun.J'

import ConfigParser
from pylab import *
import numpy as np
from numpy.linalg import inv
import random


#Make sure the cython function is complied
# from subprocess import call
# call(["python setup.py build_ext --inplace"], shell = True)
#
# import Asg3_cython as ac

DEFAULT_CORRESPONDENCE_FILE = 'cali_data1.txt'

if len(sys.argv) == 2:
    correspondence_file = open(sys.argv[1],'r')
else:
    correspondence_file = open(DEFAULT_CORRESPONDENCE_FILE,'r')

config = ConfigParser.RawConfigParser()
config.read('RANSAC.config')

RANSAC = config.getboolean('RANSAC', 'ENABLE_RANSAC')

def get_matrix_A(obj_points, img_points):
    matA = []

    for i in range(len(obj_points)):
        minusX = -1.*float(img_points[i][0])
        minusY = -1.*float(img_points[i][1])
        Xi, Yi, Zi = float(obj_points[i][0]), float(obj_points[i][1]), float(obj_points[i][2])
        matA.append( [ Xi, Yi, Zi, 1., 0. ,0. ,0. ,0., minusX*Xi, minusX*Yi, minusX*Zi, minusX])
        matA.append( [ 0. ,0. ,0. ,0., Xi, Yi, Zi, 1., minusY*Xi, minusY*Yi, minusY*Zi, minusY])

    return matA

def get_KRT(matA):
    U, D, VT = np.linalg.svd(matA)

    #Check if the matrix is singular
    if min(D) < 0.00000000001 :
        return False, 0,0,0
    else :
        M = VT[len(VT)-1,:]

    a1 = np.array([M[0],M[1],M[2]])
    a2 = np.array([M[4],M[5],M[6]])
    a3 = np.array([M[8],M[9],M[10]])

    b = np.array([M[3],M[7],M[11]])

    rho = 1./np.sqrt(sum(i**2 for i in a3))

    u_zero = np.dot((rho**2)*a1,a3)
    v_zero = np.dot((rho**2)*a2,a3)

    alpha_v = np.sqrt(np.dot(rho**2*a2,a2)-v_zero**2)

    s = (rho**4/alpha_v)*np.dot(np.cross(a1,a3),np.cross(a2,a3))

    alpha_u = np.sqrt(np.dot(rho**2*a1,a1)-s**2-u_zero**2)

    sign = np.sign(b[2])

    r3 = sign*np.abs(rho)*a3
    r1 = (rho**2/(alpha_u))*np.cross(a2, a3)

    r2 = np.cross(r3,r1)
    R_star = np.array([r1,r2,r3])

    K_star = np.array([[alpha_u, s, u_zero], [0.0, alpha_v, v_zero], [0.0, 0.0, 1.0]])
    T_star = sign*np.abs(rho)*np.dot(inv(K_star),b)

    return True, K_star, R_star, T_star

def get_new_M(K_star, R_star, T_star):
    RT = np.zeros((3,4))
    RT[0:3,0:3] = R_star
    RT[0:3,3] = T_star

    return np.dot(K_star,RT)

orig_obj_points = []
orig_img_points = []

for line in correspondence_file:
    coords = (line.rstrip('\n')).split(' ')
    coords = filter(None, coords)
    orig_obj_points.append([coords[0],coords[1],coords[2]])
    orig_img_points.append([coords[3],coords[4]])

orig_obj_points = np.array(orig_obj_points, np.float32)
orig_img_points = np.array(orig_img_points, np.float32)

nPoints = len(orig_obj_points)

obj_points_3DH = np.ones((nPoints,4))
obj_points_3DH[:,0:3] = orig_obj_points

if nPoints > 6:
    matA = get_matrix_A(orig_obj_points, orig_img_points)
    ret, K_star, R_star, T_star = get_KRT(matA)

    if not ret:
        print "ERROR! All points are on the same plane"

    else:
        if RANSAC:

            MAX_ITER = config.getint('RANSAC', 'MAX_ITER')
            DESIRED_PROB = config.getfloat('RANSAC', 'DESIRED_PROB')
            MINIMUM_POINTS = config.getint('RANSAC', 'MINIMUM_POINTS')

            rand_point = lambda: random.randint(0,nPoints-1)
            nIter = 0
            ransac_w = 0.5
            ransac_k = 1
            min_error = 10000
            best_M = []
            best_K = []
            best_R = []
            best_T = []

            while nIter < MAX_ITER and nIter < ransac_k:
                random_points = [rand_point() for i in range(MINIMUM_POINTS)]
                random_obj_points = [(orig_obj_points[i][0],orig_obj_points[i][1],orig_obj_points[i][2]) for i in random_points]
                random_img_points = [(orig_img_points[i][0],orig_img_points[i][1]) for i in random_points]

                evaluation_mat = get_matrix_A(random_obj_points, random_img_points)

                ret, K_star, R_star, T_star = get_KRT(evaluation_mat)

                if not ret:
                    continue

                new_M = get_new_M(K_star, R_star, T_star)

                img_points_2DH = [np.dot(new_M,obj_points_3DH[i]) for i in range(nPoints)]
                homogenized_img_points = [(img_points_2DH[i][0]/img_points_2DH[i][2],img_points_2DH[i][1]/img_points_2DH[i][2]) for i in range(nPoints)]

                distances = [np.sqrt((orig_img_points[i][0]-homogenized_img_points[i][0])**2+(orig_img_points[i][1]-homogenized_img_points[i][1])**2) for i in range(nPoints)]
                median_distance = np.median(distances)

                inliers = [i for i in range(nPoints) if distances[i] < median_distance]
                nInliers = len(inliers)

                ransac_w = float(len(inliers))/float(nPoints)
                ransac_k = np.log(1.-DESIRED_PROB)/np.log(1.-ransac_w**MINIMUM_POINTS)

                if nInliers >= MINIMUM_POINTS:
                    inlier_obj_points = [(orig_obj_points[i][0],orig_obj_points[i][1],orig_obj_points[i][2]) for i in inliers]
                    inlier_img_points = [(orig_img_points[i][0],orig_img_points[i][1]) for i in inliers]

                    matA = get_matrix_A(inlier_obj_points, inlier_img_points)
                    ret, K_star, R_star, T_star = get_KRT(matA)

                    if not ret:
                        continue

                    projM = get_new_M(K_star, R_star, T_star)

                    inlier_obj_points_3DH = np.ones((nInliers,4))
                    inlier_obj_points_3DH[:,0:3] = inlier_obj_points

                    img_points_2DH = [np.dot(projM, inlier_obj_points_3DH[i]) for i in range(nInliers)]
                    homogenized_img_points = [(img_points_2DH[i][0]/img_points_2DH[i][2],img_points_2DH[i][1]/img_points_2DH[i][2]) for i in range(nInliers)]
                    distances = [np.sqrt((inlier_img_points[i][0]-homogenized_img_points[i][0])**2+(inlier_img_points[i][1]-homogenized_img_points[i][1])**2) for i in range(nInliers)]
                    error = np.mean(distances)

                    if error < min_error :
                        min_error = error
                        best_M = projM
                        best_K, best_R, best_T = K_star, R_star, T_star

                elif min_error == 10000:
                    best_M = new_M
                    best_K, best_R, best_T = K_star, R_star, T_star

                nIter += 1

            if nIter == MAX_ITER and nIter != ransac_k:
                print "WARNING: Max iterations exceed.\n"

            print "###################### Result #########################\n"
            print "Number of experiments  = ", nIter, " times"
            print "\n( u0 , v0 )            = ( ",best_K[0][2],' , ',best_K[1][2],' )'
            print "\ns                      = ",best_K[0][1]
            print "\n( alphaU , alphaV )    = ( ",best_K[0][0],' , ',best_K[1][1],' )'
            print "\nT*                     = ",best_T
            print "\nR*                     = \n",best_R
            print "\nM (K*[R*|T*])          = \n",best_M
            print "\nError                  = ",min_error

            if min_error == 10000:
                print "WARNING : Best projection equation cannot be calculated by RANSAC if there are few points."
                print "          Increase the amount of points,or disable RANSAC might solve this issue."


        else:
            new_M = get_new_M(K_star, R_star, T_star)

            obj_points_3DH = np.ones((nPoints,4))
            obj_points_3DH[:,0:3] = orig_obj_points

            img_points_2DH = [np.dot(new_M,obj_points_3DH[i]) for i in range(nPoints)]
            homogenized_img_points = [(img_points_2DH[i][0]/img_points_2DH[i][2],img_points_2DH[i][1]/img_points_2DH[i][2]) for i in range(nPoints)]

            error = (1./nPoints)*sum([np.sqrt((orig_img_points[i][0]-homogenized_img_points[i][0])**2+(orig_img_points[i][1]-homogenized_img_points[i][1])**2) for i in range(nPoints)])

            # Output file
            # output = open('output.txt','w')
            # for i in range(nPoints):
            #     output.write(str(homogenized_img_points[i])+'\n')
            # output.close()

            print " ###################### Result #########################\n"
            print "( u0 , v0 )         = ( ",K_star[0][2],' , ',K_star[1][2],' )'
            print "\ns                   = ",K_star[0][1]
            print "\n( alphaU , alphaV ) = ( ",K_star[0][0],' , ',K_star[1][1],' )'
            print "\nT*                  = ",T_star
            print "\nR*                  = \n",R_star
            print "\nM (K*[R*|T*])       = \n",new_M
            print "\nError               = ",error

else:
    print "ERROR : amount of points should be more than 6."