#include <stdio.h>
#include <stdlib.h>
#include <time.h>

void print_uchar_array(u_int8_t *buf, int count);

void fill_with_random(u_int8_t *buf, int count);

void convierte(u_int8_t *in, int tam_in, float *out, int tam_out);

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

    convierte(array_in, tam_array_in, array_out, tam_array_out);
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

void convierte(u_int8_t *in, int tam_in, float *out, int tam_out){
        for (size_t i = 0; i < tam_out; i++) {
            out[i] = in[i] + 0.34;
        }
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
