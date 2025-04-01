#include <SoftwareSerial.h>

#define borneENA        10      // On associe la borne "ENA" du L298N à la pin D10 de l'arduino
#define borneIN1        9       // On associe la borne "IN1" du L298N à la pin D9 de l'arduino
#define borneIN2        8       // On associe la borne "IN2" du L298N à la pin D8 de l'arduino
#define borneIN3        7       // On associe la borne "IN3" du L298N à la pin D7 de l'arduino
#define borneIN4        6       // On associe la borne "IN4" du L298N à la pin D6 de l'arduino
#define borneENB        5       // On associe la borne "ENB" du L298N à la pin D5 de l'arduino
// Définition des broches pour les capteurs ultrasons
#define FRONT_TRIGGER1 22
#define FRONT_ECHO1    23
#define FRONT_TRIGGER2 26
#define FRONT_ECHO2    27
#define REAR_TRIGGER  24
#define REAR_ECHO     25
// Seuil en centimètres pour détecter un obstacle
const int DISTANCE_SEUIL = 40;
// Durée du signal trigger (en microsecondes)
const int TRIGGER_PULSE = 10;
const int VITESSE=180;

SoftwareSerial HM10(2, 3); // RX, TX
int NB_DONNEE_RECU = 10;
int NB_DONNEE_BOUTONS = 4;
int NB_DONNEE_JOYSTICKS = 6;
bool VALBOUTONS[4] ; //valBoutons
float VALJOYSTICKS[6];

void setup() {
    // Initialisation des broches des capteurs ultrasons
  pinMode(FRONT_TRIGGER1, OUTPUT);
  pinMode(FRONT_ECHO1, INPUT);
  pinMode(FRONT_TRIGGER2, OUTPUT);
  pinMode(FRONT_ECHO2, INPUT);
  pinMode(REAR_TRIGGER, OUTPUT);
  pinMode(REAR_ECHO, INPUT);

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
  //Reception Bluetooth
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
  /*
  // Mesure des distances
  long distanceFront1 = getDistance(FRONT_TRIGGER1, FRONT_ECHO1);
  long distanceFront2 = getDistance(FRONT_TRIGGER2, FRONT_ECHO2);
  long distanceRear  = getDistance(REAR_TRIGGER, REAR_ECHO);
  if (distanceFront1 < DISTANCE_SEUIL && distanceFront1 != 0 || distanceFront2 < DISTANCE_SEUIL && distanceFront2 != 0) {
    reculer();
    delay(400);
    arreter();
  }
  if (distanceRear > DISTANCE_SEUIL && distanceRear != 0) {
    avancer();
    delay(400);
    arreter();
  }
  */

  if(VALJOYSTICKS[1] == 1){
    avancer();
  }elif (VALJOYSTICKS[1] == -1){
    reculer();
  }elif (VALJOYSTICKS[2] == 1){
    droite();
  }elif (VALJOYSTICKS[2] == -1){
    gauche();
  }elif {
    arreter();
  }

}

//************************************************************************************//
// Fonction : MOTEUR()                                             //
// But :      Active l'alimentation du moteur branché sur le pont A                   //
//            pendant 2 secondes, puis le met à l'arrêt (au moins 1 seconde)          //
//************************************************************************************//
long getDistance(int trigPin, int echoPin) {
  // Envoi du signal trigger
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(TRIGGER_PULSE);
  digitalWrite(trigPin, LOW);
  
  // Lecture du temps d'impulsion
  long duration = pulseIn(echoPin, HIGH, 30000); // Timeout de 30ms
  // Calcul de la distance en centimètres (vitesse du son = 0.034 cm/us)
  long distance = duration * 0.034 / 2;
  return distance;
}

// Fonctions de commande des moteurs
void reculer() {
  digitalWrite(borneIN1, HIGH);                 // L'entrée IN1 doit être au niveau haut
  digitalWrite(borneIN2, LOW);
  digitalWrite(borneIN3, HIGH);                  // L'entrée IN1 doit être au niveau bas
  digitalWrite(borneIN4, LOW); 
  
  Serial.println("Reculer");
}

void avancer() {
  // Pour reculer, activer les sorties en arrière et désactiver l'avant
  digitalWrite(borneIN1, LOW);                  // L'entrée IN1 doit être au niveau bas
  digitalWrite(borneIN2, HIGH);                 // L'entrée IN2 doit être au niveau haut
  digitalWrite(borneIN3, LOW);                  // L'entrée IN1 doit être au niveau bas
  digitalWrite(borneIN4, HIGH);
  analogWrite(borneENA, VITESSE);
  analogWrite(borneENB, VITESSE); 

  Serial.println("Avancer");
}

void droite() {
  // Pour tourner, par exemple, faire tourner le moteur gauche en avant et le droit en arrière
  digitalWrite(borneIN1, HIGH);                  // L'entrée IN1 doit être au niveau bas
  digitalWrite(borneIN2, LOW);                 // L'entrée IN2 doit être au niveau haut
  digitalWrite(borneIN3, LOW);                  // L'entrée IN1 doit être au niveau bas
  digitalWrite(borneIN4, HIGH); 
  analogWrite(borneENA, 200);
  analogWrite(borneENB, 200); 
  delay(1100);
  
  Serial.println("Tourner à droite");
}

void gauche() {
  // Pour tourner, par exemple, faire tourner le moteur gauche en avant et le droit en arrière
  digitalWrite(borneIN1, LOW);                  // L'entrée IN1 doit être au niveau bas
  digitalWrite(borneIN2, HIGH);                 // L'entrée IN2 doit être au niveau haut
  digitalWrite(borneIN3, HIGH);                  // L'entrée IN1 doit être au niveau bas
  digitalWrite(borneIN4, LOW); 
  analogWrite(borneENA, 200);
  analogWrite(borneENB, 200); 
  delay(1100);
  
  Serial.println("Tourner à gauche");
}

void arreter() {
  // Désactiver tous les moteurs
  digitalWrite(borneIN1, LOW);                  // L'entrée IN1 doit être au niveau bas
  digitalWrite(borneIN2, LOW);                 // L'entrée IN2 doit être au niveau haut
  digitalWrite(borneIN3, LOW);                  // L'entrée IN1 doit être au niveau bas
  digitalWrite(borneIN4, LOW);
  digitalWrite(borneENA, LOW);
  digitalWrite(borneENB, LOW);  
  
  
  Serial.println("Arrêt");

}

void changeVitesseMoteur(int nouvelleVitesse) {
  
  // Génère un signal PWM permanent, de rapport cyclique égal à "nouvelleVitesse" (valeur comprise entre 0 et 255)
  analogWrite(borneENA, nouvelleVitesse);
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


