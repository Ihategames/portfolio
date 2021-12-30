// master 3
#include <Wire.h>
#define RAIL 1
#define LED 2

void setup() {
  Wire.begin();
  Serial.begin(9600);

}

void loop() {

  while(Serial.available()){

    int master_input = Serial.parseInt();
    Serial.println(master_input);

    if (2<master_input && 33>master_input){
      
    Wire.beginTransmission(RAIL);
    Wire.write(master_input);
    Wire.endTransmission(RAIL);
    delay(100);
    Serial.println("레일 신호 전송");

      if ( master_input <= 6 ){
        Wire.beginTransmission(LED);
        Wire.write(5);
        Wire.endTransmission();
        delay(100);
        Serial.println("LED 5번신호");
      }
      
      else if ( 6 < master_input and master_input <= 15){
        Wire.beginTransmission(LED);
        Wire.write(6);
        Wire.endTransmission();
        delay(100);
        Serial.println("LED 중간왼쪽신호");
      }

      else if ( 15 < master_input and master_input <= 30){
        Wire.beginTransmission(LED);
        Wire.write(7);
        Wire.endTransmission();
        delay(100);
        Serial.println("LED 중간오른쪽신호");
      }

      else if (master_input > 30){
        Wire.beginTransmission(LED);
        Wire.write(8);
        Wire.endTransmission();
        delay(100);
        Serial.println("LED 8번 신호");
      }

    }

    else{
      Serial.println("거리범위를 벗어남");
    }

   


    
  }

}
