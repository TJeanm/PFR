#ifndef __INTERFACE_H__
#define __INTERFACE_H__

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define TAILLE_MAX 10

int appel();

int verif_mdp(const char *) ;

void menu_principal();

void mode_administrateur ();

void mode_utilisateur();

void actions_administrateur();

void modif_mdp(const char *);

void modif_mode_vocal();

void modif_mode_manuel();

void mode_manel();

void mode_vocal();

void mode_auto();


#endif