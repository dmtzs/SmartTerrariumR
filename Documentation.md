# Documentation
Here you can find the explanation of each of the methods that are in the whole program. So you can now the purpose of that methods.
<br>
This is the official documentation of the program.

## Arduino
@Author: Diego Martínez Sánchez
<br>
@Description: For turning on all components everytime the app its initialized all components for check if all works fine.
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