#include <Arduino.h>
#include <DHT.h>
#include <OneWire.h>
#include <DallasTemperature.h>

// ------------------------Pin´s definitions------------------------
#define DHT_PIN 7
#define DHTTYPE DHT22//DHT11
#define PinPrueba 4//Relay test.
#define sensorFlotador 2//Global variables, it can be used to assign a reference to a pin or just a global variable.
DHT dht(DHT_PIN, DHTTYPE);
OneWire ourWire(8);//pin for submersible temperature sensor.

// Global variables
int bande= 0;//Variable to test to turn the light on with the relay.
String cadeRecibida= "";//To receive the string from the serial port that is connected to the Raspberry.
char inChar;
DallasTemperature submersibleSensor(&ourWire);

// ------------------------Setup function------------------------
void setupProyecto()
{
  dht.begin();
  Serial.begin(9600);
  pinMode(sensorFlotador, INPUT_PULLUP);//Pin in pull up mode
  pinMode(PinPrueba, OUTPUT);//Relay test.
  cadeRecibida.reserve(30);//Size reserved for the chain, see if this works or if it can be reduced.
  submersibleSensor.begin();
}

// ------------------------Functions for the functionality of the project------------------------
/*
 * @Author: Diego Martínez Sánchez
 * @Description: some description
 */
String floatingSensor()
{
  //For floating water sensor
  if(digitalRead(sensorFlotador)== HIGH)
  {
    //Here the functionality to refill the drinker
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
  //float arreglo[2];
  float* arreglo= new float[2];
  arreglo[0]= dht.readHumidity();
  arreglo[1]= dht.readTemperature();

  return arreglo;
}

/*
 * @Author: Diego Martínez Sánchez
 * @Description: some description
 */
void PruebaRecibidoRasp()
{
  if (Serial.available())
  {
    inChar= Serial.read();//Character reading.
    cadeRecibida+= inChar;//Creation of the received string.

    Serial.println("Cadena que se formo: ");
    Serial.println(cadeRecibida);
  }
}

/*
 * @Author: Diego Martínez Sánchez
 * @Description: some description
 */
void PruebaRelay()
{
  if (bande== 1)
  {
    bande= 0;
    digitalWrite(PinPrueba, LOW);
    //delay(3000);
  }
  else
  {
    bande= 1;
    digitalWrite(PinPrueba, HIGH);
    //delay(3000);
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
