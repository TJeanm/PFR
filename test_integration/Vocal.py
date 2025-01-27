import speech_recognition as sr
import pyaudio
from gtts import gTTS

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

def ecrire_commande_fichier(commande):
    with open("ligne_vocal.txt", "w", encoding="utf-8") as fichier:
        fichier.write(commande + "\n")
    #print("Commande écrite dans 'ligne_vocal.txt'.")

numero, langue = lire_choix_langue("choix_langue.txt")
code_langue = obtenir_code_langue(langue)
print(f"Langue choisie : {langue} (code : {code_langue})")

r = sr.Recognizer()
micro = sr.Microphone()
with micro as source:
    print("Speak!")
    audio_data = r.listen(source)
    print("End!")

result = r.recognize_google(audio_data, language=code_langue)
ecrire_commande_fichier(result)
print ("Vous avez dit : ", result)