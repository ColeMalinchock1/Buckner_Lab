const int inputPin = A0;
const int abovePin = 22;
const int belowPin = 24;
const double setVoltage = 1.64;

void setup() {
  pinMode(abovePin, OUTPUT);
  pinMode(belowPin, OUTPUT);
  digitalWrite(abovePin, LOW);
  digitalWrite(belowPin, LOW);
  Serial.begin(9600);
  Serial.print("Set Voltage: ");
  Serial.println(setVoltage);
}

void loop() {
  int sensorValue = analogRead(inputPin);
  float voltage = sensorValue * (5.0 / 1023.0); // Convert ADC value to voltage

  if (voltage > (setVoltage + 0.02)) { // loostens cable if voltage is too high
    digitalWrite(abovePin, HIGH);
    digitalWrite(belowPin, LOW);
  } else if (voltage < (setVoltage - 0.02)) { // tightens cable is voltage is too low
    digitalWrite(abovePin, LOW);
    digitalWrite(belowPin, HIGH);
  } else { // does nothing if voltage = setVoltage (+-0.02)
    digitalWrite(abovePin, LOW);
    digitalWrite(belowPin, LOW);
  }

  Serial.print("AnalogRead: ");
  Serial.println(sensorValue);
  Serial.print("Voltage: ");
  Serial.print(voltage);
  Serial.println("V");
  delay(200); 
}

