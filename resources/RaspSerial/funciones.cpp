#include <Arduino.h>
#include <DHT.h>
#include <OneWire.h>
#include <DallasTemperature.h>


void chooseAction(String key);

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
DallasTemperature submersibleSensor(&ourWire);
int iniciar= 0, dia= 1, noche= 0, automatico= 0; //Iniciar para que se ejecute la función iniciar solo una vez. 0 manual y 1 automático.
float rangoHumedad= 0, rangoTempReservaAgua= 0, rangoTempDHT= 0;
float* TH = new float[3]; //lecturas de sensor para mandar por serial


//----------------Variables para comunicacion serial---------------
char inChar;
const int buffersize = 64;
char inString[buffersize];         // a String to hold incoming data from raspberry
char outString[buffersize];         // a String to hold incoming data from raspberry
bool stringComplete = false;  // whether the string is complete
int count = 0;
String out = "";
String value;
String Action = "nnnn";


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
  for(int i = 0; i < buffersize; i++){
    inString[i] = 0;
    outString[i] = 0;
  }
  delay(2000);
}

// ------------------------Functions for the functionality of the project------------------------
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
  if(estadoFlotador.equals("on"))
  {
    digitalWrite(bombaBebedero, HIGH);
    delay(5000);
    digitalWrite(bombaBebedero, LOW);
  }
  else if(estadoFlotador.equals("off"))
  {
    digitalWrite(bombaBebedero, LOW);
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
    Action = String(inString);
    
    value = Action.substring(4, buffersize);
    Action = Action.substring(0, 4);
    
    chooseAction(Action);

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

/*
 * @Author: Guillermo Ortega Romo
 * @Description: Fucntion for do an action acording to the chain received.
 */
void chooseAction(String Action){
  //Modificar
  if(Action.equals("strm")){
    out = "{\"strm\":{\"t_1\":" + String(TH[0]) + ",\"t_2\":" + String(TH[1]) + ",\"h_1\":" + String(TH[2]) + "}}";
    out.toCharArray(outString, buffersize);
  }
}
