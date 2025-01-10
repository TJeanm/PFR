import speech_recognition as sr
import pyaudio
from gtts import gTTS

def ecrire_commande_fichier(commande):
    with open("ligne_vocal.txt", "w", encoding="utf-8") as fichier:
        fichier.write(commande + "\n")
    #print("Commande écrite dans 'ligne_vocal.txt'.")

r = sr.Recognizer()
micro = sr.Microphone()
with micro as source:
 print("Speak!")
 audio_data = r.listen(source)
 print("End!")
result = r.recognize_google(audio_data, language="fr-FR")
# pour une reconnaissance de la parole en anglais
# result = r.recognize_google(audio_data, language="en-EN")
ecrire_commande_fichier(result)
print ("Vous avez dit : ", result)