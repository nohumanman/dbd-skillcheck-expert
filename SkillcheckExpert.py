# timeit much more accurate than time.time()
from timeit import default_timer as timer
import pyautogui # for screenshots
import time # for waiting

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
        time.sleep(abs(time_until_skillcheck - (end - start)))

    def _time_until_skillcheck(self, filename):
        # returns time until enter key should be pressed
        # this is calculated from the screenshot which
        # contains a red bar and white bar :. image processing
        return 0

    def _get_screenshot(self):
        # get screenshot of the screen
        filename = "screenie.png"
        screenshot = pyautogui.screenshot()
        screenshot.save(filename)
        return filename

    def _press_enter(self):
        # presses the enter key to complete the skillcheck
        pass

SkillcheckExpert().assistance_required()
