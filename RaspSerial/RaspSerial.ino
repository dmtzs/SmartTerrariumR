#include <SoftwareSerial.h>

SoftwareSerial BT(3, 2);//Rx | Tx del módulo bluetooth hacia los pines del arduino.

void setup()
{
  Serial.begin(9600);
  BT.begin(57600);//Se inicia el puerto para mandar los datos bluetooth.
}

void loop()
{
  if(BT.available())
  {
    //variable= GetlineBT();//Para obtener lo que se le manda por bluetooth en caso de ser necesario
    BT.println();
  }
}
