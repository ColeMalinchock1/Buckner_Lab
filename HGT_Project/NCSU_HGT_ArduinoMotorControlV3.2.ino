// ScoliosisMotorOutputArduino_displayKeypadV3.2
// Edward Katz
// 7/3/2023

// Multiple opensource libraries are used in this project, you will need to add them to your workspace before it runs.
//  U8g2 library exists in Arduino's database. Use Tools->Manage Libraries.
//    Search U8g2; install the "U8g2" library by Oliver.
//  Keypad library exists in Arduino's database. Use Tools->Manage Libraries.
//    Search Keypad; install the "Keypad" library by Mark Stanley, Alexander Brevig (may be a few entries down in the list).
//  SD library exists in Arduino's database. Use Tools->Manage Libraries.
//    Search SD; install the "SD" library by Arduino/Sparkfun (should be the first entry). 


#include <Arduino.h>
#include <U8g2lib.h>

#include <Keypad.h>

#include <SPI.h>
#include <SD.h>

#ifdef U8X8_HAVE_HW_SPI
#include <SPI.h>
#endif
#ifdef U8X8_HAVE_HW_I2C
#include <Wire.h>
#endif

#include <stdio.h>
#include <stdlib.h>

// NCSU MAE Logo Bitmap startup splash screen
// version 1

#define u8g_MAElogo_width 128
#define u8g_MAElogo_height 64

static unsigned char u8g_MAElogo_bits[] = {
 0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,
 0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,
 0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,
 0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,
 0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xfb,0xff,0xff,0xff,0xbf,0xff,0xff,0xff,
 0xff,0xff,0xff,0xff,0xff,0xff,0xdf,0xfd,0xfb,0x7f,0xf0,0xff,0xff,0xfd,0x1f,
 0xf8,0xff,0xbb,0xff,0xff,0xff,0xff,0xdf,0x8d,0xfb,0x3f,0xbf,0xe2,0xb6,0xe8,
 0x7f,0x4e,0x3e,0xe3,0x73,0xff,0xff,0xff,0xdf,0x2d,0x1b,0xbe,0x3f,0xcb,0xb6,
 0xcd,0x7e,0xe3,0xd9,0xba,0x6d,0xf0,0xff,0xff,0x1f,0x5c,0xdb,0xbe,0xb1,0xc7,
 0xb6,0xdd,0x7e,0xf7,0xe8,0xbb,0x6d,0xf7,0xff,0xff,0xdf,0x4d,0xdb,0xbe,0xb7,
 0xdb,0xb6,0x5d,0x7f,0x37,0xeb,0xbb,0x6d,0xf7,0xff,0xff,0xdf,0x6d,0xdb,0x3e,
 0xb7,0xdb,0xb9,0x3d,0x7f,0xb7,0xeb,0xbb,0x6d,0xf7,0xff,0xff,0xdf,0x0d,0x1b,
 0x7e,0xb0,0xc3,0xbb,0x31,0x7f,0x37,0x18,0xa6,0x61,0xf7,0xff,0xff,0xff,0xff,
 0xff,0xff,0xff,0xff,0xff,0xbf,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,
 0xff,0xff,0xff,0xff,0xff,0xff,0x9f,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,
 0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,
 0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,
 0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,
 0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,
 0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xdf,0xff,0xff,
 0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xbf,0xff,
 0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0x7f,
 0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xef,0x0d,0x1f,0xec,0xbf,0xff,0xff,
 0x7f,0xfe,0x3f,0x9f,0xff,0xff,0xff,0xff,0xff,0xcf,0xe5,0xdf,0xc7,0x1c,0xff,
 0xff,0xff,0xfc,0x1f,0x0e,0xff,0xff,0xff,0xff,0xff,0x8f,0xf5,0x9f,0xef,0xb2,
 0xe3,0xff,0xff,0xf9,0x0f,0x00,0xfe,0xff,0xff,0xff,0xff,0xaf,0xf5,0x3f,0xec,
 0xb1,0xdd,0xff,0xff,0x73,0x06,0x00,0xcc,0xff,0xff,0xff,0xff,0x2f,0xf5,0xff,
 0x6d,0xb4,0xc1,0xff,0xff,0x67,0xf0,0xff,0xc0,0xff,0xff,0xff,0xff,0x6f,0xe4,
 0xff,0x6d,0xb7,0xfd,0xff,0xff,0x0f,0xfc,0xff,0xc7,0xff,0xff,0xff,0xff,0xef,
 0x0d,0x1e,0x4c,0x30,0xc3,0xff,0xff,0x1f,0xfe,0xff,0xcf,0xff,0xff,0xff,0xff,
 0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0x3f,0xff,0xff,0x9f,0xff,0xff,0xff,
 0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0x07,0xfe,0xff,0x3f,0xfc,0xff,
 0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xc3,0xfc,0xff,0x7f,0xf8,
 0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xc3,0xf9,0xff,0xff,
 0xf8,0xff,0xff,0xc3,0xff,0xc3,0xff,0xc3,0xff,0x03,0x00,0xff,0xe7,0xf3,0xff,
 0xff,0xfc,0xff,0xff,0x81,0xff,0xc1,0xff,0xc3,0xff,0x01,0x00,0xff,0xe7,0xe7,
 0xff,0xfe,0xfc,0xff,0xff,0x81,0xff,0xc1,0xff,0x81,0xff,0x01,0x00,0xff,0xf3,
 0xcf,0x7f,0xff,0xfd,0xff,0xff,0x81,0xff,0xc0,0xff,0x81,0xff,0xe1,0xff,0xff,
 0xf3,0x9f,0x9f,0xff,0xf9,0xff,0xff,0x01,0xff,0xc0,0xff,0x80,0xff,0xe1,0xff,
 0xff,0xf8,0x3f,0xc3,0xff,0xe1,0xff,0xff,0x01,0xff,0xc0,0xff,0x08,0xff,0xe1,
 0xff,0xff,0xf8,0x7f,0xc0,0xff,0xe1,0xff,0xff,0x21,0x7e,0xc4,0xff,0x18,0xff,
 0xe1,0xff,0xff,0xf8,0xff,0xc0,0xff,0xe1,0xff,0xff,0x21,0x7e,0xc4,0x7f,0x18,
 0xff,0xe1,0xff,0xff,0xfb,0x7f,0xe0,0xff,0xf9,0xff,0xff,0x21,0x3e,0xc6,0x7f,
 0x3c,0xfe,0xe1,0xff,0xff,0xf3,0x7f,0xe0,0xff,0xf9,0xff,0xff,0x61,0x3c,0xc6,
 0x3f,0x3c,0xfe,0xe1,0xff,0xff,0xf3,0x7f,0xe0,0xff,0xf9,0xff,0xff,0x61,0x3c,
 0xc6,0x3f,0x3e,0xfc,0x01,0x80,0xff,0xf3,0xff,0xc8,0xff,0xf9,0xff,0xff,0x61,
 0x1c,0xc7,0x3f,0x7e,0xfc,0x01,0x80,0xff,0xf1,0xff,0x9f,0xff,0xf1,0xff,0xff,
 0xe1,0x18,0xc7,0x1f,0x7e,0xfc,0xe1,0xff,0xff,0xf1,0xff,0x3f,0xff,0xf1,0xff,
 0xff,0xe1,0x18,0xc7,0x1f,0x7f,0xf8,0xe1,0xff,0xff,0xe1,0xff,0x7f,0xfe,0xf0,
 0xff,0xff,0xe1,0x81,0xc7,0x1f,0x7f,0xf8,0xe1,0xff,0xff,0xe7,0xff,0xff,0xfc,
 0xfc,0xff,0xff,0xe1,0x81,0xc7,0x0f,0x00,0xf0,0xe1,0xff,0xff,0xcf,0xff,0xff,
 0x79,0xfe,0xff,0xff,0xe1,0xc1,0xc7,0x0f,0x00,0xf0,0xe1,0xff,0xff,0xcf,0xff,
 0xff,0x73,0xff,0xff,0xff,0xe1,0xc3,0xc7,0x87,0xff,0xf1,0xe1,0xff,0xff,0x9f,
 0xff,0xff,0x07,0xff,0xff,0xff,0xe1,0xc3,0xc7,0x87,0xff,0xe1,0xe1,0xff,0xff,
 0x1f,0xff,0xff,0x0f,0xfe,0xff,0xff,0xe1,0xff,0xc7,0xc7,0xff,0xe3,0xe1,0xff,
 0xff,0x1f,0xfe,0xff,0x07,0xff,0xff,0xff,0xe1,0xff,0xc7,0xc3,0xff,0xe3,0x01,
 0x00,0xff,0xff,0xf8,0xff,0x23,0xff,0xff,0xff,0xe1,0xff,0xc7,0xe3,0xff,0xc3,
 0x01,0x00,0xff,0xff,0xe1,0xff,0x78,0xfe,0xff,0xff,0xe1,0xff,0xc7,0xe1,0xff,
 0xc7,0x01,0x00,0xff,0xff,0x03,0x00,0xf8,0xfc,0xff,0xff,0xff,0xff,0xff,0xff,
 0xff,0xff,0xff,0xff,0xff,0xff,0x63,0xc0,0xf8,0xf9,0xff,0xff,0xff,0xff,0xff,
 0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xf7,0xf1,0xfd,0xf3,0xff,0xff,0xff,0xff,
 0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xf1,0xff,0xe7,0xff,0xff,0xff,
 0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xcf,0xff,0xff,
 0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xbf,0xff,
 0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0x7f,
 0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,
 0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,
 0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,
 0xff,0xff,0xff,0xff };

//
//

// set up variables using the SD utility library functions:
Sd2Card card;
SdVolume volume;
SdFile root;

const byte ROWS = 4; // defines the four keypad rows
const byte COLS = 4; // defines the four keypad columns
//define the cymbols on the buttons of the keypads
char hexaKeys[ROWS][COLS] = { // defines each button on the keypad in CHAR form
  {'1','2','3','A'},
  {'4','5','6','B'},
  {'7','8','9','C'},
  {'*','0','#','D'}
};
byte rowPins[ROWS] = {30, 32, 34, 36}; //connect to the row pinouts of the keypad 
byte colPins[COLS] = {31, 33, 35, 37}; //connect to the column pinouts of the keypad

// When Keypad is facing you, pinout from left to right on Arduino Mega:
// (30/D30/PC/A15), (32/D32/PC5/A13), (34/D34/PC3/A11), (36/D36/PC1/A9),
// (31/D31/PC6/A14), (33/D33/PC4/A12), (35/D35/PC2/A10), (37/D37/PC0/A8)


//initialize an instance of class NewKeypad
Keypad customKeypad = Keypad(makeKeymap(hexaKeys), rowPins, colPins, ROWS, COLS); 

// Pin to take input from load cell
const int inputPin = A0; // Analogue input (A0/PF0/ADC[0])
// Two pinouts to motor
const int abovePin = 22; // Direction pin (22/D22/PA0/AD0)
const int belowPin = 24; // Direction pin (24/D24/PA2/AD2)
const int speedPin = 43; // Speed pin (43/D43/PL6)
// Emergency Stop relay pin
const int stopPin = 47; // Stop pin (47/D47/PL2)
// SD Card Chip Select Pin
const int chipSelect = 53; // SD Chip Select (53/D53/PB0/SS)



double setWeight = 0; // variable for desired weight for applied pressure

// 128x64 OLED I2C display setup. See File->examples->U8G2->Full Buffer->Hello World (or any other program) to see other examples listed.
U8G2_SSD1306_128X64_NONAME_F_HW_I2C u8g2(U8G2_R0, /* reset=*/ U8X8_PIN_NONE);

bool systemStartup = true;
bool systemStartupSplashscreen = true;
bool sdCardInitialized = true;

double currentWeight = 0;
double previousWeight = 0;

unsigned long sampleRateBufferAlpha;
unsigned long sampleRateBufferBeta = 0;
bool SampleRate = true;
bool activeMotion = true;
double setSampleRate;

double deadband = 0.75;

bool applyingTension = false;

unsigned long tensionBurstBufferA;
unsigned long tensionBurstBufferB = 0;

File sensorData;
String dataFileName;

long dataLogBuffer1 = 0;
long dataLogBuffer2 = 0;
long dataCounterTotalBuffer = 1;
int dataCounterLocalBuffer = 1;
int dataFileNameCounter = 1;



void setup() { // Setup to run once; initiates pinouts, serial connection, and u8g2

  pinMode(abovePin, OUTPUT);
  pinMode(belowPin, OUTPUT);
  pinMode(speedPin, OUTPUT);
  pinMode(stopPin, OUTPUT);
  digitalWrite(abovePin, LOW);
  digitalWrite(belowPin, LOW);
  digitalWrite(speedPin, LOW);
  digitalWrite(stopPin, LOW);

  Serial.begin(9600);
  Serial.println();
  Serial.println("Serial connection established. ");

  Serial.print("Initializing SD card...");

  if (!SD.begin(53)) {
    Serial.println("initialization failed!");
    sdCardInitialized = false;
  }
  Serial.println("initialization done.");

  // open the file. note that only one file can be open at a time,
  // so you have to close this one before opening another.
  dataFileName = "hgtlog.csv";
  sensorData = SD.open(dataFileName, FILE_WRITE);

  // if the file opened okay, write to it:
  if (sensorData) {
    Serial.print("Formatting data file...");
    sensorData.println("Halo Gravity Traction Data Log. Starting Data Collection.");
    sensorData.println();
    sensorData.println("Data #, SetTension (lbs), Tension (lbs), MotorStatus");
    // close the file:
    sensorData.close();
    Serial.println("done.");
  } else {
    // if the file didn't open, print an error:
    Serial.println("Error opening data file.");
  }


  

  u8g2.begin();
  
  u8g2.setFontRefHeightExtendedText();
  u8g2.setDrawColor(1);
  u8g2.setFontPosTop();
  u8g2.setFontDirection(0);
  Serial.println("u8g2 setup complete. ");
  Serial.print("Deadband: ");
  Serial.print(deadband);
  Serial.println("lbs \n");
  Serial.println("Beginning main loop. ");

}

///////////////////////////////////////////////




void loop() { // Main code loop

//GET ANALOG INPUT
  int sensorValue = analogRead(inputPin);
  float voltage = sensorValue * (5.0 / 1023.0); // Convert ADC value to voltage

  double currentWeight = ((voltage - 4.9874) / -0.0966); // conversion from weight to volts, derived from load cell calibration 
  double weight;

  if (activeMotion == true){
    weight = (0.40 * currentWeight) + (0.60 * previousWeight);
    previousWeight = weight;
  }

  if (activeMotion == false){
    weight = (0.05 * currentWeight) + (0.95 * previousWeight);
    previousWeight = weight;
  }
  
  

  u8g2.clearBuffer();

  if (systemStartupSplashscreen == true){
    u8g2.clearBuffer();
    u8g2.drawXBM( 0, 0, u8g_MAElogo_width, u8g_MAElogo_height, u8g_MAElogo_bits);
    u8g2.sendBuffer();
    delay(5000);
    u8g2.clearBuffer();
    systemStartupSplashscreen = false;
  }

  if ((sdCardInitialized == false) && (systemStartup == true)){
    u8g2.setCursor(0,0);
    u8g2.setFont(u8g2_font_lubB10_te);
    u8g2.print("Warning!");
    u8g2.setCursor(0, 15);
    u8g2.setFont(u8g2_font_crox5t_tf);
    u8g2.print("SD Card");
    u8g2.setCursor(0, 35);
    u8g2.print("Unavailable");
    u8g2.sendBuffer();
    delay(2000);
    u8g2.clearBuffer();
  }



////////////////////////////////////////////////////////////
// SCREEN UPDATING
////////////////////////////////////////////////////////////


  char customKey = customKeypad.getKey();

  //EDITING SETWEIGHT WITH NUMBERPAD
  if ((customKey == '#') || (systemStartup == true)){
    int digitPlace = 1; // which place digit you are editing; when user types, this goes up by one (first editing 10s place, then the 1s place, then tenths place)
    double newSetWeight = 0;
    double newKeypadDouble = 0;
    digitalWrite(abovePin, LOW);
    digitalWrite(belowPin, LOW);
    digitalWrite(speedPin, LOW);
    char newSetWeightBuffer[6];
    while (digitPlace < 4){
      char customKey = customKeypad.getKey();
      if (customKey){
        bool keypadCheck = false;
        if (customKey == '1'){newKeypadDouble = 1; digitPlace++; keypadCheck = true;}
        if (customKey == '2'){newKeypadDouble = 2; digitPlace++; keypadCheck = true;}
        if (customKey == '3'){newKeypadDouble = 3; digitPlace++; keypadCheck = true;}
        if (customKey == '4'){newKeypadDouble = 4; digitPlace++; keypadCheck = true;}
        if (customKey == '5'){newKeypadDouble = 5; digitPlace++; keypadCheck = true;}
        if (customKey == '6'){newKeypadDouble = 6; digitPlace++; keypadCheck = true;}
        if (customKey == '7'){newKeypadDouble = 7; digitPlace++; keypadCheck = true;}
        if (customKey == '8'){newKeypadDouble = 8; digitPlace++; keypadCheck = true;}
        if (customKey == '9'){newKeypadDouble = 9; digitPlace++; keypadCheck = true;}
        if (customKey == '0'){newKeypadDouble = 0; digitPlace++; keypadCheck = true;}
        if (keypadCheck == true){newSetWeight = (newSetWeight + (newKeypadDouble/(0.01*(pow(10, (digitPlace-1))))));}
        keypadCheck = false;

        if (customKey == '*'){
          u8g2.setCursor(0,0);
          u8g2.setFont(u8g2_font_lubB10_te);
          u8g2.print("Cancelled.");
          u8g2.setCursor(0, 15);
          u8g2.setFont(u8g2_font_fub30_tf);
          u8g2.print(newSetWeight);
          u8g2.print("lb");
          u8g2.sendBuffer();
          u8g2.clearBuffer();
          break;
        }
      }

      dtostrf(newSetWeight, -3 /*min width, left justified*/, 1 /*characters after decimal*/, newSetWeightBuffer /* buffer to store*/);

      u8g2.setCursor(0,0);
      u8g2.setFont(u8g2_font_lubB10_te);
      u8g2.print("set weight:");
      u8g2.setCursor(0, 15);
      u8g2.setFont(u8g2_font_fub30_tf);
      if (newSetWeight < 10){u8g2.print("0");}
      u8g2.print(newSetWeightBuffer);
      u8g2.print("lb");
      u8g2.setCursor(0, 20);
      if (digitPlace == 1){u8g2.print("_  ");}
      if (digitPlace == 2){u8g2.print("  _ ");}
      if (digitPlace == 3){u8g2.print("     _");}
      u8g2.sendBuffer();
      u8g2.clearBuffer();

      // Confirming user input data
      bool confirmed = false;
      bool cancelled = false;
      if (digitPlace == 4){
        while ((confirmed == false) && (cancelled == false)){
          u8g2.setCursor(0,0);
          u8g2.setFont(u8g2_font_lubB10_te);
          u8g2.print("Confirm change?");
          u8g2.setCursor(0,15);
          u8g2.print("* cancel|# confirm");
          u8g2.setCursor(0, 30);
          u8g2.setFont(u8g2_font_fub30_tf);
          u8g2.print(newSetWeightBuffer);
          u8g2.print("lb");
          u8g2.sendBuffer();
          u8g2.clearBuffer();

          char customKey = customKeypad.getKey();
          if (customKey == '*'){
            u8g2.setCursor(0,0);
            u8g2.setFont(u8g2_font_lubB10_te);
            u8g2.print("Cancelled.");
            u8g2.setCursor(0, 15);
            u8g2.setFont(u8g2_font_fub30_tf);
            u8g2.print(newSetWeightBuffer);
            u8g2.print("lb");
            u8g2.sendBuffer();
            u8g2.clearBuffer();

            cancelled = true;
            if (systemStartup == true){
            digitPlace = 1; // resets digitPlace in case of cancel on startup
            newSetWeight = 0;
            newKeypadDouble = 0;
            }

            delay(2000);

          }
          if (customKey == '#'){
            u8g2.setCursor(0,0);
            u8g2.setFont(u8g2_font_lubB10_te);
            u8g2.print("Weight set.");
            u8g2.setCursor(0, 15);
            u8g2.setFont(u8g2_font_fub30_tf);
            u8g2.print(newSetWeightBuffer);
            u8g2.print("lb");
            u8g2.sendBuffer();
            u8g2.clearBuffer();

            confirmed = true;
            setWeight = newSetWeight;

            delay(2000);
          }
        } // while 
      } // if digitplace = 4
    } // while digitplace < 4


    
  } //if ((customKey == '#') || (systemStartup == true)){

  // SET SAMPLE RATE
  if ((customKey == 'C') || (systemStartup == true)){
    int digitPlace = 1; // which place digit you are editing; when user types, this goes up by one (first editing 1s place, then the tenths place, then hundredths place)
    double newSetSampleRate = 0;
    double newKeypadDouble = 0;
    digitalWrite(abovePin, LOW);
    digitalWrite(belowPin, LOW);
    digitalWrite(speedPin, LOW);
    char newSetSampleRateBuffer[6];
    while (digitPlace < 4){
      char customKey = customKeypad.getKey();
      if (customKey){
        bool keypadCheck = false;
        if (customKey == '1'){newKeypadDouble = 1; digitPlace++; keypadCheck = true;}
        if (customKey == '2'){newKeypadDouble = 2; digitPlace++; keypadCheck = true;}
        if (customKey == '3'){newKeypadDouble = 3; digitPlace++; keypadCheck = true;}
        if (customKey == '4'){newKeypadDouble = 4; digitPlace++; keypadCheck = true;}
        if (customKey == '5'){newKeypadDouble = 5; digitPlace++; keypadCheck = true;}
        if (customKey == '6'){newKeypadDouble = 6; digitPlace++; keypadCheck = true;}
        if (customKey == '7'){newKeypadDouble = 7; digitPlace++; keypadCheck = true;}
        if (customKey == '8'){newKeypadDouble = 8; digitPlace++; keypadCheck = true;}
        if (customKey == '9'){newKeypadDouble = 9; digitPlace++; keypadCheck = true;}
        if (customKey == '0'){newKeypadDouble = 0; digitPlace++; keypadCheck = true;}
        if (keypadCheck == true){newSetSampleRate = (newSetSampleRate + (newKeypadDouble/(0.01*(pow(10, (digitPlace-1))))));}
        keypadCheck = false;
      }

      dtostrf(newSetSampleRate, -3 /*min width, left justified*/, 1 /*characters after decimal*/, newSetSampleRateBuffer /* buffer to store*/);

      u8g2.setCursor(0,0);
      u8g2.setFont(u8g2_font_lubB10_te);
      u8g2.print("Set Sample Rate:");
      u8g2.setCursor(0, 15);
      u8g2.setFont(u8g2_font_fub30_tf);
      if (newSetSampleRate < 10){u8g2.print("0");}
      u8g2.print(newSetSampleRateBuffer);
      u8g2.print("s.");
      u8g2.setCursor(0, 20);
      if (digitPlace == 1){u8g2.print("_  ");}
      if (digitPlace == 2){u8g2.print("  _ ");}
      if (digitPlace == 3){u8g2.print("     _");}
      u8g2.sendBuffer();
      u8g2.clearBuffer();

      // Confirming user input data
      bool confirmed = false;
      bool cancelled = false;
      if (digitPlace == 4){
        while ((confirmed == false) && (cancelled == false)){
          u8g2.setCursor(0,0);
          u8g2.setFont(u8g2_font_lubB10_te);
          u8g2.print("Confirm change?");
          u8g2.setCursor(0,15);
          u8g2.print("* cancel|# confirm");
          u8g2.setCursor(0, 30);
          u8g2.setFont(u8g2_font_fub30_tf);
          u8g2.print(newSetSampleRateBuffer);
          u8g2.print("s.");
          u8g2.sendBuffer();
          u8g2.clearBuffer();

          char customKey = customKeypad.getKey();
          if (customKey == '*'){
            u8g2.setCursor(0,0);
            u8g2.setFont(u8g2_font_lubB10_te);
            u8g2.print("Cancelled.");
            u8g2.setCursor(0, 15);
            u8g2.setFont(u8g2_font_fub30_tf);
            u8g2.print(newSetSampleRateBuffer);
            u8g2.print("lb");
            u8g2.sendBuffer();
            u8g2.clearBuffer();

            cancelled = true;
            if (systemStartup == true){
              digitPlace = 1; // resets digitPlace in case of cancel on startup
              newSetSampleRate = 0;
              newKeypadDouble = 0;
            }

            delay(2000);

          }
          if (customKey == '#'){
            u8g2.setCursor(0,0);
            u8g2.setFont(u8g2_font_lubB10_te);
            u8g2.print("Sample Rate Set.");
            u8g2.setCursor(0, 15);
            u8g2.setFont(u8g2_font_fub30_tf);
            u8g2.print(newSetSampleRateBuffer);
            u8g2.print("s.");
            u8g2.sendBuffer();
            u8g2.clearBuffer();

            confirmed = true;
            setSampleRate = newSetSampleRate;


            delay(2000);
          }
        } // while 
      } // if digitplace = 4
    } // while digitplace < 4

    systemStartup = false;
    
  } //if ((customKey == 'C') || (systemStartup == true)){



  int counter = 0;

  if (customKey && (customKey != '#') && (customKey != 'C')){
    while (counter < 20){ // counter used as a kind of timer for the set weight screen
      // EMERGENCY STOP WITH D
      bool emergStop = false;
      if (customKey == 'D'){
        digitalWrite(abovePin, LOW);
        digitalWrite(belowPin, LOW);
        digitalWrite(speedPin, LOW);
        digitalWrite(stopPin, LOW);
        emergStop = true;
        u8g2.setCursor(0,0);
        u8g2.setFont(u8g2_font_lubB10_te);
        u8g2.print("Press D to restart");
        u8g2.setCursor(0, 15);
        u8g2.setFont(u8g2_font_fub30_tf);
        u8g2.print("STOP");
        u8g2.sendBuffer();
        u8g2.clearBuffer();
        Serial.println("WARNING: System Stop -- key command");

        if (sdCardInitialized == true){
          sensorData = SD.open(dataFileName, FILE_WRITE);
          sensorData.println("SYSTEM STOP ---- KEY COMMAND. Data collection halted until restart.");
          sensorData.close();
        }

        delay (1000);
        while (emergStop == true){
          char customKey = customKeypad.getKey();
          if (customKey == 'D'){
            emergStop = false;
            u8g2.setCursor(0,0);
            u8g2.setFont(u8g2_font_lubB10_te);
            u8g2.print("Restarting...");
            u8g2.setCursor(0, 15);
            u8g2.setFont(u8g2_font_fub30_tf);
            u8g2.print("STOP");
            u8g2.sendBuffer();
            delay(1000);
            u8g2.clearBuffer();
            counter = 20;
            digitalWrite(stopPin, HIGH);
          }
        }
      } // if customkey == D

      digitalWrite(abovePin, LOW);
      digitalWrite(belowPin, LOW);
      digitalWrite(speedPin, LOW);

      // drawing the setweight screen
      char setWeightBuffer[6];
      dtostrf(setWeight, -3 /*min width, left justified*/, 1 /*characters after decimal*/, setWeightBuffer /* buffer to store*/);
      
      u8g2.setCursor(0,0);
      u8g2.setFont(u8g2_font_lubB10_te);
      u8g2.print("set weight:");
      u8g2.setCursor(0, 15);
      u8g2.setFont(u8g2_font_fub30_tf);
      u8g2.print(setWeightBuffer);
      u8g2.print("lb");

      u8g2.sendBuffer();
      u8g2.clearBuffer();
      counter++; // adding to timer
      char customKey = customKeypad.getKey(); // calls customKey again

      //EDITING setWeight WITH A AND B
      if (customKey == 'A'){
        setWeight = (setWeight + 0.5);
        counter = 0;
      }
      if (customKey == 'B'){
        setWeight = (setWeight - 0.5);
        counter = 0;
      }
    } // while (counter < 20)
  } // if (customKey && customKey != '#')

  else{
    char weightBuffer[6];
    dtostrf(weight, -3 /*min width, left justified*/, 1 /*characters after decimal*/, weightBuffer /* buffer to store*/);

    char setWeightBuffer[6];
    dtostrf(setWeight, -3 /*min width, left justified*/, 1 /*characters after decimal*/, setWeightBuffer /* buffer to store*/);


    u8g2.setCursor(0,2);
    u8g2.setFont(u8g2_font_lubB10_te);
    u8g2.print("current weight:");
    u8g2.setCursor(0,15);
    u8g2.setFont(u8g2_font_fub30_tf);
    u8g2.print(weightBuffer);
    u8g2.print("lb");
    u8g2.setCursor(0,50);
    u8g2.setFont(u8g2_font_lubB10_te);
    u8g2.print("Setpoint: ");
    u8g2.print(setWeightBuffer);
    u8g2.print("lb");
  }

  u8g2.sendBuffer(); 

////////////////////////////////////////////




  sampleRateBufferAlpha = millis();

//////////////////////////////////////////////////
// PIN OUTPUT:
//////////////////////////////////////////////////

  if (((sampleRateBufferAlpha - sampleRateBufferBeta) > (setSampleRate*1000)) || (activeMotion == true) || (SampleRate == false)){
    if (weight < (setWeight - deadband)) { // tightens cable if weight is too low
      digitalWrite(abovePin, LOW);
      digitalWrite(belowPin, HIGH);
      digitalWrite(stopPin, HIGH);
      activeMotion = true;
      sampleRateBufferBeta = sampleRateBufferAlpha;
      applyingTension = true;
      tensionBurstBufferB = millis();
    } 
    else if ((weight < setWeight) && (weight > (setWeight - deadband)) && (activeMotion == true)){ // overshoots to the setpoint if tightening
      digitalWrite(abovePin, LOW);
      digitalWrite(belowPin, HIGH);
      digitalWrite(stopPin, HIGH);
      activeMotion = true;
      sampleRateBufferBeta = sampleRateBufferAlpha;
      applyingTension = true;
      tensionBurstBufferB = millis();

    }
    else if (weight > (setWeight + deadband)) { // loostens cable if weight is too high
      digitalWrite(abovePin, HIGH);
      digitalWrite(belowPin, LOW);
      activeMotion = true;
      sampleRateBufferBeta = sampleRateBufferAlpha;
      applyingTension = false;
      tensionBurstBufferB = millis();

    } 
      else if ((weight > (setWeight + 1.0)) && (weight < (setWeight + deadband)) && (activeMotion == true)){ // overshoots to 1.0lb before the setpoint if loostening
      digitalWrite(abovePin, HIGH);
      digitalWrite(belowPin, LOW);
      activeMotion = true;
      sampleRateBufferBeta = sampleRateBufferAlpha;
      applyingTension = false;
      tensionBurstBufferB = millis();

    }
    else { // does nothing if weight = setweight (+-deadband)
      digitalWrite(abovePin, LOW);
      digitalWrite(belowPin, LOW);
      activeMotion = false;
      sampleRateBufferBeta = sampleRateBufferAlpha;
      applyingTension = false;

    }

    if (((setWeight - 3.0) > weight) || ((setWeight + 3.0) < weight)){
      digitalWrite(speedPin, HIGH);
    }
    else{
      digitalWrite(speedPin, LOW);
    }


  
  }


/////////////////////////////////
// Tension Burst 
/////////////////////////////////

  if (weight > (setWeight-0.1)){
    tensionBurstBufferB = millis();
  }

  tensionBurstBufferA = millis();

  if (((tensionBurstBufferA - tensionBurstBufferB) > 15000) && (activeMotion == false) && ((weight < setWeight) && (weight > (setWeight - deadband)))){
    tensionBurst();
    tensionBurstBufferB = tensionBurstBufferA;
  }



////////////////////////////////////
// Data Logging
////////////////////////////////////

  if (sdCardInitialized == true){
    dataLogBuffer1 = millis();
    int dataLogRate = 1000; // Sample Rate for the Data Log in milliseconds. Currently set to once per second. 
    String motionTypeLog = "";
    if ((dataLogBuffer1 - dataLogBuffer2) > dataLogRate){ 
      if (activeMotion == true){
        if (applyingTension == true){
          motionTypeLog = "Applying Tension";
        }
        else{
          motionTypeLog = "Releasing Tension";
        }
      }
      else{
        motionTypeLog = "Holding";
      }
      String dataString = String(dataCounterTotalBuffer) + ", " + String(setWeight) + ", " + String(weight) + ", " + motionTypeLog;
      saveData(dataString); // call function to save to SD card
      dataCounterTotalBuffer++;
      dataCounterLocalBuffer++;


      dataLogBuffer2 = dataLogBuffer1;

      // Open and Format a new file if the old one reaches a certain number of data points. 
      if (dataCounterLocalBuffer > 3600){ // 
        dataFileName = "hgtlog" + String(dataFileNameCounter) + ".csv"; // renames new file
        dataFileNameCounter++;
        
        sensorData = SD.open(dataFileName, FILE_WRITE);

        // if the file opened okay, write to it:
        if (sensorData) {
          Serial.println("Data exeeds current recommended file size. ");
          Serial.print("Creating and Formatting new Data File...");
          sensorData.println("Halo Gravity Traction Data Log. Starting Data Collection.");
          sensorData.println();
          sensorData.println("Data #, SetTension, Tension, MotorStatus");
          // close the file:
          sensorData.close();
          Serial.println("done.");
          Serial.println();
        } else {
          // if the file didn't open, print an error:
          Serial.println("Error opening data file.");
        }
        dataCounterLocalBuffer = 1;
      }
    }
  }// if sd card initialized

///////////////////////////////////////
// Safety Shutoff
//////////////////////////////////////

  // 20LBS OVER THE SET TENSION WILL CUT POWER TO THE MOTOR
  if (weight > (setWeight + 20)){ // && (setWeight > 30.00))|| (weight < 1.50)
    digitalWrite(abovePin, LOW);
    digitalWrite(belowPin, LOW);
    digitalWrite(speedPin, LOW);
    digitalWrite(stopPin, LOW);
    Serial.println("WARNING: System Stop -- excessive weight");

    if (sdCardInitialized == true){
      sensorData = SD.open(dataFileName, FILE_WRITE);
      sensorData.println("SYSTEM STOP ---- EXCESSIVE WEIGHT. Data collection halted until restart.");
      sensorData.close();
    }

    u8g2.clearBuffer();
    char customKey = customKeypad.getKey();
    while (true){ 
      u8g2.setCursor(0,0);
      u8g2.setFont(u8g2_font_lubB10_te);
      u8g2.print("WARNING!!");
      u8g2.setCursor(0, 15);
      u8g2.setFont(u8g2_font_fub30_tf);
      u8g2.print("STOP");
      u8g2.sendBuffer();
      u8g2.clearBuffer();
      char customKey = customKeypad.getKey();
      if (customKey == 'D'){
        u8g2.setCursor(0,0);
        u8g2.setFont(u8g2_font_lubB10_te);
        u8g2.print("Restarting...");
        u8g2.setCursor(0, 15);
        u8g2.setFont(u8g2_font_fub30_tf);
        u8g2.print("STOP");
        u8g2.sendBuffer();
        delay(1000);
        u8g2.clearBuffer();
        digitalWrite(stopPin, HIGH);
        break;
      }
    }
  }




} // main loop


// FUNCTION TO WRITE DATA TO SD CARD
void saveData(String data){
  //  append new data file
  sensorData = SD.open(dataFileName, FILE_WRITE);
  if (sensorData){
    sensorData.println(data);
    sensorData.close(); // close the file
  }
  else{
  Serial.println("Error writing to file!");
  sensorData.close();
  }
}

// TensionBurst Function; applies a tiny burst of tension every 30 seconds if low but still within deadband to keep near setpoint
void tensionBurst(){
  digitalWrite(belowPin, HIGH);
  delay(75);
  digitalWrite(belowPin, LOW);
}
