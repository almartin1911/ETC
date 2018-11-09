#include <SoftwareSerial.h>

SoftwareSerial gps(9,8);

char dato=' ';

void setup()
{
 Serial.begin(115200);            
 gps.begin(9600); 
}


void loop()
{
  
  if(gps.available()>0)
  {
    Serial.print("->");
    Serial.print(gps.available());
    Serial.print("<-");
    dato=gps.read();
    Serial.print(dato);
    
//    Serial.print(ver);
  }
  
}
