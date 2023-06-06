import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont

def cv2_putText_5(img, text, org, fontFace, fontScale, color, mode=0):
# cv2.putText()にないオリジナル引数「mode」　orgで指定した座標の基準
# 0（デフォ）＝cv2.putText()と同じく左下　1＝左上　2＝中央

    # テキスト描写域を取得
    fontPIL = ImageFont.truetype(font = fontFace, size = fontScale)
    dummy_draw = ImageDraw.Draw(Image.new("RGB", (0,0)))
    bbox = dummy_draw.multiline_textbbox((0, 0), text, font=fontPIL)
    _, _, text_w, text_h = bbox
#    text_w, text_h = dummy_draw.textsize(text, font=fontPIL)
#    text_b = int(0.1 * text_h) # バグにより下にはみ出る分の対策

    # テキスト描写域の左上座標を取得（元画像の左上を原点とする）
    x, y = org
    offset_x = [0, 0, text_w//2]
    offset_y = [text_h, 0, text_h//2]
    x0 = x - offset_x[mode]
    y0 = y - offset_y[mode]
    img_h, img_w = img.shape[:2]

    # 画面外なら何もしない
    if not ((-text_w < x0 < img_w) and (-text_h < y0 < img_h)) :
        print ("out of bounds")
        return img

    # テキスト描写域の中で元画像がある領域の左上と右下（元画像の左上を原点とする）
    x1, y1 = max(x0, 0), max(y0, 0)
    x2, y2 = min(x0+text_w, img_w), min(y0+text_h, img_h)

    # テキスト描写域と同サイズの黒画像を作り、それの全部もしくは一部に元画像を貼る
    text_area = np.full((text_h,text_w,3), (0,0,0), dtype=np.uint8)
    text_area[y1-y0:y2-y0, x1-x0:x2-x0] = img[y1:y2, x1:x2]

    # それをPIL化し、フォントを指定してテキストを描写する（色変換なし）
    imgPIL = Image.fromarray(text_area)
    draw = ImageDraw.Draw(imgPIL)
    draw.text(xy = (0, 0), text = text, fill = color, font = fontPIL)

    # PIL画像をOpenCV画像に戻す（色変換なし）
    text_area = np.array(imgPIL, dtype = np.uint8)

    # 元画像の該当エリアを、文字が描写されたものに更新する
    img[y1:y2, x1:x2] = text_area[y1-y0:y2-y0, x1-x0:x2-x0]

    return img

def main():
    img = np.full((200,400,3), (160,160,160), dtype=np.uint8)
    imgH, imgW = img.shape[:2]

    fontPIL = "DFLGS9.TTC" # DF麗雅宋
    size = 30
    text = "日本語も\n可能なり"
    color = (255,0,0)

    positions = [(-imgW,-imgH),                 # これは画像外にあり描写されない
                 (0,0), (0,imgH//2), (0,imgH),
                 (imgW//2,0), (imgW//2,imgH//2), (imgW//2,imgH),
                 (imgW,0), (imgW,imgH//2), (imgW,imgH)]

    for pos in positions:
        img = cv2.circle(img, pos, 60, (0,0,255), 3)
        img = cv2_putText_5(img = img,
                            text = text,
                            org = pos,          # 円の中心と同じ座標を指定した
                            fontFace = fontPIL,
                            fontScale = size,
                            color = color,
                            mode = 2)           # 今指定した座標は文字描写域の中心だぞ

    cv2.imshow("", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
