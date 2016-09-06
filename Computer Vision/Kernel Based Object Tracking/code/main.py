import numpy as np
import cv2
import kotutilities as k
from pylab import *

WINDOW_NAME = 'Object Tracking'
selected_area = [0,0,0,0] # [x1,y1,x2,y2]
selected = False
is_drawing = False
kernel_sum = 0.0
nBin = 16
MAX_ITER = 5
exit_program=False
valid_name=False


def mouse_callback(event,x,y,flags,param):
    global first_frame, is_drawing, selected

    if not selected:
        if event == cv2.EVENT_LBUTTONDOWN:
            is_drawing = True
            selected_area[0] = x
            selected_area[1] = y
        elif event == cv2.EVENT_LBUTTONUP:
            is_drawing = False
            if selected_area[2] > selected_area[0] and selected_area[3] > selected_area[1]:
                selected = True
        else:
            if is_drawing:
                selected_area[2] = x
                selected_area[3] = y


def get_pdf(img, box):
    global nBin
    return k.get_pdf(img,box_to_array(box),nBin)


def box_to_array(box):
    return np.array([box['x'],box['y'],box['width'],box['height']], np.uint16)


def check_box(box):
    if box['x'] < 0:
        box['x']=0
    if box['y'] < 0:
        box['y']=0
    if box['x']+box['width'] >= current_frame.shape[1]:
        box['x']=current_frame.shape[1]-box['width']
    if box['y']+box['height'] >= current_frame.shape[0]:
        box['y']=current_frame.shape[0]-box['height']
    return box


def print_instructions(initial):
    if initial:
        print "Please, select the area to track drawing a rectangle with the mouse\n"
    else:
        print "Guide:\n   - Main steps:\n   -------------------\n\t1. Introduce the name of the video"
        print "\t2. Select an area to track with the mouse"
        print "\t3. The program will track it during the whole video"
        print "'s' - Press 's' to stop the tracking process in the present video and start again"
        print "Esc - Press Esc to exit the program"
        print "Write 'exit' as filename to close the program\n"




print "KERNEL-BASED OBJECT TRACKING\n*******************************************\n"

if len(sys.argv) == 2:
    cap = cv2.VideoCapture(sys.argv[1])
    print "Program initiated with "+sys.argv[1]
    print_instructions(True)
else:
    while not valid_name:
        print_instructions(False)
        nvideo = raw_input("Please introduce the name of the video: ")
        if  nvideo == "exit":
            exit_program=True
            break
        else:
            cap = cv2.VideoCapture(nvideo)
            ret, frame = cap.read()
            if ret:
                valid_name=True

while not exit_program:
    valid_name=False
    ret, frame = cap.read()

    cv2.namedWindow(WINDOW_NAME)
    cv2.setMouseCallback(WINDOW_NAME,mouse_callback)

    while not selected:
        draw_frame = frame.copy()

        p1 = (selected_area[0],selected_area[1])
        p2 = (selected_area[2],selected_area[3])
        if p1 < p2:
            cv2.rectangle(draw_frame, p1, p2, (0,255,0),1)
        cv2.imshow(WINDOW_NAME,draw_frame)
        if cv2.waitKey(1) & 0xFF == 27:
            exit(0)
        #Display help
        if cv2.waitKey(1) & 0xFF == 104:
            print_instructions(False)

    box_width = selected_area[2] - selected_area[0]
    box_width = box_width + 1 if box_width%2 == 0 else box_width
    box_height = selected_area[3] - selected_area[1]
    box_height = box_height + 1 if box_height%2 == 0 else box_height

    first_frame = frame.copy()
    box = {'x':selected_area[0], 'y':selected_area[1], 'width':box_width, 'height':box_height}
    box_center = (box_height/2, box_width/2)
    target_model = get_pdf(first_frame, box)


    norm_x = [[float(j-box_center[1])/box_center[1] for j in range(box_width)] for i in range(box_height)]
    norm_y = [[float(i-box_center[0])/box_center[0] for j in range(box_width)] for i in range(box_height)]



    while(cap.isOpened()):
        ret, current_frame = cap.read()
        if not ret:
            break

        for i in range(MAX_ITER):
            next_box = box.copy()


            target_candidate, weight, weight_sum = k.get_pdf_and_weight2(current_frame, target_model, box_to_array(check_box(next_box)), nBin)
            directions_x = (norm_x*weight)/weight_sum
            directions_y = (norm_y*weight)/weight_sum

            sum_x = int(directions_x.sum()*box_center[1])
            sum_y = int(directions_y.sum()*box_center[0])


            next_box['x'] += sum_x
            next_box['y'] += sum_y

            dist = k.calc_bhattacharya(target_model, target_candidate)
            if dist < 0.6:
                target_model=target_candidate
                break
            else:
                box = next_box

        p1 = (box['x'],box['y'])
        p2 = ( box['x']+box_width, box['y']+box_height)
        cv2.rectangle(current_frame, p1, p2, (0,255,0),1)
        cv2.imshow(WINDOW_NAME,current_frame)

        key = cv2.waitKey(1)
        if  key & 0xFF == 27:
            exit_program=True
            break
        #Stop this video
        if key & 0xFF == 115:
            exit_program=False
            break
        #Display help
        if key & 0xFF == 104:
            print_instructions(False)

    print "Stopping tracking process"
    cap.release()
    cv2.destroyAllWindows()
    if not exit_program:
        selected=False
        selected_area = [0,0,0,0]
        while not valid_name:
            print_instructions(False)
            nvideo = raw_input("Please introduce the name of the next video: ")
            if  nvideo == "exit":
                exit_program=True
                break
            else:
                cap = cv2.VideoCapture(nvideo)
                ret, frame = cap.read()
                if ret:
                    valid_name=True
