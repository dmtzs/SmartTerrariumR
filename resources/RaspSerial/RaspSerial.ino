#include "funciones.h"

void setup()
{
  setupProyecto();
}

void loop()
{
  /*
  String cade= "", estadoFlotador= "", temporal= "";
  float *TH, tempSumergible;

  //temporal= inicio();//Regresar a void la función después de probar.
  estadoFlotador= floatingSensor();
  //rellenarBebedero(estadoFlotador);//Función para rellenar el bebedero
  TH= TempHum();
  tempSumergible= sensorSumergible();
  //humedecerTerrario(TH[1]); //Hace falta recibir el rango desde la rasp.
  //reserveWater(tempSumergible);//For keep warm the reserve water. Hace falta recibir el rango desde la rasp
  //void focosEncendidos(TH[0]);//Hace falta recibir el rango y estado del día desde la rasp, para saber qué foco encender

  //The order of the data is: temp, hum
  cade+= TH[0];
  cade+= ",";
  cade+= TH[1];
  cade+= ",";
  cade+= estadoFlotador;
  cade+= ",";
  cade+= tempSumergible;
  Serial.println(cade);
*/
  TempHum();
  sendSerialRasp();

  // Esperamos 5 segundos entre medidas
  delay(2500);
  
  //Validar que si el sensor de temperatura sumergible baja a cierta temperatura encienda la resistencia por un tiempo para calentar el agua.
  //For the temperature and humidity sensor cause the sensor needs time to measure the data.

}

void serialEvent() {
  eventoSerial();
}
