#define borneENA        10      // On associe la borne "ENA" du L298N à la pin D10 de l'arduino
#define borneIN1        9       // On associe la borne "IN1" du L298N à la pin D9 de l'arduino
#define borneIN2        8       // On associe la borne "IN2" du L298N à la pin D8 de l'arduino
#define borneIN3        7       // On associe la borne "IN3" du L298N à la pin D7 de l'arduino
#define borneIN4        6       // On associe la borne "IN4" du L298N à la pin D6 de l'arduino
#define borneENB        5       // On associe la borne "ENB" du L298N à la pin D5 de l'arduino


//*******//
// SETUP //
//*******//
void setup() {
  
  // Configuration de toutes les pins de l'Arduino en "sortie" (car elles attaquent les entrées du module L298N)
  pinMode(borneENA, OUTPUT);
  pinMode(borneIN1, OUTPUT);
  pinMode(borneIN2, OUTPUT);
  pinMode(borneIN3, OUTPUT);
  pinMode(borneIN4, OUTPUT);
  pinMode(borneENB, OUTPUT);
}

//**************************//
// Boucle principale : LOOP //
//**************************//
void loop() {

  // Configuration du L298N en "marche avant", pour le moteur connecté au pont A. Selon sa table de vérité, il faut que :
  digitalWrite(borneIN1, HIGH);                 // L'entrée IN1 doit être au niveau haut
  digitalWrite(borneIN2, LOW);
  digitalWrite(borneIN3, HIGH);                  // L'entrée IN1 doit être au niveau bas
  digitalWrite(borneIN4, LOW);                   // L'entrée IN2 doit être au niveau bas

  // Et on lance le moteur (branché sur le pont A du L298N)
  lancerRotationMoteurPontA();

  // Puis on configure le L298N en "marche arrière", pour le moteur câblé sur le pont A. Selon sa table de vérité, il faut que :
  digitalWrite(borneIN1, LOW);                  // L'entrée IN1 doit être au niveau bas
  digitalWrite(borneIN2, HIGH);                 // L'entrée IN2 doit être au niveau haut
  digitalWrite(borneIN3, LOW);                  // L'entrée IN1 doit être au niveau bas
  digitalWrite(borneIN4, HIGH);  
  // Et on relance le moteur (branché sur le pont A du L298N)
  lancerRotationMoteurPontA();
  
  // Puis... on boucle à l'infini !
}


//************************************************************************************//
// Fonction : lancerRotationMoteurPontA()                                             //
// But :      Active l'alimentation du moteur branché sur le pont A                   //
//            pendant 2 secondes, puis le met à l'arrêt (au moins 1 seconde)          //
//************************************************************************************//
void lancerRotationMoteurPontA() {
  digitalWrite(borneENA, HIGH);       // Active l'alimentation du moteur 1
                         // et attend 2 secondes
  
  digitalWrite(borneENB, HIGH);       // Active l'alimentation du moteur 1
  delay(2000);                        // et attend 2 secondes
  
  digitalWrite(borneENB, LOW);        // Désactive l'alimentation du moteur 1
  

  digitalWrite(borneENA, LOW);        // Désactive l'alimentation du moteur 1
  delay(1000);                        // et attend 1 seconde
}