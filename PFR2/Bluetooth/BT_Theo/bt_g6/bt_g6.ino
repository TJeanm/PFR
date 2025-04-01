

void setup() {
  // Pour le debug via USB sur le moniteur série
  Serial.begin(115200);
  // Pour la communication Bluetooth (par exemple via HM-10 connecté sur Serial1)
  Serial1.begin(115200);  // Ajuste ce baudrate selon ton module


  Serial.println("Système démarré. En attente de commandes Bluetooth...");

}
void loop() {
  if (Serial1.available()) {
    // Lecture de la commande jusqu'au saut de ligne
    String commande = Serial1.readStringUntil('\n');
    commande.trim();  // Supprime espaces et retours superflus
    Serial.print("Commande brute reçue : ");
    Serial.println(commande);


    // Si la chaîne commence par "OK+CONN", on la nettoie pour récupérer la commande utile
    if (commande.startsWith("OK+CONN")) {
      commande = commande.substring(7); // Supprime les 7 premiers caractères ("OK+CONN")
    }


    // Pour ignorer une éventuelle réponse "OK+LOST" indiquant une déconnexion
    if (commande.startsWith("OK+LOST")) {
      Serial.println("Déconnexion détectée, commande ignorée");
      return;
    }


    Serial.print("Commande utile après filtrage : ");
    Serial.println(commande);


  }
}

