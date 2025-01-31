#Marius Pinard, le mardi 7 janvier 2025
#script python qui lit dans un fichier csv afin d'effectuer la visualisation turtle


from turtle import*
import csv

screen=Screen()


with open("commande_vocale/Transmission_to_simulation.csv", 'r') as file:
    reader = csv.reader(file, delimiter=';') #on lit dans le fichier
    index=0
    for row in reader: #on parcourt les lignes
        print(row)
        fonction_a_executer=row[0] #on enregistre la commande

        distance_angle=int(row[1]) #on enregistre la distance ou l'angle

        index=int(row[2])

        print(fonction_a_executer)
        print(distance_angle)
        print(index)
# ces conditions permettent d'exécuter la bonne commande turtle
        if fonction_a_executer == "avancer":
            forward(distance_angle)

            print("test avancer")

        if fonction_a_executer=="tourner a gauche":
            left(distance_angle)

            print("test tourner à gauche")

        if fonction_a_executer=="tourner a droite":
            right(distance_angle)

            print("test tourner a droite")

done()
