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


# traitement
historique_commandes = []


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
    fichier_csv = os.path.join(os.path.dirname(__file__), os.pardir, "Casse_Noisette", "liste_commande_vocal_v2.csv")
    #fichier_path = "liste_commande_vocal_v2.csv"
    try:
        with open(fichier_csv, "r", encoding="utf-8") as fichier:
            reader = csv.reader(fichier, delimiter=',')

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
                                                      "direction": "", "envoi": ""}

                            elif ligne[1] == "logiciel":
                                structure_commande["logiciel"] = ligne[0]

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
        if historique_commandes[i]["commande"] == 'f':  # avance
            if historique_commandes[i]["direction"] == 'l':  # avance gauche
                historique_commandes[i]["envoi"] = 'a'
            elif historique_commandes[i]["direction"] == 'r':  # avance droite
                historique_commandes[i]["envoi"] = 'e'
            else:
                print("traite avance")
                historique_commandes[i]["envoi"] = 'z'  # avance normale

        elif historique_commandes[i]["commande"] == 'b':
            if historique_commandes[i]["direction"] == 'l':
                historique_commandes[i]["envoi"] = 'w'
            elif historique_commandes[i]["direction"] == 'r':
                historique_commandes[i]["envoi"] = 'x'
            else:
                historique_commandes[i]["envoi"] = 's'

        elif historique_commandes[i]["commande"] == "t":
            if historique_commandes[i]["direction"] == 'l':
                historique_commandes[i]["envoi"] = 'q'
            else:
                historique_commandes[i]["envoi"] = 'd'

        elif historique_commandes[i]["commande"] == "c":
            historique_commandes[i]["envoi"] = "c"


def executer_logiciel(structure_commande):
    pass


async def main():
    # calcul du chemin de choix_langue.txt comme frère de Programmes
    base_dir = os.path.dirname(__file__)
    interface_dir = os.path.abspath(os.path.join(base_dir, os.pardir))
    chemin = os.path.join(interface_dir, "Casse_Noisette", "choix_langue.txt")
    #chemin = "choix_langue.txt"

    numero, langue = lire_choix_langue(chemin)
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
    except Exception:
        print("Problème reconnaissance vocale")

    historique_commandes=[]
    structure_commande=parcourir_commande(lire_commande_fichier(), numero,historique_commandes)
    print(structure_commande)
    executer_mouvement(historique_commandes)
    envoi=historique_commandes[1]["envoi"]
    print(historique_commandes)
    print(envoi)
    com = communication()
    await com.init_HM10()
    await com.envoie_bluetooth(envoi)
    #print(structure)


if __name__ == "__main__":
    asyncio.run(main())
