#include <stdio.h>
#include <stdlib.h>
#include <time.h>

void print_uchar_array(u_int8_t *buf, int count);

void fill_with_random(u_int8_t *buf, int count);

void parse_package(u_int8_t *in, int tam_in, float *out, int tam_out);

int conver1(int cad1, int cad2, short salida);

void print_float_array(float *buf, int count);

int add_int_array(int *buf, int count);

void copy_array(int array_in[], int size, int array_out[]);

void update_array(int array_in[], int size);

int main() {
    int tam_array_in = 30;
    int tam_array_out = 16;
    u_int8_t array_in[30];
    float array_out[16];

    srand(time(NULL));

    fill_with_random(array_in, tam_array_in);
    print_uchar_array(array_in, tam_array_in);

    printf("\n\n");

    parse_package(array_in, tam_array_in, array_out, tam_array_out);
    print_float_array(array_out, tam_array_out);

    return 0;
}

void print_uchar_array(u_int8_t *buf, int count){
    for (size_t i = 0; i < count; i++) {
        printf("%d, ", buf[i]);
    }
}

void fill_with_random(u_int8_t *buf, int count) {
    u_int8_t num;

    for(size_t i = 0; i < count; ++i){
        num = rand();
        buf[i] = num;
    }
}

void parse_package(u_int8_t *cadena, int tam_in, float *datos, int tam_out){
        // for (size_t i = 0; i < tam_out; i++) {
        //     out[i] = in[i] + 0.343;
        // }
        short nukaworld=0;
         short new_vegas1=0;
         short new_vegas2=0;
         short new_vegas3=0;
         short farharbor=0;
         short farharbor1=0;
         short farharbor2=0;
         int farharbor3=0;
         short vault_tec=0;
         short vault_tec1=0;
         int vault_tec2=0;
         short wasteland=0;
         short wasteland0=0;
         short wasteland1=0;
         short wasteland2=0;
         short wasteland3=0;
         short brokensteel0=0;
         short brokensteel1=0;
         short brokensteel2=0;
         short brokensteel3=0;
         short anchorage0=0;
         short anchorage1=0;
         short anchorage2=0;
         short anchorage3=0;
          short anchoragea=0;
         short point_lookout0=0;
         short point_lookout1=0;
         short point_lookout2=0;
         short point_lookout3=0;
         short mothership0=0;
         short mothership1=0;
         short mothership2=0;
         short mothership3=0;
          short mothership4=0;


         short automatron=0;


         float magne = 2.56;
         float dps=0.076335877;
         float acce= 0.000061035;

         float barometro = 0.008;
         float valor = 0.0002442;

//-------------------------magx-------------------
float magx;

         nukaworld=conver1(cadena[0],cadena[1],nukaworld);
         magx=nukaworld;//*magne;
         // printf("magnetometro: %f\n ", magx);

//--------------------------------------------------------
//--------------------------------magy-----------------------


        float magy;
        nukaworld=conver1(cadena[2],cadena[3],nukaworld);
        magy=nukaworld;//*magne;
        // printf("magnetometro: %f\n ", magy);


//-----------------------------------------------------
//--------------------------------magz-----------------------

         float magz;
         nukaworld=conver1(cadena[4],cadena[5],nukaworld);
         magz=nukaworld;//*magne;
         // printf("magnetometro: %f\n ", magz);



 //-------------------------acelerometro en x-------------------

                   float acelx;
                   nukaworld=conver1(cadena[6],cadena[7],nukaworld);
                   acelx=nukaworld;//*dps;
                   // printf("acelerometro: %f\n ", acelx);

  //--------------------------------------------------------
  //--------------------------------acelerometro en y-----------------------


                  float acely;
                  nukaworld=conver1(cadena[8],cadena[9],nukaworld);
                  acely=nukaworld;//*dps;
                   //printf("acelerometro: %f\n ", acely);


  //-----------------------------------------------------
  //--------------------------------acelerometro en z-----------------------

                   float acelz;
                   nukaworld=conver1(cadena[10],cadena[11],nukaworld);
                   acelz=nukaworld;//*dps;
                 //   printf("acelerometro: %f\n ", acelz);

   //-------------------------giroscopio en x-------------------
                    float girox;

                     nukaworld=conver1(cadena[12],cadena[13],nukaworld);
                     girox=nukaworld*dps;
                    //  printf("giroscopio: %f\n ", girox);
   //--------------------------------------------------------
    //--------------------------------giroscopio en y-----------------------

                    float giroy;
                    nukaworld=conver1(cadena[14],cadena[15],nukaworld);
                    giroy=nukaworld*dps;
                  //   printf("giroscopio: %f\n ", giroy);


 //-----------------------------------------------------
   //--------------------------------giroscopio en z-----------------------

                float giroz;
                nukaworld=conver1(cadena[16],cadena[17],nukaworld);
                 giroz=nukaworld*magne;
                // printf("giroscopio: %f\n ", giroz);

//--------------------------------------------------------------------------
//--------------------------------barometro------------------------------

        automatron= (int)(cadena[20]);

        float barome;

        automatron & 0xf0;
        automatron >>=4;



        new_vegas1=(short)(cadena[19]);

        new_vegas2=new_vegas1 & 0x0f;
        new_vegas2 <<=4;


        farharbor = new_vegas2 | automatron;

        new_vegas3=new_vegas1& 0xf0;
        new_vegas3 <<=4;

        farharbor1= farharbor | new_vegas3;



        vault_tec=(short)cadena[18];

        vault_tec1=vault_tec& 0x0f;
        vault_tec1 <<= 12;

        farharbor2= farharbor1 | vault_tec1;

        vault_tec2=vault_tec & 0xf0;
        vault_tec2<<=12;

        farharbor3= farharbor2 | vault_tec2;

        barome=farharbor3 *barometro;



//------------------------temperatura 1-----------
//--------------------------------------------------

        wasteland= (int)cadena[20];
        wasteland0=wasteland& 0x0f;
        wasteland0<<=8;

        wasteland1=(int)cadena[21];

        wasteland2=wasteland0 | wasteland1;


//--------------------------temperatura 2 ----------------------
//----------------------------------------------------

        brokensteel0 = (int)cadena[22];
        brokensteel0<<=8;
        brokensteel1= (int)cadena[23];

        brokensteel2 = brokensteel0 | brokensteel1;
        brokensteel3 = brokensteel2 & 0xfff0;
        brokensteel3>>=4;
//--------------------------temperatura 3----------------------
//----------------------------------------------------

        anchorage0 = (int)cadena[23];
        anchoragea=anchorage0<<8;
        anchorage1= (int)cadena[24];

        anchorage2 = anchoragea| anchorage1;

        anchorage3 = anchorage2 & 0x0fff;


//--------------------------sensor de corriente ----------------------
//----------------------------------------------------

        point_lookout0 = (int)cadena[25];
        point_lookout0<<=8;
        point_lookout1= (int)cadena[26];

        point_lookout2 = point_lookout0 | point_lookout1;
        point_lookout3 = point_lookout2 & 0xfff0;
        point_lookout3>>=4;

//--------------------------sensor de voltaje----------------------
//----------------------------------------------------

        mothership0 = (int)cadena[26];
        mothership1=mothership0<<8;
        mothership2= (int)cadena[27];

        mothership3 = mothership1| mothership2;

        mothership4 = mothership3 & 0x0fff;



        //printf("mimi: %i\n ", mothership4);


//--------------------------sensor ultravioleta----------------------
//----------------------------------------------------


float ultra;

         nukaworld=conver1(cadena[28],cadena[29],nukaworld);
         ultra=nukaworld;//*valor;
         // printf("ultra: %f\n ", ultra);




          datos[0]=magx;
          datos[1]=magy;
          datos[2]=magz;
          datos[3]=acelx;
          datos[4]=acely;
          datos[5]=acelz;
          datos[6]=girox;
          datos[7]=giroy;
          datos[8]=giroz;
          datos[9]=barome;
          datos[10]=wasteland2;
          datos[11]=brokensteel3;
          datos[12]=anchorage3;
          datos[13]=point_lookout3;
          datos[14]=mothership4;
          datos[15]=ultra;

}

int conver1 (int cad1, int cad2, short salida){
        short entero, entero2;
        short massfusion=0;

        entero=(int)cad1;
        entero2=(int)cad2;
        entero<<=8;
        salida= entero | entero2;

        //printf("entero = %i\n",salida);
        return salida;
}

void print_float_array(float *buf, int count){
    for (size_t i = 0; i < count; i++) {
        printf("%.8f, ", buf[i]);
    }
}

int add_int_array(int *buf, int count){
    int i;
    int result = 0;

    for (i = 0; i < count; i++) {
        result += buf[i];
    }

    return result;
}

void copy_array(int array_in[], int size, int array_out[]){
    int i;

    for (i = 0; i < size; i++) {
        array_out[i] = array_in[i];
    }
}

void update_array(int array_in[], int size){
    int i;

    for (i = 0; i < size; i++) {
        array_in[i] = array_in[i] * 2;
    }
}
