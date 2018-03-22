import cv2 
import numpy as np 
import imutils

# initializing video feed
capture = cv2.VideoCapture('compilation.mp4') # 0 for webcam

# initializing global variables
previous_frame = None  
sensitivity = 20
square_size = 40
accuracy = 5

''' Checks if two squares overlap given their respective coordinates
    left1 - coordinates for the top-left point of the first square
    right1 - coordinates for the bottom-right point of the first square
    left2 - coordinates for the top-left point of the second square
    right2 - coordinates for the bottom-left point of the second square
    returns True if squares overlap and False otherwise
 '''
def overlap(left1, right1, left2, right2):
    if left1[0] > right2[0] or left2[0] > right1[0]:
        return False 
    if left1[1] > right2[1] or left2[1] > right1[1]:
        return False 
    return True

# infinite loop to read video frames
while True:
    # Check if a new frame is available for input 
    response, frame = capture.read()
    # quit application if there are no more frames
    if response == False: quit()
    # resize frame to a width of 800
    frame = imutils.resize(frame,width= 800)
    # convert frame to gray scale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # check if there is a previous frame available
    if previous_frame is not None:
        diff = abs(gray - previous_frame)
        retval, threshold = cv2.threshold(diff, sensitivity, 255, cv2.THRESH_BINARY)
        threshold = 255 - threshold
        cv2.imshow('threshold', threshold)
        height = threshold.shape[0]
        width = threshold.shape[1]
        rectangles = []
        # iterate through pixels and append active regions to rectangles array
        for i in range(0, height,accuracy):
            for j in range(0, width,accuracy):
                if threshold[i][j] == 255:
                    rectangles.append((j-square_size,i-square_size,j+square_size,i+square_size))
        # iterate through rectangles array and merge overlapping rectangles
        for i in range(len(rectangles)-1):
           if rectangles[i] == 0:
               continue
           for j in range(len(rectangles)-1): 
               if i != j:
                   if rectangles[i] != 0 and rectangles[j] != 0:
                       left1 = (rectangles[i][0],rectangles[i][1])
                       right1 = (rectangles[i][2],rectangles[i][3])
                       left2 = (rectangles[j][0],rectangles[j][1])
                       right2 = (rectangles[j][2],rectangles[j][3])
                       if overlap(left1, right1, left2, right2):
                            min_x = left1[0]
                            max_x = right1[0]
                            min_y = left1[1]
                            max_y = right1[1]
                            if left2[0] < min_x:
                                min_x = left2[0]
                            if right2[0] > max_x:
                                max_x = right2[0]
                            if left2[1] < min_y:
                                min_y = left2[1]
                            if right2[1] > max_y:
                                max_y = right2[1]
                            rectangles[i] = (min_x,min_y,max_x,max_y)
                            rectangles[j] = 0
        # merge first and last rectangle in the rectangles array
        if len(rectangles) > 0:
            if len(rectangles)-1 != 0:
                f = len(rectangles)-1
                if rectangles[len(rectangles)-1] != 0 and rectangles[0] != 0:
                    left1 = (rectangles[f][0],rectangles[f][1])
                    right1 = (rectangles[f][2],rectangles[f][3])
                    left2 = (rectangles[0][0],rectangles[0][1])
                    right2 = (rectangles[0][2],rectangles[0][3])
                    if overlap(left1, right1, left2, right2):
                            min_x = left1[0]
                            max_x = right1[0]
                            min_y = left1[1]
                            max_y = right1[1]
                            if left2[0] < min_x:
                                min_x = left2[0]
                            if right2[0] > max_x:
                                max_x = right2[0]
                            if left2[1] < min_y:
                                min_y = left2[1]
                            if right2[1] > max_y:
                                max_y = right2[1]
                            rectangles[0] = (min_x,min_y,max_x,max_y)
                            rectangles[f] = 0
        # iterate through rectangles array and draw a rectangle on the current frame
        for rectangle in rectangles:
            if rectangle != 0:
                cv2.rectangle(frame, (rectangle[0], rectangle[1]), (rectangle[2], rectangle[3]), (0,0,255), 2)   
        # show frame
        cv2.imshow('frame', frame)
    # set previous frame the the current frame
    previous_frame = gray + 200
    # listen for keyboard input to terminate application
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# release video capture and terminate all windows
capture.release()
cv2.destroyAllWindows()

