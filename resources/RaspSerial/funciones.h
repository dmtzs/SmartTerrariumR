/*
 * @Filename: funciones.h
 * @Authors: Guillermo Ortega Romo and Diego Martínez Sánchez
 * @Description: This file is used to declare all functions used on the program
*/

void setupProyecto();
void sendSerialRasp();
void eventoSerial();
void floatingSensor();
void TempHum();
void sensorSumergible();
void humedecerTerrario(float hum);
void reserveWater(float tempSub);
void focosEncendidosAutomatico(float tempDHT);
void rellenarBebedero(String estadoFlotador);
