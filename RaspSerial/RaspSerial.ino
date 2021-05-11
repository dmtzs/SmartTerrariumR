#include <DHT.h>

#define DHT_PIN 7
#define DHTTYPE DHT22//DHT11
const int pinBuzzer= 9;//Constant of the buzzer.
int BandBoton= 0;//Global variables, it can be used for soing a reference to a pin or just a global variable.
int adc_id= 0;

DHT dht(DHT_PIN, DHTTYPE);
String cadeRecibida= "";//Para recibir la cadena desde el puerto serial.
char inChar;

void setup()
{
  dht.begin();
  Serial.begin(9600);
  pinMode(pinBuzzer, OUTPUT);
  pinMode(8, INPUT);
  cadeRecibida.reserve(30);//Tamaño reservado para la cadena, ver si así funciona o si se puede reducir.
}

void loop()
{
  float h= dht.readHumidity();
  float t= dht.readTemperature();
  int valor= analogRead(adc_id);
  int EstadoBoton= digitalRead(8);
  String cade= "";

  //El orden de los datos es: temp, hum, nivel agua y edo boton
  cade+= t;
  cade+= ",";
  cade+= h;
  cade+= ",";
  cade+= valor;
  cade+= ",";
  cade+= BandBoton;

  Serial.println(cade);

  if (Serial.available())
  {
    inChar= Serial.read();//Lectura de caracteres.
    cadeRecibida+= inChar;//Creación de la cadena recibida.

    Serial.println("Cadena que se formo: ");
    Serial.println(cadeRecibida);
  }

  //For buzzer
  if(EstadoBoton==HIGH)
  {
    BandBoton= 1;
  }

  if(valor<120 && BandBoton==0)
  {
    digitalWrite(pinBuzzer, HIGH);//Se enciende buzzer
  }
  else if(valor<120 && BandBoton==1)
  {
    digitalWrite(pinBuzzer, LOW);//Se apaga el buzzer
  }
  else if(valor>120)
  {
    BandBoton=0;
    digitalWrite(pinBuzzer, LOW);//Se apaga el buzzer
  }
  delay(3000);//Para el sensor de temperatura y humedad, pero de igual manera afecta al de agua.
}
