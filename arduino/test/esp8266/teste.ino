// Programa: Versao firmware modulo Serial3 e
//           mudanca de baud rate
// Autor : FILIPEFLOP
 
#include <SoftwareSerial.h>
 
//RX pino 2, TX pino 3
//SoftwareSerial Serial3(2, 3);

//SoftwareSerial Serial3(2, 3);
 
#define DEBUG true

void setup()
{
  Serial.begin(19200);
  // Configure na linha abaixo a velocidade inicial do
  // modulo Serial3
  Serial3.begin(19200);
//  sendData("AT", 2000, DEBUG);
//  delay(1000);
  sendData("AT+RST\r\n", 5000, DEBUG);
  delay(1000);
//  sendData("AT+CIOBAUD=9600\r\n", 5000, DEBUG);
//  delay(1000);

  Serial.println("Versao de firmware");
  delay(3000);
  sendData("AT+GMR\r\n", 5000, DEBUG); // rst
  // Configure na linha abaixo a velocidade desejada para a
  // comunicacao do modulo Serial3 (9600, 19200, 38400, etc)
//  sendData("AT+CIOBAUD=19200\r\n", 2000, DEBUG);
  Serial.println("** Final **");
}
 
void loop() {}
 
String sendData(String command, const int timeout, boolean debug)
{
  // Envio dos comandos AT para o modulo
  String response = "";
  Serial3.print(command);
  long int time = millis();
  while ( (time + timeout) > millis())
  {
    while (Serial3.available())
    {
      // The esp has data so display its output to the serial window
      char c = Serial3.read(); // read the next character.
      response += c;
    }
  }
  if (debug)
  {
    Serial.print(response);
  }
  return response;
}
