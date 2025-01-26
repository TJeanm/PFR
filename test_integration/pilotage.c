#include "pilotage.h"
#include <math.h>


// Compteur global pour suivre le nombre total d'actions
int compteur_actions = 0;

void configurer_terminal() {
    struct termios term;
    tcgetattr(STDIN_FILENO, &term);
    term.c_lflag &= ~(ICANON | ECHO); // Désactiver le mode canonique et l'écho
    tcsetattr(STDIN_FILENO, TCSANOW, &term);
}

void reinitialiser_terminal() {
    struct termios term;
    tcgetattr(STDIN_FILENO, &term);
    term.c_lflag |= (ICANON | ECHO); // Réactiver le mode canonique et l'écho
    tcsetattr(STDIN_FILENO, TCSANOW, &term);
}

// Fonction pour ajouter un mouvement dans l'historique et le fichier CSV
void ajouter_mouvement(const char *mouvement, const char *description, int valeur) {
    FILE *fichier = fopen("Histo.txt", "a");
    if (!fichier) {
        perror("Erreur lors de l'ouverture du fichier historique");
        exit(EXIT_FAILURE);
    }

    time_t maintenant = time(NULL);
    fprintf(fichier, ">> %s : %s", description, ctime(&maintenant));
    fclose(fichier);

    FILE *fichier_csv = fopen("Log_Deplacements.csv", "a");
    if (!fichier_csv) {
        perror("Erreur lors de l'ouverture du fichier CSV");
        exit(EXIT_FAILURE);
    }

    compteur_actions++;
    fprintf(fichier_csv, "%s, %d, %d\n", mouvement, valeur, compteur_actions);
    fclose(fichier_csv);
}

// Fonction pour calculer les nouvelles coordonnées après un mouvement
void calculer_nouvelles_coordonnees(int *x, int *y, int angle, int valeur) {
    *x += round(cos(angle * M_PI / 180) * valeur);
    *y -= round(sin(angle * M_PI / 180) * valeur);
}

// Fonction pour lire une touche instantanément
char lire_touche() {
#ifdef _WIN32
    return _getch(); // Lecture instantanée sous Windows
#else
    char touche;
    read(STDIN_FILENO, &touche, 1); // Lecture instantanée sous Linux/macOS
    return touche;
#endif
}

// Fonction de gestion du pilotage manuel
void pilotage_manuel() {
    int x = 10, y = 10;
    int angle = 0;

#ifndef _WIN32
    configurer_terminal(); // Configurer le terminal en mode non-bloquant (Linux/macOS)
#endif

    printf("Commandes: z (avancer), s (reculer), q (tourner à gauche), d (tourner à droite), x (quitter)\n");
    char touche='a';
    while (touche!='x') {
        touche = lire_touche(); // Lire une touche instantanément
        printf("%c",touche);


        switch (touche) {
            case 'z':
                calculer_nouvelles_coordonnees(&x, &y, angle, 1);
                ajouter_mouvement("Avancer", "Le robot avance", 1);
                break;

            case 's':
                calculer_nouvelles_coordonnees(&x, &y, angle, -1);
                ajouter_mouvement("Reculer", "Le robot recule", 1);
                break;

            case 'q':
                angle = (angle + 45) % 360;
                ajouter_mouvement("Tourner à gauche", "Le robot tourne à gauche", 45);
                break;

            case 'd':
                angle = (angle - 45 + 360) % 360;
                ajouter_mouvement("Tourner à droite", "Le robot tourne à droite", 45);
                break;

            case 'x':
                printf("Fin de la simulation.\n");


#ifndef _WIN32
                reinitialiser_terminal(); // Réinitialiser le terminal (Linux/macOS)
#endif
              //  return;
                break;

            default:
                break;
        }

        printf("Position actuelle: (%d, %d)\n", x, y);
        printf("Angle actuel: %d degrés\n", angle);
    }
}