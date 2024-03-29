#include <RGBmatrixPanel.h>

#define CLK 11
#define OE   9
#define LAT 10
#define A   A0
#define B   A1
#define C   A2
#define D   A3


RGBmatrixPanel matrix(A, B, C, D, CLK, LAT, OE, false, 64);


// Color definitions
#define BLACK           0x0000
#define BLUE            0x001F
#define RED             0xF800
#define GREEN           0x07E0
#define CYAN            0x07FF
#define MAGENTA         0xF81F
#define YELLOW          0xFFE0
#define WHITE           0xFFFF

const int IMG_WIDTH  = 16;
const int IMG_HEIGHT = 16;
const int IMG_MAX    = 1;

const uint16_t mario[IMG_WIDTH*IMG_HEIGHT] = {
    0xFFFF,0xFFFF,0xFFFF,0xFFFF,0xFFFF,0xD286,0xF223,0xF223,0xF223,0xF223,0xFF9D,0xFFFF,0xFFFF,0xFFFF,0xFFFF,0xFFFF,
    0xFFFF,0xFFFF,0xFFFF,0xFFFF,0xBAC8,0xEA44,0xF223,0xF223,0xF223,0xF223,0xDA65,0xD286,0xD286,0xFFBD,0xFFFF,0xFFFF,
    0xFFFF,0xFFFF,0xFFFF,0xFFFF,0xABC6,0xB3A3,0xB3A3,0xFDCE,0xFDAF,0xBBA3,0xFDCE,0xFF9B,0xFF9D,0xFFFF,0xFFFF,0xFFFF,
    0xFFFF,0xFFFF,0xFFFF,0x9408,0xF62F,0xA403,0xF62E,0xFE0F,0xFE0F,0xA3E3,0xFE2E,0xF611,0xF611,0xFFFE,0xFFFF,0xFFFF,
    0xFFFF,0xFFFF,0xFFFF,0x9406,0xFE2E,0xA3E3,0xA403,0xFE0F,0xFE0F,0xFE0F,0xA3E4,0xFE0F,0xFE0F,0xF611,0xFFFE,0xFFFF,
    0xFFFF,0xFFFF,0xFFFF,0x9406,0xA403,0xF62E,0xFE2E,0xFE0F,0xFE0F,0xABE4,0x9C03,0xA403,0xA3E3,0xFFFB,0xFFFF,0xFFFF,
    0xFFFF,0xFFFF,0xFFFF,0xFFFD,0xFFFC,0xF611,0xFE0F,0xFE0F,0xFE0F,0xFE0F,0xFE2E,0xFE2E,0xFFFA,0xFFFF,0xFFFF,0xFFFF,
    0xFFFF,0xFFFF,0xFFFF,0xFFFF,0x9408,0x9C04,0xD2C3,0xB3A4,0xA3E3,0xA3E3,0xFFFB,0xFFFD,0xFFFF,0xFFFF,0xFFFF,0xFFFF,
    0xFFFF,0xFFFF,0xFFFF,0x9408,0x9C03,0x9C03,0xDA83,0xB3A3,0x9C03,0xCAE2,0xABC5,0x9406,0x9406,0xFFFD,0xFFFF,0xFFFF,
    0xFFFF,0xFFFF,0x9408,0x9C03,0x9C03,0x9C03,0xDA83,0xE263,0xDA83,0xF243,0xB3A3,0x9C03,0x9C03,0x9C05,0xFFFD,0xFFFF,
    0xFFFF,0xFFFF,0xEE31,0xFE2E,0xA403,0xCAE2,0xFD8E,0xEA63,0xF223,0xFD8E,0xD2A3,0xB3C3,0xF62E,0xFE2E,0xFFFD,0xFFFF,
    0xFFFF,0xFFFF,0xF611,0xFE0F,0xFE0F,0xE283,0xEA63,0xF243,0xF223,0xEA63,0xF243,0xFDCE,0xFE0F,0xFE0F,0xFFFD,0xFFFF,
    0xFFFF,0xFFFF,0xF611,0xFE0F,0xD2A4,0xF243,0xF223,0xF223,0xF223,0xF223,0xF223,0xEA63,0xFDCF,0xFE0F,0xFFFD,0xFFFF,
    0xFFFF,0xFFFF,0xFFFE,0xFFFD,0xDA85,0xF223,0xF223,0xFF5B,0xFF9D,0xDA65,0xF223,0xF223,0xFF9B,0xFFFD,0xFFFF,0xFFFF,
    0xFFFF,0xFFFF,0xFFFF,0x9408,0xABC4,0xB3A3,0xFFBA,0xFFFF,0xFFFF,0xFFBD,0xB3A5,0xB3A3,0x9BE5,0xFFFD,0xFFFF,0xFFFF,
    0xFFFF,0xFFFF,0x9408,0x9C03,0x9C03,0x9C03,0xFFFC,0xFFFF,0xFFFF,0xFFFF,0x9406,0x9C03,0x9C03,0x9C05,0xFFFD,0xFFFF
};

//初期化
void setup() {

  matrix.begin();
  matrix.fillScreen(BLACK);
  matrix.drawRect(16,16,16,16, BLUE);
  matrix.drawRGBBitmap(0, 0, mario, IMG_WIDTH, IMG_HEIGHT);
}

//メインループ
void loop() {


}//loop
