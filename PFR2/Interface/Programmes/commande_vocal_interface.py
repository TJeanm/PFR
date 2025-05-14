import asyncio
import tkinter as tk
from tkinter import messagebox
import os
import sys
import csv
import speech_recognition as sr
import keyboard
from communication_HM10 import communication

# === Initialisation de variables globales ===
liste_commandes = []
historique_commandes = []
com = None  # instance de communication HM10
en_ecoute = False  # flag d'écoute

# === Interface Graphique ===
fenetre = tk.Tk()
fenetre.title("Commande Vocale Robot")
fenetre.geometry("900x500")
fenetre.configure(bg="#1e1e1e")  

label_phrase = tk.Label(fenetre, text="Phrase entendue : ", font=("Arial", 16), bg="#2b2b2b", fg="#f1f1f1")
label_phrase.pack(pady=10)

#label_commande = tk.Label(fenetre, text="Commande interprétée : ", font=("Arial", 16), bg="#2b2b2b")
#label_commande.pack(pady=10)

bouton_ecouter = tk.Button(fenetre, text="Écouter", font=("Arial", 14), command=lambda: fenetre.after(100, asyncio.run, traiter_reconnaissance()))
bouton_ecouter.pack(pady=20)

bouton_stop = tk.Button(fenetre, text="Quitter", font=("Arial", 14), command=lambda: arreter_application())
bouton_stop.pack(pady=10)

# === Fonctions ===

def lire_choix_langue(fichier_choix):
    try:
        with open(fichier_choix, "r", encoding="utf-8") as fichier:
            lignes = fichier.read().splitlines()
            return lignes[0].strip(), lignes[1].strip() if len(lignes) >= 2 else (None, None)
    except FileNotFoundError:
        print(f"Fichier introuvable : {fichier_choix}")
        return None, None

def obtenir_code_langue(nom_langue):
    return f"{nom_langue[:2].lower()}-{nom_langue[:2].upper()}"

def afficher_phrase(phrase):
    label_phrase.config(text=f"Phrase entendue : {phrase}")

#def afficher_commande(cmd):
#    label_commande.config(text=f"Commande interprétée : {cmd}")

def recuperer_audio(code_langue):
    try:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Parlez...")
            audio = r.listen(source)
        texte = r.recognize_google(audio, language=code_langue)
        afficher_phrase(texte)
        return texte.split()
    except Exception:
        afficher_phrase("Erreur de reconnaissance vocale")
        return []

def lire_csv_commandes(mots, num_langue):
    structure = {"commande": "", "logiciel": "", "angle_distance": 0, "direction": "", "envoi": "", "vitesse": "", "unité": ""}
    base = os.path.dirname(__file__)
    fichier = os.path.join(base, os.pardir, "Casse_Noisette", "liste_commande_vocale.csv")
    resultat = []
    with open(fichier, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=';')
        for mot in mots:
            if mot.isdigit():
                structure["angle_distance"] = int(mot)
            else:
                f.seek(0)
                for ligne in reader:
                    if ligne[int(num_langue) + 1] == mot:
                        if ligne[1] == "commande":
                            resultat.append(structure.copy())
                            structure = {"commande": ligne[0], "logiciel": "", "angle_distance": 0, "direction": "", "envoi": "", "vitesse": "", "unité": ""}
                        elif ligne[1] == "direction":
                            structure["direction"] = ligne[0]
                        elif ligne[1] == "vitesse":
                            structure["vitesse"] = ligne[0]
                        elif ligne[1] == "unité":
                            structure["unité"] = ligne[0]
    resultat.append(structure)
    return resultat

def executer_mouvement(liste, historique):
    for i in range(1, len(liste)):
        vitesse = liste[i]["vitesse"] == "s"
        cmd = liste[i]["commande"]
        dir = liste[i]["direction"]
        if cmd == "f":
            if dir == "l": liste[i]["envoi"] = "r" if vitesse else "a"
            elif dir == "r": liste[i]["envoi"] = "y" if vitesse else "e"
            else: liste[i]["envoi"] = "t" if vitesse else "z"
        elif cmd == "b":
            if dir == "l": liste[i]["envoi"] = "v" if vitesse else "w"
            elif dir == "r": liste[i]["envoi"] = "b" if vitesse else "x"
            else: liste[i]["envoi"] = "g" if vitesse else "s"
        elif cmd == "t":
            if dir == "l": liste[i]["envoi"] = "f" if vitesse else "q"
            else: liste[i]["envoi"] = "h" if vitesse else "d"
        elif cmd == "c":
            if dir == "l": liste[i]["envoi"] = "r" if vitesse else "q"
            else: liste[i]["envoi"] = "h" if vitesse else "d"
        elif cmd == "e":
            liste[i]["envoi"] = "l"
        else:
            liste[i]["envoi"] = "m"

def calculer_temps(cmd):
    d = 100 if cmd["unité"] == "cm" else 1
    if cmd["commande"] in ['f', 'b']:
        facteur = 0.8 if cmd["vitesse"] == 's' else 1
        return cmd["angle_distance"] / d * facteur if cmd["angle_distance"] else 1 * facteur
    elif cmd["commande"] == "t":
        return 0.4 if cmd["vitesse"] == 's' else 0.5
    elif cmd["commande"] == "c":
        return 2 if cmd["vitesse"] == 's' else 2.3
    return 1

async def envoi_commandes(liste, com):
    for i in range(1, len(liste)):
        if liste[i]["commande"] != "e":
            envoi = liste[i]["envoi"]
            await com.envoie_bluetooth(envoi)
            print(f"Envoyé : {envoi}")
            await asyncio.sleep(calculer_temps(liste[i]))
    await com.envoie_bluetooth("m")

async def traiter_reconnaissance():
    global liste_commandes, historique_commandes, com
    chemin_langue = os.path.join(os.getcwd(), "Casse_Noisette", "choix_langue.txt")
    num, langue = lire_choix_langue(chemin_langue)
    if langue is None: return
    code = obtenir_code_langue(langue)
    mots = recuperer_audio(code)
    if mots:
        liste_commandes.clear()
        liste_commandes = lire_csv_commandes(mots, num)
        #afficher_commande(" ".join([c["commande"] for c in liste_commandes if c["commande"]]))
        executer_mouvement(liste_commandes, historique_commandes)
        #await envoi_commandes(liste_commandes, com)
        historique_commandes.append(liste_commandes)

def arreter_application():
    #if com:
        #asyncio.run(com.envoie_bluetooth("m"))
        #asyncio.run(com.envoie_bluetooth("p"))
        #asyncio.run(com.close())
    fenetre.destroy()

async def initialiser_bluetooth():
    global com
    #com = communication()
    #await com.init_HM10()
    #await com.envoie_bluetooth("i")

# === Lancement de l'appli ===
asyncio.run(initialiser_bluetooth())
fenetre.mainloop()
