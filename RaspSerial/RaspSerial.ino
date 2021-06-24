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

  estadoFlotador= floatingSensor();//Function for floating sensor and all what this sensor will manage.

  //The order of the data is: temp, hum
  cade+= t;
  cade+= ",";
  cade+= h;
  cade+= ",";
  cade+= estadoFlotador;
  Serial.println(cade);

  //Validar que si la temperatura baja a cierto punto que encienda un foco y dependiendo del día o de noche.

  //Validar que si la humedad baja a cierto punto rocie con la bomba que tengo para rociar.

  //Validar que si el sensor de temperatura sumergible baja a cierta temperatura encienda la resistencia por un tiempo para calentar el agua.

  PruebaRecibidoRasp();//Función temporal para imprimir lo que recibo de la raspberry

  delay(4000);//For the temperature and humidity sensor cause the sensor needs time to measure the data.
}

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
