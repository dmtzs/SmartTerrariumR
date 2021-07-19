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
  // Esperamos 4 segundos entre medidas
  delay(4000);
}

void serialEvent() {
  eventoSerial();
}
