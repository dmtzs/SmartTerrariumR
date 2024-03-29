/*
 * @Filename: funciones.cpp
 * @Authors: Guillermo Ortega Romo and Diego Martínez Sánchez
 * @Description: This file contains all functions used on the project
*/

#include "global.h"

// ------------------------------------------------------------------------------ //
// ---------------------------------Setup function------------------------------- //
// ------------------------------------------------------------------------------ //
/*
 * @Authors: Guillermo Ortega Romo and Diego Martínez Sánchez
 * @Description: A function in which are all the setup talking about the actions that the pin´s should do and other initializing-
 * functions from the beggining of the execution of the arduino program.
*/
void setupProyecto()
{
  pinMode(LED_BUILTIN, OUTPUT);// Quitar después de comprobar bandera de conf.
  dht.begin();
  Serial.begin(115200);
  submersibleSensor.begin();
  pinMode(sensorFlotador, INPUT_PULLUP); //Pin in pull up mode
  pinMode(focoDia, OUTPUT);
  pinMode(focoNoche, OUTPUT);
  pinMode(calentarAguaReserva, OUTPUT);
  pinMode(bombaBebedero, OUTPUT);
  pinMode(bombaHumedad, OUTPUT);

  digitalWrite(focoDia, HIGH);
  digitalWrite(focoNoche, HIGH);
  digitalWrite(bombaHumedad, HIGH);
  digitalWrite(calentarAguaReserva, HIGH);
  
  for(int i = 0; i < buffersize; i++){
    inString[i] = 0;
    outString[i] = 0;
  }
}

// ------------------------------------------------------------------------------ //
// ----------------------Functions for sensor readings--------------------------- //
// ------------------------------------------------------------------------------ //
/*
 * @Author: Diego Martínez Sánchez
 * @Description: This function measures the temperature of the water that will be used for refill the drinker and humidify the terrarium.
 *               Also this function will activate a resistor that will keep warm the reserve water of this recipient.
 */
void sensorSumergible()
{
  submersibleSensor.requestTemperatures();
  TH[0]= submersibleSensor.getTempCByIndex(0);
  //TH[0] = random(50);
}

/*
 * @Author: Diego Martínez Sánchez
 * @Description: A function to get the state of the floating water sensor in order to let the arduino know about the drinker if we need to refill-
 * manual or in automatic way in order to manage better the parameters of the terrarium.
*/
void floatingSensor()
{
  //For floating water sensor
  if(digitalRead(sensorFlotador) == HIGH)
  {
    statusFlotador = 1;
  }
  else
  {
    statusFlotador = 0;
  }
  //statusFlotador = random(2);
}

/*
 * @Author: Diego Martínez Sánchez
 * @Description: A function to update the variables of the array that will be used to send the data to the raspberry program in to show the-
 * parameters through the raspberry application and to manage the automatic functionality of the terrarium.
*/
void TempHum()
{
  TH[1]= dht.readTemperature();
  TH[2]= dht.readHumidity();
  
  // TH[1]= random(29);
  // TH[2]= random(29);
}
// ------------------------------------------------------------------------------ //
// ------------------------------------------------------------------------------ //



// ------------------------------------------------------------------------------ //
// ------------Functions for complete functionality of the project--------------- //
// ------------------------------------------------------------------------------ //
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

// ------------------------------------------------------------------------------ //
// ---------------------Functions for serial communication-------- -------------- //
// ------------------------------------------------------------------------------ //
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
    
    chooseAction();

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

void chooseAction(){
  //Modificar
  //Returns stream data to the page on monitor in the flask app
  if(ActionApp.equals("strm")){
    out = String(TH[0]) + "," + String(TH[1]) +
          "," + String(TH[2]) + "," + String(statusFlotador);
    out.toCharArray(outString, buffersize);
  }

  //Changes the operation mode
  if(ActionApp.equals("auto")){
    automatico = value.toInt();
  }

  //Turns on or off the bulb according if its day or night
  if(ActionApp.equals("bulb")){
    focosEncendidosManualAuto(0);
  }

  //Change the day or night mode
  if(ActionApp.equals("lght")){
    dia_noche = value.toInt();
    focosEncendidosManualAuto(1);
  }

  //Activates or desactivate the refill of the drinker
  if(ActionApp.equals("bwtr")){
    rellenarBebederoManual();
  }

  //Activates the water bomb for humidifiying the terrarrium
  if(ActionApp.equals("hmdf")){
    humedecerTerrarioManual();
  }

  //Modifies the range values for turning on some components in automatic mode
  if(ActionApp.equals("conf")){
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
    rangoTempReservaAgua= confValues[0];
    rangoTempDHT= confValues[1];
    rangoHumedad= confValues[2];
    //Agregar cambiar la variable apra 
  }
}
// ------------------------------------------------------------------------------ //
// ------------------------------------------------------------------------------ //


// ------------------------------------------------------------------------------ //
// --------------------------Functions manual operation-------------------------- //
// ------------------------------------------------------------------------------ //
/*
 * @Author: Diego Martínez Sánchez
 * @Description: Function for refill the drinker of the terrarium only if the floating sensor is in "on" state
 */
void rellenarBebederoManual()
{
  if (bebederoSignal == 0) {
    bebederoSignal = 1;
    digitalWrite(bombaBebedero, HIGH);
  }else{
    bebederoSignal = 0;
    digitalWrite(bombaBebedero, LOW);
  }
}

/*
 * @Author: Guillermo Ortega Romo
 * @Description: This function is used to manage the status of the   
 *               day and night lightbulbs
*/
void focosEncendidosManualAuto(int act){
  if (act == 0){
    if(dia_noche == 1)
        onOffDia = value.toInt();
    if(dia_noche == 0)
        onOffNoche = value.toInt();
  }
  if (act == 1) {
    //dia
    if (dia_noche == 1) {
      if (onOffNoche == 1) {
        onOffDia = HIGH;
        onOffNoche = LOW;
      }
    }
    //noche
    if (dia_noche == 0) {
      if(onOffDia == 1){
        onOffNoche = HIGH;//original: 1
        onOffDia = LOW;//original 0
      }
    }
  }
  digitalWrite(focoDia, !onOffDia);
  digitalWrite(focoNoche, !onOffNoche);
}

/*
 * @Author: Diego Martínez Sánchez
 * @Description: A function for activate the humidity water bomb in order to humidify the terrarium in the automatic mode.
*/
void humedecerTerrarioManual()
{
  if (humedecerSignal == 0) {
    humedecerSignal = 1;
    digitalWrite(bombaHumedad, LOW);
  }else{
    humedecerSignal = 0;
    digitalWrite(bombaHumedad, HIGH);
  }
}

// ------------------------------------------------------------------------------ //
// ------------------------------------------------------------------------------ //


// ------------------------------------------------------------------------------ //
// ------------------------Functions automatic operation------------------------- //
// ------------------------------------------------------------------------------ //
/*
 * @Author: Diego Martínez Sánchez
 * @Description: A function for activate the humidity water bomb in order to humidify the terrarium in the automatic mode.
*/
void humedecerTerrarioAuto()
{
  if (TH[2] < rangoHumedad) {
    if (humedecerSignal == 0) {
      humedecerSignal = 1;
      digitalWrite(bombaHumedad, LOW);
    }
    else {
      humedecerSignal = 0;
      digitalWrite(bombaHumedad, HIGH);
    }
  }
  else{
    digitalWrite(bombaHumedad, HIGH);
  }
}

/*
 * @Author: Diego Martínez Sánchez
 * @Description: Function for keeping warm the water of the reserve water in the automatic mode.
 */
void reserveWaterManualAuto()
{
  if (TH[0] < rangoTempReservaAgua)
  {
    digitalWrite(calentarAguaReserva, LOW);
  }
  else
  {
    digitalWrite(calentarAguaReserva, HIGH);
  }
}

 /*
 * @Author: Diego Martínez Sánchez
 * @Description: Function for refill the drinker of the terrarium only if the floating sensor is in "on" state
 */
 void rellenarBebederoAuto()
 {
  if(statusFlotador == 0){
    digitalWrite(bombaBebedero, !statusFlotador);
  }
  else {
    digitalWrite(bombaBebedero, !statusFlotador);
  }
 }
 
// ------------------------------------------------------------------------------ //
// ------------------------------------------------------------------------------ //