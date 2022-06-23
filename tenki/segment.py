import cv2

def read_7segs(img, digit, cnt):                            # imgはgray前提
    str_num = ""                                            # 読み取った数字が入る変数
    ret = True                                              # 正しく読み取れたかどうかの初期値
    for i in range(cnt):                                    # 7セグ数字の数だけループ
        x1 = i*(digit.w + digit.space)                      # 文字の左座標
        x2 = x1 + digit.w                                   # 右座標（左座標＋文字幅）
        roi = img[:, x1:x2]                                 # 1文字の画像
        seg = []                                            # セグメントオンオフ状況の初期値
        for pos in digit.pos:                               # 1文字の中の各セグメント
            x, y = pos                                      # 注目する場所
            val = 1 if roi[y][x]==255 else 0                # そこの値によって1か0を取る
            seg.append(val)                                 # 配列変数に追加する

        if seg in digit.numbers.values():                   # セグメントのオンオフ状況が数字辞書にあったら
            for key, value in digit.numbers.items():        # 数字辞書で
                if seg == value:                            # セグメントのオンオフ状況が一致したら
                    str_num += key                          # そのキーの値を追加する
        else:                                               # 数字辞書になかったら
            ret = False                                     # 結果をFalseにして
            str_num += "?"                                  # ?を追加する
    return ret, str_num


class Digit():
    def __init__(self, type):
        if type == "co2":
            width, height, thickness, space = 115, 208, 26, 24
        elif type == "temperature":
            width, height, thickness, space = 50, 85, 12, 8
        elif type == "humidity":
            width, height, thickness, space = 50, 85, 12, 8

        self.w = width                                      # 7セグ文字の幅
        self.h = height                                     # 7セグ文字の高さ
        self.t = thickness                                  # セグメントの幅
        self.space = space                                  # 7セグ文字の間隔
        
        # 7個のセグメントの座標
        xa, ya = width//2, thickness//2                     # 上
        xb, yb = width-thickness//2, height//4              # 右上
        xc, yc = xb, 3*yb                                   # 右下
        xd, yd = xa, height-thickness//2                    # 下
        xe, ye = thickness//2, yc                           # 左下
        xf, yf = xe, yb                                     # 左上
        xg, yg = xa, height//2                              # 中
        self.pos = [(xa,ya), (xb,yb), (xc,yc), (xd,yd), (xe,ye), (xf,yf), (xg,yg)]

        # 7セグ文字の値とセグメントのオンオフ状況の辞書
        self.numbers = {"0": [1,1,1,1,1,1,0],
                        "1": [0,1,1,0,0,0,0],
                        "2": [1,1,0,1,1,0,1],
                        "3": [1,1,1,1,0,0,1],
                        "4": [0,1,1,0,0,1,1],
                        "5": [1,0,1,1,0,1,1],
                        "6": [1,0,1,1,1,1,1],
                        "7": [1,1,1,0,0,0,0],
                        "7": [1,1,1,0,0,1,0],
                        "8": [1,1,1,1,1,1,1],
                        "9": [1,1,1,1,0,1,1],
                        "-": [0,0,0,0,0,0,1],
                        "_": [0,0,0,1,0,0,0],
                        " ": [0,0,0,0,0,0,0],
                        }

def readROI(image, type):
    # CO2は二つのエリアを合体して文字を読み取る必要があるのでそれ以外もリスト化している
    if type == "co2":
        params = [(22, 63, 254, 208), (316, 63, 254, 208)]
        digit = Digit("co2")
        cnt = 2
        color = (0, 0, 255)
    elif type == "temperature":
        params = [(749, 52, 108, 85)]
        digit = Digit("temperature")
        cnt = 2
        color = (0, 255, 0)
    elif type == "humidity":
        params = [(749, 194, 108, 85)]
        digit = Digit("humidity")
        cnt = 2
        color = (255, 0, 0)
    else:
        raise ValueError(type + " is unlnown")

    value = ""
    result = True                                               # 全部正しく読み取れたかどうかの初期値
    for x, y, w, h in params:
        roi = image[y:y+h, x:x+w]                               # 7セグ文字があるエリア
        roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)             # グレー化
        _, roi = cv2.threshold(roi, 0, 255, cv2.THRESH_OTSU)    # 二値化
        ret, val = read_7segs(roi, digit, cnt)                  # エリア内の7セグ数字を読み取る
        if not ret:                                             # 正しく読み取れていなかったら
            result = False                                      # 総合結果をFalseにする
        value += val
        cv2.rectangle(image, (x,y), (x+w,y+h), color, 1)
    return result, value


def read_values(image):
    # 温度
    type = "temperature"
    result, value_temp = readROI(image, type)
    if result:
        value_temp = int(value_temp.strip())
    else:
        value_temp = False

    # 湿度
    type = "humidity"
    result, value_hum = readROI(image, type)
    if result:
        value_hum = int(value_hum.strip())
    else:
        value_hum = False

    # CO2濃度　この機種は時計にもなるのか、2桁と2桁の間が空いているので2回取得する必要がある
    type = "co2"
    result, value_co2 = readROI(image, type)
    if result:
        value_co2 = int(value_co2.strip())
    else:
        value_co2 = False

    return value_co2, value_temp, value_hum


if __name__=="__main__":
    filename = "co2.png"
    image = cv2.imread(filename)
    result = read_values(image)
    for value in result:
        print(value)
