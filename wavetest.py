import pygame
import pygame.camera
from roboflow import Roboflow
import os
import time
import webbrowser
import datetime
import subprocess
from subprocess import run
import pyautogui
import json


pygame.camera.init()

camlist = pygame.camera.list_cameras()
print("Available cameras:", camlist)

filename = 'file:///'+os.getcwd()+'/' + 'waveweb.html'
webbrowser.open_new_tab(filename)


class PredictionGroup:
    def __init__(self, predictions):
        self.predictions = predictions

    def to_dict(self):
        return {
            "predictions": [p.to_dict() for p in self.predictions]
        }


def default_serializer(obj):
    if isinstance(obj, PredictionGroup):
        return obj.to_dict()


counter = 1
if camlist:
    cam = pygame.camera.Camera(camlist[0], (640, 480))
    cam.start()

    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Webcam Feed")

while counter != 0:
    if not camlist:
        print("No camera on current device")
        break

    image = cam.get_image()
    pygame.image.save(image, "image2.jpg")

    screen.blit(image, (0, 0))
    pygame.display.update()

    # Roboflow API call
    # Replace API Key with your own
    rf = Roboflow(api_key="KEtgafRxTGDcI2NgvODP")
    project = rf.workspace().project("wave-detect")
    model = project.version(1).model
    prediction = model.predict("image2.jpg")
    print(prediction.json())
    predictionjson = prediction.json()
    data = json.dumps(predictionjson)
    print(data)

    if "Awake" in data:
        curTime = datetime.datetime.now().strftime("%H:%M:%S")
        with open("waveweb.html", "r+") as f:
            if curTime not in f.read():
                message = '''
                <main>
                <section id="fatigue-logs">
                    <article class="log-entry">
                        <time datetime="{}">{}</time>
                        <p>Fatigue detected</p>
                    </article>
                </section>
                </main>
                '''.format(curTime, curTime)
                f.write(message)

        #Path to xcode watch application
        open_xcode_command = f"open /Users/rohit/Documents/Conrad/software/WAvEAICODE-1/WAvE_haptics_watch/WAvE_haptics_watch.xcodeproj"
        subprocess.run(open_xcode_command, shell=True)
        pyautogui.hotkey('command', 'r')

    time.sleep(1.5)
    os.remove("image2.jpg")
    time.sleep(1)
    time.sleep(10)
    pyautogui.hotkey('command', '.')

