#include <SoftwareSerial.h>
#include <ESP8266wifi.h>
//#include <HttpClient.h>
//#include <ESP8266HTTPClient.h>
//#include <Bridge.h>


//#define sw_serial_rx_pin 4 //  Connect this pin to TX on the esp8266
//#define sw_serial_tx_pin 6 //  Connect this pin to RX on the esp8266
#define esp8266_reset_pin 255 // Connect this pin to CH_PD on the esp8266, not reset. (let reset be unconnected)
//
//SoftwareSerial swSerial(sw_serial_rx_pin, sw_serial_tx_pin);

// the last parameter sets the local echo option for the ESP8266 module..
ESP8266wifi wifi(Serial3, Serial3, esp8266_reset_pin, Serial);//adding Serial enabled local echo and wifi debug

void processCommand(WifiMessage msg);

void setup() {
//  inputString.reserve(20);
//  swSerial.begin(19200);
  Serial.begin(19200);
  Serial3.begin(19200);
  while (!Serial)
    ;
  Serial.println("Starting wifi");

  wifi.setTransportToTCP();// this is also default
  // wifi.setTransportToUDP();//Will use UDP when connecting to server, default is TCP

  wifi.endSendWithNewline(true); // Will end all transmissions with a newline and carrage return ie println.. default is true

  wifi.begin();

//  pinMode(13, OUTPUT);
//  digitalWrite(13, LOW);
//  Bridge.begin();
//  while(!Serial);


  wifi.connectToAP("LENS-ESE", "LensESE*789");
  wifi.connectToServer("192.168.0.107", "8080");
//  wifi.send(SERVER, "GET /");
}

void sendHTTP(String content) {
    
  String httpHeader;
  String httpRequest;
  
  
  httpHeader = "GET / HTTP/1.1\r\n"; 
//  httpHeader += "Content-Type: text/html; charset=UTF-8\n\r";
  
  httpHeader += "Host: 192.168.0.107\r\n";
//  httpHeader += "Connection: keep-alive\n\r";
//  httpHeader += "Cache-Control: max-age=0\n\r";
//  httpHeader += "Upgrade-Insecure-Requests: 1\n\r";
  httpHeader += "User-Agent: Arduino/1.0\r\n";
//  httpHeader += "User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36\r\n";
//  httpHeader += "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8\n\r";


//  httpHeader = "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=UTF-8\r\n"; 
//  httpHeader += "Content-Length: ";
//  httpHeader += content.length();
//  httpHeader += "\r\n";
  httpHeader +="Connection: close\r\n\r\n";
  
  httpRequest = httpHeader;

  wifi.send(SERVER,httpRequest);
  
}

void loop() {

  String content = "teste";
  sendHTTP(content);

  // See if there is a message
  WifiMessage msg = wifi.getIncomingMessage();
  // Check message is there
  if (msg.hasData) {
    // process the command
    Serial.println(msg.message);
  }
}









