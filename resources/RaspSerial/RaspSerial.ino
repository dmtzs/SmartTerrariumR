#include "funciones.h"

unsigned long previousMillis = 0;
const long interval = 1000;
int secondInterval = 0;

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
    previousMillis = currentMillis;
    secondInterval++;
    if (secondInterval == 5){
      secondInterval = 0;
      sensorSumergible();
      TempHum();
    }
  }
  
  sendSerialRasp();
  
  //Validar que si el sensor de temperatura sumergible baja a cierta temperatura encienda la resistencia por un tiempo para calentar el agua.
}

void serialEvent() {
  eventoSerial();
}
