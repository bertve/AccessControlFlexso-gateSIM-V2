#include <LiquidCrystal.h>
#include <Servo.h> 
#include <string.h>
#include <stdio.h>


Servo myservo;
LiquidCrystal lcd(7, 8, 9, 10, 11 , 12);
int rows = 2;
int cols = 16;
int pos = 90;    // variable to store the servo position 
String address = "";

void setup() {
  Serial.begin(9600);  
  Serial.println("ARDUINO SERIAL CONNECTION SUCCES");
  lcd.begin(cols, rows);
  myservo.attach(13);  // attaches the servo on pin 13 to the servo object 
  myservo.write(pos);
}


void loop() {
  if (Serial.available()){
      String incoming = Serial.readStringUntil("\n");
      incoming.trim();
      handle_incoming_message(incoming);
  }else{
    address_scroll(450);
  }
 }

 void handle_incoming_message(String message){
  int delim = message.indexOf(";");
  display_centered(message);
  String command = message.substring(0,delim);
  String para = message.substring(delim+1);

  if (command == "ADDRESS" ){
    address = para;
  }else{
    if(command == "SERVO"){
      handle_servo(para);
    }else{
      if (command == "PRINT"){
        travel_message_over_lcd(para,750);
      }
    }
  }
  print_address();

  
 }

 void print_address(){
    lcd.clear();
    lcd.setCursor(0,0);
    lcd.print(address);
    if (address.length() > cols){
      address_scroll(500);
    }
  
  }

 void address_scroll(int interval){
      int diff = address.length() - cols;
      for (int i=0; i< diff;i++){
        lcd.scrollDisplayLeft();
        delay(interval);
      }     
      for (int i=0; i< diff;i++){
        lcd.scrollDisplayRight();
        delay(interval);
      }

 }
 
 void handle_servo(String servo_command){
    if(servo_command == "OPEN"){
      open_door();
    }else{
      close_door();
    }
  }

 void open_door(){
    myservo.write(180);
    display_centered("OPEN");
    delay(1000);
 }

 void close_door(){
    myservo.write(90);
    display_centered("CLOSED");
    delay(1000);
 }

 
 void display_centered(String message){
    lcd.clear();
    int message_length = message.length();
    int start = (cols - message_length)/2;
    lcd.setCursor(start,0);
    lcd.print(message);

 }
 
 
 void travel_message_over_lcd(String message,int interval){
  lcd.clear();
  int message_length = message.length();
  int mod = cols / message_length;
  int col = 0;
  int row = 0;
  
  for (int i=0; i<mod*rows; i++){
    if(i<mod){
     col= i*message_length;
     row= 0;
    }else{
     col = i*message_length - cols;
     row= 1;
    }
    
    lcd.setCursor(col,row);
    lcd.print(message);
    delay(interval);
    lcd.clear();

  } 

 }
