#include <RGBmatrixPanel.h>
#define CLK 11
#define OE   9
#define LAT 10
#define A   A0
#define B   A1
#define C   A2
#define D   A3

int cx;
int lx;
int color;
int cnt = 0;              // ループごとに1増えるカウンター
String text;              // 表示したいメッセージ
String double_text;       // 流れるメッセージを表示する際に使う文字列
int text_width;           // テキストの横の大きさ（ピクセル）

RGBmatrixPanel matrix(A, B, C, D, CLK, LAT, OE, false, 64);

void setup() {
  matrix.begin();
  drawSingalBase();
  matrix.setTextWrap(false);
  matrix.setTextSize(2);
}

void loop() {
  drawSingal("GREEN");
}

void drawSingalBase() {
  matrix.fillScreen(matrix.Color333(0, 0, 0));
  matrix.fillCircle(17, 8, 7, matrix.Color333(7, 7, 7));
  matrix.fillCircle(47, 8, 7, matrix.Color333(7, 7, 7));
  matrix.fillRect(17, 1, 30, 15, matrix.Color333(7, 7, 7));

  matrix.fillCircle(17, 8, 5, matrix.Color333(0, 0, 0));
  matrix.fillCircle(32, 8, 5, matrix.Color333(0, 0, 0));
  matrix.fillCircle(47, 8, 5, matrix.Color333(0, 0, 0));
}

void drawSingal(String signal) {
  cnt ++ ;
  matrix.fillCircle(17, 8, 5, matrix.Color333(0, 0, 0));
  matrix.fillCircle(32, 8, 5, matrix.Color333(0, 0, 0));
  matrix.fillCircle(47, 8, 5, matrix.Color333(0, 0, 0));
  matrix.fillRect(0, 17, 64, 16, matrix.Color333(0, 0, 0));

  if (signal=="GREEN") {
    color = matrix.Color333(0, 7, 4);
    cx = 17;
    lx = 3;
    text = "CAUTION!";
    text_width = 6*2*(text.length()+1);
    double_text = text + " " + text;

  } else if (signal=="YELLOW") {
    color = matrix.Color333(7, 7, 0);
    cx = 32;
    lx = 3;
  } else if (signal=="RED") {
    color = matrix.Color333(7, 0, 0);
    cx = 47;
    lx = 16;
  }

  if (cnt >= text_width) {
    cnt = 0;
  }

  matrix.fillCircle(cx, 8, 5, color);
  matrix.setCursor(lx-cnt, 17);
  matrix.setTextColor(color);
  matrix.drawRect(lx-cnt, 17, text_width, 15, matrix.Color333(7, 0, 0));
  matrix.println(double_text);
}