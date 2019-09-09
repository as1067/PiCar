#include <Servo.h>

Servo throttle;
Servo steering;
String input;
int t;
int s;
void setup()
{
  throttle.attach(3);
  steering.attach(5);
  throttle.write(0);
  steering.write(125);
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    input = Serial.readString();
    char mode = input.charAt(0);
    if(mode == 't')
    {
      t = input.substring(1).toInt();
    }
    else if(mode=='s')
    {
      s = input.substring(1).toInt();
    }
    throttle.write(t);
    steering.write(s);
    Serial.println(input);
    delay (10);
  }

}
