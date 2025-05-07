import csv

from turtle import*

historique_commandes=[]


def lire_commande_fichier():

    fichier_path = "ligne_vocal.txt"
    try:
        with open(fichier_path, "r", encoding="utf-8") as fichier:
            print("le fichier a bien été ouvert.")
            #for ligne in fichier : 
             #   print(ligne)
            for ligne in fichier : 
                commande = ligne.split()
            print(commande)
            return commande
    except FileNotFoundError:
        print("Erreur : fichier ligne_vocal.txt introuvable.")
        return



def parcourir_commande(commande_texte) :

    structure_commande={"commande":"","logiciel":"","angle_distance":0,"direction":"","envoi":""}
    fichier_path = "liste_commande_vocal_v2.csv"
    try:
        with open(fichier_path, "r", encoding="utf-8") as fichier:
            reader = csv.reader(fichier, delimiter=',')

            for mot in commande_texte:
                print(mot)
                #on teste si le mot est un nombre
                if mot.isdigit():
                    print("nombre détécté")
                    structure_commande["angle_distance"]=int(mot)
                else :
                    fichier.seek(0) #on remet le curseur de lecture au début du fichier
                    #on teste si le mot est une commande
                    for ligne in reader:
                        if ligne[2]==mot:
                            print("mot détécté")
                            if ligne[1]=="commande":
                                print("commande detectee")
                                structure_commande["commande"]=ligne[0]
                            elif ligne[1]=="logiciel":
                                structure_commande["logiciel"]=ligne[0]
                            
                            elif ligne[1]=="direction":
                                structure_commande["direction"]=ligne[0]

    except FileNotFoundError:
        print("Erreur : fichier ligne_vocal.txt introuvable.")
        return
    
    historique_commandes.append(structure_commande)
    return structure_commande

def ecrire_fichier(structure_commande):
    return

def executer_commande(structure_commande):
    if structure_commande["commande"]!="":
        exectuer_mouvement(structure_commande)
    if structure_commande["logiciel"]!="":
        executer_logiciel(structure_commande)



def executer_mouvement(structure_commande):
    print("test")
    if structure_commande["commande"]=='f':
        if structure_commande["direction"]=='l':
            structure_commande["envoi"]='a'
        elif structure_commande["direction"]=='r':
            structure_commande["envoi"]='e'
        else:
            structure_commande["envoi"]='z'

    elif structure_commande["commande"]=='b':
        if structure_commande["direction"]=='l':
            structure_commande["envoi"]='w'
        elif structure_commande["direction"]=='r':
            structure_commande["envoi"]='x'
        else:
            structure_commande["envoi"]='s'
    
    else:
        print("test2")
        if structure_commande["direction"]=='l':
            structure_commande["envoi"]='q'
        elif structure_commande["direction"]=='r':
            structure_commande["envoi"]='d'


    mots=[structure_commande["commande"],structure_commande["angle_distance"],structure_commande["logiciel"]]
    with open("envoi_commande.csv", "w", newline="", encoding="utf-8") as fichier_csv:
        writer = csv.writer(fichier_csv, delimiter=';')  # Tu peux changer le délimiteur
        writer.writerow(mots)  # Écrit tous les mots dans une seule ligne (1 ligne, plusieurs colonnes)

def exectuter_logiciel():
    return



structure_commande=parcourir_commande(lire_commande_fichier())

print(structure_commande)

executer_mouvement(structure_commande)

print(structure_commande)