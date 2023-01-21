# timeit much more accurate than time.time()
from timeit import default_timer as timer
import pyautogui # for screenshots
import time # for waiting
from keyboard import press
from PIL import Image
import cv2
import numpy as np

class SkillcheckExpert():
    def __init__(self):
        pass

    def assistance_required(self):
        # the expert is required to do a skillcheck
        start = timer()
        filename = self._get_screenshot()
        time_until_skillcheck = self._time_until_skillcheck(filename)
        end = timer()
        # wait for time until skillcheck minus the time we've wasted
        wasted_time = end - start
        time_to_wait = time_until_skillcheck - wasted_time
        if time_to_wait < 0:
            time_to_wait = 0
            print("Rendering took too long! Skillcheck missed!")
        time.sleep(time_to_wait)
        #self._press_space()
        print("Time wasted: " + str(wasted_time))

    def _time_until_skillcheck(self, filename):
        # returns time until enter key should be pressed
        # this is calculated from the screenshot which
        # contains a red bar and white bar :. image processing
        # note the time for the red line to move halfway along the circle is 0.33 seconds
        im = cv2.imread(filename)
        # crop image to only contain the skillcheck circle
        im_crop = self._crop_image_center(im)
        # get position of red pixels (current skillcheck pos) 
        mask = cv2.inRange(im_crop, (10, 4, 180), (20, 4, 185))
        coords = cv2.findNonZero(mask)
        red_coord = (coords[0][0][0], coords[0][0][1])
        cv2.circle(im_crop, red_coord, 10, (255, 255, 0), 1)

        # get position of group of white pixels (aim)

        #cv2.imwrite("image.png", im_crop)
        return 2
  
    def _crop_image_center(self, im, w = 300, h = 300):
        # crops the image to only contain the skillcheck circle
        # returns the cropped image
        center = im.shape
        x = center[1]/2 - w/2
        y = center[0]/2 - h/2
        im_crop = im[int(y):int(y+h), int(x):int(x+w)]
        return im_crop

    def _get_screenshot(self):
        # get screenshot of the screen
        filename = "screenie.png"
        screenshot = pyautogui.screenshot()
        screenshot.save(filename)
        return filename

    def _press_space(self):
        # presses the enter key to complete the skillcheck
        press('space')

SkillcheckExpert().assistance_required()
