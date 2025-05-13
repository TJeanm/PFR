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


def parcourir_commande(commande_texte, numero_langue,historique_commandes):
    structure_commande = {"commande": "", "logiciel": "", "angle_distance": 0, "direction": "", "envoi": ""}
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
                                historique_commandes.append(structure_commande.copy())
                                structure_commande = {"commande": ligne[0], "logiciel": "", "angle_distance": 0,
                                                      "direction": "", "envoi": "", "vitesse": ""}

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

    historique_commandes.append(structure_commande)
    return historique_commandes


def executer_mouvement(historique_commandes):
    for i in range(1, len(historique_commandes)):
        print("traitement")
        print()
        print(historique_commandes[i])
        vitesse=(historique_commandes[i]["vitesse"]=='s')
        #print(vitesse)
        if historique_commandes[i]["commande"] == 'f':  # avancées ?

            if historique_commandes[i]["direction"] == 'l':  # avance gauche ?
                if vitesse:
                    historique_commandes[i]["envoi"]='r' #avance gauche rapide
                else:
                    historique_commandes[i]["envoi"] = 'a' #avance gauche

            elif historique_commandes[i]["direction"] == 'r':  # avance droite ?
                if vitesse:
                    historique_commandes[i]["envoi"]='y' #avance droite rapide
                else:
                    historique_commandes[i]["envoi"] = 'e' #avance droite

            else:                                           #avance normale ?
                if vitesse:
                    historique_commandes[i]["envoi"] = 't' # avance normale rapide
                else:
                    historique_commandes[i]["envoi"] = 'z'  # avance normale


        elif historique_commandes[i]["commande"] == 'b': # recule

            if historique_commandes[i]["direction"] == 'l': # recule gauche ?
                if vitesse:
                    historique_commandes[i]["envoi"] = 'v' #recule gauche rapide
                else:
                    historique_commandes[i]["envoi"] = 'w' # recule gauche

            elif historique_commandes[i]["direction"] == 'r': #recule droite ?
                if vitesse:
                    historique_commandes[i]["envoi"] = 'b' #recule droite rapide
                else:
                    historique_commandes[i]["envoi"] = 'x' #recule droite

            else:                                           #recule normale ?
                if vitesse:
                    historique_commandes[i]["envoi"] = 'g'    #recule normale rapide
                else : 
                    historique_commandes[i]["envoi"] = 's'    #recule normale


        elif historique_commandes[i]["commande"] == "t":      #tourner

            if historique_commandes[i]["direction"] == 'l':     #tourner à gauche ?
                if vitesse:
                    historique_commandes[i]["envoi"]='f'       #tourner à gauche rapide
                else:
                    historique_commandes[i]["envoi"] = 'q'      #tourner à gauche normale

            else:                                               #tourner à droite ?
                if vitesse:
                    historique_commandes[i]["envoi"]='h'        #tourner à droite rapide
                else:
                    historique_commandes[i]["envoi"] = 'd'      #tourner à droite

        elif historique_commandes[i]["commande"] == "c":        #faire demi-tour

            if historique_commandes[i]["direction"]=='l':       #faire demi-tour à gauche
                if vitesse:
                    historique_commandes[i]["envoi"]=='r'       #demi-tour gauche rapide
                else:
                    historique_commandes[i]["envoi"]="q"        #demi-tour gauche normal

            else:                                               #faire demi-tour à droite
                if vitesse:
                    historique_commandes[i]["envoi"]=='h'       #demi-tour droite rapide
                else : 
                    historique_commandes[i]["envoi"]="d"        #demi-tour droite normal  

        elif historique_commandes[i]["commande"]=='a':
            historique_commandes[i]=historique_commandes[i-1]  

        elif historique_commandes[i]["commande"]=="e":
            historique_commandes[i]["envoi"]='l'

        else:                                                   #si pas de commmande, on envoie arrêt
            historique_commandes[i]["envoi"]='m'


def executer_logiciel(structure_commande):
    pass



async def envoi_commandes(historique_commandes, com):

    for i in range(1,len(historique_commandes)):
        if historique_commandes[i]["commande"]!='e':
            
            delai=calculer_temps(historique_commandes[i])
            envoi=historique_commandes[i]["envoi"]
            if historique_commandes[i]["commande"]=='z':
                await envoi_zigzag(historique_commandes[i],com)
            else:
                await com.envoie_bluetooth(envoi)
                print(envoi)
                print("délai : ",delai)
                await asyncio.sleep(delai)
        else:
            break
    await com.envoie_bluetooth('m')


def calculer_temps(commande):
    if commande["commande"]=='f' or commande["commande"]=='b':
        if commande["angle_distance"]==0:
            print("durée avancée")
            return 1
        else:
            return commande["angle_distance"]
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

def test_arret(historique_commandes):
    for commande in historique_commandes:
        if commande["commande"]=='e':
            return True
    return False


async def main():
    com = communication()
    await com.init_HM10()
    historique_commandes=[]
    while True:
        if keyboard.is_pressed('l') or test_arret(historique_commandes):
            await com.envoie_bluetooth("m")
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
            historique_commandes=[]
            structure_commande=parcourir_commande(lire_commande_fichier(), numero, historique_commandes)
            print(structure_commande)
            executer_mouvement(historique_commandes)
        # envoi=historique_commandes[1]["envoi"]
            print(historique_commandes)

            #print(envoi)
            #com = communication()
            #await com.init_HM10()
            #await com.envoie_bluetooth('m')
            await envoi_commandes(historique_commandes, com)
        

if __name__ == "__main__":
    asyncio.run(main())