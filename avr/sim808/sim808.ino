#include <DFRobot_SIM808.h>
#include <SoftwareSerial.h>

#define PIN_TX 10
#define PIN_RX 11
#define button 4
SoftwareSerial mySerial(PIN_TX,PIN_RX);
DFRobot_SIM808 sim808(&mySerial); //Connect RX,TX,PWR

void setup() {
  mySerial.begin(9600);
  Serial.begin(9600);

  pinMode(button, INPUT);
}

void getGPS();

void loop() {
  getGPS();
  delay(1);
}

void getGPS() {
  while(!sim808.attachGPS()) {
    Serial.println("Dead");
  }
  while(!sim808.getGPS()) {

  }
  Serial.print(getDate());
  Serial.print(" ");
  Serial.print(getTime());
  Serial.print(" ");
  Serial.print(sim808.GPSdata.lat, 6);
  Serial.print(" ");
  Serial.println(sim808.GPSdata.lon, 6);
}

String getDate() {
  int day = sim808.GPSdata.day;
  int month = sim808.GPSdata.month;
  int year = sim808.GPSdata.year;
  return String((day < 10 ? "0" + String(day) : String(day)) + "/" + (month < 10 ? "0" + String(month) : String(month)) + "/" + String(year));
}

String getTime() {
  int hour = sim808.GPSdata.hour;
  int minute = sim808.GPSdata.minute;
  int second = sim808.GPSdata.second;

  if (hour >= 24 ) {
    hour = hour - 24;
  }
  return String((hour < 10 ? "0" + String(hour) : String(hour)) + ":" + (minute < 10 ? "0" + String(minute) : String(minute)) + ":" + (second < 10 ? "0" + String(second) : String(second)));
}