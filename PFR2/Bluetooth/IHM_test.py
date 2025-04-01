
import tkinter as tk
import subprocess
import os

# Définition des constantes pour les menus
UTILISATEUR = "Utilisateur"
ADMINISTRATEUR = "Administrateur"
QUITTER = "Quitter"
MODE_AUTOMATIQUE = "Mode automatique"
MODE_MANUEL = "Mode manuel"
CHANGER_LANGUE = "Changer la langue"
CHANGER_MDP = "Changer le mot de passe"
CHANGER_GRUISSAN = "Changer le gruissan"
AVEC_MANETTE = "Avec la manette"
AVEC_VOIX = "Avec la voix"
RETOUR = "Retour"

class MenuApp:
    def __init__(self, root):
        """Initialisation de l'application et des menus"""
        self.root = root
        self.root.title("Menu de Navigation")
        self.root.geometry("800x300")
        
        # Définition des menus
        self.main_menu = [UTILISATEUR, ADMINISTRATEUR, QUITTER]
        self.user_menu = [MODE_AUTOMATIQUE, MODE_MANUEL, CHANGER_LANGUE, RETOUR, QUITTER]
        self.admin_menu = [CHANGER_MDP, CHANGER_GRUISSAN, RETOUR, QUITTER]
        self.manuel_menu = [AVEC_MANETTE, AVEC_VOIX, RETOUR, QUITTER]
        
        self.current_menu = self.main_menu
        self.selected_index = 0
        self.in_submenu = False
        
        # Création de l'affichage
        self.label = tk.Label(self.root, text="", font=("Arial", 21), justify=tk.LEFT)
        self.label.pack(pady=50)
        
        # Mise à jour de l'affichage et gestion des événements clavier
        self.update_menu()
        self.root.bind("<Up>", self.navigate_up)
        self.root.bind("<Down>", self.navigate_down)
        self.root.bind("<Return>", self.select_option)
    
    def update_menu(self):
        """Mise à jour de l'affichage du menu avec l'élément sélectionné"""
        display_text = "\n".join(
            [f"> {item} <" if i == self.selected_index else item for i, item in enumerate(self.current_menu)]
        )
        self.label.config(text=display_text)
    
    def navigate_up(self, event):
        """Navigation vers le haut dans le menu"""
        self.selected_index = (self.selected_index - 1) % len(self.current_menu)
        self.update_menu()
    
    def navigate_down(self, event):
        """Navigation vers le bas dans le menu"""
        self.selected_index = (self.selected_index + 1) % len(self.current_menu)
        self.update_menu()
    
    def select_option(self, event):
        """Gestion de la sélection d'une option du menu"""
        choice = self.current_menu[self.selected_index]
        if choice == UTILISATEUR:
            self.current_menu = self.user_menu
            self.selected_index = 0
            self.in_submenu = True
        elif choice == ADMINISTRATEUR:
            self.current_menu = self.admin_menu
            self.selected_index = 0
            self.in_submenu = True
        elif choice == MODE_AUTOMATIQUE:
            print("Mode automatique activé")
        elif choice == MODE_MANUEL:
            self.current_menu = self.manuel_menu
            self.selected_index = 0
        elif choice == CHANGER_LANGUE:
            print("Changer la langue sélectionné")
        elif choice == CHANGER_MDP:
            print("Changer le mot de passe sélectionné")
        elif choice == CHANGER_GRUISSAN:
            print("Changer le gruissan sélectionné")
            
        elif choice == AVEC_MANETTE:
            print("Contrôle avec la manette activé")
            subprocess.run(["python", os.getcwd()+"\pilotage.py"])  # Exécute le script pilotage.py
            
        elif choice == AVEC_VOIX:
            print("Contrôle avec la voix activé")
        elif choice == RETOUR:
            self.current_menu = self.main_menu
            self.selected_index = 0
            self.in_submenu = False
        elif choice == QUITTER:
            self.root.quit()
        
        self.update_menu()

if __name__ == "__main__":
    # Création et exécution de l'application Tkinter
    root = tk.Tk()
    app = MenuApp(root)
    root.mainloop()
