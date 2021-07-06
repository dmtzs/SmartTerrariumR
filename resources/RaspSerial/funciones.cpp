#include <Arduino.h>
#include <DHT.h>
#include <OneWire.h>
#include <DallasTemperature.h>

// ------------------------Pin´s definitions------------------------
#define sensorFlotador 2
#define DHT_PIN 4
#define DHTTYPE DHT22
#define focoDia 5
#define focoNoche 6
#define calentarAguaReserva 7
#define bombaBebedero 8
#define bombaHumedad 9

DHT dht(DHT_PIN, DHTTYPE);
OneWire ourWire(3); //pin 3 for submersible water sensor.

// ------------------------Global variables------------------------
int iniciar= 0, dia= 1, noche= 0; //Para que se ejecute la función iniciar solo una vez.
char inChar;
float rangoHumedad= 0, rangoTempReservaAgua= 0, rangoTempDHT= 0;
String inString = "";         // a String to hold incoming data from raspberry
bool stringComplete = false;  // whether the string is complete
DallasTemperature submersibleSensor(&ourWire);

// ------------------------Setup function------------------------
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
  inString.reserve(200);// reserve 200 bytes for the inputString:
}

// ------------------------Functions for the functionality of the project------------------------
/*
 * @Author: Diego Martínez Sánchez
 * @Description: For turning on all components everytime the app its initialized all components for check if all works fine.
 */
String inicio()//Poner en void cuando compruebe en efecto la variable global se mantiene en 1 después.
{
  if (iniciar== 0)
  {
    //Poner que todo se encienda por unos segundos como prueba de que los componentes instalados sirven
    delay(4000);
    iniciar= 1;

    return "Entre if iniciar";//Quitar return después de prueba.
  }
  else//Quitar todo el bloque else después de prueba.
  {
    return "Entre else iniciar";
  }
}

/*
 * @Author: Guillermo Ortega Romo
 * @Description: Fucntion to detect if something comes from the serial port.
 */
void eventoSerial(){
  while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read();
    // add it to the inputString:
    inString += inChar;
    // if the incoming character is a newline, set a flag so the main loop can
    // do something about it:
    if (inChar == '\n') {
      stringComplete = true;
    }
  }
}

/*
 * @Author: Diego Martínez Sánchez
 * @Description: some description
 */
String floatingSensor()
{
  //For floating water sensor
  if(digitalRead(sensorFlotador)== HIGH)
  {
    return "on";
  }
  else
  {
    return "off";
  }
}

/*
 * @Author: Diego Martínez Sánchez
 * @Description: some description
 */
float* TempHum()
{
  float* params= new float[2];
  params[0]= dht.readTemperature();
  params[1]= dht.readHumidity();

  return params;
}

/*
 * @Author: Diego Martínez Sánchez
 * @Description: A function for activate the humidity water bomb for humidify the terrarium.
 */
void humedecerTerrario(float hum)
{
  //Descomentar cuando se reciba el rango de humedad desde la raspberry.
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
float sensorSumergible()
{
  float tempSub;
  
  submersibleSensor.requestTemperatures();
  tempSub= submersibleSensor.getTempCByIndex(0);

  return tempSub;
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
 void focosEncendidos(float tempDHT)
 {
  if (tempDHT < rangoTempDHT)
  {
    if (dia== 1 && noche== 0)
    {
      //Encender el foco de día, falta definir pin
      digitalWrite(focoDia, HIGH);
      digitalWrite(focoNoche, LOW);
    }
    else if (noche== 1 && dia== 0)
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

 /*
 * @Author: Diego Martínez Sánchez
 * @Description: Function for refill the drinker of the terrarium only if the floating sensor is in "on" state
 */
 void rellenarBebedero(String estadoFlotador)
 {
  if (estadoFlotador== "on")
  {
    digitalWrite(bombaBebedero, HIGH);
    delay(5000);
    digitalWrite(bombaBebedero, LOW);
  }
  else if(bombaBebedero== "off")
  {
    digitalWrite(bombaBebedero, LOW);
  }
 }

/*
 * @Author: Guillermo Ortega Romo
 * @Description: Fucntion for receive the data from de raspberry and put it in a global variable to manage the rest of the Arduino program.
 */
void PruebaRecibidoRasp()
{
  if (stringComplete) {
    Serial.println(inString);
    // clear the string:
    inString = "";
    stringComplete = false;
    //delay(1000);
  }
}
