# Documentation
Here you can find the explanation of each of the methods that are in the whole program. So you can now the purpose of that methods.
<br>
This is the official documentation of the program.

## Arduino
### File: funciones.cpp
@Authors: Guillermo Ortega Romo and Diego Martínez Sánchez
<br>
@Description: A function in which are all the setup talking about the actions that the pin´s should do and other initializing functions from the
beggining of the execution of the arduino program.
```
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
}
```

@Author: Diego Martínez Sánchez
<br>
@Description: For turning on all components everytime the app its initialized all components for check that all components works fine.
```
void inicio()//Poner en void cuando compruebe en efecto la variable global se mantiene en 1 después.
{
  if (iniciar == 0)
  {
    delay(4000);
    iniciar = 1;
  }
}
```
@Author: Guillermo Ortega Romo
<br>
@Description: Fucntion to detect if something comes from the serial port.

```
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
```

@Author: Diego Martínez Sánchez
<br>
@Description: A function to get the state of the floating water sensor in order to let the arduino know about the drinker if we need to refill
manual or in automatic way in order to manage better the parameters of the terrarium.

```
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
}
```

@Author: Diego Martínez Sánchez
<br>
@Description: A function to update the variables of the array that will be used to send the data to the raspberry program in to show the
parameters through the raspberry application and to manage the automatic functionality of the terrarium.
```
void TempHum()
{
  TH[1]= dht.readTemperature();
  TH[2]= dht.readHumidity();
}
```

@Author: Diego Martínez Sánchez
<br>
@Description: A function for activate the humidity water bomb in order to humidify the terrarium in the automatic mode.
```
void humedecerTerrario(float hum)
{
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
```