#include "DHT.h"
#include "timer.h"
#include "timerManager.h"
#include "MathBox.h"
#include "OneWire.h"
#include "DallasTemperature.h"
#include <SoftwareSerial.h>
#include <ESP8266wifi.h>

// Pins
#define esp8266_reset_pin 255
const byte LDR_PIN = 4;
const byte DHT_PIN = 5;

// DHT sensor
DHT dht(DHT_PIN, DHT11);

// Wifi module
ESP8266wifi wifi(Serial3, Serial3, esp8266_reset_pin, Serial);

// Wifi config
String SSID = "LENS-ESE";
String PWD = "LensESE*789";
String SERVER_IP = "52.67.192.182";
String SERVER_PORT = "8080";

// Timers
Timer ldr_timer;
Timer dht_timer;
Timer temp_timer;
Timer send_timer;

// Temperature Sensors
#define ONE_WIRE_BUS 3
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);
DeviceAddress sensor1, sensor2;

// Intervals [ms]
unsigned int ldr_interval = 3000;
unsigned int dht_interval = 5000;
unsigned int temp_interval = 5000;
unsigned int send_interval = 15000;

// Signal processing
MathBox ldr_signal;
MathBox temperature_signal;
MathBox humidity_signal;
MathBox heat_index_signal;
MathBox machine1_temperature_signal;
MathBox machine2_temperature_signal;

// Print functions
void printLDR(byte ldr)
{
  Serial.print("LDR: ");
  Serial.println(ldr);
  Serial.println("");
}

void printDHT(float humidity, float temperature, float heat_index)
{
  Serial.print("Humidity: ");
  Serial.print(humidity);
  Serial.println(" %");
  Serial.print("Temperature: ");
  Serial.print(temperature);
  Serial.println(" *C ");
  Serial.print("Heat index: ");
  Serial.print(heat_index);
  Serial.println(" *C ");
  Serial.println("");
}

void printTemp(int id, float temperature)
{
  Serial.print("Temperature ");
  Serial.print(id);
  Serial.print(": ");
  Serial.print(temperature);
  Serial.println(" *C");
  Serial.println("");
}

// Callbacks
void readLDR()
{
  Serial.println("==== LDR ====");
  byte ldr = !digitalRead(LDR_PIN);

  ldr_signal.add(ldr);

  printLDR(ldr);
}

void readDHT()
{
  Serial.println("==== DHT ====");
  float humidity = dht.readHumidity();                                   // [percentage]
  float temperature = dht.readTemperature();                             // [Celsius]
  float heat_index = dht.computeHeatIndex(humidity, temperature, false); // [Celsius]

  if (isnan(humidity) || isnan(temperature) || isnan(heat_index))
  {
    Serial.println("Failed toESP8266wifi wifi(Serial3, Serial3, esp8266_reset_pin, Serial); read from DHT sensor!");
    Serial.println("");
    return;
  }

  humidity_signal.add(humidity);
  temperature_signal.add(temperature);
  heat_index_signal.add(heat_index);

  printDHT(humidity, temperature, heat_index);
}

void readTemp()
{
  Serial.println("==== TEMP ====");
  sensors.requestTemperatures();
  float tempC1 = sensors.getTempC(sensor1);
  float tempC2 = sensors.getTempC(sensor2);
  machine1_temperature_signal.add(tempC1);
  machine2_temperature_signal.add(tempC2);
  printTemp(1, tempC1);
  printTemp(2, tempC2);
}

void send()
{
  Serial.println("==== Send ====");

  // TODO: Send the message to the server


  // printLDR(ldr_signal.getAverage());
  // printDHT(
  //     humidity_signal.getAverage(),
  //     temperature_signal.getAverage(),
  //     heat_index_signal.getAverage());
  // printTemp(1, machine1_temperature_signal.getAverage());
  // printTemp(2, machine2_temperature_signal.getAverage());

  String content;
  content += "{\"MAC\":\"AB:BB:CC:DD:EE\",\"lab_id\":1,\"dados\":{\"luz\":";
  content += ldr_signal.getAverage();
  content += ",\"umidade\":";
  content += humidity_signal.getAverage();
  content += ",\"sensacao_termica\":";
  content += temperature_signal.getAverage();
  content += ",\"equipamentos\":[";
  content += machine1_temperature_signal.getAverage();
  content += ",";
  content += machine2_temperature_signal.getAverage();
  content += "]}}";

  Serial.println(content);

  sendHTTP(content);
  // See if there is a message
  WifiMessage msg = wifi.getIncomingMessage();
  // Check message is there
  if (msg.hasData) {
    // process the command
    Serial.println("-------RESPOSTA-------");
    Serial.println(msg.message);
  }

  ldr_signal.clear();
  humidity_signal.clear();
  temperature_signal.clear();
  heat_index_signal.clear();
  machine1_temperature_signal.clear();
  machine2_temperature_signal.clear();
}

void sendHTTP(String content) {
  String httpHeader;
  String httpRequest;

  httpHeader = "POST /arduino HTTP/1.1\r\n";
  httpHeader += "Host: 52.67.192.182\r\n";
  httpHeader += "User-Agent: Arduino/1.0\r\n";
  httpHeader += "Content-Type: application/json\r\n";
  httpHeader += "Content-Length: ";
  httpHeader += content.length();
  httpHeader += "\r\n";
  httpHeader +="Connection: close\r\n\r\n";

  httpRequest = httpHeader + content;

  Serial.println(httpRequest);
  wifi.send(SERVER,httpRequest);
}

void setup()
{
  Serial.begin(19200);
  Serial3.begin(19200);
  while (!Serial)
    ;

  // Wifi setup
  Serial.println("Starting wifi");
  wifi.setTransportToTCP();
  wifi.endSendWithNewline(true);
  wifi.begin();
  wifi.connectToAP(SSID, PWD);
  wifi.connectToServer(SERVER_IP, SERVER_PORT);

  // LDR setup
  pinMode(LDR_PIN, INPUT);

  // DHT setup
  dht.begin();

  // Timer setup
  ldr_timer.setInterval(ldr_interval);
  dht_timer.setInterval(dht_interval);
  temp_timer.setInterval(temp_interval);
  send_timer.setInterval(send_interval);

  ldr_timer.setCallback(readLDR);
  dht_timer.setCallback(readDHT);
  temp_timer.setCallback(readTemp);
  send_timer.setCallback(send);

  //Temperature sensors setup
  sensors.begin();
  sensors.getAddress(sensor1, 0);
  sensors.getAddress(sensor2, 1);

  TimerManager::instance().start();
}

void loop()
{
  TimerManager::instance().update();
}
