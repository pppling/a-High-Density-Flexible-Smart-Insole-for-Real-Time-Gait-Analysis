#include<SoftwareSerial.h>
SoftwareSerial BT(10, 11);

int s0 = 2; 
int s1 = 3; 
int s2 = 12; 
int s3 = 13; // 多路复用器开关控制
int h[6] = {4, 5, 6, 7, 8, 9}; // 按列供电
int SIG_pin = 3; // 多路复用器模拟输入引脚
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
  BT.begin(38400); // 设置蓝牙波特率
  Serial.println("BT Already");
}

void loop(){
  aaa = 0;
  BT.println("a"); // 开始信号
  for(int i = 0; i < 6; i ++){
    digitalWrite(h[i], HIGH); // 选中当前列
    for(int j = 0; j < 12; j++){
      pressure[i][j] = readMux(j);
      // 特殊位置清零处理（根据鞋垫形状调整）
      if(i == 0 && j >= 5) pressure[i][j] = 0;
      if(i == 4 && (j == 0 || j == 11)) pressure[i][j] = 0;
      if(i == 5 && (j <= 1 || j >= 7)) pressure[i][j] = 0;
      
      aaa = pressure[i][j];
      BT.println(aaa); // 发送压力值
    }
    digitalWrite(h[i], LOW);
  }
  BT.println("b"); // 结束信号
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