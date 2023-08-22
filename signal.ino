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

RGBmatrixPanel matrix(A, B, C, D, CLK, LAT, OE, false, 64);

void setup() {
  matrix.begin();
  drawSingalBase();
  matrix.setTextWrap(false);
  matrix.setTextSize(2);
}

void loop() {
  for (;;) {
    drawSingal("GREEN");
    delay(500);
    drawSingal("YELLOW");
    delay(500);
    drawSingal("RED");
    delay(500);
  }
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
  matrix.fillCircle(17, 8, 5, matrix.Color333(0, 0, 0));
  matrix.fillCircle(32, 8, 5, matrix.Color333(0, 0, 0));
  matrix.fillCircle(47, 8, 5, matrix.Color333(0, 0, 0));
  matrix.fillRect(0, 17, 64, 16, matrix.Color333(0, 0, 0));

  if (signal=="GREEN") {
    color = matrix.Color333(1, 5, 5);
    cx = 17;
    lx = 3;
  } else if (signal=="YELLOW") {
    color = matrix.Color333(7, 7, 0);
    cx = 32;
    lx = 3;
    signal = "YE OW";
    matrix.drawLine(26, 17, 26, 30, matrix.Color333(7, 7, 0));
    matrix.drawLine(26, 30, 30, 30, matrix.Color333(7, 7, 0));
    matrix.drawLine(33, 17, 33, 30, matrix.Color333(7, 7, 0));
    matrix.drawLine(33, 30, 37, 30, matrix.Color333(7, 7, 0));
  } else if (signal=="RED") {
    color = matrix.Color333(7, 0, 0);
    cx = 47;
    lx = 16;
  }
  matrix.fillCircle(cx, 8, 5, color);
  matrix.setCursor(lx, 17);
  matrix.setTextColor(color);
  matrix.println(signal);
}