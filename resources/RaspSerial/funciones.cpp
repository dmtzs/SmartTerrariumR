#include <Arduino.h>
#include <DHT.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include "variables.h"

void chooseAction(String key);
void focosEncendidosManual(int act);

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
float* TH = new float[3];          //Metrics of the sensors to be sent thropugh serial.
float* confValues= new float[3];   //For the values of the vonf flag


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


// ------------------------Setup function------------------------
/*
 * @Authors: Guillermo Ortega Romo and Diego Martínez Sánchez
 * @Description: A function in which are all the setup talking about the actions that the pin´s should do and other initializing-
 * functions from the beggining of the execution of the arduino program.
*/
void setupProyecto()
{
  dht.begin();
  Serial.begin(115200);
  submersibleSensor.begin();
  pinMode(sensorFlotador, INPUT_PULLUP); //Pin in pull up mode
  pinMode(focoDia, OUTPUT);
  pinMode(focoNoche, OUTPUT);
  pinMode(calentarAguaReserva, OUTPUT);
  pinMode(bombaBebedero, OUTPUT);
  pinMode(bombaHumedad, OUTPUT); //Checar si debe ser diferente la config del pin para usar lo de PWM.
  
  for(int i = 0; i < buffersize; i++){
    inString[i] = 0;
    outString[i] = 0;
  }
}

// ------------------------Functions for the functionality of the project------------------------
/*
 * @Author: Diego Martínez Sánchez
 * @Description: For turning on all components everytime the app its initialized all components for check that all components works fine.
*/
void inicio()//Poner en void cuando compruebe en efecto la variable global se mantiene en 1 después.
{
  if (iniciar == 0)
  {
    //Poner que todo se encienda por unos segundos como prueba de que los componentes instalados sirven
    delay(4000);
    iniciar = 1;
  }
}

/*
 * @Author: Guillermo Ortega Romo
 * @Description: Fucntion to detect if something comes from the serial port.
*/
void eventoSerial(){
  count = 0;
  while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read();
    // add it to the inputString:
    inString[count] = inChar;
    // if the incoming character is a newline, set a flag so the main loop can
    // do something about it:
    if(inChar = '\n'){
      stringComplete = true;
    }
    count++;
  }
}

/*
 * @Author: Diego Martínez Sánchez
 * @Description: A function to get the state of the floating water sensor in order to let the arduino know about the drinker if we need to refill-
 * manual or in automatic way in order to manage better the parameters of the terrarium.
*/
void floatingSensor()
{
  /*
  //For floating water sensor
  if(digitalRead(sensorFlotador) == HIGH)
  {
    statusFlotador = 1;
  }
  else
  {
    statusFlotador = 0;
  }*/
  statusFlotador = random(2);
}

/*
 * @Author: Diego Martínez Sánchez
 * @Description: A function to update the variables of the array that will be used to send the data to the raspberry program in to show the-
 * parameters through the raspberry application and to manage the automatic functionality of the terrarium.
*/
void TempHum()
{
  /*
  TH[1]= dht.readTemperature();
  TH[2]= dht.readHumidity();
  */
  TH[1]= random(50);
  TH[2]= random(50);
}

/*
 * @Author: Diego Martínez Sánchez
 * @Description: A function for activate the humidity water bomb in order to humidify the terrarium in the automatic mode.
*/
void humedecerTerrario(float hum)
{
  if (hum < rangoHumedad)
  {
    digitalWrite(bombaHumedad, HIGH);
    //Checar si poner delay o solo esperar que el sensor DHT marque que se elevo la humedad.
    delay(6000);
    digitalWrite(bombaHumedad, LOW);
  }
  else
  {
    digitalWrite(bombaHumedad, LOW);
  }
}

/*
 * @Author: Diego Martínez Sánchez
 * @Description: This function measures the temperature of the water that will be used for refill the drinker and humidify the terrarium.
 *               Also this function will activate a resistor that will keep warm the reserve water of this recipient.
 */
void sensorSumergible()
{
  /*
  submersibleSensor.requestTemperatures();
  TH[0]= submersibleSensor.getTempCByIndex(0);
  TH[0]= 0;*/
  TH[0] = random(50);
}

/*
 * @Author: Diego Martínez Sánchez
 * @Description: Function for keeping warm the water of the reserve water.
 */
void reserveWater(float tempSub)
{
  //Descomentar cuando se reciba el rango de la temperatura a la que se desea mantener la reserva de agua desde la raspberry.
  if (tempSub < rangoTempReservaAgua)
  {
    digitalWrite(calentarAguaReserva, HIGH);
  }
  else
  {
    digitalWrite(calentarAguaReserva, LOW);
  }
}

/*
 * @Author: Diego Martínez Sánchez
 * @Description: Function for turning on the correct bulbs according to the day, if its at night then it will turns on the night bulb and if not the day bulb.
 */
 /*
 void focosEncendidosAutomatico(float tempDHT)
 {
  if (tempDHT < rangoTempDHT)
  {
    if (dia == 1 && noche == 0)
    {
      //Encender el foco de día, falta definir pin
      digitalWrite(focoDia, HIGH);
      digitalWrite(focoNoche, LOW);
    }
    else if (noche == 1 && dia == 0)
    {
      //Encender el foco de noche, falta definir pin
      digitalWrite(focoNoche, HIGH);
      digitalWrite(focoDia, LOW);
    }
    else
    {
      //Mantener apagado ambos focos por si acaso
      digitalWrite(focoDia, LOW);
      digitalWrite(focoNoche, LOW);
    }
  }
  else
  {
    //Mantener apagado ambos focos por si acaso
    digitalWrite(focoDia, LOW);
    digitalWrite(focoNoche, LOW);
  }
 }
 */


 void focosEncendidosManual(int act){
  if (act == 0){
    if(dia_noche == 1)
        onOffDia = (onOffDia == 1) ? 0:1;  
    if(dia_noche == 0)
        onOffNoche = (onOffNoche == 1) ? 0:1;
  }
  if (act == 1){
    if(dia_noche == 1){
      if(onOffNoche == 1){
        onOffDia = 1;
        onOffNoche = 0;
      }
    }
    if(dia_noche == 0){
      if(onOffDia == 1){
        onOffNoche = 1;
        onOffDia = 0;
      }
    }
  }
  
  digitalWrite(focoDia, onOffDia);
  digitalWrite(focoNoche, onOffNoche);
 }

 /*
 * @Author: Diego Martínez Sánchez
 * @Description: Function for refill the drinker of the terrarium only if the floating sensor is in "on" state
 */
 void rellenarBebedero()
 {
  if(statusFlotador == 0){
    digitalWrite(bombaBebedero, value.toInt());
  }
 }

/*
 * @Author: Guillermo Ortega Romo
 * @Description: Fucntion for receive the data from de raspberry and put it in a global variable to manage the rest of the Arduino program.
 */
void sendSerialRasp()
{
  if (stringComplete) {  
    //lee el json recibido por comunicacion serial
    ActionApp = String(inString);
    
    value = ActionApp.substring(4, buffersize);
    ActionApp = ActionApp.substring(0, 4);
    
    chooseAction(ActionApp);

    Serial.println(outString);
    Serial.println();

    stringComplete = false;
  }
  // clear the string:
  for(int i = 0; i < buffersize; i++){
    inString[i] = 0;
    outString[i] = 0;
  }
  delay(100);
}

void chooseAction(String Action2){
  //Modificar
  //Returns stream data to the page on monitor in the flask app
  if(Action2.equals("strm")){
    out = String(TH[0]) + "," + String(TH[1]) +
          "," + String(TH[2]) + "," + String(statusFlotador);
    out.toCharArray(outString, buffersize);
  }

  //Changes the operation mode
  if(Action2.equals("auto")){
    automatico = value.toInt();
  }

  //Turns on or off the bulb according if its day or night
  if(Action2.equals("bulb")){
    focosEncendidosManual(0);
  }

  //Change the day or night mode
  if(Action2.equals("lght")){
    dia_noche = value.toInt();
    focosEncendidosManual(1);
  }

  //Activates or desactivate the refill of the drinker
  if(Action2.equals("bwtr")){
    rellenarBebedero();
  }

  //Activates the water bomb for humidifiying the terrarrium
  if(Action2.equals("hmdf")){
  }

  //Modifies the range values for turning on some components in automatic mode
  if(Action2.equals("conf")){
    String cadeConf;
    int contadorTemp= 0;
    inicioConf= 0;
    finConf= value.indexOf(separador, inicioConf);

    while(finConf!= -1) {
      cadeConf= value.substring(inicioConf, finConf);
      confValues[contadorTemp]= cadeConf.toFloat();
      delay(500);

      inicioConf= finConf+1;
      finConf= value.indexOf(separador, inicioConf);
      contadorTemp+= 1;
    }
    cadeConf= value.substring(inicioConf, value.length());
    confValues[contadorTemp]= cadeConf.toFloat();
    delay(500);
    rangoHumedad= confValues[0];
    rangoTempReservaAgua= confValues[1];
    rangoTempDHT= confValues[2];
  }
}
