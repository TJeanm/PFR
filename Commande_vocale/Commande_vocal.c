#include<stdio.h>
#include <stdlib.h>
#include <string.h>

//_________________________________DEFINITION_ELEMENT_________________________________

#define MAX_LETTRES 50
#define ELEMENT_VIDE "                                                                                                    "
typedef char ELEMENT[MAX_LETTRES];

void saisir_ELEMENT(ELEMENT element1)
{
  //printf("Saisir élément : ");
  scanf("%s", element1);
}

void affiche_ELEMENT(ELEMENT element1)
{
  //printf("L élément est : ");
  printf("%s\n", element1);
}

void affiche_ELEMENT_enLigne(ELEMENT element1)
{
  //printf("L élément est : ");
  printf("%s ", element1);
}

void affect_ELEMENT(ELEMENT element1, ELEMENT element2)
{
  for(int i=0; i<MAX_LETTRES; i++){
    element1[i] = element2[i];
  }
}

int compare_ELEMENT(ELEMENT element1, ELEMENT element2)
{
  //for(int i=0; i<MAX_LETTRES; i++){
  //  if (element1[i] != element2[i]) return 0;
  //}
  //return 1;

  return strcmp(element1, element2) == 0;
}

void fusion2ELEMENT(ELEMENT element1, ELEMENT element2, ELEMENT *element3)
{
  int i = 0;
  int nb_char_elem1 = 0;

  for(i; i<MAX_LETTRES; i++){
    if (element1[i] == '\0')
      break;
    (*element3)[i] = element1[i];
  }
  nb_char_elem1 = i+1;
  (*element3)[i] = ' ';
  i++;
  for(i; i<MAX_LETTRES-nb_char_elem1; i++){
    (*element3)[i] = element2[i-nb_char_elem1];
  }
}


//_________________________________DEFINITION_PILE_STATIQUE_________________________________

#define MAX_MOTS 50
typedef struct {
  int tete; 
  ELEMENT tab[MAX_MOTS];
}PILE;

PILE init_PILE(void)
{
  PILE pile;
  pile.tete = 0;
  return pile;
}

void affiche_PILE(PILE pile)
{
  int i;
  for(i=0; i<pile.tete; i++){
    //printf("L élément est : ");
    affiche_ELEMENT(pile.tab[i]);
  }
}

void affiche_PILE_enLigne(PILE pile)
{
  int i;
  for(i=0; i<pile.tete; i++){
    //printf("L élément est : ");
    affiche_ELEMENT_enLigne(pile.tab[i]);
  }
}

int PILE_estVide(PILE pile)
{
  return(pile.tete == 0);
}

int PILE_estPleine(PILE pile)
{
  return(pile.tete == MAX_MOTS);
}

PILE emPILE(PILE pile , ELEMENT element)
{
  if (PILE_estPleine(pile)) return pile;

  affect_ELEMENT(pile.tab[pile.tete], element);
  pile.tete++;
  return pile;
}

PILE dePILE(PILE pile, ELEMENT element)
{
  if (PILE_estVide(pile)) return pile;
  pile.tete--;
  affect_ELEMENT(element, pile.tab[pile.tete]);
  affect_ELEMENT(pile.tab[pile.tete], ELEMENT_VIDE);

  return pile;
}

PILE saisir_PILE()
{
  PILE pile = init_PILE();
  ELEMENT elem;
  int i, nb_mot;

  printf("Saisir le nombre de mot à entrer : ");
  scanf("%d", &nb_mot);

  for (i=0; i<nb_mot; i++)
  {
    printf("Saisir un mot à mettre dans la pile : ");
    saisir_ELEMENT(elem);
    pile = emPILE(pile, elem);
  }
  return pile;
}

PILE ligne_to_PILE(PILE p,char chaine[], char * delimitateur)
{
  int i = 0;
  int nbchar = 0;
  ELEMENT elem;
  p = init_PILE();

  do{
    if ((chaine[i] != *delimitateur) && (chaine[i] != '\0')) { // Vérifie s'il y a un espace  et que chaine[i] != '\0'
      elem[nbchar] = chaine[i]; // Ajoute le charactere au mot
      nbchar++;
    } else {
      elem[nbchar] = '\0'; // Fini le mot et passe au suivant
      p = emPILE(p, elem);
      nbchar = 0;
    }
    i++;
  }while (chaine[i-1] != '\0');
  return p;
}


//_________________________________FONCTION_______________________________________________

#include <string.h>

#define MAX_LANGUES 5
#define MAX_COMMANDES 400

#define DISTANCE_INIT 10
#define ANGLE_INIT 90
#define DEMI_TOUR 180


PILE recuperation_liste_commande()
{
  FILE *fichier_choix = fopen("choix_langue.txt", "r");
  if (!fichier_choix) {
    perror("Erreur lors de l'ouverture du fichier choix_langue.txt");
    return init_PILE();
  }
  int choix = 0; // 400 char par langue
  fscanf(fichier_choix, "%d", &choix);

  fclose(fichier_choix);


  FILE *fichier = fopen("liste_commande_vocal.csv", "r");
  if (!fichier) {
    perror("Erreur lors de l'ouverture du fichier liste_commande_vocal.csv");
    return init_PILE();
  }

  char ligne[MAX_COMMANDES]; // 400 char par langue
  for(int i=1; i<=choix; i++){
    fgets(ligne, sizeof(ligne), fichier);
  }

  PILE liste_commande = init_PILE();
  liste_commande = ligne_to_PILE(liste_commande, ligne, ";");
  //affiche_PILE(liste_commande);

  fclose(fichier);
  return liste_commande;
}

void choix_langue()
{
  FILE *fichier = fopen("liste_commande_vocal.csv", "r");
  if (!fichier) {
    perror("Erreur lors de l'ouverture du fichier liste_commande_vocal.csv");
  }else {
    PILE commandes[MAX_LANGUES]; // Chaque langue a une pile de commandes
    char ligne[MAX_COMMANDES]; // 400 char par langue
    int idx_langue = 0;
    int choix = 0;
    
    while (fgets(ligne, sizeof(ligne), fichier) != NULL && idx_langue < MAX_COMMANDES) {
      commandes[idx_langue] = init_PILE();
      commandes[idx_langue] = ligne_to_PILE(commandes[idx_langue], ligne, ";");
      idx_langue++;
    }

    printf("\nSelectionner la langue désiré :\n");
    for(int i=0; i<idx_langue; i++)
    {
      printf("  %d = ", i+1);
      affiche_ELEMENT(commandes[i].tab[0]);
    }
    scanf("%d", &choix);
    fclose(fichier);

    FILE *fichier_langue = fopen("choix_langue.txt", "w");
    if (!fichier_langue) {
      perror("Erreur lors de l'ouverture du fichier choix_langue.txt");
    } else {
      fprintf(fichier_langue, "%d\n", choix); // Écrit dans le fichier
      fprintf(fichier_langue, "%s\n", commandes[choix-1].tab[0]); // Écrit dans le fichier
      fclose(fichier_langue);
    }
  }
}

PILE receptionVocal()
{
  FILE *fichier = fopen("ligne_vocal.txt", "r");
  if (!fichier) {
    perror("Erreur lors de l'ouverture du fichier");
    return init_PILE();
  }

  char ligne[MAX_COMMANDES];
  fgets(ligne, sizeof(ligne), fichier);

  PILE recept_vocal = init_PILE();
  recept_vocal = ligne_to_PILE(recept_vocal, ligne, " ");
  affiche_PILE_enLigne(recept_vocal);

  fclose(fichier);
  return recept_vocal;
}

void ecriture_commande(char action[20], int distance)
{
  FILE *fichier_simu_LECTURE = fopen("../Transmission_to_simulation.csv", "r");
    if (!fichier_simu_LECTURE) {
      perror("Erreur lors de l'ouverture du fichier Transmission_to_simulation.csv");
    } else {

      char ligne[MAX_COMMANDES];
      fgets(ligne, sizeof(ligne), fichier_simu_LECTURE);
      PILE recept_index = init_PILE();
      recept_index = ligne_to_PILE(recept_index, ligne, ";");

      int index = atoi(recept_index.tab[2]) + 1;
      fclose(fichier_simu_LECTURE);

      FILE *fichier_simu_ECRITURE = fopen("../Transmission_to_simulation.csv", "w");
      if (!fichier_simu_ECRITURE) {
        perror("Erreur lors de l'ouverture du fichier Transmission_to_simulation.csv");
      } else {
        fprintf(fichier_simu_ECRITURE, "%s;%d;%d;0\n", action, distance, index); // Écrit dans le fichier
        fclose(fichier_simu_ECRITURE);
      }
    }
}

int verif_action_ok()
{
  FILE *fichier_simu_LECTURE = fopen("../Transmission_to_simulation.csv", "r");
    if (!fichier_simu_LECTURE) {
      perror("Erreur lors de l'ouverture du fichier Transmission_to_simulation.csv");
      return 0;

    } else {

      char ligne[MAX_COMMANDES];
      fgets(ligne, sizeof(ligne), fichier_simu_LECTURE);
      PILE recept_res = init_PILE();
      recept_res = ligne_to_PILE(recept_res, ligne, ";");

      int res = atoi(recept_res.tab[3]);
      fclose(fichier_simu_LECTURE);
      return res;
    }
}

int detectMot(PILE vocal, PILE commande, int *action, int *distance, int nb_mot) // nb_mot max = 5
{
  //printf("\nnbr mot de vocal = %d\n", vocal.tete);
  //printf("nbr mot de commande = %d\n", commande.tete);
  //printf("nb_mot reagerdé = %d\n", nb_mot);
  ELEMENT tempo;
  *action = 0;
  *distance = 0;
  int detect = 0;


  if (nb_mot == 1){
    for(int i=0; i<vocal.tete; i++){
      for(int j=0;j<commande.tete; j++){
        if (compare_ELEMENT(vocal.tab[i], commande.tab[j])){
          *action = j;
          detect = 1;
        }
      }
    }

  }else if (vocal.tete-nb_mot-1 > 0){
    PILE vocalmots = init_PILE();

    for(int i=0; i<vocal.tete-nb_mot-1; i++){
      
      if (nb_mot>=2){
        fusion2ELEMENT(vocal.tab[i], vocal.tab[i+1], &tempo);
        if (nb_mot>=3){
          fusion2ELEMENT(tempo, vocal.tab[i+2], &tempo);
          if (nb_mot>=4){
            fusion2ELEMENT(tempo, vocal.tab[i+3], &tempo);
            if (nb_mot>=5){
              fusion2ELEMENT(tempo, vocal.tab[i+4], &tempo);
            }
          }
        }
      }
      vocalmots = emPILE(vocalmots, tempo);
    }

    for(int i=0; i<vocalmots.tete; i++){
      for(int j=1;j<commande.tete; j++){
        if (compare_ELEMENT(vocalmots.tab[i], commande.tab[j])){
          *action = j;
          detect = 1;
          printf("Commande détecté : %s", commande.tab[j]);

          if (j==2 || j==6 || j==9 || j==13){

            *distance = atoi(vocal.tab[i+nb_mot]);

            printf(" %d", *distance);
          }
          printf("\n");
        }
      }
    }
  }
  
  if (detect == 0 && nb_mot != 1)
    detect = detectMot(vocal, commande, &(*action), &(*distance), nb_mot-1);

  return detect;
}

int realisation_Action(PILE commande, int action, int distance)
{
  char avancer[20] = "avancer";
  char droite[20] = "tourne a droite";
  char gauche[20] = "tourne a gauche";
  int fin_commande_vocal = 0;
  

  if (verif_action_ok()){  //!
    printf("L'acion précédente n'est pas fini, veillez attendre puis recommencer\n");
  }else{
    switch(action){
      case 1 :
        //avance
        ecriture_commande(avancer, DISTANCE_INIT);
        affiche_ELEMENT(commande.tab[1]);
        break;
      case  2 :
        //avance de
        ecriture_commande(avancer, distance);
        affiche_ELEMENT(commande.tab[2]);
        break;
      case 3 :
        //avance sans fin
        affiche_ELEMENT(commande.tab[3]);
        break;
      case 4 :
        //stop
        affiche_ELEMENT(commande.tab[4]);
        break;
      case 5 :
        //recule
        ecriture_commande(avancer, -DISTANCE_INIT);
        affiche_ELEMENT(commande.tab[5]);
        break;
      case 6 :
        //recule de
        ecriture_commande(avancer, -distance);
        affiche_ELEMENT(commande.tab[6]);
        break;
      case 7 :
        //recule sans fin
        affiche_ELEMENT(commande.tab[7]);
        break;
      case 8 :
        //tourne à droite
        ecriture_commande(droite, ANGLE_INIT);
        affiche_ELEMENT(commande.tab[8]);
        break;
      case 9 :
        //tourne à droite de
        ecriture_commande(droite, distance);
        affiche_ELEMENT(commande.tab[9]);
        break;
      case 10 :
        //tourne à droite sans fin
        affiche_ELEMENT(commande.tab[10]);
        break;
      case 11 :
        //tourne à gauche
        ecriture_commande(gauche, ANGLE_INIT);
        affiche_ELEMENT(commande.tab[11]);
        break;
      case 12 :
        //tourne à gauche de
        ecriture_commande(gauche, distance);
        affiche_ELEMENT(commande.tab[12]);
        break;
      case 13 :
        //tourne à gauche sans fin
        affiche_ELEMENT(commande.tab[13]);
        break;
      case 14 :
        //fait un tour
        affiche_ELEMENT(commande.tab[14]);
        break;
      case 15 :
        //fait un demi tour
        ecriture_commande(droite, DEMI_TOUR);
        affiche_ELEMENT(commande.tab[15]);
        break;
      case 16 :
        //quitte le mode vocal
        fin_commande_vocal = 1;
        affiche_ELEMENT(commande.tab[16]);
        break;
      case 17 :
        //avance jusqu'a
        affiche_ELEMENT(commande.tab[17]);
        break;
      case 18 :
        //tourne jusqu'a
        affiche_ELEMENT(commande.tab[18]);
        break;
      case 19 :
        //réalise trajectoire
        affiche_ELEMENT(commande.tab[19]);
        break;
      case 20 :
        //enregistre ma trajectoire
        affiche_ELEMENT(commande.tab[20]);
        break;
      case 21 :
        //fin trajectoire
        affiche_ELEMENT(commande.tab[21]);
        break;
      case 22 :
        //fait trajectoire
        affiche_ELEMENT(commande.tab[22]);
        break;

      default:
      printf("Aucune action n'a été détecter.\n");
      break;
    }
  }
}

void commande_vocal()
{
  choix_langue();
  int fin_commande_vocal = 0;
  PILE liste_vocal = init_PILE();
  PILE liste_commande = init_PILE();
  liste_commande = recuperation_liste_commande();
  int action;
  int distance;
  int action_detecte;

  while(!fin_commande_vocal){

    int status = system("./Vocal.py");
    printf("status = %d\n", status);

    // Vérification du résultat de l'exécution
    if (status == -1) {
        perror("Erreur lors de l'exécution du programme");
    } else {
        printf("Programme exécuté avec succès.\n");
    }

    liste_vocal = receptionVocal();
    action_detecte = detectMot(liste_vocal, liste_commande, &action, &distance, 5);
    if (action_detecte){
      fin_commande_vocal = realisation_Action(liste_commande, action, distance);
    }else {
      printf("Aucune action détecté !\n");
    }
  }
}

int main()
{
  printf("Début des tests\n\n");
  
  commande_vocal();

  printf("\nFin des tests\n");
}