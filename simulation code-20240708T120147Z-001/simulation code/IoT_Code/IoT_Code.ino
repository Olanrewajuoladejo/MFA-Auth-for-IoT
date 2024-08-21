#include <TimerOne.h>
#include <LiquidCrystal.h>

LiquidCrystal lcd(13, 12, 11, 10, 9, 8);

int HBSensor = A0; // Sensor Pin
int TempSensor = A1; // Temp Sensor Pin
int HBCount = 0;
int HBCheck = 0;
int TimeinSec = 0;
int HBperMin = 0;

void setup()
{
  pinMode(HBSensor, INPUT);
  pinMode(TempSensor, INPUT);
  Timer1.initialize(1000000); // 1 second
  Timer1.attachInterrupt(timerIsr);
  
  lcd.begin(20, 4); // set up the LCD's number of columns and rows:
  lcd.clear();
  lcd.setCursor(0,0); // set the cursor position:
  lcd.print("MFA IN IoT HEALTHCARE");
  lcd.setCursor(0,1);
  lcd.print("Temp: ");
  lcd.setCursor(0,2);
  lcd.print("HB: ");

  Serial.begin(9600); // Initialize serial communication at 9600 bits per second
}

void loop() 
{
  if((digitalRead(HBSensor) == HIGH) && (HBCheck == 0))
  {
    HBCount = HBCount + 1;
    HBCheck = 1;
  }
  
  if((digitalRead(HBSensor) == LOW) && (HBCheck == 1))
  {
    HBCheck = 0;   
  }
}

void timerIsr()
{
  TimeinSec++;
  double Temperature = ((5.0/1024.0) * analogRead(TempSensor)) * 100;  //10mV per degree 0.01V/C. Scalling
  lcd.setCursor(6,1);
  lcd.print(Temperature);
  
  // Blinking "SC" indicator
  if(TimeinSec <= 3)
  {
    lcd.setCursor(1,3);
    lcd.print("SCANNING");
  }
  else
  {
    lcd.setCursor(1,3);
    lcd.print("     "); // Clear the "SCANNING" message
  }
  
  if(TimeinSec == 2)
  {
    HBperMin = HBCount * 60; // assuming 20 beats per minute per count
    lcd.setCursor(4,2);
    lcd.print(HBperMin);
    lcd.print("  ");
    
    // Send data via serial port
    Serial.print("Temperature: ");
    Serial.print(Temperature);
    Serial.print(" C, ");
    Serial.print("Heart Beat: ");
    Serial.print(HBperMin);
    Serial.println(" BPM");
    
    HBCount = 0;
    TimeinSec = 0;
  }
}
