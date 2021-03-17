void setup()
{
  Serial.begin(9600);
}

void loop()
{
  int a= 2, b= 2, resul;
  int arre[4];

  resul= a+b;
  //Serial.print("El resultado es: ");
  //Serial.println(resul);
  //Serial.println("Otra cosa");
  //Serial.println("Otra cosa 2");
  arre[0]= 1;
  arre[1]= 2;
  arre[2]= 3;
  arre[3]= 4;
  Serial.println(arre[0], arre[1], arre[2], arre[3]);
  delay(1000);
}
