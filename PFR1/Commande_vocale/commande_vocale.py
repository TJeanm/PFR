import speech_recognition as sr
import pyaudio
from gtts import gTTS





def commande_vocale():
    fin=False
    choix(langue)

    while (not fin) :
        enregistrer_commande()




def choix_langue():
    fichier_path = "ligne_vocal.txt"  # Nom du fichier contenant les langues

    # Essayer d'ouvrir le fichier et lire les langues
    try:
        with open(fichier_path, "r", encoding="utf-8") as fichier:
            langues = [ligne.strip().split(",")[0] for ligne in fichier]  # Prend uniquement le nom des langues
    except FileNotFoundError:
        print("Erreur : fichier ligne_vocal.txt introuvable.")
        return

    # Affichage des options
    print("\nSélectionner la langue désirée :")
    for i, langue in enumerate(langues, start=1):
        print(f"{i} = {langue}")

    # Demander le choix de l'utilisateur
    try:
        choix = int(input("\nVotre choix : "))
        if choix < 1 or choix > len(langues):
            print("Choix invalide.")
            return
    except ValueError:
        print("Veuillez entrer un nombre valide.")
        return

    # Écriture du choix dans un fichier "choix_langue.txt"
    try:
        with open("choix_langue.txt", "w", encoding="utf-8") as fichier_langue:
            fichier_langue.write(f"{choix}\n{langues[choix-1]}\n")
        print(f"Langue sélectionnée : {langues[choix-1]}")
    except Exception as e:
        print("Erreur lors de l'écriture dans choix_langue.txt :", e)


print("Début")
commande_vocale()
print("Fin")
















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


def enregistrer_commande(): #enregistre ce que dit l'utilisteur

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
        ecrire_commande_fichier(result)
        print ("Vous avez dit : ", result)
    except Exception as e : 
        print("pb")