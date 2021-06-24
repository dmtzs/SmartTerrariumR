#include <DHT.h>

#define DHT_PIN 7
#define DHTTYPE DHT22//DHT11
int sensorFlotador= 2;//Global variables, it can be used to assign a reference to a pin or just a global variable.

DHT dht(DHT_PIN, DHTTYPE);
String cadeRecibida= "";//To receive the string from the serial port that is connected to the Raspberry.
char inChar;

void setup()
{
  dht.begin();
  Serial.begin(9600);
  pinMode(sensorFlotador, INPUT_PULLUP);//Pin in pull up mode
  cadeRecibida.reserve(30);//Size reserved for the chain, see if this works or if it can be reduced.
}

void loop()
{
  float h= dht.readHumidity();
  float t= dht.readTemperature();
  String cade= "", estadoFlotador= "";

  //For floating water sensor
  if(digitalRead(sensorFlotador)== HIGH)
  {
    estadoFlotador= "off";
  }
  else
  {
    estadoFlotador= "on";
    //Aquí poner lo de rellenar el bebedero
  }

  //The order of the data is: temp, hum
  cade+= t;
  cade+= ",";
  cade+= h;
  cade+= ",";
  cade+= estadoFlotador;

  Serial.println(cade);

  if (Serial.available())
  {
    inChar= Serial.read();//Character reading.
    cadeRecibida+= inChar;//Creation of the received string.

    Serial.println("Cadena que se formo: ");
    Serial.println(cadeRecibida);
  }

  delay(4000);//For the temperature and humidity sensor cause the sensor needs time to measure the data.
}
