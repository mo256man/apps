import PySimpleGUI as sg
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont

class Frame():
    def __init__(self):
        sg.theme("Reddit")

        no_image = Image.new("RGB", (300,300), (255,0,0))
        sg_image = sg.Image("", key="image")

        frame1 = sg.Frame("",
            [
                [sg.Text("名前"), sg.InputText("", key="name", enable_events=True,)],
                [sg.Submit(button_text="作成", key="start")]
            ] ,
            size=(340, 300)
        )

        frame2 = sg.Frame("",
            [
                [sg_image]
            ],
            size=(300, 300)
        )

        layout = [[frame1, frame2]]
        self.window = sg.Window("はんこメーカー", layout, resizable=False)

class Hanko():
    def __init__(self, name, size=240):
        self.size = size
        self.name = name

    def draw(self):
        image = np.full((self.size,self.size,3), (255,255,255), np.uint8)
        cv2.circle(image, (self.size//2,self.size//2), self.size//2-2, (0,0,255), 2)
        return cv2.imencode('.png', image)[1].tobytes()


def main():
    f = Frame()
    while True:
        # ウィンドウ表示
        event, values = f.window.read()
        #
        if event=="start":
            name = values.get("name")
            hanko = Hanko(name)
            print(hanko.name)            
            image = hanko.draw()
            f.window["image"].update(data=image)

        #クローズボタンの処理
        if event is None:
            print('exit')
            break

    f.window.close()

if __name__=="__main__":
    main()
