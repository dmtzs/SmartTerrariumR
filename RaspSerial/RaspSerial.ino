#include "funciones.h"

void setup()
{
  setupProyecto();
}

void loop()
{
  String cade= "", estadoFlotador= "", temporal= "";
  float *TH, tempSumergible;

  //temporal= inicio();//Regresar a void la función después de probar.
  estadoFlotador= floatingSensor();
  TH= TempHum();
  tempSumergible= sensorSumergible();
  //humedecerTerrario(TH[0]); //Hace falta recibir el rango desde la rasp.
  //reserveWater(tempSumergible);//For keep warm the reserve water. Hace falta recibir el rango desde la rasp

  //The order of the data is: temp, hum
  cade+= TH[0];
  cade+= ",";
  cade+= TH[1];
  cade+= ",";
  cade+= estadoFlotador;
  cade+= ",";
  cade+= tempSumergible;
  //Serial.println(cade);
  //Serial.println(temporal);//Quitar después de prueba
  //Serial.println("hola pinche putita");
  //Validar que si la temperatura baja a cierto punto que encienda un foco y dependiendo del día o de noche.

  PruebaRecibidoRasp();
  
  //Validar que si el sensor de temperatura sumergible baja a cierta temperatura encienda la resistencia por un tiempo para calentar el agua.
  //For the temperature and humidity sensor cause the sensor needs time to measure the data.
}

void serialEvent() {
  eventoSerial();
}
