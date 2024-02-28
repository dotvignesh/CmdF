import time
from pynput import keyboard
from pynput.keyboard import Key, Controller
import pyperclip


controller = Controller()
url = None

def getURL():

    with controller.pressed(Key.cmd):
        controller.tap("l")
        controller.tap("a")
        controller.tap("c")

    time.sleep(0.1)

    url = pyperclip.paste()

    if not url: return
    print("Video:", url)


def getQuery():

    print("Video URL from F11:", url)

    with controller.pressed(Key.cmd):
        controller.tap("a")
        controller.tap("c")

    time.sleep(0.1)

    query = pyperclip.paste()

    if not query: return
    print("Query:", query)
    


def f9():
    getURL()
    
def f10():
    getQuery()


with keyboard.GlobalHotKeys({"<109>": f10, "<101>": f9}) as h:
    h.join()
