#include "funciones.h"

void setup()
{
  setupProyecto();
}

void loop()
{
  String cade= "", estadoFlotador= "";
  float *TH;

  estadoFlotador= floatingSensor();//Function for floating sensor and all what this sensor will manage.
  TH= TempHum();

  //The order of the data is: temp, hum
  cade+= TH[0];
  cade+= ",";
  cade+= TH[1];
  cade+= ",";
  cade+= estadoFlotador;
  Serial.println(cade);

  PruebaRelay();//Prueba del relay

  //Validar que si la temperatura baja a cierto punto que encienda un foco y dependiendo del día o de noche.

  //Validar que si la humedad baja a cierto punto rocie con la bomba que tengo para rociar.

  //Validar que si el sensor de temperatura sumergible baja a cierta temperatura encienda la resistencia por un tiempo para calentar el agua.

  PruebaRecibidoRasp();//Función temporal para imprimir lo que recibo de la raspberry

  delay(4000);//For the temperature and humidity sensor cause the sensor needs time to measure the data.
}
