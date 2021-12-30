int k=3;
void setup() {
  Serial.begin(9600); 
  pinMode(2, OUTPUT); //2번이 모니터, 3번이 컴퓨터, 4번이 선풍기
  pinMode(3, OUTPUT);
  pinMode(4, OUTPUT);
  

  }


void loop() {

  
 int bed = analogRead(A0);
 int chair = analogRead(A1);
 int sumc = 0;
 int sumb = 0;
 int avec = 0;
 int aveb = 0;
 int i;

  if (Serial.available())
  { 
    k=Serial.read();
  }

if (k==1){
  for (i=0;i<100;i++){
    sumc = sumc + chair;
    sumb = sumb + bed;
    delay(10);
  }
    avec = sumc/100;
    aveb = sumb/100;
    Serial.println(" Cvalue : "+String(avec)+" Bvalue : "+String(aveb));

  if (avec < 100)
  {
   if (aveb > 100){
    digitalWrite(2, LOW);
    digitalWrite(3, HIGH);
    digitalWrite(4, HIGH);
   }
   if (aveb < 100){
    digitalWrite(2, LOW);
    digitalWrite(3, HIGH);
    digitalWrite(4, LOW);
   }
  }
 else  {
  digitalWrite(2, HIGH);
  digitalWrite(3, HIGH);
  digitalWrite(4, HIGH);
}
 
 
delay(50);
  }

else if (k==0){
Serial.println("connection error");
  digitalWrite(2, HIGH);
  digitalWrite(3, HIGH);
  digitalWrite(4, HIGH);
}

else if (k==2)
{
  digitalWrite(2, HIGH);
  digitalWrite(3, LOW);
  digitalWrite(4, LOW);
}

else if (k==3)
{
  digitalWrite(2, LOW);
  digitalWrite(3, HIGH);
  digitalWrite(4, LOW);
}

else if (k==4)
{
  digitalWrite(2, LOW);
  digitalWrite(3, LOW);
  digitalWrite(4, HIGH);
}

 else {
  Serial.println("error");
}
}
