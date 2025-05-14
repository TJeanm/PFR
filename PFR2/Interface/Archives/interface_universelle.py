import tkinter as tk
import subprocess
import os
import platform
import csv
import sys
from pathlib import Path

# Constantes de menu
UTILISATEUR = "👤 Utilisateur"
ADMINISTRATEUR = "🔧 Administrateur"
MODE_AUTOMATIQUE = "🤖 Mode automatique"
MODE_MANUEL = "🎮 Mode manuel"
MODE_IMAGE = "📷 Mode reconnaissance image"
CARTOGRAPHIE = "🗼️ Cartographie"
SUIVEUR = "🏀 Mode suiveur de balle"
DETECTION = "🔍 Détection d'objet"
CHANGER_LANGUE = "🌐 Changer la langue"
AJOUTER_LANGUE = "➕ Ajouter une langue"
CHANGER_MDP = "🔐 Changer le mot de passe"
AVEC_MANETTE = "🕹️ Avec la manette"
AVEC_VOIX = "🎤 Avec la voix"
RETOUR = "🔙 Retour"
QUITTER = "❌ Quitter"

# Répertoires et fichiers (cross-platform)
BASE_DIR = Path(__file__).resolve().parent
PROGRAMMES_DIR = BASE_DIR / "Programmes"
CS_DIR = BASE_DIR / "Casse_Noisette"

INITIALISATION_UTILISATEUR = PROGRAMMES_DIR / "initialisation_utilisateur.py"
LISTE_COMMANDE_VOCAL = CS_DIR / "liste_commande_vocal_v3.csv"
ACTIVATION_VOCAL = PROGRAMMES_DIR / "commande_vocale_finale.py"
ACTIVATION_MANETTE = PROGRAMMES_DIR / "Com_Manette_V3.py"

# Utiliser le même interpréteur Python
PYTHON = sys.executable

class MenuApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Menu de Navigation")
        self.root.geometry("800x400")
        self.root.configure(bg="#1e1e1e")
        self.root.focus_force()

        self.langue_selectionnee = None
        self.langue_menu_actif = False

        # Widgets d'aide
        self.help_frame = tk.Frame(self.root, bg="#2b2b2b")
        self.help_label = tk.Label(self.help_frame, text="", justify=tk.LEFT,
                                   wraplength=600, bg="#2b2b2b", fg="#f1f1f1")
        self.help_label.pack(pady=10)
        btn_frame = tk.Frame(self.help_frame, bg="#2b2b2b")
        tk.Button(btn_frame, text="⬅ Retour", command=self.retour_depuis_aide,
                  bg="#444", fg="#fff", font=("TkDefaultFont", 12, "bold")).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="❌ Quitter", command=self.root.quit,
                  bg="#b22222", fg="#fff", font=("TkDefaultFont", 12, "bold")).pack(side=tk.LEFT)
        btn_frame.pack(pady=10)

        # Définition des menus
        self.menus = {
            'main': [UTILISATEUR, ADMINISTRATEUR, QUITTER],
            'user': [MODE_AUTOMATIQUE, MODE_MANUEL, MODE_IMAGE, CARTOGRAPHIE, CHANGER_LANGUE, RETOUR, QUITTER],
            'manuel': [AVEC_MANETTE, AVEC_VOIX, RETOUR, QUITTER],
            'image': [SUIVEUR, DETECTION, RETOUR, QUITTER],
            'admin': [CHANGER_MDP, AJOUTER_LANGUE, RETOUR, QUITTER]
        }
        self.current_menu = 'main'
        self.selected_index = 0

        # Label principal
        self.label = tk.Label(self.root, font=("TkDefaultFont", 18), justify=tk.LEFT,
                              bg="#1e1e1e", fg="#dcdcdc")
        self.label.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

        # Bindings clavier
        self.root.bind("<Up>", self.up)
        self.root.bind("<Down>", self.down)
        self.root.bind("<Return>", self.return_)

        self.update_menu()

    def update_menu(self):
        items = self.menus[self.current_menu]
        lines = []
        for i, item in enumerate(items):
            if i == self.selected_index:
                lines.append(f"> {item} <")
            else:
                lines.append(item)
        self.label.config(text="\n".join(lines))
        self.root.update_idletasks()

    def up(self, event):
        self.selected_index = (self.selected_index - 1) % len(self.menus[self.current_menu])
        self.update_menu()

    def down(self, event):
        self.selected_index = (self.selected_index + 1) % len(self.menus[self.current_menu])
        self.update_menu()

    def return_(self, event):
        choice = self.menus[self.current_menu][self.selected_index]
        if self.current_menu == 'main' and choice == UTILISATEUR:
            subprocess.run([PYTHON, str(INITIALISATION_UTILISATEUR)])
            self.switch_menu('user')
        elif self.current_menu == 'main' and choice == ADMINISTRATEUR:
            self.switch_menu('admin')
        elif choice == QUITTER:
            self.root.quit()
        elif choice == RETOUR:
            self.switch_menu('main' if self.current_menu in ['user','admin'] else 'user')
        elif choice == MODE_MANUEL:
            self.switch_menu('manuel')
        elif choice == MODE_IMAGE:
            self.switch_menu('image')
        elif choice == CHANGER_LANGUE:
            self.ouvrir_menu_langue()
        elif choice == AVEC_MANETTE:
            subprocess.run([PYTHON, str(ACTIVATION_MANETTE)])
        elif choice == AVEC_VOIX:
            subprocess.run([PYTHON, str(ACTIVATION_VOCAL)])
        elif choice == SUIVEUR:
            print("Suivi de balle activé")
        elif choice == DETECTION:
            print("Détection d'objet activée")
        elif choice == AJOUTER_LANGUE:
            self.afficher_aide_ajout_langue()
        self.update_menu()

    def switch_menu(self, name):
        self.current_menu = name
        self.selected_index = 0

    def ouvrir_menu_langue(self):
        try:
            with open(LISTE_COMMANDE_VOCAL, encoding='utf-8') as f:
                reader = csv.reader(f, delimiter=';')
                header = next(reader)
                langues = [l for l in header[2:] if l]
            self.menus['langues'] = langues + [RETOUR]
            self.switch_menu('langues')
        except Exception as e:
            print(f"Erreur lecture CSV: {e}")

    def afficher_aide_ajout_langue(self):
        self.label.pack_forget()
        self.help_frame.pack(expand=True, fill=tk.BOTH)
        system = platform.system()
        try:
            if system == 'Windows': os.startfile(LISTE_COMMANDE_VOCAL)
            elif system == 'Darwin': subprocess.run(['open', LISTE_COMMANDE_VOCAL])
            else: subprocess.run(['xdg-open', LISTE_COMMANDE_VOCAL])
        except Exception as e:
            print(f"❌ Impossible d’ouvrir: {e}")

    def retour_depuis_aide(self):
        self.help_frame.pack_forget()
        self.label.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        self.switch_menu('admin')
        self.update_menu()

if __name__ == '__main__':
    root = tk.Tk()
    MenuApp(root)
    root.mainloop()
