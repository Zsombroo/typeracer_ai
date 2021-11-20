''' To select the bounding box of the text you must define it by the top-left
    and bottom-right corners in this order!
'''


from PIL.Image import Image
import numpy as np
import pytesseract
from pynput import keyboard
import pyautogui
import time
from PIL import ImageGrab
import matplotlib.pyplot as plt


# It is more like an upper limit than the real speed of the program
DESIRED_WPM = 250


_n_ctrl_strokes = 0
_bounding_box = np.zeros((2, 2))


def _on_press(key):
    global _n_ctrl_strokes
    if key == keyboard.Key.ctrl:
        _bounding_box[_n_ctrl_strokes] = pyautogui.position()
        _n_ctrl_strokes += 1
        print(_n_ctrl_strokes)


if __name__=='__main__':
    bbox_selected = False
    listener = keyboard.Listener(on_press=_on_press)
    listener.start()
    while not bbox_selected:
        # wait here until the user defines the bounding box of the text by 
        # moving the mouse and pressing the ctrl key twice
        if _n_ctrl_strokes == 2:
            bbox_selected = True
    #time.sleep(0.05)
    image = ImageGrab.grab(list(_bounding_box.flatten().astype(int)))
    text = pytesseract.image_to_string(image)
    # Typeracer expects ' ' instead of '\n' at the end of the line
    text = text.replace('\n', ' ')
    # Sometimes 'I' is misrecognized as '|'
    text = text.replace('|', 'I')
    pyautogui.typewrite(text, interval=1/(DESIRED_WPM*5/60))