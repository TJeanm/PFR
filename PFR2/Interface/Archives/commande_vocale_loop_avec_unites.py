import keyboard
import asyncio
from communication_HM10 import communication
import csv
import os
import sys
import speech_recognition as sr
import pyaudio
from gtts import gTTS


def lire_choix_langue(fichier_choix):
    try:
        with open(fichier_choix, "r", encoding="utf-8") as fichier:
            contenu = fichier.read()
            lignes = contenu.splitlines()
            if len(lignes) >= 2:
                # Le numéro de la langue est la première ligne et le nom de la langue est la deuxième
                return lignes[0].strip(), lignes[1].strip()
            else:
                print("Fichier de choix langue incomplet.")
                return lignes[0], lignes[1]
    except FileNotFoundError:
        print(f"Fichier introuvable : {fichier_choix}")
        return None, None


def obtenir_code_langue(nom_langue):
    if not nom_langue or len(nom_langue) < 2:
        raise ValueError(f"Nom de langue invalide : {nom_langue!r}")
    prefixe = nom_langue[:2].lower()
    return f"{prefixe}-{prefixe.upper()}"


def ecrire_commande_fichier(commande, fich):
    print(commande)
    with open(fich, "w", encoding="utf-8") as fichier:
        fichier.write(commande + "\n")


def lire_commande_fichier():
    # calcul du chemin de ligne_vocal.txt comme frère de Programmes
    base_dir = os.path.dirname(__file__)
    interface_dir = os.path.abspath(os.path.join(base_dir, os.pardir))
    fichier_path = os.path.join(interface_dir, "Casse_Noisette", "ligne_vocal.txt")
    # fichier_path="ligne_vocal.txt"
    try:
        with open(fichier_path, "r", encoding="utf-8") as fichier:
            print("Le fichier a bien été ouvert.")
            lignes = fichier.read().split()
            if not lignes:
                print("Le fichier de commande est vide.")
                return []
            return lignes
    except FileNotFoundError:
        print(f"Erreur : fichier {fichier_path} introuvable.")
        return []


def parcourir_commande(commande_texte, numero_langue,liste_commandes):
    structure_commande = {"commande": "", "logiciel": "", "angle_distance": 0, "direction": "", "envoi": "", "vitesse":"", "unité":""}
    fichier_csv = os.path.join(os.path.dirname(__file__), os.pardir, "Casse_Noisette", "liste_commande_vocale.csv")
    #fichier_path = "liste_commande_vocale.csv"
    try:
        with open(fichier_csv, "r", encoding="utf-8") as fichier:
            reader = csv.reader(fichier, delimiter=';')

            for mot in commande_texte:
                print(mot)
                # on teste si le mot est un nombre
                if mot.isdigit():
                    print("nombre détécté")
                    structure_commande["angle_distance"] = int(mot)
                else:
                    fichier.seek(0)  # on remet le curseur de lecture au début du fichier
                    # on teste si le mot est une commande
                    for ligne in reader:
                        if ligne[int(numero_langue) + 1] == mot:
                            print("mot détécté")
                            if ligne[1] == "commande":
                                print("commande detectee")
                                liste_commandes.append(structure_commande.copy())
                                structure_commande = {"commande": ligne[0], "logiciel": "", "angle_distance": 0,
                                                      "direction": "", "envoi": "", "vitesse": "", "unité": ""}

                          #  elif ligne[1] == "logiciel":
                           #     structure_commande["logiciel"] = ligne[0]

                            elif ligne[1] == "direction":
                                structure_commande["direction"] = ligne[0]

                            elif ligne[1] == "vitesse":
                                structure_commande["vitesse"] = ligne[0]

                            elif ligne[1] == "unité":
                                structure_commande["unité"] = ligne[0]

    except FileNotFoundError:
        print("Erreur : fichier ligne_vocal.txt introuvable.")
        return

    liste_commandes.append(structure_commande)
    return liste_commandes


def executer_mouvement(liste_commandes,historique_commandes):
    for i in range(1, len(liste_commandes)):
        print("traitement")
        print()
        print(liste_commandes[i])
        vitesse=(liste_commandes[i]["vitesse"]=='s')
        #print(vitesse)
        if liste_commandes[i]["commande"] == 'f':  # avancées ?

            if liste_commandes[i]["direction"] == 'l':  # avance gauche ?
                if vitesse:
                    liste_commandes[i]["envoi"]='r' #avance gauche rapide
                else:
                    liste_commandes[i]["envoi"] = 'a' #avance gauche

            elif liste_commandes[i]["direction"] == 'r':  # avance droite ?
                if vitesse:
                    liste_commandes[i]["envoi"]='y' #avance droite rapide
                else:
                    liste_commandes[i]["envoi"] = 'e' #avance droite

            else:                                           #avance normale ?
                if vitesse:
                    liste_commandes[i]["envoi"] = 't' # avance normale rapide
                else:
                    liste_commandes[i]["envoi"] = 'z'  # avance normale


        elif liste_commandes[i]["commande"] == 'b': # recule

            if liste_commandes[i]["direction"] == 'l': # recule gauche ?
                if vitesse:
                    liste_commandes[i]["envoi"] = 'v' #recule gauche rapide
                else:
                    liste_commandes[i]["envoi"] = 'w' # recule gauche

            elif liste_commandes[i]["direction"] == 'r': #recule droite ?
                if vitesse:
                    liste_commandes[i]["envoi"] = 'b' #recule droite rapide
                else:
                    liste_commandes[i]["envoi"] = 'x' #recule droite

            else:                                           #recule normale ?
                if vitesse:
                    liste_commandes[i]["envoi"] = 'g'    #recule normale rapide
                else : 
                    liste_commandes[i]["envoi"] = 's'    #recule normale


        elif liste_commandes[i]["commande"] == "t":      #tourner

            if liste_commandes[i]["direction"] == 'l':     #tourner à gauche ?
                if vitesse:
                    liste_commandes[i]["envoi"]='f'       #tourner à gauche rapide
                else:
                    liste_commandes[i]["envoi"] = 'q'      #tourner à gauche normale

            else:                                               #tourner à droite ?
                if vitesse:
                    liste_commandes[i]["envoi"]='h'        #tourner à droite rapide
                else:
                    liste_commandes[i]["envoi"] = 'd'      #tourner à droite

        elif liste_commandes[i]["commande"] == "c":        #faire demi-tour

            if liste_commandes[i]["direction"]=='l':       #faire demi-tour à gauche
                if vitesse:
                    liste_commandes[i]["envoi"]=='r'       #demi-tour gauche rapide
                else:
                    liste_commandes[i]["envoi"]="q"        #demi-tour gauche normal

            else:                                               #faire demi-tour à droite
                if vitesse:
                    liste_commandes[i]["envoi"]=='h'       #demi-tour droite rapide
                else : 
                    liste_commandes[i]["envoi"]="d"        #demi-tour droite normal  

        elif liste_commandes[i]["commande"]=='a':
            print("commande précédente : ", historique_commandes[-1])
            for commande in historique_commandes[-1]:
                liste_commandes.append(commande)

        elif liste_commandes[i]["commande"]=="e":
            liste_commandes[i]["envoi"]='l'

        else:                                                   #si pas de commmande, on envoie arrêt
            liste_commandes[i]["envoi"]='m'


def executer_logiciel(structure_commande):
    pass

#def enregistrer_trajectoire(liste_commandes,historique_commandes)


async def envoi_commandes(liste_commandes, com):

    for i in range(1,len(liste_commandes)):
        if liste_commandes[i]["commande"]!='e':
            
            delai=calculer_temps(liste_commandes[i])
            envoi=liste_commandes[i]["envoi"]
            if liste_commandes[i]["commande"]=='z':
                await envoi_zigzag(liste_commandes[i],com)
            else:
                await com.envoie_bluetooth(envoi)
                print(envoi)
                print("délai : ",delai)
                await asyncio.sleep(delai)
        else:
            break
    await com.envoie_bluetooth('m')


def calculer_temps(commande):
    diviseur=1
    print("unité délai : ", commande["unité"])
    if commande["unité"]=='cm':
        diviseur=100
        print("diviseur cm : ",diviseur)
    if commande["commande"]=='f' or commande["commande"]=='b':
        if commande["angle_distance"]==0:
            print("durée avancée")
            print("durée : ",1/diviseur)
            return 1
        else:
            return commande["angle_distance"]/diviseur
    elif commande["commande"]=='t':
        return 0.5
    elif commande["commande"]=='c':
        return 2.3
    else:
        return commande["angle_distance"] #a modifier

async def envoi_zigzag(commande_zigzag,com):
    nb_zigzag=commande_zigzag["angle_distance"]
    if nb_zigzag==0:
        if commande_zigzag["direction"]=='l':
            await com.envoie_bluetooth('z')
            await asyncio.sleep(0.7)
            await com.envoie_bluetooth('q')
            await asyncio.sleep(0.5)
            await com.envoie_bluetooth('z')
            await asyncio.sleep(0.7)
            await com.envoie_bluetooth('d')
            await asyncio.sleep(0.5)
            await com.envoie_bluetooth('z')
            await asyncio.sleep(0.5)
        else:
            await com.envoie_bluetooth('z')
            await asyncio.sleep(0.7)
            await com.envoie_bluetooth('d')
            await asyncio.sleep(0.5)
            await com.envoie_bluetooth('z')
            await asyncio.sleep(0.7)
            await com.envoie_bluetooth('q')
            await asyncio.sleep(0.5)
            await com.envoie_bluetooth('z')
            await asyncio.sleep(0.5)
    else:
        for i in range(nb_zigzag):
            if commande_zigzag["direction"]=='l':
                await com.envoie_bluetooth('z')
                await asyncio.sleep(0.7)
                await com.envoie_bluetooth('q')
                await asyncio.sleep(0.5)
                await com.envoie_bluetooth('z')
                await asyncio.sleep(0.7)
                await com.envoie_bluetooth('d')
                await asyncio.sleep(0.5)
                await com.envoie_bluetooth('z')
                await asyncio.sleep(0.5)
            else:
                await com.envoie_bluetooth('z')
                await asyncio.sleep(0.7)
                await com.envoie_bluetooth('d')
                await asyncio.sleep(0.5)
                await com.envoie_bluetooth('z')
                await asyncio.sleep(0.7)
                await com.envoie_bluetooth('q')
                await asyncio.sleep(0.5)
                await com.envoie_bluetooth('z')
                await asyncio.sleep(0.5)
#3024

def test_arret(liste_commandes):
    for commande in liste_commandes:
        if commande["commande"]=='e':
            return True
    return False


async def main():
    com = communication()
    await com.init_HM10()
    await com.envoie_bluetooth("i")
    liste_commandes=[]
    historique_commandes=[]
    while True:
        if keyboard.is_pressed('l') or test_arret(liste_commandes):
            await com.envoie_bluetooth("p")
            await com.envoie_bluetooth("m")
            await com.close()
            break

        # calcul du chemin de choix_langue.txt comme frère de Programmes
        base_dir = os.path.dirname(__file__)
        interface_dir = os.path.abspath(os.path.join(base_dir, os.pardir))
        chemin = os.path.join(interface_dir, "Casse_Noisette", "choix_langue.txt")
        #chemin = "choix_langue.txt"

        numero, langue = lire_choix_langue(os.getcwd() + "\\Casse_Noisette\\choix_langue.txt")
        print(lire_choix_langue(chemin))
        print(numero)
        if langue is None:
            sys.exit(1)

        code_langue = obtenir_code_langue(langue)
        print(f"Langue choisie : {langue} (code : {code_langue})")


        try:
            r = sr.Recognizer()
            micro = sr.Microphone()
            with micro as source:
                print("Speak!")
                audio_data = r.listen(source)
                print("End!")

            result = r.recognize_google(audio_data, language=code_langue)
            # écriture du résultat dans ligne_vocal.txt
            ligne_vocal = os.path.join(interface_dir, "Casse_Noisette", "ligne_vocal.txt")
            ecrire_commande_fichier(result, ligne_vocal)
            print("Vous avez dit :", result)
            new_reco = 1
        except Exception:
            print("Problème reconnaissance vocale")
            new_reco = 0

        if new_reco :
            liste_commandes=[]
            structure_commande=parcourir_commande(lire_commande_fichier(), numero, liste_commandes)
            print(structure_commande)
            executer_mouvement(liste_commandes,historique_commandes)
            print("liste_commandes : ",liste_commandes)
            await envoi_commandes(liste_commandes, com)
            historique_commandes.append(liste_commandes)
        

if __name__ == "__main__":
    asyncio.run(main())