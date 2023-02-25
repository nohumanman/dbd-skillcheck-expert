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

    def custom_sleep(self, amount):
        start_time = time.time()
        
        while True:
            if (time.time()-start_time>amount):
                return

    def assistance_required(self):
        # the expert is required to do a skillcheck
        img, start = self._get_screenshot()
        time_until_skillcheck = self._time_until_skillcheck(img)
        if time_until_skillcheck == None:
            print("ACCEPTED ERROR!")
            return
        # wait for time until skillcheck minus the time we've wasted
        wasted_time = time.time()  - start
        time_to_wait = time_until_skillcheck - wasted_time
        if time_to_wait < 0:
            time_to_wait = 0
            print("Rendering took too long! Skillcheck missed!")
        self.custom_sleep(time_to_wait)
        self._press_space()
        cv2.imwrite("this.png", img)
        print("Time wasted: " + str(wasted_time))
        print("Time until skillcheck: " + str(time_until_skillcheck))
        print("Time to wait: " + str(time_to_wait))

    def _time_until_skillcheck(self, im):
        # returns time until enter key should be pressed
        im_crop = self._crop_image_center(im) # crop image to circle
        rect = self._circle_to_rect(im_crop)
        rect = im_crop
        cv2.rectangle(rect, (40, 100), (250, 200), (0, 0, 0), -1)
        # 'cropped' is now normalised circle
        #cv2.imwrite("so71416458-straight1.png", rect)
        # get position of red pixels (current skillcheck pos) 
        mask = cv2.inRange(rect, (14, 3, 175), (30, 16, 185))
        coords = cv2.findNonZero(mask)
        if coords is None:
            cv2.imwrite("error-img.png", rect)
            return None
        red_coord = (coords[-1][0][0], coords[-1][0][1])
        if red_coord == None:
            return None
        cv2.circle(rect, red_coord, 10, (255, 255, 0), 1)
        mask = cv2.inRange(rect, (200, 200, 200), (255, 255, 255))
        contours, hierarchy = cv2.findContours(image=mask, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
        largest_cnt = None
        for cnt in contours:
            if largest_cnt is None:
                largest_cnt = cnt
            elif cv2.contourArea(cnt) > cv2.contourArea(largest_cnt):
                largest_cnt = cnt
        white_coord =largest_cnt[0][0]
        cv2.circle(rect, white_coord, 10, (255, 255, 0), 1)
        angle = (self.getAngle(red_coord, (im_crop.shape[0]/2, im_crop.shape[1]/2), white_coord))
        print("~" + str(round(angle)) + "deg")
        center = (int(im_crop.shape[0]/2), int(im_crop.shape[1]/2))
        cv2.circle(rect, center, 5, (255, 255, 0), 10)
        cv2.line(rect, red_coord, center, (255, 255, 255), 4)
        cv2.line(rect, white_coord, center, (255, 255, 255), 4)
        # 180 deg = 0.33 seconds
        time_to_wait = angle * (0.17 / 90)
        #cv2.imwrite("so71416458-straight2.png", rect)
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
            time_of_shot = time.time()
        img = Image.frombytes("RGB", sct_image.size, sct_image.bgra, "raw", "BGRX")
        img_bgr = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        return img_bgr, time_of_shot

    def _press_space(self):
        # presses the enter key to complete the skillcheck
        press('space')

import keyboard  # using module keyboard
while True:  # making a loop
    if keyboard.is_pressed('q'):  # if key 'q' is pressed
        print("-----")
        SkillcheckExpert().assistance_required()


 