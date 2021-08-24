/*
 * @Filename: funciones.h
 * @Authors: Guillermo Ortega Romo and Diego Martínez Sánchez
 * @Description: This file is used to declare all functions used on the program
*/

void setupProyecto();
void sendSerialRasp();
void eventoSerial();

//Automatic functions
void humedecerTerrarioAuto();
void reserveWaterAuto();
void focosEncendidosAuto();
void rellenarBebederoAuto();
void focosEncendidosAuto();

//Functions for the sensors of humidity and temperatures.
void floatingSensor();
void sensorSumergible();
void TempHum();
