#ifndef RECO_IMAGE_H
#define RECO_IMAGE_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#define LONGUEUR 300
#define LARGEUR 300

// Structure représentant un pixel
typedef struct {
    int x;
    int y;
} Pixel;

// Déclarations des fonctions
int length(Pixel liste[], int taille_max);
void attribuerPixel(int pixel, int longueur, int largeur, int matrice[LONGUEUR][LARGEUR], int i, int j);
int distancePixel(Pixel p1, Pixel p2);
int calculerMediane(int fenetre[9]);
char* couleurPixel(int i, int j, int longueur, int largeur, int rouge[LONGUEUR][LARGEUR], int vert[LONGUEUR][LARGEUR], int bleu[LONGUEUR][LARGEUR]);
void filtrerBruit(int longueur, int largeur, int matrice[LONGUEUR][LARGEUR]);
void supprimerPixelsIsoles(int longueur, int largeur, int matrice[LONGUEUR][LARGEUR]);
int estPixelVif(int i, int j, int longueur, int largeur, int rouge[LONGUEUR][LARGEUR], int vert[LONGUEUR][LARGEUR], int bleu[LONGUEUR][LARGEUR]);

#endif // RECO_IMAGE_H
