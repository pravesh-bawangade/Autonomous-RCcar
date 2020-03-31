#include<SoftwareSerial.h>
#define IN1 12
#define IN2 11
#define IN3 10
#define IN4 9

SoftwareSerial mySerial(2, 3); // RX, TX
String data;
int blData;
void setup() 
{  

    pinMode(IN1, OUTPUT);
    pinMode(IN2, OUTPUT);
    pinMode(IN3, OUTPUT);
    pinMode(IN4, OUTPUT);
    
    digitalWrite(IN1, LOW);
    digitalWrite(IN2, LOW);
    digitalWrite(IN3, LOW);
    digitalWrite(IN4, LOW);
    
    mySerial.begin(115200);
}
void loop()
{
    while (mySerial.available()){  
       
        data = mySerial.readStringUntil('\n');
        blData = (data.toInt());
  
        switch (blData) 
           {
              case 1:                                
                forward();
                break;
              case 2:                 
                reverse();
                break;
              case 3:         
                right();
                break;
              case 4:                     
                left();
                break;
              case 0:                     
                stop();
                break;      
          }
     } 
}
void forward()
{
digitalWrite(IN1, HIGH);
digitalWrite(IN2, LOW);
digitalWrite(IN3, HIGH);
digitalWrite(IN4, LOW);
}
void reverse()
{
digitalWrite(IN1, LOW);
digitalWrite(IN2, HIGH);
digitalWrite(IN3, LOW);
digitalWrite(IN4, HIGH);
}
void left()
{
digitalWrite(IN1, LOW);
digitalWrite(IN2, LOW);
digitalWrite(IN3, HIGH);
digitalWrite(IN4, LOW);
}
void right()
{
digitalWrite(IN1, HIGH);
digitalWrite(IN2, LOW);
digitalWrite(IN3, LOW);
digitalWrite(IN4, LOW);
}
void stop()
{
digitalWrite(IN1, LOW);
digitalWrite(IN2, LOW);
digitalWrite(IN3, LOW);
digitalWrite(IN4, LOW);
}
