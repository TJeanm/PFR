#define borneENA        10      // On associe la borne "ENA" du L298N à la pin D10 de l'arduino
#define borneIN1        9       // On associe la borne "IN1" du L298N à la pin D9 de l'arduino
#define borneIN2        8       // On associe la borne "IN2" du L298N à la pin D8 de l'arduino
#define borneIN3        7       // On associe la borne "IN3" du L298N à la pin D7 de l'arduino
#define borneIN4        6       // On associe la borne "IN4" du L298N à la pin D6 de l'arduino
#define borneENB        5       // On associe la borne "ENB" du L298N à la pin D5 de l'arduino

// Définition des broches pour les capteurs ultrasons
#define FRONT_TRIGGER1 13
#define FRONT_ECHO1    12
#define FRONT_TRIGGER2 3
#define FRONT_ECHO2    2
#define REAR_TRIGGER  11
#define REAR_ECHO     4

// Seuil en centimètres pour détecter un obstacle
const int DISTANCE_SEUIL = 40;

// Durée du signal trigger (en microsecondes)
const int TRIGGER_PULSE = 10;

const int VITESSE=170;

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
  
  // Optionnel : initialisation de la communication série
  Serial.begin(9600);
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

// Fonctions de commande des moteurs
void reculer() {
  digitalWrite(borneIN1, HIGH);                 // L'entrée IN1 doit être au niveau haut
  digitalWrite(borneIN2, LOW);
  digitalWrite(borneIN3, HIGH);                  // L'entrée IN1 doit être au niveau bas
  digitalWrite(borneIN4, LOW); 
   analogWrite(borneENA, VITESSE);
  analogWrite(borneENB, VITESSE); 
  
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

void loop() {
  // Mesure des distances
  
  long distanceFront1 = getDistance(FRONT_TRIGGER1, FRONT_ECHO1);
  long distanceFront2 = getDistance(FRONT_TRIGGER2, FRONT_ECHO2);
  long distanceRear  = getDistance(REAR_TRIGGER, REAR_ECHO);
  
  // Affichage pour debug
  Serial.print("Avant 1: ");
  Serial.print(distanceFront1);
  Serial.print(" cm  |  Avant 2 : ");
  Serial.print(distanceFront2);
  Serial.print(" cm  |  Arrière: ");
  Serial.print(distanceRear);
  Serial.println(" cm");
  
  // Si aucun obstacle devant (distance > seuil), avancer
  if (distanceFront1 > DISTANCE_SEUIL || distanceFront1 == 0 && distanceFront1 > DISTANCE_SEUIL || distanceFront1 == 0) {
    reculer();
    if (distanceFront1 < DISTANCE_SEUIL && distanceFront1 != 0 || distanceFront1 < DISTANCE_SEUIL && distanceFront1 != 0) {
      reculer();
      delay(400);
      droite();
    }
  } 
  else {
    reculer();
    delay(400);
    droite();
  }
  
  // Petite pause pour ne pas saturer le bus série et laisser le temps aux moteurs
  delay(100);
}
void changeVitesseMoteur(int nouvelleVitesse) {
  
  // Génère un signal PWM permanent, de rapport cyclique égal à "nouvelleVitesse" (valeur comprise entre 0 et 255)
  analogWrite(borneENA, nouvelleVitesse);
}



