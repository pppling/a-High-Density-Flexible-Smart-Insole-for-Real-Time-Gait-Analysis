#include<SoftwareSerial.h>
SoftwareSerial BT(10, 11);

int s0 = 2; 
int s1 = 3; 
int s2 = 12; 
int s3 = 13; // Multiplexer switch control
int h[6] = {4, 5, 6, 7, 8, 9}; // Power supply by column
int SIG_pin = 3; // Multiplexer analog input pin
int aaa;
int x;
int pressure[6][12];

void setup(){
  pinMode(s0, OUTPUT);
  pinMode(s1, OUTPUT);
  pinMode(s2, OUTPUT);
  pinMode(s3, OUTPUT);
  for(int i=0; i<6; i++) {
    pinMode(h[i], OUTPUT);
    digitalWrite(h[i], LOW);
  }
  digitalWrite(s0, LOW);
  digitalWrite(s1, LOW);
  digitalWrite(s2, LOW);
  digitalWrite(s3, LOW);
  
  Serial.begin(9600);
  BT.begin(38400); // Set Bluetooth baud rate
  Serial.println("BT Already");
}

void loop(){
  aaa = 0;
  BT.println("a"); // Start signal
  for(int i = 0; i < 6; i ++){
    digitalWrite(h[i], HIGH); // Select current column
    for(int j = 0; j < 12; j++){
      pressure[i][j] = readMux(j);
      // Special position reset (adjust according to insole shape)
      if(i == 0 && j >= 5) pressure[i][j] = 0;
      if(i == 4 && (j == 0 || j == 11)) pressure[i][j] = 0;
      if(i == 5 && (j <= 1 || j >= 7)) pressure[i][j] = 0;
      
      aaa = pressure[i][j];
      BT.println(aaa); // Send pressure value
    }
    digitalWrite(h[i], LOW);
  }
  BT.println("b"); // End signal
}

int readMux(int channel){
  int controlPin[] = {s0, s1, s2, s3};
  int muxChannel[12][4]={
    {0,0,0,0}, {1,0,0,0}, {0,1,0,0}, {1,1,0,0},
    {0,0,1,0}, {1,0,1,0}, {0,1,1,0}, {1,1,1,0},
    {0,0,0,1}, {1,0,0,1}, {0,1,0,1}, {1,1,0,1}
  };
  for(int i = 0; i < 4; i ++){
    digitalWrite(controlPin[i], muxChannel[channel][i]);
  }
  return analogRead(SIG_pin);
}