#ifndef __COMMANDE_VOCAL_H__
#define __COMMANDE_VOCALE_H__

#include <stdio.h>
#include <stdlib.h>





//_________________________________DEFINITION_ELEMENT_________________________________

#define MAX_LETTRES 50
#define ELEMENT_VIDE "                                                                                                    "
typedef char ELEMENT[MAX_LETTRES];

void saisir_ELEMENT(ELEMENT element1);

void affiche_ELEMENT(ELEMENT element1);

void affiche_ELEMENT_enLigne(ELEMENT element1);

void affect_ELEMENT(ELEMENT element1, ELEMENT element2);

int compare_ELEMENT(ELEMENT element1, ELEMENT element2);

void fusion2ELEMENT(ELEMENT element1, ELEMENT element2, ELEMENT *element3);




//_________________________________DEFINITION_PILE_STATIQUE_________________________________

#define MAX_MOTS 50
typedef struct {
  int tete; 
  ELEMENT tab[MAX_MOTS];
}PILE;

PILE init_PILE(void);

void affiche_PILE(PILE pile);

void affiche_PILE_enLigne(PILE pile);

int PILE_estVide(PILE pile);

int PILE_estPleine(PILE pile);

PILE emPILE(PILE pile , ELEMENT element);

PILE dePILE(PILE pile, ELEMENT element);

PILE saisir_PILE();

PILE ligne_to_PILE(PILE p,char chaine[], char * delimitateur);


//_________________________________FONCTION_______________________________________________

#include <string.h>

#define MAX_LANGUES 5
#define MAX_COMMANDES 400

#define DISTANCE_INIT 10
#define ANGLE_INIT 90
#define DEMI_TOUR 180

PILE recuperation_liste_commande();

void choix_langue();

PILE receptionVocal();

void ecriture_commande(char action[20], int distance);

int verif_action_ok();

int detectMot(PILE vocal, PILE commande, int *action, int *distance, int nb_mot);

int realisation_Action(PILE commande, int action, int distance);

void commande_vocal();

void simulation_vocal();

#endif