# timeit much more accurate than time.time()
from timeit import default_timer as timer
from mss import mss
import time # for waiting
from keyboard import press
from PIL import Image
import cv2
import numpy as np
import math

class SkillcheckExpert():
    def __init__(self):
        pass

    def assistance_required(self):
        # the expert is required to do a skillcheck
        start = timer()
        img = self._get_screenshot()
        time_until_skillcheck = self._time_until_skillcheck(img) 
        # wait for time until skillcheck minus the time we've wasted
        wasted_time = timer()  - start
        time_to_wait = time_until_skillcheck - wasted_time
        if time_to_wait < 0:
            time_to_wait = 0
            print("Rendering took too long! Skillcheck missed!")
        time.sleep(time_to_wait)
        self._press_space()
        cv2.imwrite("this.png", img)
        print("Time wasted: " + str(wasted_time))
        print("Time until skillcheck: " + str(time_until_skillcheck))
        print("Time to wait: " + str(time_to_wait))

    def _time_until_skillcheck(self, im):
        # returns time until enter key should be pressed
        im_crop = self._crop_image_center(im) # crop image to circle
        rect = self._circle_to_rect(im_crop)
        # 'cropped' is now normalised circle
        cv2.imwrite("so71416458-straight1.png", rect)
        # get position of red pixels (current skillcheck pos) 
        mask = cv2.inRange(rect, (18, 6, 175), (27, 14, 185))
        coords = cv2.findNonZero(mask)
        red_coord = (coords[0][0][0], coords[0][0][1])
        cv2.circle(rect, red_coord, 10, (255, 255, 0), 1)

        # get position of white pixels (skillcheck aim)
        mask = cv2.inRange(rect, (200, 200, 200), (255, 255, 255))
        coords = cv2.findNonZero(mask)
        white_coord = (coords[0][0][0], coords[0][0][1])
        cv2.circle(rect, white_coord, 10, (255, 255, 0), 1)

        # get distance between red and white pixels on the horizontal axis
        distance = math.sqrt((red_coord[0] - white_coord[0])**2)
        print("Distance: " + str(distance))
        time_to_wait = distance * 0.00226
        # 167 = 0.33 seconds
        # 73 = 0.165 seconds
        cv2.imwrite("so71416458-straight2.png", rect)
        return time_to_wait
  
    def _circle_to_rect(self, im):
        size = im.shape[0]  # assumes square image
        outer_radius = size // 2
        inner_radius_factor = 0.8  # 0.70 measured empirically from image
        # Unwarp ring
        warped = cv2.warpPolar(
            im,
            (im.shape[0], im.shape[1]),
            (outer_radius, outer_radius),
            outer_radius,
            0
        )
        # Rotate 90 degrees
        straightened = cv2.rotate(warped, cv2.ROTATE_90_COUNTERCLOCKWISE)
        # Crop to ring only
        return straightened[: int(straightened.shape[0] * (1 - inner_radius_factor)), :]

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
        with mss() as sct:
            sct_image = sct.grab(sct.monitors[2])
        img = Image.frombytes("RGB", sct_image.size, sct_image.bgra, "raw", "BGRX")
        img_bgr = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        return img_bgr

    def _press_space(self):
        print("HERE")
        # presses the enter key to complete the skillcheck
        press('space')

import keyboard  # using module keyboard
while True:  # making a loop
    if keyboard.is_pressed('q'):  # if key 'q' is pressed
        try:
            print("-----\n\n")
            SkillcheckExpert().assistance_required()
        except:
            pass


 