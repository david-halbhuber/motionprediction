#include <Time.h>
#include <TimeLib.h>
unsigned long time;

#define SHOCK_PIN 2

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);       // on-board LED, usually pin 13
  pinMode(SHOCK_PIN, INPUT);

  Serial.begin(9600); // shock sensor pin set to input
}

void loop() {
  if (digitalRead(SHOCK_PIN)) {       // shock detected?
    // shock not detected with pull-up resistor
    digitalWrite(LED_BUILTIN, LOW);   // switch LED off
  }
  else {
    // shock detected with pull-up resistor
    Serial.println(millis());

    digitalWrite(LED_BUILTIN, HIGH);  // switch LED on



    // leave LED on for period
  }
}
