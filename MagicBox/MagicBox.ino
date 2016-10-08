#include <Bounce.h>

Bounce button0 = Bounce(3, 10); 
Bounce button1 = Bounce(4, 10); 
Bounce button2 = Bounce(5, 10); 
IntervalTimer sendDataSerialTimer;
IntervalTimer sendButtons;

void setup()
{                
  pinMode(0, INPUT_PULLUP);
  pinMode(1, INPUT_PULLUP);
  pinMode(2, INPUT_PULLUP);
  pinMode(3, INPUT_PULLUP);
  pinMode(4, INPUT_PULLUP);
  pinMode(5, INPUT_PULLUP);
  pinMode(11, INPUT_PULLUP);
  pinMode(12, INPUT_PULLUP);

  Serial.begin(38400);
  sendDataSerialTimer.begin(sendDataSerial, 250000);
}
  int aval0;
  int aval1;
  int dval0;
  int dval1;
  int dval2;
  int dval11;
  int dval12;


void sendDataSerial(){
  Serial.print("A0:");
  Serial.println(aval0);
  
  Serial.print("A1:");
  Serial.println(aval1);

  Serial.print("D0:");
  Serial.println(!dval0);
  
  Serial.print("D1:");
  Serial.println(!dval1);
  
  Serial.print("D2:");
  Serial.println(!dval2);
  
  Serial.print("D11:");
  Serial.println(!dval11);
  
  Serial.print("D12:");
  Serial.println(!dval12);
  
}

void media_buttons(){
  if (button0.risingEdge()) {
    Keyboard.press(KEY_MEDIA_NEXT_TRACK);
    Keyboard.release(KEY_MEDIA_NEXT_TRACK);
  }
  if (button1.risingEdge()) {
    Keyboard.press(KEY_MEDIA_PLAY_PAUSE);
    Keyboard.release(KEY_MEDIA_PLAY_PAUSE);
  }
  if (button2.risingEdge()) {
    Keyboard.press(KEY_MEDIA_PREV_TRACK);
    Keyboard.release(KEY_MEDIA_PREV_TRACK);
  }
}

void sendKeyStrokes(){
  Serial.print("B0:");
  Serial.println(!digitalRead(3));
  Serial.print("B1:");
  Serial.println(!digitalRead(4));
  Serial.print("B2:");
  Serial.println(!digitalRead(5));
  
}

void updateData(){
  button0.update();
  button1.update();
  button2.update();
  aval0 = analogRead(0);
  aval1 = analogRead(1);
  dval0 = digitalRead(0);
  dval1 = digitalRead(1);
  dval2 = digitalRead(2);
  dval11 = digitalRead(11);
  dval12 = digitalRead(12);  
}

bool sending_buttons = false;
void loop()                     
{
  updateData();
  if (dval11){
    media_buttons();
    if (sending_buttons){
      sending_buttons = false;
      sendButtons.end();
    }
  } else {
    if (!sending_buttons){
      sending_buttons = true;
      sendButtons.begin(sendKeyStrokes, 250000);
    }
  }
}

