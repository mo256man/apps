import glob
import tkinter
import datetime
import tkinter.ttk
import PySimpleGUI as sg
from PIL import Image, ImageTk

# パラメータ
mouse_x = 0
mouse_y = 0
mouse_c = 0
x = 0
y = 0
x1 = 0
y1 = 0
n = 0
x_px = 0
y_px = 0
x1_px = 0
y1_px = 0

# クロップサイズ
px = 300

# マウスボタンを押したときの関数
def mouse_press(e):
    global mouse_c, x, y

    # マウスボタンが押されたときmouse_cに1をセット
    mouse_c = 1

    # 読み込んだ画像に長方形を描画
    # 一段目に関数でアウトラインの線を描画しタグを付ける
    # 二段目の関数で長方形を塗りつぶし一段目とは別のタグを付ける。fillは塗りつぶし、stippleは点描画
    cvs.create_rectangle(e.x, e.y, e.x+1, e.y+1, outline="red", tag="rect1")
    cvs.create_rectangle(e.x, e.y, e.x+1, e.y+1, fill="orange", stipple='gray50', tag="rect2") # 色候補 orange, pink
    cvs.create_rectangle(e.x, e.y, e.x+1, e.y+1, fill="pink", stipple='gray50', tag="rect3")   # 色候補 orange, pink
    
    # マウスボタンを押したときの座標をx, yにセット
    x = e.x
    y = e.y

# マウスを動かしているときの関数
def mouse_move(e):
    global mouse_x, mouse_y, end_x, end_y, x_px, y_px, x1_px, y1_px, px

    # マウス座標がマイナスになったときの判定
    if e.x < 0:
        end_x = 0
    else:
        end_x = min(x, e.x)
    
    if e.y < 0:
        end_y = 0
    else:
        end_y = min(y, e.y)

    # マウスの選択エリアが300px X 300pxサイズ以上になると300px X 300pxのエリアの色が変わるよう判定
    if abs(mouse_x - end_x) and abs(mouse_y - end_y) >= px:
        cvs.coords("rect1", mouse_x, mouse_y, end_x, end_y)
        cvs.coords("rect2", mouse_x, mouse_y, end_x, end_y)
        cvs.coords("rect3", end_x, end_y, end_x+px, end_y+px)

        # 300pxエリアの座標を代入
        x_px = end_x
        y_px = end_y
        x1_px = end_x+px
        y1_px = end_y+px
        
    else:
        cvs.coords("rect1", mouse_x, mouse_y, end_x, end_y)
        cvs.coords("rect2", mouse_x, mouse_y, end_x, end_y)
    
    # マウスが動いた座標を逐次mouse_x, mouse_yにセット
    mouse_x = e.x
    mouse_y = e.y

# マウスボタンを離したときの関数
def mouse_release(e):
    global mouse_c, x1, y1, n

    # マウスボタンを離したときにmouse_cに2をセット
    mouse_c = 2

    # マウスボタンを離したときの座標をx1, y1にセット
    x1 = e.x
    y1 = e.y

    # マウスボタンを離したとき描画した図形を消す
    cvs.delete("rect1")
    cvs.delete("rect2")
    cvs.delete("rect3")

    n += 1

# 選択エリアの画像を保存する関数
def img_save(*args):
    global x, y, x1, y1

    crop_img = read_image.crop(box=args)

    # クロップ画像の保存
    d_today = datetime.date.today()   # 日付の取得
    dt_now = datetime.datetime.now()  # 時間の取得

    crop_img.save('./cnn_act/mov/trimming/' +
                        str(d_today) + str("_") +
                        str(dt_now.hour) + str("_") +
                        str(dt_now.minute) + str("_") +
                        str(dt_now.second) + '.png')


def img_save_2(a, b, c, d, *args):
    global x, y, x1, y1, x_px, y_px, x1_px, y1_px

    crop_img_300 = read_image.crop(box=args)

    if abs(c - a) >= px and abs(d - b) >= px:

        d_today = datetime.date.today()   # 日付の取得
        dt_now = datetime.datetime.now()  # 時間の取得

        crop_img_300.save('./cnn_act/mov/trimming/' + str(px) + str("_") + 
                                str(d_today) + str("_") +
                                str(dt_now.hour) + str("_") +
                                str(dt_now.minute) + str("_") +
                                str(dt_now.second) + '.png')
    
    # 座標の初期化
    x = 0
    y = 0
    x1 = 0
    y1 = 0
    x_px = 0
    y_px = 0
    x1_px = 0
    y1_px = 0


# クロップ画像を保存する判定
def img_main():
    global x, y, x1, y1, mouse_c, n, x_px, y_px, x1_px, y1_px, px

    if x != 0 and x1 != 0:
        if mouse_c == 2 and n == 1:
            img_save(x, y, x1, y1)
            img_save_2(x, y, x1, y1, x_px, y_px, x1_px, y1_px)
            n -= 1

    root.after(100, img_main)

# プログラム実行
if __name__ == "__main__":

    # ファイルを開くポップアップ表示
    #fname = sg.popup_get_file('File to open')
    # ファイル読み込み
    #f = glob.glob(fname)
    f = "IMG_20230513_143630.jpg"

    # ファイルを開く
    read_image = Image.open(f)

    # 画像サイズを取得
    w, h = read_image.size
    #print('w=', w, 'h=', h)

    root = tkinter.Tk()
    root.title("Tomo Crop Tool")
    root.resizable(False, False)

    # tkinterで表示できるように画像変換
    img = ImageTk.PhotoImage(image=read_image)

    # Canvasの準備
    cvs = tkinter.Canvas(root, bg="black", width=w, height=h)

    # Canvasに画像を描画
    cvs.create_image(0, 0, image=img, anchor='nw')
    
    # Canvasを配置しマウスのイベントを設定
    cvs.pack()
    cvs.bind("<Motion>", mouse_move)
    cvs.bind("<ButtonPress>", mouse_press)
    cvs.bind(">ButtonRelease>", mouse_release)

    # クロップ画像を保存する判定
    img_main()

    root.mainloop()
