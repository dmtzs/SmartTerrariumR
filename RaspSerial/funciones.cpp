#include <Arduino.h>
#include <DHT.h>

// Pin´s definitions
#define DHT_PIN 7
#define DHTTYPE DHT22//DHT11
#define PinPrueba 4//Relay test.
#define sensorFlotador 2//Global variables, it can be used to assign a reference to a pin or just a global variable.
DHT dht(DHT_PIN, DHTTYPE);

// Global variables
int bande= 0;//Variable to test to turn the light on with the relay.
String cadeRecibida= "";//To receive the string from the serial port that is connected to the Raspberry.
char inChar;

// Setup function
void setupProyecto()
{
  dht.begin();
  Serial.begin(9600);
  pinMode(sensorFlotador, INPUT_PULLUP);//Pin in pull up mode
  pinMode(PinPrueba, OUTPUT);//Relay test.
  cadeRecibida.reserve(30);//Size reserved for the chain, see if this works or if it can be reduced.
}

// Functions for the functionality of the project.
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

float* TempHum()
{
  //float arreglo[2];
  float* arreglo= new float[2];
  arreglo[0]= dht.readHumidity();
  arreglo[1]= dht.readTemperature();

  return arreglo;
}

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
