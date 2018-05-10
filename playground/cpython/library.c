// (On Linux) Execute this to compile:
// gcc -shared -Wl ,-install_name,library.so -o library.so -fPIC library.c
#include <stdio.h>

//Header
int evenOrOdd(int);

//Function
/*  Returns 1 if it's even, 0 if it's odd
    \param integer x */
int evenOrOdd(int x){
  if(x % 2 == 0)
    return 1;
  return 0;
}
