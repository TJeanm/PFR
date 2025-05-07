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
                return None, None
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
    try:
        with open(fichier_path, "r", encoding="utf-8") as fichier:
            print("Le fichier a bien été ouvert.")
            lignes = fichier.read().splitlines()
            if not lignes:
                print("Le fichier de commande est vide.")
                return []
            return lignes
    except FileNotFoundError:
        print(f"Erreur : fichier {fichier_path} introuvable.")
        return []


def parcourir_commande(commande_texte):
    structure_commande = {"commande": "", "logiciel": "", "angle_distance": 0, "direction": "", "envoi": ""}
    fichier_csv = os.path.join(os.path.dirname(__file__), os.pardir, "Casse_Noisette", "liste_commande_vocal_v2.csv")
    try:
        with open(fichier_csv, "r", encoding="utf-8") as fichier:
            reader = csv.reader(fichier, delimiter=',')
            for mot in commande_texte:
                if mot.isdigit():
                    structure_commande["angle_distance"] = int(mot)
                else:
                    fichier.seek(0)
                    for ligne in reader:
                        if ligne[2] == mot:
                            typ = ligne[1]
                            val = ligne[0]
                            if typ == "commande":
                                structure_commande["commande"] = val
                            elif typ == "logiciel":
                                structure_commande["logiciel"] = val
                            elif typ == "direction":
                                structure_commande["direction"] = val
    except FileNotFoundError:
        print(f"Erreur : fichier {fichier_csv} introuvable.")
    historique_commandes.append(structure_commande)
    return structure_commande


def executer_commande(structure_commande):
    if structure_commande["commande"]:
        executer_mouvement(structure_commande)
    if structure_commande["logiciel"]:
        executer_logiciel(structure_commande)


def executer_mouvement(structure_commande):
    if structure_commande["commande"] == 'f':
        if structure_commande["direction"] == 'l':
            structure_commande["envoi"] = 'a'
        elif structure_commande["direction"] == 'r':
            structure_commande["envoi"] = 'e'
        else:
            structure_commande["envoi"] = 'z'
    elif structure_commande["commande"] == 'b':
        if structure_commande["direction"] == 'l':
            structure_commande["envoi"] = 'w'
        elif structure_commande["direction"] == 'r':
            structure_commande["envoi"] = 'x'
        else:
            structure_commande["envoi"] = 's'
    else:
        if structure_commande["direction"] == 'l':
            structure_commande["envoi"] = 'q'
        elif structure_commande["direction"] == 'r':
            structure_commande["envoi"] = 'd'


def executer_logiciel(structure_commande):
    pass


async def main():
    # calcul du chemin de choix_langue.txt comme frère de Programmes
    base_dir = os.path.dirname(__file__)
    interface_dir = os.path.abspath(os.path.join(base_dir, os.pardir))
    chemin = os.path.join(interface_dir, "Casse_Noisette", "choix_langue.txt")

    numero, langue = lire_choix_langue(chemin)
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

    structure = parcourir_commande(lire_commande_fichier())
    print(structure)
    executer_mouvement(structure)

    com = communication()
    await com.envoie_bluetooth(structure["envoi"])
    print(structure)

if __name__ == "__main__":
    asyncio.run(main())
