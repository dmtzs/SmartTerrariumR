/*
 * @Filename: global.h
 * @Authors: Guillermo Ortega Romo and Diego Martínez Sánchez
 * @Description: This file contains all the global variables 
 *              definitions used in funciones.cpp
*/

#include <Arduino.h>
#include <DHT.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include "extern.h"

// ------------------------Prototype functions------------------------
void chooseAction();
void focosEncendidosManual(int act);
void humedecerTerrarioManual();
void rellenarBebederoManual();

// ------------------------Pin´s  definitions------------------------
#define sensorFlotador 2
#define DHT_PIN 4
#define DHTTYPE DHT22
#define focoDia 5
#define focoNoche 6
#define calentarAguaReserva 7
#define bombaBebedero 8
#define bombaHumedad 9

// ------------------------Objects definitions------------------------
DHT dht(DHT_PIN, DHTTYPE);
OneWire ourWire(3); //pin 3 for submersible water sensor.

// ------------------------Global variables------------------------
#define separador ','              //Separator for conf flag.
DallasTemperature submersibleSensor(&ourWire);
int iniciar = 0;                   //Just for execute a function once
int dia_noche = 0;                 //To know which bulb needs to turn on or off. day = 1, night = 0
int onOffDia = 0, onOffNoche = 0;  //State of the bulbs, day and nigth.
int automatico = 0;                //0 manual y 1 automatic.
int statusFlotador = 0;            //State of the drinker. 1 = lleno, 0 = no lleno
int inicioConf, finConf;                   //For comma separated values.
float rangoHumedad = 0, rangoTempReservaAgua = 0, rangoTempDHT = 0;
float* TH = new float[3];          //Metrics of the sensors to be sent through serial.
float* confValues= new float[3];   //For the values of the vonf flag
int bebederoSignal = 0;            //Keep the status of the motor for the drinker
int humedecerSignal = 0;           //Keep the status of the motor for the sprays


//----------------Variables for serial communication---------------
char inChar;
const int buffersize = 64;
char inString[buffersize];          // a String to hold incoming data from raspberry
char outString[buffersize];         // a String to hold data to send to raspberry
bool stringComplete = false;        // whether the string is complete
int count = 0;
String out = "";
String value;
String ActionApp = "nnnn";
