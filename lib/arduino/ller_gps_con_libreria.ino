#include <SoftwareSerial.h>
#include <TinyGPS.h>

TinyGPS gps;
SoftwareSerial ss(4, 3);
  long lat=0, lon=0;
  unsigned long age, fix_age;
  unsigned long altura=0;
  int year;
  byte month=0, day=0, hour=0, minute=0, second=0, hundredths=0;
void setup()
{
  Serial.begin(115200);
  ss.begin(9600);
  Serial.println();

}

void loop()
{
  bool newData = false;
  
  for (unsigned long start = millis(); millis() - start < 500;)  //tiempo de espera de 1000ms
  {
    while (ss.available())
    {
      char g = ss.read();
       if (gps.encode(g)) // Recibio una línea nueva?
        {newData = true;
    }}
  }

  if (newData)
  {
    altura=gps.altitude();
    gps.get_position(&lat, &lon, &age);
    gps.crack_datetime(&year, &month, &day, &hour, &minute, &second, &hundredths, &fix_age);
    if(hour >= 4) //Reajusta la hora UTC a la hora LOCAL
      {hour-=4;}
    else
      {hour+=20;}
    year-=2000;
  }

    Serial.print(" LAT= ");
    Serial.print(lat,HEX);
    
    Serial.print("  LON= ");
    Serial.print(lon,HEX);
    
    Serial.print("  ALT= ");
    Serial.print(altura);
    
    Serial.print("  HORA= ");
    

    Serial.print(hour);Serial.print(":");
    Serial.print(minute);Serial.print(":");
    Serial.print(second);

    Serial.print("  FECHA= ");
    Serial.print(day);Serial.print("/");
    Serial.print(month);Serial.print("/");
    Serial.println(year,BIN);
    
    byte trama[14];
    trama[0]=(hour<<3)|(minute>>3);
    trama[1]=(minute<<5)|(second>>1);
    trama[2]=(second<<7)|(day<<2)|(month>>2);
    trama[3]=(month<<6)|(year);
    trama[4]=(altura>>8);
    trama[5]=(altura&0xFF);
    trama[6]=(lat>>24);
    trama[7]=(lat>>16)&(0xFF);
    trama[8]=(lat>>8)&(0xFF);
    trama[9]=(lat)&(0xFF);
    trama[10]=(lon>>24);
    trama[11]=(lon>>16)&(0xFF);
    trama[12]=(lon>>8)&(0xFF);
    trama[13]=(lon)&(0xFF); 
//    Serial.print(" LAT= ");
//    Serial.print(trama[6],HEX); 
//    Serial.print(trama[7],HEX); 
//    Serial.print(trama[8],HEX); 
//    Serial.print(trama[9],HEX); 
//
//    Serial.print(" LON= ");
//    Serial.print(trama[10],HEX); 
//    Serial.print(trama[11],HEX); 
//    Serial.print(trama[12],HEX); 
//    Serial.println(trama[13],HEX);
}
