#include <DHT.h>
#include <SoftwareSerial.h>

SoftwareSerial bt(3, 2);//Rx | Tx del modulo de bluetooth.

#define DHT_PIN 7
#define DHTTYPE DHT22
const int pinBuzzer= 9;//Constant of the buzzer.
int BandBoton= 0;//Global variables, it can be used for soing a reference to a pin or just a global variable.
int adc_id= 0;

DHT dht(DHT_PIN, DHTTYPE);


void setup()
{
  dht.begin();
  Serial.begin(9600);
  bt.begin(9600);
  pinMode(pinBuzzer, OUTPUT);
  pinMode(8, INPUT);
}

void loop()
{
  float h= dht.readHumidity();
  float t= dht.readTemperature();
  int valor= analogRead(adc_id);
  int EstadoBoton= digitalRead(8);
  String cade= "";

  cade+= t;
  cade+= ",";
  cade+= h;
  cade+= ",";
  cade+= valor;

  Serial.print(cade);

  //Bluetooth read from serial monitor to bt.
  /*if (Serial.available())
  {
    bt.write(Serial.read());
  }*/

  //For buzzer
  if(EstadoBoton==HIGH)
  {
    BandBoton= 1;
  }

  if(valor<200 && BandBoton==0)
  {
    digitalWrite(pinBuzzer, HIGH);//Se enciende buzzer
  }
  else if(valor<200 && BandBoton==1)
  {
    digitalWrite(pinBuzzer, LOW);//Se apaga el buzzer
  }
  else if(valor>200)
  {
    BandBoton=0;
    digitalWrite(pinBuzzer, LOW);//Se apaga el buzzer
  }
  delay(3000);//Para el sensor de temperatura y humedad, pero de igual manera afecta al de agua.
}
