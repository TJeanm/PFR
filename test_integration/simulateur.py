import turtle
import csv

# Fonction pour lire les mouvements depuis le fichier CSV
def lire_mouvements():
    mouvements = []
    try:
        with open('Log_Deplacements.csv', 'r') as fichier_csv:
            csv_reader = csv.reader(fichier_csv)
            next(csv_reader)  # Passer l'en-tête
            for row in csv_reader:
                mouvements.append(row)
    except FileNotFoundError:
        print("Le fichier Log_Deplacements.csv n'existe pas.")
    return mouvements

# Fonction pour simuler les déplacements du robot avec Turtle
def simuler_mouvements():
    screen = turtle.Screen()
    screen.setup(width=600, height=600)
    screen.title("Simulation de Robot avec Turtle")
    
    robot = turtle.Turtle()
    robot.shape("turtle")
    robot.speed(1)

    mouvements = lire_mouvements()

    for mouvement in mouvements:
        action, valeur, compteur = mouvement
        valeur = int(valeur)  # Convertir la valeur en entier

        if action == "Avancer":
            robot.forward(valeur * 10)  # Avancer selon la valeur
        elif action == "Reculer":
            robot.backward(valeur * 10)  # Reculer selon la valeur
        elif action == "Tourner à gauche":
            robot.left(45)  # Tourner à gauche
        elif action == "Tourner à droite":
            robot.right(45)  # Tourner à droite

    turtle.done()

# Lancer la simulation
if __name__ == "__main__":
    simuler_mouvements()
