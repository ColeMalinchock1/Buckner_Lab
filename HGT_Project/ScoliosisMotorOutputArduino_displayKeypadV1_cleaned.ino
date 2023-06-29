#include <Arduino.h>
#include <U8g2lib.h>

#include <Keypad.h>

#ifdef U8X8_HAVE_HW_SPI
#include <SPI.h>
#endif
#ifdef U8X8_HAVE_HW_I2C
#include <Wire.h>
#endif

#include <stdio.h>
#include <stdlib.h>


const byte ROWS = 4; //four rows
const byte COLS = 4; //four columns
//define the cymbols on the buttons of the keypads
char hexaKeys[ROWS][COLS] = {
  {'1','2','3','A'},
  {'4','5','6','B'},
  {'7','8','9','C'},
  {'*','0','#','D'}
};
byte rowPins[ROWS] = {30, 32, 34, 36}; //connect to the row pinouts of the keypad
byte colPins[COLS] = {31, 33, 35, 37}; //connect to the column pinouts of the keypad

//initialize an instance of class NewKeypad
Keypad customKeypad = Keypad(makeKeymap(hexaKeys), rowPins, colPins, ROWS, COLS); 


const int inputPin = A0;
const int abovePin = 22;
const int belowPin = 24;
double setVoltage = 1.65;

U8G2_SSD1306_128X64_NONAME_F_HW_I2C u8g2(U8G2_R0, /* reset=*/ U8X8_PIN_NONE);



void setup() {

  pinMode(abovePin, OUTPUT);
  pinMode(belowPin, OUTPUT);
  digitalWrite(abovePin, LOW);
  digitalWrite(belowPin, LOW);
  Serial.begin(9600);

  double setVoltage = 1.65;

  u8g2.begin();
  
  u8g2.setFontRefHeightExtendedText();
  u8g2.setDrawColor(1);
  u8g2.setFontPosTop();
  u8g2.setFontDirection(0);

}

///////////////////////////////////////////////

void loop() {

//GET ANALOG INPUT
  int sensorValue = analogRead(inputPin);
  float voltage = sensorValue * (5.0 / 1023.0); // Convert ADC value to voltage

  u8g2.clearBuffer();

//PIN OUTPUT:
  if (voltage < (setVoltage - 0.02)) { // loostens cable if voltage is too high
    digitalWrite(abovePin, HIGH);
    digitalWrite(belowPin, LOW);
  } else if (voltage > (setVoltage + 0.02)) { // tightens cable is voltage is too low
    digitalWrite(abovePin, LOW);
    digitalWrite(belowPin, HIGH);
  } else { // does nothing if voltage = setVoltage (+-0.02)
    digitalWrite(abovePin, LOW);
    digitalWrite(belowPin, LOW);
  }



// SCREEN UPDATING
  int counter = 0;
  char customKey = customKeypad.getKey();

  if (customKey){
    while (counter < 20){ // counter used as a kind of timer for the set volt screen
      // drawing the setvolt screen
      u8g2.setCursor(0,0);
      u8g2.setFont(u8g2_font_lubB10_te);
      u8g2.print("set volt:");
      u8g2.setCursor(0, 15);
      u8g2.setFont(u8g2_font_fub30_tf);
      u8g2.print(setVoltage);
      u8g2.print("V");

      u8g2.sendBuffer();
      u8g2.clearBuffer();
      counter++; // adding to timer

      //EDITING SETVOLTAGE WITH NUMBERPAD
      if (customKey == '#'){
        double digitPlace = 1; // which place digit you are editing; when user types, this goes up by one (first editing 1s place, then the tenths place, then hundredths place)
        double newSetVoltage = 0;
        double newKeypadDouble = 0;
        while (digitPlace < 4){
          char customKey = customKeypad.getKey();
          if (customKey){
            if (customKey == '1'){newKeypadDouble = 1;}
            if (customKey == '2'){newKeypadDouble = 2;}
            if (customKey == '3'){newKeypadDouble = 3;}
            if (customKey == '4'){newKeypadDouble = 4;}
            if (customKey == '5'){newKeypadDouble = 5;}
            if (customKey == '6'){newKeypadDouble = 6;}
            if (customKey == '7'){newKeypadDouble = 7;}
            if (customKey == '8'){newKeypadDouble = 8;}
            if (customKey == '9'){newKeypadDouble = 9;}
            if (customKey == '0'){newKeypadDouble = 0;}
            newSetVoltage = (newSetVoltage + (newKeypadDouble/(0.1*(pow(10, digitPlace)))));
            digitPlace++;
          }
          u8g2.setCursor(0,0);
          u8g2.setFont(u8g2_font_lubB10_te);
          u8g2.print("set volt:");
          u8g2.setCursor(0, 15);
          u8g2.setFont(u8g2_font_fub30_tf);
          u8g2.print(newSetVoltage);
          u8g2.print("V");

          u8g2.sendBuffer();
          u8g2.clearBuffer();
        }

        setVoltage = newSetVoltage;
        counter = 20;
        u8g2.setCursor(0,0);
        u8g2.setFont(u8g2_font_lubB10_te);
        u8g2.print("Voltage Set.");
        u8g2.setCursor(0, 15);
        u8g2.setFont(u8g2_font_fub30_tf);
        u8g2.print(newSetVoltage);
        u8g2.print("V");

        u8g2.sendBuffer();
        u8g2.clearBuffer();
        
        delay(1000);
      }

      //EDITING SETVOLTAGE WITH A AND B
      char customKey = customKeypad.getKey();
      if (customKey){
        if (customKey == 'A'){
          setVoltage = (setVoltage + 0.05);
          counter = 0;
        }
        if (customKey == 'B'){
          setVoltage = (setVoltage - 0.05);
          counter = 0;
        }
      }
    }
  }

  else{
    u8g2.setCursor(0,0);
    u8g2.setFont(u8g2_font_lubB10_te);
    u8g2.print("load volt:");
    u8g2.setCursor(0,15);
    u8g2.setFont(u8g2_font_fub30_tf);
    u8g2.print(voltage);
    u8g2.print("V");
  }


  u8g2.sendBuffer(); 

  delay(50);

}

