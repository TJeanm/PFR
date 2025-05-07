#define borneENA        10      // On associe la borne "ENA" du L298N à la pin D10 de l'arduino
#define borneIN1        9       // On associe la borne "IN1" du L298N à la pin D9 de l'arduino
#define borneIN2        8       // On associe la borne "IN2" du L298N à la pin D8 de l'arduino
#define borneIN3        7       // On associe la borne "IN3" du L298N à la pin D7 de l'arduino
#define borneIN4        6       // On associe la borne "IN4" du L298N à la pin D6 de l'arduino
#define borneENB        5       // On associe la borne "ENB" du L298N à la pin D5 de l'arduino
// Définition des broches pour les capteurs ultrasons
#define FRONT_TRIGGER1 27
#define FRONT_ECHO1    26
#define FRONT_TRIGGER2 22
#define FRONT_ECHO2    23
#define REAR_TRIGGER  24
#define REAR_ECHO     25
// Seuil en centimètres pour détecter un obstacle
const int DISTANCE_SEUIL = 40;
// Durée du signal trigger (en microsecondes)
const int TRIGGER_PULSE = 10;
const int VITESSE=180;
const int VITESSE_RAPIDE=255;
char currentState='p';
char var;


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
  // Pour la communication Bluetooth (par exemple via HM-10 connecté sur Serial1)
  Serial1.begin(115200);   // HM‑10 par défaut en 9600 bauds

  Serial.println("Initialisation terminée !");
}

void loop() {
  //Reception Bluetooth
  long distanceFront1 = getDistance(FRONT_TRIGGER1, FRONT_ECHO1);
  long distanceFront2 = getDistance(FRONT_TRIGGER2, FRONT_ECHO2);
  if (Serial1.available()) {  // Si on a bien reçu quelque chose
    String received = Serial1.readStringUntil('\n'); // Lit le message complet
    if (received != "OK+CONN" && received != "OK+LOST"){
      received.trim();
      //Serial.println(received);
      // Si la chaîne commence par "OK+CONN", on la nettoie pour récupérer la commande utile
      if (received.startsWith("OK+CONN")) {
        received = received.substring(7); // Supprime les 7 premiers caractères ("OK+CONN")
        Serial.print("Message reçu : ");
        // Traitement de la donnée reçu
        
      }else if (received.startsWith("OK+LOST")) {
        Serial.println("Déconnexion détectée, received ignorée");
        return;
      }
      Serial.println(received.charAt(0));
       var=received.charAt(0);
    }
  }else{
    var = 'n';
  }
   

  
  if (var=='p'){
    currentState='p';
  }
  if(var=='o'){
    currentState='o';
  }

    
  if (currentState=='o'){
      modeAuto(distanceFront1,distanceFront2);
  }
  else {
      modeManuel(var);
    }
}

void modeManuel(char val){
  switch(val){
      
        case 'm': 
          arreter();
          break;
        case 'z': 
          avancer();
          break;
        case 's': 
          reculer();
          break;
        case 'q': 
          gauche();
          break;
        case 'd': 
          droite();
          break;
        case 'a': 
          avancerGauche();
          break;
        case 'e': 
          avancerDroite();
          break;
        case 'w': 
          reculerGauche();
          break;
        case 'x': 
          reculerDroite();
          break;
        case 't': 
          avancerRapide();
          break;
        case 'g': 
          reculerRapide();
          break;
        case 'f': 
          gaucheRapide();
          break;
        case 'h': 
          droiteRapide();
          break;
        case 'r': 
          avancerGauche();
          break;
        case 'y': 
          avancerDroite();
          break;
        case 'v': 
          reculerGauche();
          break;
        case 'b': 
          reculerDroite();
          break;
      }
}
   
void modeAuto(long distanceFront1,long distanceFront2){
  long distanceRear  = getDistance(REAR_TRIGGER, REAR_ECHO);
  if (distanceFront1 > DISTANCE_SEUIL || distanceFront1 == 0 && distanceFront2 > DISTANCE_SEUIL || distanceFront2 == 0) {
    avancer();
    if (distanceFront1 < DISTANCE_SEUIL && distanceFront1 != 0 || distanceFront2 < DISTANCE_SEUIL && distanceFront2 != 0) {
      reculer();
      delay(400);
      droite();
      delay(500);
    }
  } 
  else {
    reculer();
    delay(400);
    droite();
    delay(500);
  }
  
  // Petite pause pour ne pas saturer le bus série et laisser le temps aux moteurs
  delay(100);
}


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

void reculer() {
  
  digitalWrite(borneIN1, HIGH);                 // L'entrée IN1 doit être au niveau haut
  digitalWrite(borneIN2, LOW);
  digitalWrite(borneIN3, HIGH);                  // L'entrée IN1 doit être au niveau bas
  digitalWrite(borneIN4, LOW); 
  changeVitesseMoteur(VITESSE);
  
}

void avancer() {
  // Pour reculer, activer les sorties en arrière et désactiver l'avant
  
  digitalWrite(borneIN1, LOW);                  // L'entrée IN1 doit être au niveau bas
  digitalWrite(borneIN2, HIGH);                 // L'entrée IN2 doit être au niveau haut
  digitalWrite(borneIN3, LOW);                  // L'entrée IN1 doit être au niveau bas
  digitalWrite(borneIN4, HIGH);
  changeVitesseMoteur(VITESSE);
}

void droite() {
  // Pour tourner, par exemple, faire tourner le moteur gauche en avant et le droit en arrière
  digitalWrite(borneIN1, HIGH);                  // L'entrée IN1 doit être au niveau bas
  digitalWrite(borneIN2, LOW);                 // L'entrée IN2 doit être au niveau haut
  digitalWrite(borneIN3, LOW);                  // L'entrée IN1 doit être au niveau bas
  digitalWrite(borneIN4, HIGH); 
  changeVitesseMoteur(200); 
  //delay(1100);
  
}

void gauche() {
  // Pour tourner, par exemple, faire tourner le moteur gauche en avant et le droit en arrière
  digitalWrite(borneIN1, LOW);                  // L'entrée IN1 doit être au niveau bas
  digitalWrite(borneIN2, HIGH);                 // L'entrée IN2 doit être au niveau haut
  digitalWrite(borneIN3, HIGH);                  // L'entrée IN1 doit être au niveau bas
  digitalWrite(borneIN4, LOW); 
  changeVitesseMoteur(200); 
  //delay(1100);
  
}

void avancerDroite() {
  // Pour tourner, par exemple, faire tourner le moteur gauche en avant et le droit en arrière
  digitalWrite(borneIN1, HIGH);                  // L'entrée IN1 doit être au niveau bas
  digitalWrite(borneIN2, LOW);                 // L'entrée IN2 doit être au niveau haut
  digitalWrite(borneIN3, LOW);                  // L'entrée IN1 doit être au niveau bas
  digitalWrite(borneIN4, HIGH);
  analogWrite(borneENA, VITESSE/3);
  analogWrite(borneENB, VITESSE_RAPIDE); 
  
  
}

void avancerGauche() {
  // Pour tourner, par exemple, faire tourner le moteur gauche en avant et le droit en arrière
  digitalWrite(borneIN1, LOW);                  // L'entrée IN1 doit être au niveau bas
  digitalWrite(borneIN2, HIGH);                 // L'entrée IN2 doit être au niveau haut
  digitalWrite(borneIN3, HIGH);                  // L'entrée IN1 doit être au niveau bas
  digitalWrite(borneIN4, LOW);
  analogWrite(borneENA, VITESSE_RAPIDE);
  analogWrite(borneENB, VITESSE/3); 
 
  
  Serial.println("Tourner à gauche");
}

void reculerDroite() {
  // Pour tourner, par exemple, faire tourner le moteur gauche en avant et le droit en arrière
  digitalWrite(borneIN1, LOW);                  // L'entrée IN1 doit être au niveau bas
  digitalWrite(borneIN2, HIGH);                 // L'entrée IN2 doit être au niveau haut
  digitalWrite(borneIN3, HIGH);                  // L'entrée IN1 doit être au niveau bas
  digitalWrite(borneIN4, LOW);
  analogWrite(borneENA, VITESSE/3);
  analogWrite(borneENB, VITESSE_RAPIDE);  

  
}

void reculerGauche() {
  // Pour tourner, par exemple, faire tourner le moteur gauche en avant et le droit en arrière
  digitalWrite(borneIN1, HIGH);                  // L'entrée IN1 doit être au niveau bas
  digitalWrite(borneIN2, LOW);                 // L'entrée IN2 doit être au niveau haut
  digitalWrite(borneIN3, LOW);                  // L'entrée IN1 doit être au niveau bas
  digitalWrite(borneIN4, HIGH);
  analogWrite(borneENA, VITESSE_RAPIDE);
  analogWrite(borneENB, VITESSE/3); 

  
}

void arreter() {
  // Désactiver tous les moteurs
  digitalWrite(borneIN1, LOW);                  // L'entrée IN1 doit être au niveau bas
  digitalWrite(borneIN2, LOW);                 // L'entrée IN2 doit être au niveau haut
  digitalWrite(borneIN3, LOW);                  // L'entrée IN1 doit être au niveau bas
  digitalWrite(borneIN4, LOW);
  digitalWrite(borneENA, LOW);
  digitalWrite(borneENB, LOW);  
  
  

}

void reculerRapide() {
  
  digitalWrite(borneIN1, HIGH);                 // L'entrée IN1 doit être au niveau haut
  digitalWrite(borneIN2, LOW);
  digitalWrite(borneIN3, HIGH);                  // L'entrée IN1 doit être au niveau bas
  digitalWrite(borneIN4, LOW); 
  changeVitesseMoteur(VITESSE_RAPIDE);
  
}

void avancerRapide() {
  // Pour reculer, activer les sorties en arrière et désactiver l'avant
  
  digitalWrite(borneIN1, LOW);                  // L'entrée IN1 doit être au niveau bas
  digitalWrite(borneIN2, HIGH);                 // L'entrée IN2 doit être au niveau haut
  digitalWrite(borneIN3, LOW);                  // L'entrée IN1 doit être au niveau bas
  digitalWrite(borneIN4, HIGH);
  changeVitesseMoteur(VITESSE_RAPIDE);
}

void droiteRapide() {
  // Pour tourner, par exemple, faire tourner le moteur gauche en avant et le droit en arrière
  digitalWrite(borneIN1, HIGH);                  // L'entrée IN1 doit être au niveau bas
  digitalWrite(borneIN2, LOW);                 // L'entrée IN2 doit être au niveau haut
  digitalWrite(borneIN3, LOW);                  // L'entrée IN1 doit être au niveau bas
  digitalWrite(borneIN4, HIGH); 
  changeVitesseMoteur(VITESSE_RAPIDE); 
  //delay(1100);
  
}

void gaucheRapide() {
  // Pour tourner, par exemple, faire tourner le moteur gauche en avant et le droit en arrière
  digitalWrite(borneIN1, LOW);                  // L'entrée IN1 doit être au niveau bas
  digitalWrite(borneIN2, HIGH);                 // L'entrée IN2 doit être au niveau haut
  digitalWrite(borneIN3, HIGH);                  // L'entrée IN1 doit être au niveau bas
  digitalWrite(borneIN4, LOW); 
  changeVitesseMoteur(VITESSE_RAPIDE); 
  //delay(1100);
  
}


void changeVitesseMoteur(int nouvelleVitesse) {
  
  // Génère un signal PWM permanent, de rapport cyclique égal à "nouvelleVitesse" (valeur comprise entre 0 et 255)
  analogWrite(borneENA, nouvelleVitesse);
  analogWrite(borneENB, nouvelleVitesse);
}


