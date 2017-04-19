const int sensor_ldr = 50;     // pino de leitura digital do sensor
 
void setup() {
  // define o pino relativo ao sensor como entrada digital
  pinMode(sensor_ldr, INPUT);
}
 
void loop() {
  // lê o estado do sensor e armazena na variavel leitura
  int leitura = digitalRead(sensor_ldr);

  //a leitura pode ser LOW ou HIGH

  //LOW = pouca luz
  //HIGH = muita luz

  //o limiar entre "pouca e muita" é ajustável pelo potenciômetro no sensor

  //temos que definir o limiar
 
  
}
