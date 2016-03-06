# (c) Copyright 2016, Ian K T Tan
# Multimedia University

import sys      # Only using this to exit the program
import cv2      # OpenCV
 
# To run the program
#   python vidsegment.py <videofile> [threshold]
if len(sys.argv) < 2:
    print "Usage: python vidsegment.py <filename> [threshold]"
    sys.exit()

# Initial variables
vidCap = cv2.VideoCapture()
vidCap.open(sys.argv[1])
                              
if not vidCap.isOpened():
    print "%s cannot be opened" % sys.argv[1]
    sys.exit()
                                                                   
if len(sys.argv) > 2 and int(sys.argv[2]) > 0:
    threshold = int(sys.argv[2])
else:
    threshold = 20

print "Using the threshold value of %d." % threshold

# Print out basic information about the video
print "Reading video with resolution: %d x %d" % (vidCap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH), vidCap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))

last_mean = 0

# Read frame by frame
while True:
    (rv, im) = vidCap.read()
    # if rv is not TRUE, then it means end of video
    if not rv:
        break

    # This is simply using the mean of the frame intensity to determine
    # whether it is fading out or in.

    # To improve this to check on differences in mean value instead
    # The code below is partially taken from www.bcastell.com (Brandon Castell)

    frame_mean = im.mean()

    # Detect fade in from black.
    if frame_mean >= threshold and last_mean < threshold:
        print "Detected fade in at %dms (frame %d)." % (vidCap.get(cv2.cv.CV_CAP_PROP_POS_MSEC), vidCap.get(cv2.cv.CV_CAP_PROP_POS_FRAMES))
        cv2.imwrite(str(vidCap.get(cv2.cv.CV_CAP_PROP_POS_FRAMES)) + "_in.jpg", im)
                                                        
    # Detect fade out to black.
    elif frame_mean < threshold and last_mean >= threshold:
        print "Detected fade out at %dms (frame %d)." % (vidCap.get(cv2.cv.CV_CAP_PROP_POS_MSEC), vidCap.get(cv2.cv.CV_CAP_PROP_POS_FRAMES))
        cv2.imwrite(str(vidCap.get(cv2.cv.CV_CAP_PROP_POS_FRAMES)) + "_out.jpg", im)

    last_mean = frame_mean
                                                                   
# End of WHILE loop

frame_count = vidCap.get(cv2.cv.CV_CAP_PROP_POS_FRAMES)  # current position
print "Read %d frames from video." % frame_count
vidCap.release()

