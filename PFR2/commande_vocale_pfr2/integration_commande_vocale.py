import speech_recognition as sr
import pyaudio
from gtts import gTTS


#récupération de l'instruction

def lire_choix_langue(fichier_choix):
    try:
        with open(fichier_choix, "r", encoding="utf-8") as fichier:
            lignes = fichier.readlines()
            if len(lignes) >= 2:
                # Le numéro de la langue est la première ligne et le nom de la langue est la deuxième
                numero_langue = lignes[0].strip()
                nom_langue = lignes[1].strip()
                return numero_langue, nom_langue
            else:
                print("Fichier de choix langue incomplet.")
                return None, None
    except FileNotFoundError:
        print(f"Fichier '{fichier_choix}' introuvable.")
        return None, None

def obtenir_code_langue(nom_langue):
    # Prend les deux premières lettres du nom de la langue
    prefixe = nom_langue[:2].lower()  # Minuscule
    return f"{prefixe}-{prefixe.upper()}"  # Forme ISO dynamique (ex. "fr-FR", "en-EN")

def ecrire_commande_fichier(commande,fich):
    with open(fich, "w", encoding="utf-8") as fichier:
        fichier.write(commande + "\n")

numero, langue = lire_choix_langue("choix_langue.txt")
code_langue = obtenir_code_langue(langue)
print(f"Langue choisie : {langue} (code : {code_langue})")


#print(sr.Microphone.list_microphone_names())

try :
    r = sr.Recognizer()
    micro = sr.Microphone()
    with micro as source:
        print("Speak!")
        audio_data = r.listen(source)
        print("End!")
        
    result = r.recognize_google(audio_data, language=code_langue)
    ecrire_commande_fichier(result,"ligne_vocal.txt")
    print ("Vous avez dit : ", result)
except Exception as e : 
    print("pb")






#traitement

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



def exectuter_logiciel():
    return



structure_commande=parcourir_commande(lire_commande_fichier())

print(structure_commande)

executer_mouvement(structure_commande)

ecrire_commande_fichier(structure_commande["envoi"],"envoi_commande.txt")

print(structure_commande)