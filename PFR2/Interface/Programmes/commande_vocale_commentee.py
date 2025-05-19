import keyboard
import asyncio
from communication_HM10 import communication
import csv
import os
import sys
import speech_recognition as sr
import pyaudio
from gtts import gTTS


def lire_choix_langue(fichier_choix): #récupère la langue
    try:    #tentative d'ouverture du fichier
        with open(fichier_choix, "r", encoding="utf-8") as fichier:
            contenu = fichier.read()
            lignes = contenu.splitlines()
            if len(lignes) >= 2:
                # Le numéro de la langue est la première ligne et le nom de la langue est la deuxième
                return lignes[0].strip(), lignes[1].strip()
            else:
                print("Fichier de choix langue incomplet.")
                return lignes[0], lignes[1]
    except FileNotFoundError: #si l'ouverture du fichier est impossible
        print(f"Fichier introuvable : {fichier_choix}")
        return None, None


def obtenir_code_langue(nom_langue): #récupère le code de la langue, utile pour la reconnaissance vocale
    if not nom_langue or len(nom_langue) < 2:
        raise ValueError(f"Nom de langue invalide : {nom_langue!r}")
    prefixe = nom_langue[:2].lower()
    return f"{prefixe}-{prefixe.upper()}"

def recuperer_audio(code_langue): #transforme les paroles de l'utilisateur en liste
    try:    #tentative d'écoute
        r = sr.Recognizer()
        micro = sr.Microphone()
        with micro as source:
            print("Speak!")
            audio_data = r.listen(source) #écoute
            print("End!")

        result = r.recognize_google(audio_data, language=code_langue) #analyse et transformation en phrase
        phrase=result.split()   #transformation de la phrase en liste
        print("Vous avez dit :", result) #affichage de la phrase de l'utilisateur
        return 1,phrase
    except Exception:
        print("Problème reconnaissance vocale")
        return 0,None


def parcourir_commande(commande_texte, numero_langue,liste_commandes):      #premier traitement, remplissage du dictionnaire

    structure_commande = {"commande": "", "distance": 0, "direction": "", "envoi": "", "vitesse":"", "unité":""}  #création d'un dictionnaire avec toutes les infos nécessaires pour chaque commande
    fichier_csv = os.path.join(os.path.dirname(__file__), os.pardir, "Casse_Noisette", "liste_commande_vocale.csv")
    #fichier_path = "liste_commande_vocale.csv"
    try: #tentative d'ouverture du fichier csv
        with open(fichier_csv, "r", encoding="utf-8") as fichier:
            reader = csv.reader(fichier, delimiter=';')

            for mot in commande_texte:      #on parcourt chaque mot de la commande
                if mot.isdigit():# on teste si le mot est un nombre
                    structure_commande["distance"] = int(mot) #on ajoute la donnée dans le dictionnaire
                else:
                    fichier.seek(0)  # on remet le curseur de lecture au début du fichier

                    for ligne in reader: # on traite maintenant les mots
                        if ligne[int(numero_langue) + 1] == mot: #on parcourt la colonne du fichier csv qui correspond à la bonne langue
                            if ligne[1] == "commande": # on teste si le mot est une commande (ex : avant)
                                liste_commandes.append(structure_commande.copy()) #on passe à une nouvelle commande, donc on ajoute la précédente à la liste de commandes
                                structure_commande = {"commande": ligne[0], "distance": 0, "direction": "", "envoi": "", "vitesse": "", "unité": ""}
                                #on initialise un nouveau dictionnaire et on remplit la clé "commande"
                            elif ligne[1] == "direction": #on teste si le mot est une direction (ex : droite)
                                structure_commande["direction"] = ligne[0] #on remplit la clé "direction" du dictionnaire

                            elif ligne[1] == "vitesse":  # on teste si le mot est un mot relatif à la vitesse (ex: rapidement)
                                structure_commande["vitesse"] = ligne[0] #on remplit la clé "vitesse" du dictionnaire

                            elif ligne[1] == "unité": # on teste si le mot est une unité (ex: cm)
                                structure_commande["unité"] = ligne[0]  #on remplit la clé "unité" du dictionnaire

    except FileNotFoundError: # échec de l'ouverture du fichier csv
        print("Erreur : fichier ligne_vocal.txt introuvable.")
        return

    liste_commandes.append(structure_commande) #on ajoute le dernier dictionnaire rempli à la liste de commandes
    return liste_commandes  #on renvoie la liste des commandes


def executer_mouvement(liste_commandes,historique_commandes): #suite du traitement, à partir des dictionnaires remplis précédemment

    for i in range(1, len(liste_commandes)): #on parcourt tous les dictionnaires

        vitesse=(liste_commandes[i]["vitesse"]=='s') #boolean qui se répétait

        #on traite tous les cas possibles et on met le bon caractère d'envoi dans le dictionnaire
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

        elif liste_commandes[i]["commande"]=='a':           # commande "encore"
            for commande in historique_commandes[-1]:       #on ajoute la (ou les) commande précédente à la liste 
                liste_commandes.append(commande)

        elif liste_commandes[i]["commande"]=="e":           #on traite l'arrêt du programme
            liste_commandes[i]["envoi"]='l'

        else:                                                   #si pas de commmande, on envoie arrêt
            liste_commandes[i]["envoi"]='m'


async def envoi_commandes(liste_commandes, com):    #fonction d'envoi de la commande

    for i in range(1,len(liste_commandes)):     #on parcourt toutes les commandes
        if liste_commandes[i]["commande"]!='e':     #si ce n'est pas une commande d'arrêt
            
            delai=calculer_temps(liste_commandes[i])      #on calcule les délais pour les distances
            envoi=liste_commandes[i]["envoi"]             #on déclare la variable d'envoi
            if liste_commandes[i]["commande"]=='z':       #cas spéciaux
                await envoi_zigzag(liste_commandes[i],com)
            elif liste_commandes[i]["commande"]=='k':
                await envoi_carre(liste_commandes[i],com)
            else:                                         #si pas de cas spécial
                await com.envoie_bluetooth(envoi)         #envoi de la commande 
                await asyncio.sleep(delai)                #en cas de délai
        else:
            break
    await com.envoie_bluetooth('m')                       #on envoie arrêt à la fin des commandes


def calculer_temps(commande): #fonction qui calcule les délais pour les distances
    diviseur=1                #diviseur pour gérer les unités
    if commande["unité"]=='cm':
        diviseur=100
        print("diviseur cm : ",diviseur)

    if commande["commande"]=='f' or commande["commande"]=='b':      #délais avancer/reculer

        if not vitesse(commande):                                #si pas rapidement

            if commande["distance"]==0:                                 #si pas de distance
                print("durée avancée")
                print("durée : ",1/diviseur)
                return 1
            else:                                                       #si distance
                return commande["distance"]/diviseur
            
        else:                                                       #si rapidement
            if commande["distance"]==0:
                print("durée avancée")
                print("durée : ",1/diviseur*0.8)
                return 1
            else:
                return commande["distance"]/diviseur*0.8
            
    elif commande["commande"]=='t':                                 #délais tourner
        if not vitesse(commande):
            return 0.5
        else:
            return 0.4
        
    elif commande["commande"]=='c':
        if not vitesse(commande):
            return 2.3
        else:
            return 2
    
    else:
        return commande["distance"]


def vitesse(commande):      #fonction qui teste si la commande est rapide, pour éviter les répétitions
    return commande["vitesse"]=='s'

async def envoi_carre(commande_carree,com):     #fonction qui traite le carré
    if vitesse(commande_carree):                #si carré rapide
        if commande_carree["direction"]=='l':       #si carré à gauche
            for i in range(4):
                await com.envoie_bluetooth('t')
                await asyncio.sleep(0.6)
                await com.envoie_bluetooth('f')
                await asyncio.sleep(0.4)
        else:                                       #si carré à droite
            for i in range(4):
                await com.envoie_bluetooth('t')
                await asyncio.sleep(0.6)
                await com.envoie_bluetooth('h')
                await asyncio.sleep(0.4)
    else:                                       #si carré pas rapide
        if commande_carree["direction"]=='l':
            for i in range(4):
                await com.envoie_bluetooth('z')
                await asyncio.sleep(0.7)
                await com.envoie_bluetooth('q')
                await asyncio.sleep(0.65)
        else:
            for i in range(4):
                await com.envoie_bluetooth('z')
                await asyncio.sleep(0.7)
                await com.envoie_bluetooth('d')
                await asyncio.sleep(0.65)



async def envoi_zigzag(commande_zigzag,com):     #fonction qui traite le zigzag
    nb_zigzag=commande_zigzag["distance"]           #nombre de zigzag à effectuer

    if vitesse(commande_zigzag):                    #si zigzag rapide
        if nb_zigzag==0:                                #si un seul zigzag
            if commande_zigzag["direction"]=='l':           #si zigzag à gauche
                await com.envoie_bluetooth('t')
                await asyncio.sleep(0.6)
                await com.envoie_bluetooth('h')
                await asyncio.sleep(0.4)
                await com.envoie_bluetooth('t')
                await asyncio.sleep(0.6)
                await com.envoie_bluetooth('f')
                await asyncio.sleep(0.4)
                await com.envoie_bluetooth('t')
                await asyncio.sleep(0.4)
            else:                                           #si zigzag à droite
                await com.envoie_bluetooth('t')
                await asyncio.sleep(0.6)
                await com.envoie_bluetooth('h')
                await asyncio.sleep(0.4)
                await com.envoie_bluetooth('t')
                await asyncio.sleep(0.6)
                await com.envoie_bluetooth('f')
                await asyncio.sleep(0.4)
                await com.envoie_bluetooth('t')
                await asyncio.sleep(0.4)
        else:                                           #si plusieurs zigzags
            for i in range(nb_zigzag):
                if commande_zigzag["direction"]=='l':
                    await com.envoie_bluetooth('t')
                    await asyncio.sleep(0.6)
                    await com.envoie_bluetooth('f')
                    await asyncio.sleep(0.4)
                    await com.envoie_bluetooth('t')
                    await asyncio.sleep(0.6)
                    await com.envoie_bluetooth('h')
                    await asyncio.sleep(0.4)
                    await com.envoie_bluetooth('t')
                    await asyncio.sleep(0.4)
                else:
                    await com.envoie_bluetooth('t')
                    await asyncio.sleep(0.6)
                    await com.envoie_bluetooth('f')
                    await asyncio.sleep(0.4)
                    await com.envoie_bluetooth('t')
                    await asyncio.sleep(0.6)
                    await com.envoie_bluetooth('h')
                    await asyncio.sleep(0.4)
                    await com.envoie_bluetooth('t')
                    await asyncio.sleep(0.4)
        
    else:                                           #si zigzag rapide
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


def test_arret(liste_commandes):  #fonction qui teste l'arrêt du programme
    for commande in liste_commandes:
        if commande["commande"]=='e':       #on teste si le caratère "e" est dans le dictionnaire
            return True
    return False


async def main():         

    com = communication()       #initialisation de la communication et connexion au robot en bluetooth
    await com.init_HM10()       
    await com.envoie_bluetooth("i")
    liste_commandes=[]          #création de la liste des commandes
    historique_commandes=[]     #création de l'historique des commandes

    while True:                    #boucle principale
        if keyboard.is_pressed('l') or test_arret(liste_commandes):   #test de l'arrêt du programme
            await com.envoie_bluetooth("p")
            await com.envoie_bluetooth("m")
            await com.close()
            break

        numero_langue, langue = lire_choix_langue(os.getcwd() + "\\Casse_Noisette\\choix_langue.txt")   #récupération du numéro de la langue

        if langue is None: #si pas de langue renseignée
            sys.exit(1)

        code_langue = obtenir_code_langue(langue)       #obtention du code de la langue
        print("Langue choisie : ", langue, ". Numéro : ", numero_langue, ". Code langue : ", code_langue, ".") #récapitulatif de la langue choisie

        new_reco,contenu_audio=recuperer_audio(code_langue)  #nouvelle écoute

        if new_reco :   #si pas de nouvelle reconnaissance, ruen n'est exécuté
            liste_commandes=[]     #réinitialisation de la liste des commandes
            parcourir_commande(contenu_audio, numero_langue, liste_commandes)  #remplissage des dictionnaires
            executer_mouvement(liste_commandes,historique_commandes)  #établissement des commandes d'envoi
            await envoi_commandes(liste_commandes, com)  #envoi des commandes
            historique_commandes.append(liste_commandes)  #mise à jour de l'historique des commandes
        

if __name__ == "__main__":
    asyncio.run(main())     #lancement du programme