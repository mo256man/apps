import PySimpleGUI as sg
import time

class Gui():
    def __init__(self) -> None:
        layout = [[sg.Output(size=(40,5), key="-LOG-")],
                  [sg.Button("Do", key="-BUTTON-")]]
        self.window = sg.Window("サンプル", layout)
    
    def call_task(self, func):
        end_key = ('-THREAD-', '-THEAD ENDED-')
        self.window.start_thread(func, end_key)

    def do_task(self):
        print("時間がかかる仕事をする")
        for i in range(3):
            print(i)
            time.sleep(1)
        print("完了")



def main():
    gui = Gui()
    window = gui.window
    while True:
        event, values = window.read()
        
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        elif event == "-BUTTON-":
            window.start_thread(lambda: gui.do_task(), ('-THREAD-', '-THEAD ENDED-'))
#             gui.call_task(gui.do_task())

    print("done.")
    window.close()

if __name__ == '__main__':
    main()
