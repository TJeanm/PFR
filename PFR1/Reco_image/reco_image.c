#include "reco_image.h"

int length(Pixel liste[], int taille_max) {
    for (int i = 0; i < taille_max; i++) {
        if (liste[i].x == 0 && liste[i].y == 0) {
            return i;
        }
    }
    return taille_max;
}

void attribuerPixel(int pixel, int longueur, int largeur, int matrice[longueur][largeur], int i, int j) {
    if (pixel >= 200) {
        matrice[i][j] = 2;
    } else if (pixel >= 100) {
        matrice[i][j] = 1;
    } else {
        matrice[i][j] = 0;
    }
}

int distancePixel(Pixel p1, Pixel p2) {
    return sqrt((p1.x - p2.x) * (p1.x - p2.x) + (p1.y - p2.y) * (p1.y - p2.y));
}

int calculerMediane(int fenetre[9]) {
    for (int i = 0; i < 9; i++) {
        for (int j = i + 1; j < 9; j++) {
            if (fenetre[j] < fenetre[i]) {
                int temp = fenetre[i];
                fenetre[i] = fenetre[j];
                fenetre[j] = temp;
            }
        }
    }
    return fenetre[4];
}

char* couleurPixel(int i, int j, int longueur, int largeur, int rouge[longueur][largeur], int vert[longueur][largeur], int bleu[longueur][largeur]) {
    if (rouge[i][j] == 2 && bleu[i][j] == 0) {
        if (vert[i][j] == 2) {
            return "Jaune";
        } else if (vert[i][j] == 1) {
            return "Orange";
        } else {
            return "Rouge";
        }
    } else if (bleu[i][j] == 2 && vert[i][j] == 0) {
        if (rouge[i][j] == 0) {
            return "Bleu";
        } else if (rouge[i][j] == 1) {
            return "Violet";
        }
    } else if (vert[i][j] == 2 && rouge[i][j] == 0 && bleu[i][j] == 0) {
        return "Vert";
    } else {
        return "Noir";
    }
}

void filtrerBruit(int longueur, int largeur, int matrice[longueur][largeur]) {
    int fenetre[9];
    for (int i = 0; i < longueur; i++) {
        for (int j = 0; j < largeur; j++) {
            int count = 0;
            for (int di = -1; di <= 1; di++) {
                for (int dj = -1; dj <= 1; dj++) {
                    int ni = i + di;
                    int nj = j + dj;
                    if (ni >= 0 && ni < longueur && nj >= 0 && nj < largeur) {
                        fenetre[count++] = matrice[ni][nj];
                    }
                }
            }
            while (count < 9) {
                fenetre[count++] = 0;
            }
            matrice[i][j] = calculerMediane(fenetre);
        }
    }
}

void supprimerPixelsIsoles(int longueur, int largeur, int matrice[longueur][largeur]) {
    int copie[longueur][largeur];
    memcpy(copie, matrice, sizeof(int) * longueur * largeur);

    for (int i = 0; i < longueur; i++) {
        for (int j = 0; j < largeur; j++) {
            int voisins = 0;
            for (int di = -1; di <= 1; di++) {
                for (int dj = -1; dj <= 1; dj++) {
                    int ni = i + di;
                    int nj = j + dj;
                    if (di == 0 && dj == 0) continue; // Ignorer le pixel central
                    if (ni >= 0 && ni < longueur && nj >= 0 && nj < largeur && copie[ni][nj] == copie[i][j]) {
                        voisins++;
                    }
                }
            }
            if (voisins < 1) { // Supprime seulement les pixels réellement isolés
                matrice[i][j] = 0;
            }
        }
    }
}

int estPixelVif(int i, int j, int longueur, int largeur, int rouge[longueur][largeur], int vert[longueur][largeur], int bleu[longueur][largeur]) {
    if ((rouge[i][j] == 2 && vert[i][j] == 0 && bleu[i][j] == 0) ||
           (rouge[i][j] == 2 && vert[i][j] == 2 && bleu[i][j] == 0) ||
           (rouge[i][j] == 0 && vert[i][j] == 2 && bleu[i][j] == 0) ||
           (rouge[i][j] == 0 && vert[i][j] == 0 && bleu[i][j] == 2)){
            return 1;
           }
        return 0;
}

int main() {
    int longueur, largeur, couleurs;
    if (scanf("%d %d %d", &longueur, &largeur, &couleurs) != 3) {
        fprintf(stderr, "Erreur de saisie des dimensions ou du nombre de couleurs.\n");
        return 1;
    }

    int rouge[longueur][largeur], vert[longueur][largeur], bleu[longueur][largeur];

    Pixel objets[20][50] = {0}; // Initialisation à 0
    Pixel p;
    int nbObjets = 0;

    // Lecture et attribution des pixels rouges
    for (int i = 0; i < longueur; i++) {
        for (int j = 0; j < largeur; j++) {
            int pixel;
            if (scanf("%d", &pixel) != 1) {
                fprintf(stderr, "Erreur de saisie des pixels rouges.\n");
                return 1;
            }
            attribuerPixel(pixel, longueur, largeur, rouge, i, j);
        }
    }
    supprimerPixelsIsoles(longueur, largeur, rouge);

    // Lecture et attribution des pixels verts
    for (int i = 0; i < longueur; i++) {
        for (int j = 0; j < largeur; j++) {
            int pixel;
            if (scanf("%d", &pixel) != 1) {
                fprintf(stderr, "Erreur de saisie des pixels verts.\n");
                return 1;
            }
            attribuerPixel(pixel, longueur, largeur, vert, i, j);
        }
    }
    supprimerPixelsIsoles(longueur, largeur, vert);

    // Lecture et attribution des pixels bleus
    for (int i = 0; i < longueur; i++) {
        for (int j = 0; j < largeur; j++) {
            int pixel;
            if (scanf("%d", &pixel) != 1) {
                fprintf(stderr, "Erreur de saisie des pixels bleus.\n");
                return 1;
            }
            attribuerPixel(pixel, longueur, largeur, bleu, i, j);
        }
    }
    supprimerPixelsIsoles(longueur, largeur, bleu);

    // Détection des objets
    for (int i = 0; i < longueur; i++) {
        for (int j = 0; j < largeur; j++) {
            if (estPixelVif(i, j, longueur, largeur, rouge, vert, bleu)==1) {
                p.x = j;
                p.y = i;
                if (nbObjets == 0) {
                    objets[0][0] = p;
                    nbObjets++;
                } else {
                    int ajout = 0;
                    for (int k = 0; k < nbObjets; k++) {
                        for (int l = 0; l < length(objets[k], 50); l++) {
                            if (distancePixel(objets[k][l], p) <= 60) {
                                objets[k][length(objets[k], 50)] = p;
                                ajout = 1;
                                break;
                            }
                        }
                    }
                    if (!ajout && nbObjets < 20) {
                        objets[nbObjets][0] = p;
                        nbObjets++;
                    }
                }
            }
        }
    }

    // Suppression des petits objets
    for (int k = 0; k < nbObjets; k++) {
        if (length(objets[k], 50) <= 10) {
            for (int m = k; m < nbObjets - 1; m++) {
                memcpy(objets[m], objets[m + 1], sizeof(objets[m]));
            }
            nbObjets--;
            k--;
        }
    }

    printf("Il y a %d objets\n", nbObjets);
    for (int k = 0; k < nbObjets; k++) {
        for (int l = 0; l < length(objets[nbObjets], 50); l++) {    
            printf("%d,%d ",objets[k][l].x,objets[k][l].y);
    
    }
    printf("\n");
    }

    printf("Couleur objet : %s",couleurPixel(objets[nbObjets][1].y,objets[nbObjets][1].x,longueur,largeur,rouge,vert,bleu));
    //printf("Nombre de pixels objet %d : ",length(objets[nbObjets],50));

    return 0;
}
