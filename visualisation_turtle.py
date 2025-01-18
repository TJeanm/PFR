from turtle import*
import csv

screen=Screen()


with open('nom_fichier_csv', 'r') as file:
    reader = csv.reader(file, delimiter=';')
    index=0
    for row in reader:
        print(row)
        fonction_a_executer=row[0]

        distance_angle=int(row[1])

        index=int(row[2])

        print(fonction_a_executer)
        print(distance_angle)
        print(index)

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