import time, threading, cv2, mss, numpy, ujson
from pynput import keyboard
import os.path
from os import path
import psutil
from playsound import playsound


monitor = {"top": 0, "left": 0, "width": 1, "height": 1}
lock = 1
adjustlock = 0
def settingsImport():
    if path.exists("./settings.json"):
        with open('./settings.json') as infile:
            settings = ujson.load(infile)
        if len(settings) == 4:
            print('Imported Settings')
            global monitor
            monitor = {"top": settings['top'], "left": settings['left'], "width": settings['width'], "height": settings['height']}
    else:
        print('Settings File Created')
        settings = {}
        settings['top'] = 799
        settings['left'] = 1640
        settings['width'] = 280
        settings['height'] = 280
        with open('settings.json','w') as outfile:
            jsonDump = ujson.dump(settings,outfile,indent=4)
        monitor = {"top": 799, "left": 1640, "width": 280, "height": 280}


def monitorUPDT(top,left,width,height):
    global monitor
    monitor = {"top": top, "left": left, "width": width, "height": height}
    print(f'Top: {top} Left: {left} Width: {width} Height: {height}')
    settingsExport()


def settingsExport():
    settings = {}
    global monitor
    settings['top'] = monitor['top']
    settings['left'] = monitor['left']
    settings['width'] = monitor['width']
    settings['height'] = monitor['height']
    with open('settings.json','w') as outfile:
        jsonDump = ujson.dump(settings,outfile,indent=4)


    

def screenCAP():
    while True:
        if lock == 1:
                with mss.mss() as sct:
                    global monitor
                    img = numpy.array(sct.grab(monitor))
                    cv2.namedWindow('Big Map 1.0', cv2.WND_PROP_FULLSCREEN | cv2.WINDOW_KEEPRATIO)
                    cv2.setWindowProperty('Big Map 1.0', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
                    cv2.imshow('Big Map 1.0', img)
                    cv2.waitKey(25)
        else:
            cv2.destroyAllWindows()
            



def enlarge():
    top = monitor['top']
    left = monitor['left']
    width = monitor['width'] - 1
    height = monitor['height'] - 1
    monitorUPDT(top,left,width,height)


def reduce():
    top = monitor['top']
    left = monitor['left']
    width = monitor['width'] + 1
    height = monitor['height'] + 1
    monitorUPDT(top,left,width,height)

def up():
    top = monitor['top'] - 1
    left = monitor['left']
    width = monitor['width']
    height = monitor['height']
    monitorUPDT(top,left,width,height)

def down():
    top = monitor['top'] + 1
    left = monitor['left']
    width = monitor['width']
    height = monitor['height']
    monitorUPDT(top,left,width,height)

def left():
    top = monitor['top']
    left = monitor['left'] - 1
    width = monitor['width']
    height = monitor['height']
    monitorUPDT(top,left,width,height)

def right():
    top = monitor['top'] 
    left = monitor['left'] + 1
    width = monitor['width']
    height = monitor['height']
    monitorUPDT(top,left,width,height)

def KInput():

    def on_press(key):
        global adjustlock
        global lock
        
        key = str(key).strip("'")
        
        if key == '[':
            if adjustlock == 1:
                adjustlock = 0
                playsound('adjustlockoff.wav')
            else:
                adjustlock = 1
                playsound('adjustlockon.wav')
        elif key == ']':
                if lock == 1:
                    lock = 0
                    playsound('screenhide.wav')
                else:
                    lock = 1
                    playsound('screenshow.wav')

        if adjustlock == 1:   
            if key == "<187>":
                enlarge()
            elif key == "<189>":
                reduce()
            elif key == "Key.up":
                up()
            elif key == "Key.down":
                down()       
            elif key == "Key.left":
                left()
            elif key == "Key.right":
                right()
        else:
            pass
    def on_release(key):
        return('released')


    listener = keyboard.Listener(
        on_press=on_press,
        on_release=on_release)
    listener.start()
    


settingsImport()
thr0 = threading.Thread(target=screenCAP, args=())
thr0.start()
KInput()


