import tkinter as tk
import subprocess
import os
import platform
import csv
from PIL import Image, ImageTk
from tkinter import simpledialog, messagebox

# Définition des constantes
UTILISATEUR = "👤 Utilisateur"
ADMINISTRATEUR = "🔧 Administrateur"
MODE_AUTOMATIQUE = "🤖 Mode automatique"
MODE_MANUEL = "🎮 Mode manuel"
MODE_IMAGE = "📷 Reconnaissance image"
CARTOGRAPHIE = "🗺️ Cartographie"
SUIVEUR = "🏀 Mode suiveur de balle"
DETECTION = "🔍 Détection d'objet"
CHANGER_LANGUE = "🌐 Changer la langue"
AJOUTER_LANGUE = "➕ Ajouter une langue"
CHANGER_MDP = "🔒 Changer le mot de passe"
ULTRASON_ACTIVE = "🔊 Activer les ultrasons"
ULTRASON_DESACTIVE = "🔊 Désactiver les ultrasons"
AVEC_MANETTE = "🕹️ Avec la manette"
AVEC_VOIX = "🎤 Avec la voix"
RETOUR = "🔙 Retour"
QUITTER = "❌ Quitter"

# Définition des fichiers
INITIALISATION_UTILISATEUR = "Programmes\\initialisation_utilisateur.py"
ACTIVATION_VOCAL = "Programmes\\commande_vocal_interface.py" #commande_vocale_v6biturbo
ACTIVATION_MANETTE = "Programmes\\Com_Manette.py"
ACTIVATION_AUTOMATIQUE = "Programmes\\automatique.py"
ACTIVATION_SUIVIE = "Programmes\\image_suivie.py"
ACTIVATION_DETECTION = "Programmes\\lancer_camera.py"
ACTIVATION_CARTOGRAPHIE = "Programmes\\connexion_Raspberry.py"


LISTE_COMMANDE_VOCAL = "Casse_Noisette\\liste_commande_vocale.csv"
LISTE_COMMANDE_VOCAL_LECTURE = "Casse_Noisette/liste_commande_vocale.csv"
CARTE = "Casse_Noisette/plan_Toulouse.jpeg"
BIENVENUE = "Casse_Noisette/image_PFR_4.png"
FICHIER_MDP = "Casse_Noisette/mdp_admin.txt"
FICHIER_CPT_ULTRASON = "Casse_Noisette/activation_capteur_ultrason.txt"

# Fonction pour lire le mot de passe enregistré
def lire_mot_de_passe():
    if not os.path.exists(FICHIER_MDP):
        with open(FICHIER_MDP, "w") as f:
            f.write("Groupe5")
        return "Groupe5"
    with open(FICHIER_MDP, "r") as f:
        return f.read().strip()

# Fonction pour écrire un nouveau mot de passe
def ecrire_mot_de_passe(nouveau_mdp):
    with open(FICHIER_MDP, "w") as f:
        f.write(nouveau_mdp.strip())

class MenuApp:
    def __init__(self, root):
        #subprocess.run(["python", INITIALISATION_UTILISATEUR])

        self.root = root
        self.root.title("Menu de Navigation")
        self.root.geometry("900x500")
        self.root.configure(bg="#1e1e1e")

        self.langue_selectionnee = None
        self.langue_menu_actif = False

        self.help_frame = tk.Frame(self.root, bg="#2b2b2b")
        self.help_label = tk.Label(self.help_frame, text="", font=("Arial", 14), justify=tk.LEFT, wraplength=700, bg="#2b2b2b", fg="#f1f1f1")
        self.help_label.pack(pady=10)

        self.help_buttons = tk.Frame(self.help_frame, bg="#2b2b2b")
        self.retour_button = tk.Button(self.help_buttons, text="⬅ Retour", command=self.retour_depuis_aide, bg="#444", fg="#fff", font=("Arial", 12, "bold"))
        self.retour_button.pack(side=tk.LEFT, padx=20)
        self.quitter_button = tk.Button(self.help_buttons, text="❌ Quitter", command=self.root.quit, bg="#b22222", fg="#fff", font=("Arial", 12, "bold"))
        self.quitter_button.pack(side=tk.RIGHT, padx=20)
        self.help_buttons.pack(pady=20)

        # Menus
        self.main_menu = [UTILISATEUR, ADMINISTRATEUR, QUITTER]
        self.user_menu = [MODE_AUTOMATIQUE, MODE_MANUEL, MODE_IMAGE, CARTOGRAPHIE, CHANGER_LANGUE, RETOUR, QUITTER]
        self.manuel_menu = [AVEC_MANETTE, AVEC_VOIX, RETOUR, QUITTER]
        self.image_menu = [SUIVEUR, DETECTION, RETOUR, QUITTER]
        self.admin_menu = [CHANGER_MDP, AJOUTER_LANGUE, ULTRASON_ACTIVE, ULTRASON_DESACTIVE, RETOUR, QUITTER]

        self.current_menu = self.main_menu
        self.selected_index = 0

        self.label = tk.Label(self.root, text="", font=("Consolas", 20), justify=tk.LEFT, anchor="nw", bg="#1e1e1e", fg="#dcdcdc")
        self.label.place(x=50, y=50)

        self.image_label = tk.Label(self.root, bg="#1e1e1e")
        self.image_label.place(x=450, y=70)

        self.update_menu()
        self.root.bind("<Up>", self.navigate_up)
        self.root.bind("<Down>", self.navigate_down)
        self.root.bind("<Return>", self.select_option)

    def afficher_image(self, chemin_image):
        try:
            image = Image.open(chemin_image)
            image = image.resize((int(768/2), int(768/2))) #(350, 350)
            self.photo = ImageTk.PhotoImage(image)
            self.image_label.config(image=self.photo)
            self.image_label.image = self.photo
        except Exception as e:
            print(f"Erreur chargement image : {e}")
            self.image_label.config(image="")

    def update_menu(self):
        display_text = "\n".join(
            [f"> {item} <" if i == self.selected_index else item for i, item in enumerate(self.current_menu)]
        )
        self.label.config(text=display_text)

        if self.current_menu == self.main_menu:
            self.afficher_image(BIENVENUE)
        elif self.current_menu in [self.user_menu, self.manuel_menu, self.image_menu]:
            self.afficher_image(CARTE)
        else:
            self.image_label.config(image="")

    def navigate_up(self, event):
        self.selected_index = (self.selected_index - 1) % len(self.current_menu)
        self.update_menu()

    def navigate_down(self, event):
        self.selected_index = (self.selected_index + 1) % len(self.current_menu)
        self.update_menu()

    def select_option(self, event):
        choice = self.current_menu[self.selected_index]
        # Si on est dans le menu des langues
        if self.langue_menu_actif:
            choix_langue = self.current_menu[self.selected_index]
            if choix_langue == RETOUR:
                self.langue_menu_actif = False
                self.current_menu = self.user_menu
            else:
                self.langue_selectionnee = choix_langue
                messagebox.showinfo("Langue sélectionnée", f"Langue définie sur : {choix_langue}")
                self.langue_menu_actif = False
                self.current_menu = self.user_menu
            self.selected_index = 0
            self.update_menu()
            return  # Ne pas exécuter le reste

        ### Menu Principal
        if choice == UTILISATEUR:
            self.current_menu = self.user_menu
        elif choice == ADMINISTRATEUR:
            if self.verifier_mot_de_passe():
                self.current_menu = self.admin_menu
            else:
                self.current_menu = self.main_menu

        ### Gestion de la sélection d'une option MODE UTILISATEUR ###
        elif choice == MODE_AUTOMATIQUE:
            subprocess.run(["python", ACTIVATION_AUTOMATIQUE])
        elif choice == MODE_MANUEL:
            self.current_menu = self.manuel_menu
            self.selected_index = 0
        elif choice == MODE_IMAGE:
            self.current_menu = self.image_menu
            self.selected_index = 0
        elif choice == CHANGER_LANGUE:     
            self.ouvrir_menu_langue()
        elif choice == CARTOGRAPHIE:
            print("Réalisation de la cartographie")
            subprocess.run(["python", ACTIVATION_CARTOGRAPHIE])

        ### Gestion de la sélection d'une option MANUEL ###
        elif choice == AVEC_MANETTE:
            print("Contrôle avec la manette activé")
            subprocess.run(["python", ACTIVATION_MANETTE])
        elif choice == AVEC_VOIX:
            print("Contrôle avec la voix activé")
            subprocess.run(["python", ACTIVATION_VOCAL])

        ### Gestion de la sélection d'une option IMAGE ###
        elif choice == SUIVEUR:
            subprocess.run(["python", ACTIVATION_SUIVIE])
        elif choice == DETECTION:
            subprocess.run(["python", ACTIVATION_DETECTION])

        ### Gestion de la sélection d'une option ADMINISTRATEUR ###
        elif choice == CHANGER_MDP:
            self.changer_mot_de_passe()
        elif choice == AJOUTER_LANGUE:
            self.afficher_aide_ajout_langue()
            return
        elif choice == ULTRASON_ACTIVE:
            with open(FICHIER_CPT_ULTRASON, "w") as f:
                f.write("i")
        elif choice == ULTRASON_DESACTIVE:
            with open(FICHIER_CPT_ULTRASON, "w") as f:
                f.write("p")
        elif choice == RETOUR:
            if self.current_menu in [self.user_menu, self.admin_menu]:
                self.current_menu = self.main_menu
            elif self.current_menu in [self.image_menu, self.manuel_menu]:
                self.current_menu = self.user_menu
        elif choice == QUITTER:
            self.root.quit()

        self.selected_index = 0
        self.update_menu()

    def verifier_mot_de_passe(self):
        mot_de_passe = lire_mot_de_passe()
        essais = 0
        while essais < 3:
            saisie = simpledialog.askstring("Mot de passe", "Entrez le mot de passe administrateur :")
            if saisie is None:
                return False  # Annulé
            if saisie == mot_de_passe:
                return True
            else:
                essais += 1
                messagebox.showerror("Erreur", f"Mot de passe incorrect ({essais}/3)")
        messagebox.showinfo("Retour", "Trop d’essais. Retour au menu principal.")
        return False

    def changer_mot_de_passe(self):
        mot_de_passe_actuel = lire_mot_de_passe()
        ancien = simpledialog.askstring("Changer mot de passe", "Entrez l’ancien mot de passe :")
        if ancien is None or ancien != mot_de_passe_actuel:
            messagebox.showerror("Erreur", "Ancien mot de passe incorrect.")
            return
        nouveau = simpledialog.askstring("Nouveau mot de passe", "Entrez le nouveau mot de passe :")
        if not nouveau:
            messagebox.showerror("Erreur", "Mot de passe vide.")
            return
        ecrire_mot_de_passe(nouveau)
        messagebox.showinfo("Succès", "Mot de passe modifié avec succès.")

    def afficher_aide_ajout_langue(self):
        self.label.place_forget()
        self.image_label.place_forget()
        self.help_label.config(text=(
            "- Ce fichier CSV contient les commandes vocales disponibles.\n"
            "- Vous pouvez l’éditer avec Excel, Libre Office ou un éditeur de texte.\n"
            "- Pour ajouter une langue, insérez une nouvelle colonne avec la langue souhaitée.\n"
            "- Il ne faut mettre chaque commande qu'une seule fois! Si vous le voulez rajouté des conjugaisons\n\n"

            "💾 N’oubliez pas d’enregistrer avant de fermer le fichier !!!"
        ))
        self.help_frame.pack(pady=30)

        try:
            if platform.system() == "Windows":  # Windows
                os.startfile(LISTE_COMMANDE_VOCAL)
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(["open", LISTE_COMMANDE_VOCAL])
            else:  # Linux
                subprocess.run(["xdg-open", LISTE_COMMANDE_VOCAL])
        except Exception as e:
            print(f"❌ Impossible d’ouvrir le fichier : {e}")
    
    def ouvrir_menu_langue(self):
        try:
            with open(LISTE_COMMANDE_VOCAL_LECTURE, mode='r', encoding='utf-8', newline='') as f:
                reader = csv.reader(f, delimiter=';')
                header = next(reader)
                langues = [col.strip() for col in header[2:] if col.strip()]
        except Exception as e:
            print(f"Erreur lors de la lecture des langues : {e}")
            langues = ["Aucune langue disponible"]

        self.menu_langues = langues  # On garde la liste pour vérifier la sélection
        self.current_menu = langues + [RETOUR]
        self.langue_menu_actif = True
        self.selected_index = 0
        self.update_menu()


    def retour_depuis_aide(self):
        self.help_frame.pack_forget()
        self.label.place(x=50, y=50)
        self.image_label.place(x=520, y=70)
        self.current_menu = self.admin_menu
        self.selected_index = 0
        self.update_menu()

if __name__ == "__main__":
    root = tk.Tk()
    app = MenuApp(root)
    root.mainloop()
