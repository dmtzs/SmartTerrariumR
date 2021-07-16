#include "funciones.h"

void setup()
{
  setupProyecto();
}

void loop()
{
  //inicio();//Descomentar cuando esté todo armado y hecho
  
  sensorSumergible();
  TempHum();
  sendSerialRasp();

  // Esperamos 5 segundos entre medidas
  delay(4000);
  
  //Validar que si el sensor de temperatura sumergible baja a cierta temperatura encienda la resistencia por un tiempo para calentar el agua.
  //For the temperature and humidity sensor cause the sensor needs time to measure the data.

}

void serialEvent() {
  eventoSerial();
}
