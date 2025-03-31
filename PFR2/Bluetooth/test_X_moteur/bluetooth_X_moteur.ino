#include <SoftwareSerial.h>

#define borneENA        10      // On associe la borne "ENA" du L298N à la pin D10 de l'arduino
#define borneIN1        9       // On associe la borne "IN1" du L298N à la pin D9 de l'arduino
#define borneIN2        8       // On associe la borne "IN2" du L298N à la pin D8 de l'arduino
#define borneIN3        7       // On associe la borne "IN3" du L298N à la pin D7 de l'arduino
#define borneIN4        6       // On associe la borne "IN4" du L298N à la pin D6 de l'arduino
#define borneENB        5       // On associe la borne "ENB" du L298N à la pin D5 de l'arduino

SoftwareSerial HM10(2, 3); // RX, TX
int NB_DONNEE_RECU = 10;
int NB_DONNEE_BOUTONS = 4;
int NB_DONNEE_JOYSTICKS = 6;
bool VALBOUTONS[4] ; //valBoutons
float VALJOYSTICKS[6];

void setup() {
  // Configuration de toutes les pins de l'Arduino en "sortie" (car elles attaquent les entrées du module L298N)
  pinMode(borneENA, OUTPUT);
  pinMode(borneIN1, OUTPUT);
  pinMode(borneIN2, OUTPUT);
  pinMode(borneIN3, OUTPUT);
  pinMode(borneIN4, OUTPUT);
  pinMode(borneENB, OUTPUT);

  Serial.begin(115200);  // Moniteur série
  HM10.begin(115200);    // Bluetooth HM-10
  for (int i = 0; i < NB_DONNEE_BOUTONS; i++) {
    VALBOUTONS[i] = false;
  }
  for (int i = 0; i < NB_DONNEE_JOYSTICKS; i++) {
    VALJOYSTICKS[i] = 0.00;
  }

  Serial.println("Initialisation terminée !");
}

void loop() {
  String received = readCompleteMessage(); // Lit le message complet

  if (received.length() > 0 && received != "OK+CONN" && received != "OK+LOST") {  // Si on a bien reçu quelque chose
    received = received.substring(7); // Supprime le début : "OK+CONN"
    Serial.print("Message complet reçu : ");
    Serial.println(received.length());
    Serial.println(received);
    
    // Traitement de la donnée reçu
    recuperationChaine(received);
  
    // Réponse longue (simule une vraie réponse)
    String response = received + " AAAAA batard woula";
    
    sendChunked(response, 36); // Envoie la rÃ©ponse en morceaux de 32 caractères
  }
  action();
}

void action(){
//TODO
}

//************************************************************************************//
// Fonction : BLUETOOTH()                                             //
// But :      Active l'alimentation du moteur branché sur le pont A                   //
//            pendant 2 secondes, puis le met à l'arrêt (au moins 1 seconde)          //
//************************************************************************************//

// Fonction pour lire un message entier avant de répondre
String readCompleteMessage() {
  String message = "";
  unsigned long startTime = millis(); // Temps de départ

  while (millis() - startTime < 2000) { // Timeout de 1 seconde
    while (HM10.available()) {
      char c = HM10.read();
      message += c;
      startTime = millis(); // Reset le timeout Ã  chaque caractère reçu
    }
  }

  message.trim(); // Nettoie les espaces et retours Ã  la ligne
  return message;
}

// Fonction pour envoyer des trames découpées
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

// Récupération des valeurs string en tableau pas string
void recuperationChaine(String chaine){
  String tabString[NB_DONNEE_RECU];
  int debutMOT = 0;
  int index = 0;
  // Séparation de la chaîne à chaque virgule
  for (int i = 0; i < chaine.length(); i++) {
    if (chaine.charAt(i) == ',') {
      tabString[index] = chaine.substring(debutMOT, i);
      debutMOT = i + 1;
      index++;
    }
  }
  // Ajout de la dernière valeur
  tabString[index] = chaine.substring(debutMOT);

  //Récupération des valeurs des boutons
  for (int i = 0; i < NB_DONNEE_BOUTONS; i++) {
    VALBOUTONS[i] = (tabString[i].toInt() == 1);  // Convertit en booléen
  }
  //Récupération des valeurs des joysticks
  for (int i = NB_DONNEE_JOYSTICKS; i < 10; i++) {
    VALJOYSTICKS[i - NB_DONNEE_BOUTONS] = tabString[i].toFloat();  // Convertit en float
  }
  /*
  // Affichage des résultats pour vérifier
  Serial.println("Tableau de booléens:");
  for (int i = 0; i < NB_DONNEE_BOUTONS; i++) {
    Serial.print(VALBOUTONS[i]);
    Serial.print("  ");
  }
  Serial.println();
  Serial.println("Tableau de floats:");
  for (int i = 0; i < NB_DONNEE_JOYSTICKS; i++) {
    Serial.print(VALJOYSTICKS[i]);
    Serial.print("  ");
  }
  Serial.println();
  */
}


