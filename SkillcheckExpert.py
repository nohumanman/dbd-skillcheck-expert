# timeit much more accurate than timer()
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

    def custom_sleep(self, amount):
        start_time = timer()
        while True:
            if (timer()-start_time>amount):
                return

    def assistance_required(self):
        # the expert is required to do a skillcheck
        start = timer()
        img = self._get_screenshot()
        time_until_skillcheck = self._time_until_skillcheck(img)
        # wait for time until skillcheck minus the time we've wasted
        wasted_time = timer()  - start
        time_to_wait = time_until_skillcheck - wasted_time
        s1 = timer()
        if time_to_wait < 0:
            time_to_wait = 0
            print("Rendering took too long! Skillcheck missed!")
        self.custom_sleep(round(time_to_wait*1000)/1000)
        self._press_space()
        s2 = timer()
        
        cv2.imwrite("this.png", img)
        print("Time wasted:           " + str(round(wasted_time*1000)/1000))
        print("Time until skillcheck: " + str(round(time_until_skillcheck*1000)/1000))
        print("Time to wait:          " + str(round(time_to_wait*1000)/1000))
        print("Time actually waited:  " + str(round((s2-s1)*1000)/1000))

    def _time_until_skillcheck(self, im):
        # returns time until enter key should be pressed
        rect = self._crop_image_center(im) # crop image to circle
        # find red coordinate
        mask = cv2.inRange(rect, (5, 1, 170), (30, 16, 255))
        contours, hierarchy = cv2.findContours(image=mask, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
        c = max(contours, key = cv2.contourArea)
        x,y,w,h = cv2.boundingRect(c)
        red_coord = (x,y)
        # find white coordinate
        mask = cv2.inRange(rect, (200, 200, 200), (255, 255, 255))
        contours, hierarchy = cv2.findContours(image=mask, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
        c = max(contours, key = cv2.contourArea)
        x,y,w,h = cv2.boundingRect(c)
        white_coord = (x,y)
        # find angle
        angle = self.getAngle(red_coord, (rect.shape[0]/2, rect.shape[1]/2), white_coord)
        print("~" + str(round(angle)) + "deg")
        center = (int(rect.shape[0]/2), int(rect.shape[1]/2))
        cv2.circle(rect, center, 5, (255, 255, 0), 10)
        cv2.line(rect, red_coord, center, (255, 255, 255), 4)
        cv2.line(rect, white_coord, center, (255, 255, 255), 4)
        # 360 deg = 0.66 seconds
        time_to_wait = (angle/360) * 0.9
        return time_to_wait

    def getAngle(self, a, b, c):
        # taken from https://manivannan-ai.medium.com/find-the-angle-between-three-points-from-2d-using-python-348c513e2cd
        ang = math.degrees(math.atan2(c[1]-b[1], c[0]-b[0]) - math.atan2(a[1]-b[1], a[0]-b[0]))
        return ang + 360 if ang < 0 else ang

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
        # presses the enter key to complete the skillcheck
        press('space')

import keyboard  # using module keyboard
while True:  # making a loop
    if keyboard.is_pressed('q'):  # if key 'q' is pressed
        print("-----")
        SkillcheckExpert().assistance_required()


 