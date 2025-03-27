#include <SoftwareSerial.h>

SoftwareSerial HM10(2, 3); // RX, TX

void setup() {
  Serial.begin(115200);  // Moniteur sÃ©rie
  HM10.begin(115200);    // Bluetooth HM-10
  Serial.println("Initialisation terminée !");
}

void loop() {
  String received = readCompleteMessage(); // Lit le message complet

  if (received.length() > 0 && received != "OK+CONN" && received != "OK+LOST") {  // Si on a bien reÃ§u quelque chose
    received = received.substring(7); // Supprime le début : "OK+CONN"
    Serial.print("Message complet reçu : ");
    Serial.println(received);
    
    // RÃ©ponse longue (simule une vraie rÃ©ponse)
    String response = received + " AAAAA batard woula";
    
    sendChunked(response, 36); // Envoie la rÃ©ponse en morceaux de 32 caractÃ¨res
  }
}

// Fonction pour lire un message entier avant de rÃ©pondre
String readCompleteMessage() {
  String message = "";
  unsigned long startTime = millis(); // Temps de dÃ©part

  while (millis() - startTime < 750) { // Timeout de 1 seconde
    while (HM10.available()) {
      char c = HM10.read();
      message += c;
      startTime = millis(); // Reset le timeout Ã  chaque caractÃ¨re reÃ§u
    }
  }

  message.trim(); // Nettoie les espaces et retours Ã  la ligne
  return message;
}

// Fonction pour envoyer des trames dÃ©coupÃ©es
void sendChunked(String message, int chunkSize) {
  for (int i = 0; i < message.length(); i += chunkSize) {
    String chunk = message.substring(i, i + chunkSize);
    HM10.print(chunk);  
    Serial.print("Envoi : ");
    Serial.println(chunk);
    delay(250);
  }
  
  HM10.println();  // Fin du message
  Serial.println("Fin de l'envoi !");
}