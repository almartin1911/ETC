#include <elapsedMillis.h>

const unsigned long BAUD_RATE = 9600;
const unsigned int interval = 6000;
const uint8_t command = 0xc2;
const uint8_t header = 0xd1;
const uint8_t header2 = 0xd2;
const uint8_t buffer_size = 31;
uint8_t buffer[buffer_size];
int pckcounter;
uint8_t received_byte;
boolean input_available;
uint8_t pin;
uint8_t data;
uint8_t i;

uint8_t checksum(){
    uint8_t result = 0;
    uint16_t sum = 0;

    for(uint8_t i = 0; i < (buffer_size - 1); i++){
        sum += buffer[i];
    }
    result = sum & 0xFF;

    return result;
}

void build_buffer(uint8_t head) {
    pin = 0;
    i = 1;

    buffer[0] = head;
    while (i < (buffer_size - 1)) {
        if(pin == 16){
            pin = 0;
        }

        data = analogRead(pin);
        buffer[i] = data;

        pin++;
        i++;
    }
    buffer[buffer_size - 1] = checksum();
    pckcounter++;
}

void send_buffer() {
    if(pckcounter < 20){
        build_buffer(header);
    }else{
        build_buffer(header2);
    }
    Serial.write(buffer, buffer_size);
}

void send_response(){
    if(input_available == true){
        if(received_byte == command){            
            elapsedMillis time_elapsed;

            while(time_elapsed < interval){
                send_buffer();
                delay(500);
            }
        input_available = false;
        }
    }
}

void recv_one_byte() {
    if(Serial.available() > 0) {
        received_byte = Serial.read();
        input_available = true;
    }
}

void setup() {
    while(!Serial);
    Serial.begin(BAUD_RATE);
    input_available = false;
    received_byte = 0;
    pin = 0;
    data = 0;
    pckcounter = 0;
}

void loop() {    
    recv_one_byte();
    send_response();    
}
