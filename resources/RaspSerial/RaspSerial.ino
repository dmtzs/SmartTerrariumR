#include "funciones.h"

unsigned long previousMillis = 0;
const long interval = 1000;
const long secondInterval = 5000;

void setup()
{
  setupProyecto();
}

void loop()
{
  unsigned long currentMillis = millis();
  
  //inicio();//Descomentar cuando esté todo armado y hecho
  if (currentMillis - previousMillis >= interval){
    floatingSensor();
    if (currentMillis - previousMillis >= secondInterval){
      previousMillis = currentMillis;
      sensorSumergible();
      TempHum();
      Serial.println("AA");
    }
  }
  
  sendSerialRasp();
  
  //Validar que si el sensor de temperatura sumergible baja a cierta temperatura encienda la resistencia por un tiempo para calentar el agua.
}

void serialEvent() {
  eventoSerial();
}
