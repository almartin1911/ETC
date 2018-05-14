#include <stdio.h>
#include <stdlib.h>
#include <time.h>

void print_u_char_array(unsigned char *buf, int count);

void fill_with_random(unsigned char *buf, int count);

void convierte(unsigned char *in, int tam_in, float *out, int tam_out);

void print_float_array(float *buf, int count);

int add_int_array(int *buf, int count);

void copy_array(int array_in[], int size, int array_out[]);

void update_array(int array_in[], int size);

int main() {
    int tam_array_in = 139;
    int tam_array_out = 16;
    unsigned char array_in[139];
    float array_out[16];

    srand(time(NULL));

    fill_with_random(array_in, tam_array_in);
    print_u_char_array(array_in, tam_array_in);

    printf("\n\n");

    convierte(array_in, tam_array_in, array_out, tam_array_out);
    print_float_array(array_out, tam_array_out);

    return 0;
}

void print_u_char_array(unsigned char *buf, int count){
    for (size_t i = 0; i < count; i++) {
        printf("%d, ", buf[i]);
    }
}

void fill_with_random(unsigned char *buf, int count) {
    unsigned char num;

    for(int i = 0; i < count; ++i){
        num = rand();
        buf[i] = num;
    }
}

void convierte(unsigned char *in, int tam_in, float *out, int tam_out){
        for (int i = 0; i < tam_out; i++) {
            out[i] = in[i] + 0.34;
        }
}

void print_float_array(float *buf, int count){
    for (size_t i = 0; i < count; i++) {
        printf("%5.2f, ", buf[i]);
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
