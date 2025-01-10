#include<stdio.h>
#include<string.h>

#define MAX_MOTS 5
#define MAX_LETTRES 20

char COMMANDE[MAX_MOTS][MAX_LETTRES] = {
    "Avance de",
    "Tourne à droite",
    "Tourne à gauche",
    "Fin"
};


void test_switch()
{
    int res;

    printf("Selectionner une commande à exécuter : ");

    scanf("%d", &res);

    switch(res) {

    case 1 :
        printf("Test 1");
        break;

    case 2 :
        printf("Test 2");
        break;

    case 3 :
        printf("Test 3");
        break;

    case 4 :
        printf("Test 4");
        break;

    case 5 :
        printf("Test 5");
    }
}

int char_to_tab(char chaine[], char mots[20][20])
{
    int i = 0;
    int nbmot = 0;
    int nbchar = 0;

    while (chaine[i] != '\0') {
        if (chaine[i] != ' ') { // Vérifie s'il y a un espace
            mots[nbmot][nbchar] = chaine[i]; // Ajoute le charactere
            nbchar++;
        } else {
            mots[nbmot][nbchar] = '\0'; // Fini le mot et passe au suivant
            nbmot++;
            nbchar = 0;
        }
        i++;
    }
    return nbmot;
}

void affiche_liste_mots(char listeMots[20][20], int nbmot)
{
    printf("Liste des mots : \n");
    for (int i = 0; i <= nbmot; i++) {
        printf("%s\n", listeMots[i]);
    }
    printf("\n\n");
}

void selectionCommande(char listeMots[20][20])
{
    char test[20];
    printf("%s\n", COMMANDE);

    printf("%s", listeMots[0]);
    printf(" %s\n", listeMots[1]);

    test = listeMots[0];
    printf("%s", test);

    if (test == COMMANDE) {
        printf("test ok");
    }
}


int main()
{
    printf("Hello worldddd! \n");

    char chaine_test[] = "Avance de 20 centimètres";
    printf("%s\n\n", chaine_test);


    int nbmot;
    char motsTab[20][20];
    nbmot = char_to_tab(chaine_test, motsTab);
    affiche_liste_mots(motsTab, nbmot);
    affiche_liste_mots(COMMANDE, MAX_MOTS-1);

    char commande[3][20];
    selectionCommande(motsTab);
}