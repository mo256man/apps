import pygame
import sys

class Joy():
    def __init__(self):
        """
        初期設定
        """
        pygame.init()
        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()
        print(self.joystick.get_name())

    def map_axis(self, val):
        """
        ジョイスティックの出力数値を調整
        """
        val = round(val, 2)
        in_min = -1
        in_max = 1
        out_min = -100
        out_max = 100
        result = int((val - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)        # 0から100までの値
        # 0かプラマイ100かのデジタル値にする
        result = 0 if abs(result)<0.5 else 100 * result // abs(result)
        return result

    def map_axis_t(self, val):
        """
        ジョイスティックの出力数値を調整(アナログトリガーのL2 R2ボタン)
        """
        val = self.map_axis(val)
        if val <= 0 and val >= -100:
            in_min = -100
            in_max = 0
            out_min = 0
            out_max = 50
            result = int((val - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)    # 0から100までの値
            result = 100 if result > 0 else 0                                                   # 0か100かのデジタル値
            return result
        else:
            in_min = 0
            in_max = 100
            out_min = 50
            out_max = 100
            result = int((val - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)    # 0から100までの値
            result = 100 if result > 0 else 0                                                   # 0か100かのデジタル値
            return result

    def get_stick(self):
        result = {
            "joy_lx": self.map_axis(self.joystick.get_axis(0)),
            "joy_ly": -self.map_axis(self.joystick.get_axis(1)),
            "joy_rx": self.map_axis(self.joystick.get_axis(2)),
            "joy_ry": -self.map_axis(self.joystick.get_axis(3)),
            "joy_lt": self.map_axis_t(self.joystick.get_axis(4)),
            "joy_rt": self.map_axis_t(self.joystick.get_axis(5)),
            "hat_x": self.joystick.get_hat(0)[0],
            "hat_y": self.joystick.get_hat(0)[1],
            "btn_a": self.joystick.get_button(0),
            "btn_b": self.joystick.get_button(1),
            "btn_x": self.joystick.get_button(2),
            "btn_y": self.joystick.get_button(3),
            "btn_lb": self.joystick.get_button(4),
            "btn_rb": self.joystick.get_button(5),
            "btn_back": self.joystick.get_button(6),
            "btn_start": self.joystick.get_button(7),
            "btn_joyl": self.joystick.get_button(8),
            "btn_joyr": self.joystick.get_button(9),
            "btn_guide": self.joystick.get_button(10),
        }
        # 以下、デバッグ用に入力された値のみ表示させる
        #pressed_buttons = {k:v for k, v in result.items() if v != 0}
        #if len(pressed_buttons) > 0:
        #    print(pressed_buttons)
        return result

    def get_command(self):
        dic = self.get_stick()
        if dic["joy_ly"] == 100 and dic["joy_ry"] == 100:
            command = "↑　↑"
        elif dic["joy_ly"] == -100 and dic["joy_ry"] == -100:
            command = "↓　↓"
        elif dic["joy_ly"] == 100 and dic["joy_ry"] == -100:
            command = "↑　↓"
        elif dic["joy_ly"] == -100 and dic["joy_ry"] == 100:
            command = "↓　↑"
        elif dic["joy_lx"] == -100 and dic["joy_rx"] == -100:
            command = "←　←"
        elif dic["joy_lx"] == 100 and dic["joy_rx"] == 100:
            command = "→　→"
        elif dic["btn_a"] == 1:
            command = "A"
        else:
            command = ""
        return command

def main():
    joy = Joy()
    while True:
        if pygame.event.get():              # イベントがある場合（起動直後を含む　ボタン押しっぱなしを含まない）
            command = joy.get_command()
        else:                               # イベントがない場合（ボタン押しっぱなしを含む）
            pass                            # 何もしない　つまりコマンドは保持される

        if command != "":
            print(command)

        if command == "A":
            sys.exit()                      # プログラム中断

if __name__ == "__main__":
    main()