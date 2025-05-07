import asyncio
from communication_HM10 import communication
import csv
import os
import speech_recognition as sr
import pyaudio
from gtts import gTTS
import sys
from pathlib import Path

def lire_choix_langue(fichier_choix):
    try:
        with open(fichier_choix, "r", encoding="utf-8") as fichier:
            lignes = fichier.readlines()
            if len(lignes) >= 2:
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
    if not isinstance(nom_langue, str) or len(nom_langue) < 2:
        raise ValueError(f"Nom de langue invalide : {nom_langue!r}")
    prefixe = nom_langue[:2].lower()
    return f"{prefixe}-{prefixe.upper()}"

def ecrire_commande_fichier(commande, fich):
    print(commande)
    with open(fich, "w", encoding="utf-8") as fichier:
        fichier.write(commande + "\n")

historique_commandes = []

def lire_commande_fichier(chemin_fichier):
    try:
        with open(chemin_fichier, "r", encoding="utf-8") as fichier:
            print("Le fichier a bien été ouvert.")
            lignes = fichier.read().splitlines()
            if not lignes:
                print("Le fichier de commande est vide.")
                return []
            return lignes
    except FileNotFoundError:
        print(f"Erreur : fichier {chemin_fichier} introuvable.")
        return []

def parcourir_commande(commande_texte):
    structure_commande = {"texte": commande_texte, "envoi": "TEST"}  # Exemple temporaire
    historique_commandes.append(structure_commande)
    return structure_commande

async def main():
    # __file__ est dans Interface/Programmes
    dossier_programmes = Path(__file__).resolve().parent
    dossier_interface = dossier_programmes.parent

    choix_langue_path = dossier_interface / "Casse_Noisette" / "choix_langue.txt"
    ligne_vocal_path = dossier_interface / "Casse_Noisette" / "ligne_vocal.txt"

    # Lecture de la langue choisie
    numero, langue = lire_choix_langue(choix_langue_path)
    if langue is None:
        print("\u26d4 Aucune langue choisie, arrêt du programme.")
        sys.exit(1)

    try:
        code_langue = obtenir_code_langue(langue)
    except ValueError as e:
        print(f"Erreur dans le code langue : {e}")
        sys.exit(1)

    print(f"Langue choisie : {langue} (code : {code_langue})")

    # Lecture et traitement des commandes vocales
    try:
        lignes = lire_commande_fichier(ligne_vocal_path)
        if not lignes:
            return
        for result in lignes:
            ecrire_commande_fichier(result, ligne_vocal_path)
            print("Vous avez dit :", result)
            structure_commande = parcourir_commande(result)
            print(structure_commande)
            # executer_mouvement(structure_commande)  # Décommenter si disponible

            com = communication()
            # await com.init_HM10()
            # await com.envoie_bluetooth("p")
            await com.envoie_bluetooth(structure_commande["envoi"])
            print("Commande envoyée :", structure_commande)
    except Exception as e:
        print("Erreur lors du traitement des commandes vocales :", e)

if __name__ == "__main__":
    asyncio.run(main())
