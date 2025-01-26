#ifndef __PILOTAGE_H__
#define __PILOTAGE_H__

#include <stdio.h>
#include <stdlib.h>

#include <time.h>

// Détection de la plateforme
#ifdef _WIN32
    #include <conio.h> // Bibliothèque pour capturer les touches sous Windows
#else
    #include <termios.h>
    #include <unistd.h>
#endif

// Fonction pour configurer le terminal en mode non-bloquant (Linux/macOS)
#ifndef _WIN32
void configurer_terminal() ;

void reinitialiser_terminal() ;
#endif

void ajouter_mouvement(const char *mouvement, const char *description, int valeur);

void calculer_nouvelles_coordonnees(int *x, int *y, int angle, int valeur);

char lire_touche();

void pilotage_manuel();


#endif