#define borneENA        10      // On associe la borne "ENA" du L298N à la pin D10 de l'arduino
#define borneIN1        9       // On associe la borne "IN1" du L298N à la pin D9 de l'arduino
#define borneIN2        8       // On associe la borne "IN2" du L298N à la pin D8 de l'arduino
#define borneIN3        7       // On associe la borne "IN3" du L298N à la pin D7 de l'arduino
#define borneIN4        6       // On associe la borne "IN4" du L298N à la pin D6 de l'arduino
#define borneENB        5       // On associe la borne "ENB" du L298N à la pin D5 de l'arduino

// Définition des broches pour les capteurs ultrasons
#define FRONT_TRIGGER 22
#define FRONT_ECHO    23
#define REAR_TRIGGER  24
#define REAR_ECHO     25

// Seuil en centimètres pour détecter un obstacle
const int DISTANCE_SEUIL = 20;

// Durée du signal trigger (en microsecondes)
const int TRIGGER_PULSE = 10;

void setup() {
  // Initialisation des broches des capteurs ultrasons
  pinMode(FRONT_TRIGGER, OUTPUT);
  pinMode(FRONT_ECHO, INPUT);
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
  digitalWrite(borneENA, HIGH);
  digitalWrite(borneENB, HIGH);  
  
  Serial.println("Avancer");
}

void avancer() {
  // Pour reculer, activer les sorties en arrière et désactiver l'avant
  digitalWrite(borneIN1, LOW);                  // L'entrée IN1 doit être au niveau bas
  digitalWrite(borneIN2, HIGH);                 // L'entrée IN2 doit être au niveau haut
  digitalWrite(borneIN3, LOW);                  // L'entrée IN1 doit être au niveau bas
  digitalWrite(borneIN4, HIGH);
  digitalWrite(borneENA, HIGH);
  digitalWrite(borneENB, HIGH); 

  Serial.println("Reculer");
}

void tourner() {
  // Pour tourner, par exemple, faire tourner le moteur gauche en avant et le droit en arrière
  digitalWrite(borneIN1, HIGH);                  // L'entrée IN1 doit être au niveau bas
  digitalWrite(borneIN2, LOW);                 // L'entrée IN2 doit être au niveau haut
  digitalWrite(borneIN3, LOW);                  // L'entrée IN1 doit être au niveau bas
  digitalWrite(borneIN4, HIGH);
  digitalWrite(borneENA, HIGH);
  digitalWrite(borneENB, HIGH); 
  delay(1000);
  digitalWrite(borneENA, LOW);
  digitalWrite(borneENB, LOW); 
  
  Serial.println("Tourner");
}

void arreter() {
  // Désactiver tous les moteurs
  digitalWrite(borneENA, LOW);
  digitalWrite(borneENB, LOW); 
  
  
  Serial.println("Arrêt");

}

void loop() {
  // Mesure des distances
  long distanceFront = getDistance(FRONT_TRIGGER, FRONT_ECHO);
  long distanceRear  = getDistance(REAR_TRIGGER, REAR_ECHO);
  
  // Affichage pour debug
  Serial.print("Avant: ");
  Serial.print(distanceFront);
  Serial.print(" cm  |  Arrière: ");
  Serial.print(distanceRear);
  Serial.println(" cm");
  
  // Si aucun obstacle devant (distance > seuil), avancer
  if (distanceFront > DISTANCE_SEUIL || distanceFront == 0) {
    avancer();
  } 
  else {
    arreter();
    delay(1000);
    // Obstacle détecté à l'avant
    // Vérifier que l'arrière est dégagé pour reculer
    if (distanceRear > DISTANCE_SEUIL || distanceRear == 0) {
      reculer();
      tourner();
    } 
    else {
      // Aucun espace pour reculer : tourner sur place puis repartir
      tourner();
    }
  }
  
  // Petite pause pour ne pas saturer le bus série et laisser le temps aux moteurs
  delay(100);
}




