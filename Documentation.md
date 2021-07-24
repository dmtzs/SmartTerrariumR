# Documentation
Here you can find the explanation of each of the methods that are in the whole program. So you can now the purpose of that methods.
<br>
This is the official documentation of the program.

## Arduino
@Author: Guillermo Ortega Romo and Diego Martínez Sánchez
<br>
@Description: A function in which are all the setup talking about the actions that the pin´s should do and other initializing functions from the-
<br>
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
