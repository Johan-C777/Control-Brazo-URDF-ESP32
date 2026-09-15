// Cambiamos el pin dañado por uno nuevo (ej. 35)
#define POT_BASE 35  
#define POT_BRAZO 33
#define POT_PINZA 34

void setup() {
  Serial.begin(115200);
  analogReadResolution(12); 
}

void loop() {
  int valBase = analogRead(POT_BASE);
  int valBrazo = analogRead(POT_BRAZO);
  int valPinza = analogRead(POT_PINZA);

  Serial.print(valBase);
  Serial.print(",");
  Serial.print(valBrazo);
  Serial.print(",");
  Serial.println(valPinza);

  delay(50); 
}