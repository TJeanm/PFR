import speech_recognition as sr
import asyncio
import fichiers
import commandes as com
import configparser
import tkinter as tk

# Récupération de la configuration utilisateur
config = configparser.ConfigParser()
config.read("config.ini")

langue_utilisateur = config["UTILISATEUR"]["langue"]

dictionnaire_langues = fichiers.recup_dictionnaire("langues.txt")
code_langue = dictionnaire_langues.get(langue_utilisateur)

dictionnaire_commandes = fichiers.recup_dictionnaire("commandes.txt")

def recup_audio(code_langue):
    try:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Parlez...")
            audio = r.listen(source)
        texte = r.recognize_google(audio, language=code_langue)
        afficher_phrase_tk(texte)  # Ajout interface
        return texte.split()
    except Exception as e:
        afficher_phrase_tk("Erreur de reconnaissance")  # Ajout interface
        return []

def interprete_commande(phrase):
    for mot in phrase:
        if mot in dictionnaire_commandes:
            commande = dictionnaire_commandes[mot]
            afficher_commande_tk(commande)  # Ajout interface
            return commande
    afficher_commande_tk("Aucune commande reconnue")  # Ajout interface
    return None

async def main():
    print("Connexion Bluetooth...")
    await com.connexion()
    await com.envoie_bluetooth("m")
    await com.envoie_bluetooth("p")

    try:
        while True:
            phrase = recup_audio(code_langue)
            commande = interprete_commande(phrase)
            if commande:
                await com.envoie_bluetooth(commande)
    except KeyboardInterrupt:
        print("Arrêt du programme.")
        await com.envoie_bluetooth("m")
        await com.envoie_bluetooth("p")
        await com.close()

# === INTERFACE GRAPHIQUE ===

def lancer_programme():
    bouton_start.config(state="disabled")
    fenetre.after(100, lambda: asyncio.run(main()))

def quitter_programme():
    try:
        asyncio.run(com.envoie_bluetooth("m"))
        asyncio.run(com.envoie_bluetooth("p"))
        asyncio.run(com.close())
    except:
        pass
    fenetre.destroy()

def afficher_phrase_tk(phrase):
    label_phrase.config(text=f"Phrase entendue : {phrase}")

def afficher_commande_tk(commande):
    label_commande.config(text=f"Commande interprétée : {commande}")

fenetre = tk.Tk()
fenetre.title("Commande Vocale Robot")
fenetre.geometry("800x400")
fenetre.configure(bg="#F0F8FF")

label_phrase = tk.Label(fenetre, text="Phrase entendue : ", font=("Arial", 16), bg="#F0F8FF")
label_phrase.pack(pady=10)

label_commande = tk.Label(fenetre, text="Commande interprétée : ", font=("Arial", 16), bg="#F0F8FF")
label_commande.pack(pady=10)

bouton_start = tk.Button(fenetre, text="Démarrer la reconnaissance", font=("Arial", 14), command=lancer_programme)
bouton_start.pack(pady=20)

bouton_quitter = tk.Button(fenetre, text="Quitter", font=("Arial", 14), command=quitter_programme)
bouton_quitter.pack(pady=10)

fenetre.mainloop()