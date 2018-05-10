#include <stdio.h>
#include <stdlib.h>
#include <string.h>




#include<conio.h>  // libreria para el uso de getch()  
#include<time.h>   // libreria para el uso de time()  

   
  





int aux1;

float *tramaa(const char *cad);



int main(int argc, char *argv[]) {
	
	float	recibir[16];
	int		direccion;
char tramag[139];


     // Declaracion de variables  
     int numero,cantidad,contador;  
     int hora = time(NULL);  
  cantidad= 139;
     // Semilla de rand();  
     srand(hora);  
  
     /* Recogemos por teclado la cantidad de 
        numeros que quiere el usuario */  
  
  
  
        /* Generamos un ciclo que se repite la cantidad 
           de veces indicada. En cada vuelta del ciclo se 
           genera y se imprime un numero aleatorio. */  
  
        for(contador = 0; contador<cantidad; contador++)  
        {  
  
               numero = rand()%100;  
              tramag[contador]=numero;       }  
              
              
	
		
		printf("direccion = %f",tramaa(tramag)[0]);

	return 0;
}
	
float *tramaa(const char *trama){
	float *datoss,auxf[16];
		char a,b,c;
	char aux[1];
short  magx;
float dps=0.06103;
float acce= 12;
float magne = 0.00222;





              
//-------------------------magnetometro x---------------------------------

float mgx;



//trnasformando de char a int

asm  (  "leal %1, %%ebx\n"          //bx<--direccion de mag
        "leal %0, %%ecx\n"          //cx<--direccion de magx
        "movb (%%ebx),%%al\n\t"        //al<--contenido(ebx)
        "movb %%al,0(%%ecx)\n\t"         //contenido(ecx)<--al
        : "=m" (magx)        //salida
        : "m"  (trama)         //entrada
        :
     );


asm  (  "leal %1, %%ebx\n"          //bx<--direccion de k
        "leal %0, %%ecx\n"          //cx<--direccion de msr
        "movb 0(%%ebx),%%al\n\t"        //al<--contenido(ebx)
        "movb %%al,1(%%ecx)\n\t"         //contenido(ecx)<--al
        
        : "=m" (magx)        //salida
        : "m"  (trama)         //entrada
        :
     );


mgx=magx*magne;
printf("entero: %i\n", mgx);

//----------- --------------magnetrometo en y



short  magy;
float mgy;





//trnasformando de char a int

asm  (  "leal %1, %%ebx\n"          //bx<--direccion de k
        "leal %0, %%ecx\n"          //cx<--direccion de varent
        "movb 3(%%ebx),%%al\n\t"        //al<--contenido(ebx)
        "movb %%al,0(%%ecx)\n\t"         //contenido(ecx)<--al
        : "=m" (magy)        //salida
        : "m"  (trama)         //entrada
        :
     );


asm  (  "leal %1, %%ebx\n"          //bx<--direccion de k
        "leal %0, %%ecx\n"          //cx<--direccion de msr
        "movb 2(%%ebx),%%al\n\t"        //al<--contenido(ebx)
        "movb %%al,1(%%ecx)\n\t"         //contenido(ecx)<--al
        : "=m" (magy)        //salida
        : "m"  (trama)         //entrada
        :
     );


mgy=magy*magne;
printf("entero: %i\n", magy);


//----------------------------------magnetometro en z----------------

short  magz;
float mgz;
//trnasformando de char a int

asm  (  "leal %1, %%ebx\n"          //bx<--direccion de k
        "leal %0, %%ecx\n"          //cx<--direccion de varent
        "movb 5(%%ebx),%%al\n\t"        //al<--contenido(ebx)
        "movb %%al,0(%%ecx)\n\t"         //contenido(ecx)<--al
        : "=m" (magz)        //salida
        : "m"  (trama)         //entrada
        :
     );


asm  (  "leal %1, %%ebx\n"          //bx<--direccion de k
        "leal %0, %%ecx\n"          //cx<--direccion de msr
        "movb 4(%%ebx),%%al\n\t"        //al<--contenido(ebx)
        "movb %%al,1(%%ecx)\n\t"         //contenido(ecx)<--al
        : "=m" (magz)        //salida
        : "m"  (trama)         //entrada
        :
     );

mgz=magz*magne;
printf("entero: %i\n", mgz);


//------------------------------acelerometro en x--------------------

short  acelx;
float aclx;
//trnasformando de char a int

asm  (  "leal %1, %%ebx\n"          //bx<--direccion de k
        "leal %0, %%ecx\n"          //cx<--direccion de varent
        "movb 7(%%ebx),%%al\n\t"        //al<--contenido(ebx)
        "movb %%al,0(%%ecx)\n\t"         //contenido(ecx)<--al
        : "=m" (acelx)        //salida
        : "m"  (trama)         //entrada
        :
     );


asm  (  "leal %1, %%ebx\n"          //bx<--direccion de k
        "leal %0, %%ecx\n"          //cx<--direccion de msr
        "movb 6(%%ebx),%%al\n\t"        //al<--contenido(ebx)
        "movb %%al,1(%%ecx)\n\t"         //contenido(ecx)<--al
        : "=m" (acelx)        //salida
        : "m"  (trama)         //entrada
        :
     );


aclx=acelx*acce;
printf("entero:%f\n", aclx);


//-----------------------------------acelerometro en y

short  acely;
float acly;
//trnasformando de char a int

asm  (  "leal %1, %%ebx\n"          //bx<--direccion de k
        "leal %0, %%ecx\n"          //cx<--direccion de varent
        "movb 9(%%ebx),%%al\n\t"        //al<--contenido(ebx)
        "movb %%al,0(%%ecx)\n\t"         //contenido(ecx)<--al
        : "=m" (acely)        //salida
        : "m"  (trama)         //entrada
        :
     );


asm  (  "leal %1, %%ebx\n"          //bx<--direccion de k
        "leal %0, %%ecx\n"          //cx<--direccion de msr
        "movb 8(%%ebx),%%al\n\t"        //al<--contenido(ebx)
        "movb %%al,1(%%ecx)\n\t"         //contenido(ecx)<--al
        : "=m" (acely)        //salida
        : "m"  (trama)         //entrada
        :
     );


acly=acely*acce;
printf("entero:%f\n", acly);

//-------------------------------------acelerometro en z

short  acelz;
float aclz;
//trnasformando de char a int

asm  (  "leal %1, %%ebx\n"          //bx<--direccion de k
        "leal %0, %%ecx\n"          //cx<--direccion de varent
        "movb 11(%%ebx),%%al\n\t"        //al<--contenido(ebx)
        "movb %%al,0(%%ecx)\n\t"         //contenido(ecx)<--al
        : "=m" (acelz)        //salida
        : "m"  (trama)         //entrada
        :
     );


asm  (  "leal %1, %%ebx\n"          //bx<--direccion de k
        "leal %0, %%ecx\n"          //cx<--direccion de msr
        "movb 10(%%ebx),%%al\n\t"        //al<--contenido(ebx)
        "movb %%al,1(%%ecx)\n\t"         //contenido(ecx)<--al
        : "=m" (acelz)        //salida
        : "m"  (trama)         //entrada
        :
     );

aclz=acelz*acce;
printf("entero:%f\n", aclz);
//------------------------------------------giroscopio en x



short  girox;
float grx;
//trnasformando de char a int

asm  (  "leal %1, %%ebx\n"          //bx<--direccion de k
        "leal %0, %%ecx\n"          //cx<--direccion de varent
        "movb 13(%%ebx),%%al\n\t"        //al<--contenido(ebx)
        "movb %%al,0(%%ecx)\n\t"         //contenido(ecx)<--al
        : "=m" (girox)        //salida
        : "m"  (trama)         //entrada
        :
     );


asm  (  "leal %1, %%ebx\n"          //bx<--direccion de k
        "leal %0, %%ecx\n"          //cx<--direccion de msr
        "movb 12(%%ebx),%%al\n\t"        //al<--contenido(ebx)
        "movb %%al,1(%%ecx)\n\t"         //contenido(ecx)<--al
        : "=m" (girox)        //salida
        : "m"  (trama)         //entrada
        :
     );


grx=girox*dps;
printf("entero:%i\n", girox);


//-----------------------------------------------giroscopio en y

short  giroy;
float gry;
//trnasformando de char a int

asm  (  "leal %1, %%ebx\n"          //bx<--direccion de k
        "leal %0, %%ecx\n"          //cx<--direccion de varent
        "movb 15(%%ebx),%%al\n\t"        //al<--contenido(ebx)
        "movb %%al,0(%%ecx)\n\t"         //contenido(ecx)<--al
        : "=m" (giroy)        //salida
        : "m"  (trama)         //entrada
        :
     );


asm  (  "leal %1, %%ebx\n"          //bx<--direccion de k
        "leal %0, %%ecx\n"          //cx<--direccion de msr
        "movb 14(%%ebx),%%al\n\t"        //al<--contenido(ebx)
        "movb %%al,1(%%ecx)\n\t"         //contenido(ecx)<--al
        : "=m" (giroy)        //salida
        : "m"  (trama)         //entrada
        :
     );


gry=giroy*dps;
printf("entero:%f\n", gry);


//---------------------------------------giroscopio en z




short  giroz;
float grz;
//trnasformando de char a int

asm  (  "leal %1, %%ebx\n"          //bx<--direccion de k
        "leal %0, %%ecx\n"          //cx<--direccion de varent
        "movb 17(%%ebx),%%al\n\t"        //al<--contenido(ebx)
        "movb %%al,0(%%ecx)\n\t"         //contenido(ecx)<--al
        : "=m" (giroz)        //salida
        : "m"  (trama)         //entrada
        :
     );


asm  (  "leal %1, %%ebx\n"          //bx<--direccion de k
        "leal %0, %%ecx\n"          //cx<--direccion de msr
        "movb 16(%%ebx),%%al\n\t"        //al<--contenido(ebx)
        "movb %%al,1(%%ecx)\n\t"         //contenido(ecx)<--al
        : "=m" (giroz)        //salida
        : "m"  (trama)         //entrada
        :
     );


grz=giroz*dps;
printf("entero:%i\n", giroz);


///----------------------barometro ----------

int baro;
short auxia;
short auxib ;
short auxic;
int auxir;
short auxix;
float barox;


asm ( "leal %1, %%ebx\n"	
      "leal %0, %%ecx\n"

	   "movb 20(%%ebx),%%al\n\t"        //al<--contenido(ebx)
       "and $0xf0,%%al\n\t"         //contenido(ecx)<--al
       "shr $4,%%al\n\t"
       "movb %%al,0(%%ecx)\n\t"
        : "=m" (auxic)        //salida
        : "m"  (trama)         //entrada
        :	
	);	
	
asm ( "leal %1, %%ebx\n"	
      "leal %0, %%ecx\n"

		"movb 19(%%ebx),%%al\n\t"     //al<--contenido(ebx)
        "shl  $4,%%al\n\t"
        
		
		"or %2,%%al\n\t"         //contenido(ecx)<--al
        "movb %%al,0(%%ecx)\n\t"
        : "=m" (auxib)               //salida
        : "m"  (trama), "m" (auxic)           //entrada
        :	
		

);




 

asm ( "leal %1, %%ebx\n"	
      "leal %0, %%ecx\n"

		"movb 19(%%ebx),%%al\n\t"     //al<--contenido(ebx)
        "shr  $4,%%al\n\t"
        
		
	//	"and $0x00,%%al\n\t"         //contenido(ecx)<--al
        "movb %%al,1(%%ecx)\n\t"
        : "=m" (auxib)               //salida
        : "m"  (trama)             //entrada
        :	
		

);

/**asm("leal %1, %%ebx\n"	b
    "leal %0, %%ecx\n"
		"movb 0(%%ebx),%%al\n\t"
		"movb %%al,0(%%ecx)\n\t"

		: "=m" (auxir)               //salida
        : "m"  (auxib)             //entrada
        :	
		



);

asm("leal %1, %%ebx\n"	
    "leal %0, %%ecx\n"
		"movb 1(%%ebx),%%al\n\t"
		"movb %%al,1(%%ecx)\n\t"

		: "=m" (auxir)               //salida
        : "m"  (auxib)             //entrada
        :	
		



);*/

asm ( "leal %1, %%ebx\n"	
      "leal %0, %%ecx\n"

		"movb 18(%%ebx),%%ah\n\t"     //al<--contenido(ebx)
        "shl  $4,%%ah\n\t"
        
		
	//	"and $0x00,%%al\n\t"         //contenido(ecx)<--al
        "mov %%ax,0(%%ecx)\n\t"
        : "=m" (auxia)               //salida
        : "m"  (trama)       //entrada
        :	
		

);





asm ( "leal %1, %%ebx\n"	
      "leal %0, %%ecx\n"

	//	"movb 14(%%ebx),%%al\n\t"     //al<--contenido(ebx)
        //"shl  $2,%%al\n\t"
        
        
        "mov %3,%%ax\n\t"
        "or %2,%%ax\n\t"
        
        
		
	//	"and $0x00,%%al\n\t"         //contenido(ecx)<--al
        "mov %%ax,0(%%ecx)\n\t"
        : "=m" (auxir)               //salida
        : "m"  (trama) , "m"  (auxia) , "m" (auxib)    //entrada
        :	
		

);


 

asm ( "leal %1, %%ebx\n"	
      "leal %0, %%ecx\n"

		"movb 18(%%ebx),%%al\n\t"     //al<--contenido(ebx)
       "shr  $4,%%al\n\t"
        
		
		
	//	"and $0x03,%%al\n\t"         //contenido(ecx)<--al
        "and $0x000f,%%ax\n\t"
		"movb %%al,0(%%ecx)\n\t"
        : "=m" (auxix)               //salida
        : "m"  (trama)             //entrada
        :	
		

);



asm ( "leal %1, %%ebx\n"	
      "leal %0, %%ecx\n"

    "movb %%al,2(%%ecx)\n\t"
        : "=m" (auxir)               //salida
        : "m"  (trama) , "m"  (auxix) , "m" (auxib)    //entrada
        :	
		

);   


//trnasformando de char a int

asm  (  "leal %1, %%ebx\n"          //bx<--direccion de mag
        "leal %0, %%ecx\n"          //cx<--direccion de magx
        "movb 1(%%ebx),%%al\n\t"        //al<--contenido(ebx)
        "movb %%al,1(%%ecx)\n\t"         //contenido(ecx)<--al
        : "=m" (baro)        //salida
        : "m"  (auxir)         //entrada
        :
     );


asm  (  "leal %1, %%ebx\n"          //bx<--direccion de k
        "leal %0, %%ecx\n"          //cx<--direccion de msr
        "movb 0(%%ebx),%%al\n\t"        //al<--contenido(ebx)
        "movb %%al,2(%%ecx)\n\t"         //contenido(ecx)<--al
        
        : "=m" (baro)        //salida
        : "m"  (auxir)         //entrada
        :
     );

asm  (  "leal %1, %%ebx\n"          //bx<--direccion de k
        "leal %0, %%ecx\n"          //cx<--direccion de msr
        "movb 2(%%ebx),%%al\n\t"        //al<--contenido(ebx)
        "movb %%al,0(%%ecx)\n\t"         //contenido(ecx)<--al
        
        : "=m" (baro)        //salida
        : "m"  (auxir)         //entrada
        :
     );


 



if (auxir>1048575)
{
	auxir=auxir-33554432	;
};



printf("entero:%i\n", auxir);

barox=auxir*dps;


printf("entero:%i\n", baro);

//-----------------------------------temp1------------------


short  temp1;
float temp1n;
//trnasformando de char a int

asm  (  "leal %1, %%ebx\n"          //bx<--direccion de k
        "leal %0, %%ecx\n"          //cx<--direccion de varent
        "movb 21(%%ebx),%%al\n\t"        //al<--contenido(ebx)
        "movb %%al,0(%%ecx)\n\t"         //contenido(ecx)<--al
        : "=m" (temp1)        //salida
        : "m"  (trama)         //entrada
        :
     );


asm  (  "leal %1, %%ebx\n"          //bx<--direccion de k
        "leal %0, %%ecx\n"          //cx<--direccion de msr
        "movb 20(%%ebx),%%al\n\t"        //al<--contenido(ebx)
        
 		"and $0x0f,%%al\n\t"        
        
        
        
        "movb %%al,1(%%ecx)\n\t"         //contenido(ecx)<--al
        : "=m" (temp1)        //salida
        : "m"  (trama)         //entrada
        :
     );

printf("entero:%i\n", temp1);

//-----------------------------------temp2------------------


short  temp2;
float temp2n;
//trnasformando de char a int

asm  (  "leal %1, %%ebx\n"          //bx<--direccion de k
        "leal %0, %%ecx\n"          //cx<--direccion de varent
        "movb 23(%%ebx),%%al\n\t"        //al<--contenido(ebx)
		"and $0xf0,%%al\n\t"        
         "shr  $4,%%al\n\t"
        
        
        
        
        "movb %%al,0(%%ecx)\n\t"         //contenido(ecx)<--al
        : "=m" (temp2)        //salida
        : "m"  (trama)         //entrada
        :
     );










asm  (  "leal %1, %%ebx\n"          //bx<--direccion de k
        "leal %0, %%ecx\n"          //cx<--direccion de msr
        "movb 22(%%ebx),%%al\n\t"        //al<--contenido(ebx)
        
 	
        
        
        
        "movb %%al,1(%%ecx)\n\t"         //contenido(ecx)<--al
        : "=m" (temp2)        //salida
        : "m"  (trama)         //entrada
        :
     );

printf("entero:%i\n", temp2);





//-----------------------------------temp3------------------


short  temp3;
float temp3n;
//trnasformando de char a int

asm  (  "leal %1, %%ebx\n"          //bx<--direccion de k
        "leal %0, %%ecx\n"          //cx<--direccion de varent
        "movb 24(%%ebx),%%al\n\t"        //al<--contenido(ebx)
        "movb %%al,0(%%ecx)\n\t"         //contenido(ecx)<--al
        : "=m" (temp3)        //salida
        : "m"  (trama)         //entrada
        :
     );


asm  (  "leal %1, %%ebx\n"          //bx<--direccion de k
        "leal %0, %%ecx\n"          //cx<--direccion de msr
        "movb 23(%%ebx),%%al\n\t"        //al<--contenido(ebx)
        
 		"and $0x0f,%%al\n\t"        
        
        
        
        "movb %%al,1(%%ecx)\n\t"         //contenido(ecx)<--al
        : "=m" (temp3)        //salida
        : "m"  (trama)         //entrada
        :
     );

printf("entero:%i\n", temp3);



//-----------------------------------sensor de corriente------------------


short  corr;
float corr1;
//trnasformando de char a int

asm  (  "leal %1, %%ebx\n"          //bx<--direccion de k
        "leal %0, %%ecx\n"          //cx<--direccion de varent
        "movb 26(%%ebx),%%al\n\t"        //al<--contenido(ebx)
		"and $0xf0,%%al\n\t"        
         "shr  $4,%%al\n\t"
        
        
        
        
        "movb %%al,0(%%ecx)\n\t"         //contenido(ecx)<--al
        : "=m" (corr)        //salida
        : "m"  (trama)         //entrada
        :
     );










asm  (  "leal %1, %%ebx\n"          //bx<--direccion de k
        "leal %0, %%ecx\n"          //cx<--direccion de msr
        "movb 25(%%ebx),%%al\n\t"        //al<--contenido(ebx)
        
 	
        
        
        
        "movb %%al,1(%%ecx)\n\t"         //contenido(ecx)<--al
        : "=m" (corr)        //salida
        : "m"  (trama)         //entrada
        :
     );

printf("entero:%i\n", corr);



//-----------------------------------sensor de voltaje------------------


short  volt;
float volt1;
//trnasformando de char a int

asm  (  "leal %1, %%ebx\n"          //bx<--direccion de k
        "leal %0, %%ecx\n"          //cx<--direccion de varent
        "movb 26(%%ebx),%%al\n\t"        //al<--contenido(ebx)
        "movb %%al,0(%%ecx)\n\t"         //contenido(ecx)<--al
        : "=m" (volt)        //salida
        : "m"  (trama)         //entrada
        :
     );


asm  (  "leal %1, %%ebx\n"          //bx<--direccion de k
        "leal %0, %%ecx\n"          //cx<--direccion de msr
        "movb 27(%%ebx),%%al\n\t"        //al<--contenido(ebx)
        
 		"and $0x0f,%%al\n\t"        
        
        
        
        "movb %%al,1(%%ecx)\n\t"         //contenido(ecx)<--al
        : "=m" (volt)        //salida
        : "m"  (trama)         //entrada
        :
     );

printf("entero:%i\n", volt);

//----------------------------------sensor ultravioleta----------------

short  suv;
float su1;
//trnasformando de char a int

asm  (  "leal %1, %%ebx\n"          //bx<--direccion de k
        "leal %0, %%ecx\n"          //cx<--direccion de varent
        "movb 29(%%ebx),%%al\n\t"        //al<--contenido(ebx)
        "movb %%al,0(%%ecx)\n\t"         //contenido(ecx)<--al
        : "=m" (suv)        //salida
        : "m"  (trama)         //entrada
        :
     );


asm  (  "leal %1, %%ebx\n"          //bx<--direccion de k
        "leal %0, %%ecx\n"          //cx<--direccion de msr
        "movb 28(%%ebx),%%al\n\t"        //al<--contenido(ebx)
        "movb %%al,1(%%ecx)\n\t"         //contenido(ecx)<--al
        : "=m" (suv)        //salida
        : "m"  (trama)         //entrada
        :
     );

mgz=magz*magne;
printf("entero: %i\n", mgz);

auxf[0]=mgx;
auxf[1]=corr;
auxf[2]=volt1;
auxf[3]=su1;
auxf[4]=barox;
auxf[5]=mgx;
auxf[6]=temp3n;
auxf[7]=temp3n;
auxf[8]=temp3n;
auxf[9]=temp3n;
auxf[10]=temp3n;
auxf[11]=temp3n;
auxf[12]=temp3n;
auxf[13]=temp3n;
auxf[14]=temp3n;
auxf[15]=temp3n;


datoss=auxf;
printf("cat=%f",mgx);
return datoss;
	
}	

	
	
	

		
	


