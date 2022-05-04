/*
 * @Filename: RaspSerial.ino MainFile
 * @Authors: Guillermo Ortega Romo and Diego Martínez Sánchez
 * @Description: Main file of the project, contains the main loop function
*/

#include "funciones.h"
#include "extern.h"

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
      // reserveWaterManualAuto();//TODO: Checar si si iría aquí el de la resistencia de la reserva de agua manual
    }
  }

  if(automatico == 1){
    humedecerTerrarioAuto();
    focosEncendidosAuto();
    rellenarBebederoAuto();
    focosEncendidosAuto();
  }

  sendSerialRasp();
  
  //Validar que si el sensor de temperatura sumergible baja a cierta temperatura encienda la resistencia por un tiempo para calentar el agua.
}

void serialEvent() {
  eventoSerial();
}