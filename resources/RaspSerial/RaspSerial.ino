#include "funciones.h"

unsigned long previousMillis = 0;
const long interval = 5000;

void setup()
{
  setupProyecto();
}

void loop()
{
  unsigned long currentMillis = millis();
  
  //inicio();//Descomentar cuando esté todo armado y hecho
  if (currentMillis - previousMillis >= interval){
    previousMillis = currentMillis;
    sensorSumergible();
    TempHum();
  }
  
  sendSerialRasp();
  
  //Validar que si el sensor de temperatura sumergible baja a cierta temperatura encienda la resistencia por un tiempo para calentar el agua.
}

void serialEvent() {
  eventoSerial();
}
