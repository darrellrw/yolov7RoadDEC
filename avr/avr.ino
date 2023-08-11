#include <WiFi.h>
#include <TinyGPS++.h>
#include <ESPAsyncWebServer.h>

#define ss Serial1

TinyGPSPlus gps;
AsyncWebServer server(80);

IPAddress ipStatic(10, 160, 116, 69); //IP bergantung pada gateway dan subnet
IPAddress gateway(10, 160, 116, 1);
IPAddress subnet(255, 255, 252, 0);

const char* ssid = "ITK-LAB.X"; //ssid harap diganti
const char* password = "K@mpusM3rdeka!"; //password harap diganti

String gpsLat() {
  if (gps.location.isValid()) {
    return String(gps.location.lat(), 6);
  }
  else {
    return String("Invalid");
  }
}

String gpsLng() {
  if (gps.location.isValid()) {
    return String(gps.location.lng(), 6);
  }
  else {
    return String("Invalid");
  }
}

String gpsDate() {
  if (gps.date.isValid()) {
    int day = gps.date.day();
    int month = gps.date.month();
    return String((day < 10 ? "0" + String(day) : String(day)) + "/" + (month < 10 ? "0" + String(month) : String(month)) + "/" + String(gps.date.year()));
  }
  else {
    return String("Invalid");
  }
}

String gpsTime() {
  if (gps.time.isValid()) {
    int hour = gps.time.hour();

    hour = hour + 8;
    if (hour >= 24 ) {
      hour = hour - 24;
    }

    int minute = gps.time.minute();
    int second = gps.time.second();
    return String((hour < 10 ? "0" + String(hour) : String(hour)) + ":" + (minute < 10 ? "0" + String(minute) : String(minute)) + ":" + (second < 10 ? "0" + String(second) : String(second)));
  }
  else {
    return String("Invalid");
  }
}

void setup() {
  Serial.begin(115200);

  ss.begin(9600, SERIAL_8N1, 17, 16);

  if (!WiFi.config(ipStatic, gateway, subnet)) {
    Serial.println("STA Failed to configure");
  }

  Serial.print("Connecting to ");
  Serial.print(ssid);

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected.");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  server.on("/gps/lat", HTTP_GET, [](AsyncWebServerRequest *request){
    request->send_P(200, "text/plain", gpsLat().c_str());
  });

  server.on("/gps/lng", HTTP_GET, [](AsyncWebServerRequest *request){
    request->send_P(200, "text/plain", gpsLng().c_str());
  });

  server.on("/gps/date", HTTP_GET, [](AsyncWebServerRequest *request){
    request->send_P(200, "text/plain", gpsDate().c_str());
  });

  server.on("/gps/time", HTTP_GET, [](AsyncWebServerRequest *request){
    request->send_P(200, "text/plain", gpsTime().c_str());
  });

  server.begin();

  delay(100);
}

void loop() {
  while (ss.available() > 0) {
    if (gps.encode(ss.read())) {
      displayInfo();
    }
  }
  if (millis() > 5000 && gps.charsProcessed() < 10) {
    Serial.println(F("No GPS detected: check wiring."));
    while (true);
  }
}

void displayInfo() { // Date Time Latitude Longitude
  Serial.print(F("Date: "));
  if (gps.date.isValid()) {
    int day = gps.date.day();
    int month = gps.date.month();

    Serial.print(day < 10 ? "0" + String(day) : String(day));
    Serial.print(F("/"));
    Serial.print(month < 10 ? "0" + String(month) : String(month));
    Serial.print(F("/"));
    Serial.print(gps.date.year());
    Serial.print(F(" "));
  }
  else {
    Serial.println(F("INVALID"));
  }

  Serial.print(F("Time: "));
  if (gps.time.isValid()) {
    int hour = gps.time.hour();

    hour = hour + 8;
    if (hour >= 24 ) {
      hour = hour - 24;
    }

    int minute = gps.time.minute();
    int second = gps.time.second();

    Serial.print(hour < 10 ? "0" + String(hour) : String(hour));
    Serial.print(F(":"));
    Serial.print(minute < 10 ? "0" + String(minute) : String(minute));
    Serial.print(F(":"));
    Serial.print(second < 10 ? "0" + String(second) : String(second));
    Serial.print(F(" "));
  }
  else {
    Serial.println(F("INVALID"));
  }

  Serial.print(F("Location: "));
  if (gps.location.isValid()) {
    Serial.print("Lat: ");
    Serial.print(gps.location.lat(), 6);
    Serial.print(F(", "));
    Serial.print("Lng: ");
    Serial.print(gps.location.lng(), 6);
    Serial.println("");
  }
  else {
    Serial.println(F("INVALID"));
  }
}