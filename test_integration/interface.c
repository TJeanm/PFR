#include "interface.h"
#include "pilotage.h"
#include "Commande_vocal.h"

const char *nom_fichier = "mdp.txt";
int nombre_tentatives =0;
int mdp;



int appel(){
    int nombre;
    scanf("%d",&nombre);
    return nombre;
}



#define TAILLE_MAX 10

int verif_mdp(const char *nom_fichier) {
    char mdp_utilisateur[TAILLE_MAX];
    char mdp_fichier[TAILLE_MAX];
    FILE *fichier;

    printf("Entrez le mot de passe : ");
    scanf("%s", mdp_utilisateur);

    fichier = fopen(nom_fichier, "r");
    if (fichier == NULL) {
        printf("Erreur : impossible d'ouvrir le fichier.\n");
        return 0;
    }

    // Lecture du mot de passe stocké dans le fichier
    if (fgets(mdp_fichier, TAILLE_MAX, fichier) == NULL) {
        printf("Erreur : impossible de lire le fichier.\n");
        fclose(fichier);
        return 0;
    }

    // Retirer le caractère de nouvelle ligne '\n' si présent
    mdp_fichier[strcspn(mdp_fichier, "\n")] = '\0';

    fclose(fichier);

    // Comparaison des deux mots de passe
    if (strcmp(mdp_utilisateur, mdp_fichier) == 0) {
        printf("Mot de passe correct !\n");
        return 1;
    } else {
        printf("Mot de passe incorrect.\n");
        return 0;
    }
    
}



void menu_principal(){
    
    printf("Que souhaitez vous faire ? \n 0 : Quitter \n 1 : Mode utilisateur \n 2 : Mode administrateur \n");
    int a=appel();
    switch (a){
        case 0:
            printf("Sortie du programme\n");
            exit(0);
        case 1 :
            mode_utilisateur();
            break;

        case 2 :
            mode_administrateur();
            break;
    }
}

void mode_administrateur (){
    mdp= verif_mdp(nom_fichier);
            switch (mdp){
                case 0 : 
                    nombre_tentatives+=1;
                    if (nombre_tentatives<3){
                    mode_administrateur();
                    }else{
                    printf("Nombre maximal de tentatives atteintes, retour au menu principal\n");
                    menu_principal();
                }
                case 1 :
                    nombre_tentatives=0;
                    actions_administrateur();
            
    
}
}

void mode_utilisateur(){
    printf("Quel mode de commande souhaitez vous ? \n 0 : Quitter \n 1 : Retour \n 2 : Mode manuel \n 3 : Mode vocal \n 4 : Mode automatique \n");
    int utilisateur =appel();
    switch (utilisateur){
        case 0:
            printf("Sortie du programme");
            exit(0);
        case 1:
            menu_principal();
            break;
        case 2:
            mode_manuel();
            break;
        case 3:
            mode_vocal();
            break;
        case 4:
            mode_auto();
            break;
    }
}

void actions_administrateur(){
    printf("Que souhaitez vous faire ? \n 0 : Quitter \n 1 : Retour \n 2 : Changer le mot de passe \n 3 : Changer les paramètres du mode vocal \n 4 : Changer les paramètres du mode manuel \n");
    int utilisateur =appel();
    switch (utilisateur){
        case 0:
            printf("Sortie du programme");
            exit(0);
        case 1:
            menu_principal();
            break;
        case 2:
            modif_mdp(nom_fichier);
            break;
        case 3:
            modif_mode_vocal();
            break;
        case 4:
            modif_mode_manuel();
            break;
    }
}

void modif_mdp(const char *nom_fichier) {
    
    char nouveau_mdp[10];
    FILE *fichier;

    printf("Pour modifier le mot de passe, ");
    verif_mdp(nom_fichier);
    printf("Entrez le nouveau mot de passe : ");
    scanf("%9s", nouveau_mdp);

    // Ouvrir le fichier en mode écriture
    fichier = fopen(nom_fichier, "w");
    if (fichier == NULL) {
        printf("Erreur : impossible d'ouvrir le fichier.\n");
        return;
    }

    // Écrire le nouveau mot de passe dans le fichier
    fprintf(fichier, "%s\n", nouveau_mdp);

    // Fermer le fichier
    fclose(fichier);

    printf("Mot de passe modifié avec succès.\n");
}

void modif_mode_vocal(){
}

void modif_mode_manuel(){
}

void mode_manuel() {
    pilotage_manuel();
    simulation();
    menu_principal();
}

void mode_vocal(){
    printf("Début des tests\n\n");
    commande_vocal();
    printf("\nFin des tests\n");
}

void mode_auto(){
}
