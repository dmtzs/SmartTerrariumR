#include "funciones.h"

void setup()
{
  setupProyecto();
}

void loop()
{
  int automatico= 0; //0 manual y 1 automático.
  //inicio();//Descomentar cuando esté todo armado y hecho

  if (automatico== 0)
  {
    sensorSumergible();
    TempHum();
    sendSerialRasp();
  }
  else if (automatico== 1)
  {
    sensorSumergible();
    TempHum();
    sendSerialRasp();
    //Poner aquí las otras funciones que deben mandar los otros datos y recibir
  }
  else
  {
    continue; //Creo que es como un pass en python
  }
  // Esperamos 5 segundos entre medidas
  delay(4000);
  
  //Validar que si el sensor de temperatura sumergible baja a cierta temperatura encienda la resistencia por un tiempo para calentar el agua.
  //For the temperature and humidity sensor cause the sensor needs time to measure the data.

}

void serialEvent() {
  eventoSerial();
}
