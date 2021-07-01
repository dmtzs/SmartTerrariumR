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
int iniciar= 0; //Para que se ejecute la función iniciar solo una vez.
String cadeRecibida= "";//To receive the string from the serial port that is connected to the Raspberry.
char inChar;
DallasTemperature submersibleSensor(&ourWire);

// ------------------------Setup function------------------------
void setupProyecto()
{
  dht.begin();
  Serial.begin(9600);
  submersibleSensor.begin();
  pinMode(sensorFlotador, INPUT_PULLUP); //Pin in pull up mode
  pinMode(focoDia, OUTPUT);
  pinMode(focoNoche, OUTPUT);
  pinMode(calentarAguaReserva, OUTPUT);
  pinMode(bombaBebedero, OUTPUT);
  pinMode(bombaHumedad, OUTPUT); //Checar si debe ser diferente la config del pin para usar lo de PWM.
  cadeRecibida.reserve(30); //Size reserved for the chain, see if this works or if it can be reduced.
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
  /*if (hum < rangoRasp)
  {
    digitalWrite(bombaHumedad, HIGH);
    //Checar si poner delay o solo esperar que el sensor DHT marque que se elevo la humedad.
    digitalWrite(bombaHumedad, LOW);
  }
  else
  {
    digitalWrite(bombaHumedad, LOW);
  }*/
}

/*
 * @Author: Diego Martínez Sánchez
 * @Description: Fucntion for receive the data from de raspberry and put it in a global variable to manage the rest of the Arduino program.
 */
void PruebaRecibidoRasp(char inString[], char outString[], int bufferSize)
{
  if (inString[0]) 
  {
    //inChar= Serial.read();//Character reading.
    //cadeRecibida+= inChar;//Creation of the received string.

    cadeRecibida = String(inString);
    cadeRecibida.toUpperCase();

    sprintf(outString, "%s", cadeRecibida);

    Serial.write(outString);
    Serial.write(10);

    //Limpiar
    for (int i = 0; i < bufferSize; i++) {
      inString[i] = 0;
      outString[i] = 0;
    }

    //Serial.println("Cadena que se formo: ");
    //Serial.println(cadeRecibida);
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
 * @Description: some description
 */
void reserveWater(float tempSub)
{
  //Descomentar cuando se reciba el rango de la temperatura a la que se desea mantener la reserva de agua desde la raspberry.
  /*if (tempSub < rangoTempReservaAgua)
  {
    digitalWrite(calentarAguaReserva, HIGH);
  }
  else
  {
    digitalWrite(calentarAguaReserva, LOW);
  }*/
}
