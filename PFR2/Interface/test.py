import tkinter as tk
import subprocess
import os
import platform
import csv

# Définition des constantes
UTILISATEUR = "👤 Utilisateur"
ADMINISTRATEUR = "🔧 Administrateur"
MODE_AUTOMATIQUE = "🤖 Mode automatique"
MODE_MANUEL = "🎮 Mode manuel"
MODE_IMAGE = "📷 Mode reconnaissance image"
CARTOGRAPHIE = "🗺️ Cartographie"
SUIVEUR = "🏀 Mode suiveur de balle"
DETECTION = "🔍 Détection d'objet"
CHANGER_LANGUE = "🌐 Changer la langue"
AJOUTER_LANGUE = "➕ Ajouter une langue"
CHANGER_MDP = "🔒 Changer le mot de passe"
ULTRASON = "🔊 Activer/Désactiver les ultrasons"
AVEC_MANETTE = "🕹️ Avec la manette"
AVEC_VOIX = "🎤 Avec la voix"
RETOUR = "🔙 Retour"
QUITTER = "❌ Quitter"

# Définition des fichiers
INITIALISATION_UTILISATEUR = "Programmes\\initialisation_utilisateur.py"
LISTE_COMMANDE_VOCAL = "Casse_Noisette/liste_commande_vocal_v3.csv"
ACTIVATION_VOCAL = "Programmes\\commande_vocale_finale.py"
ACTIVATION_MANETTE = "Programmes\\pilotage.py"


class MenuApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Menu de Navigation")
        self.root.geometry("900x500")
        self.root.configure(bg="#1e1e1e")

        self.langue_selectionnee = None
        self.langue_menu_actif = False

        # Cadre d'aide admin
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
        self.admin_menu = [CHANGER_MDP, AJOUTER_LANGUE, RETOUR, QUITTER]

        self.current_menu = self.main_menu
        self.selected_index = 0

        self.label = tk.Label(self.root, text="", font=("Consolas", 20), justify=tk.LEFT, bg="#1e1e1e", fg="#dcdcdc", padx=20, pady=20)
        self.label.pack(pady=50)

        self.update_menu()
        self.root.bind("<Up>", self.navigate_up)
        self.root.bind("<Down>", self.navigate_down)
        self.root.bind("<Return>", self.select_option)

    def update_menu(self):
        display_text = "\n".join(
            [f"> {item} <" if i == self.selected_index else item for i, item in enumerate(self.current_menu)]
        )
        self.label.config(text=display_text)

    def navigate_up(self, event):
        self.selected_index = (self.selected_index - 1) % len(self.current_menu)
        self.update_menu()

    def navigate_down(self, event):
        self.selected_index = (self.selected_index + 1) % len(self.current_menu)
        self.update_menu()

    def select_option(self, event):
        choice = self.current_menu[self.selected_index]

        if self.langue_menu_actif:
            self.langue_selectionnee = choice
            print(f"Langue sélectionnée : {self.langue_selectionnee}")
            self.langue_menu_actif = False
            self.current_menu = self.user_menu
            self.selected_index = 0
            self.update_menu()
            return

        if choice == UTILISATEUR:
            subprocess.run(["python", INITIALISATION_UTILISATEUR])
            self.current_menu = self.user_menu
        elif choice == ADMINISTRATEUR:
            self.current_menu = self.admin_menu

        ### Gestion de la sélection d'une option UTILISATEUR ###
        elif choice == MODE_MANUEL:
            self.current_menu = self.manuel_menu
        elif choice == MODE_IMAGE:
            self.current_menu = self.image_menu
        elif choice == CHANGER_LANGUE:
            self.ouvrir_menu_langue()
            return
        elif choice == CARTOGRAPHIE:
            print("Réalisation de la cartographie")

        ### Gestion de la sélection d'une option MANUEL ###
        elif choice == AVEC_MANETTE:
            print("Contrôle avec la manette activé")
            subprocess.run(["python", ACTIVATION_MANETTE])
        elif choice == AVEC_VOIX:
            subprocess.run(["python", ACTIVATION_VOCAL ])

        ### Gestion de la sélection d'une option IMAGE ###
        elif choice == SUIVEUR:
            print("Recherche d'une balle...")
            print("Balle trouvée, suivi de la balle")
        elif choice == DETECTION:
            print("Détection d’objet activée")
        
        elif choice == AJOUTER_LANGUE:
            self.afficher_aide_ajout_langue()
            return
        elif choice == RETOUR:
            if self.current_menu in [self.user_menu, self.admin_menu]:
                self.current_menu = self.main_menu
            elif self.current_menu in [self.image_menu, self.manuel_menu]:
                self.current_menu = self.user_menu
        elif choice == QUITTER:
            self.root.quit()

        self.selected_index = 0
        self.update_menu()

    def ouvrir_menu_langue(self):
        try:
            with open(LISTE_COMMANDE_VOCAL, mode='r', encoding='utf-8') as f:
                reader = csv.reader(f, delimiter=';')
                header = next(reader)
                langues = [l.strip() for l in header[2:] if l.strip()]
        except Exception as e:
            print(f"Erreur lors de la lecture des langues : {e}")
            langues = ["Aucune langue disponible"]

        self.current_menu = langues + [RETOUR]
        self.langue_menu_actif = True
        self.selected_index = 0
        self.update_menu()

    def afficher_aide_ajout_langue(self):
        self.label.pack_forget()
        self.help_label.config(text=(
            "- Ce fichier CSV contient les commandes vocales disponibles.\n"
            "- Vous pouvez l’éditer avec Excel ou un éditeur de texte.\n"
            "- Pour ajouter une langue, insérez une nouvelle colonne avec la langue souhaitée.\n\n"
            "💾 N’oubliez pas d’enregistrer avant de fermer le fichier !!!"
        ))
        self.help_frame.pack(pady=30)

        try:
            if platform.system() == "Windows":
                os.startfile(LISTE_COMMANDE_VOCAL)
        except Exception as e:
            print(f"❌ Impossible d’ouvrir le fichier : {e}")

    def retour_depuis_aide(self):
        self.help_frame.pack_forget()
        self.label.pack(pady=50)
        self.current_menu = self.admin_menu
        self.selected_index = 0
        self.update_menu()

if __name__ == "__main__":
    root = tk.Tk()
    app = MenuApp(root)
    root.mainloop()