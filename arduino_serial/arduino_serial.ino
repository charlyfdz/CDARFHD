int led = 8;
char data;
void setup() {
  Serial.begin(9600);
  pinMode(led,OUTPUT);
}
void loop() {
  //digitalWrite(led,HIGH);
  //digitalWrite(led,LOW);  
  if(Serial.available() > 0) {
    data = Serial.read();
  }
  char str[0];
  str[0]=data;
  if(str[0]=='1'){
    Serial.print("1");
    digitalWrite(led,HIGH);
    delay(10);
  }
  else if(str[0]=='0'){
    Serial.print("0");
    digitalWrite(led,LOW);
    delay(10);
  }
  else{
    Serial.print("??????");
  }
  delay(100);
}
