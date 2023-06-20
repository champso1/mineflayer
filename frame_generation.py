
# -------- generating frames -------- #
#make sure to change all the urls accordingly

import cv2
import os, os.path

#creates list with names of all videos in the directory
videos = [name for name in os.listdir('C:\\Users\\casey\\OneDrive\\Personal\\School\\Inspire_Program\\Project\\test\\')]

currentframe = 0
index = 0

while(True):

    if index == len(videos):
            break
    
    #captures a video
    cam = cv2.VideoCapture('C:\\Users\\casey\\OneDrive\\Personal\\School\\Inspire_Program\\Project\\test\\' + str(videos[index]))

    #increment index to grab next video on next passthrough
    index = index + 1

    while(True):
    
        #frame is the gathered frame, ret is boolean, True if there are frames remaining, false if not
        ret,frame = cam.read()

    
        if ret:
            #create name for output image
            name = './test_images/frame' + str(currentframe) + '.jpg'
            print ('Creating...' + name)
            
            #resize frame to 128x72
            frame = cv2.resize(frame, (128, 72))
    
            # writing the extracted images
            cv2.imwrite(name, frame)
    
            # increasing counter to ensure unique name generation
            currentframe += 1
        else:
            break




# Release all space and windows once done
cam.release()
cv2.destroyAllWindows()