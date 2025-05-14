import tkinter as tk
import subprocess
import os
import platform

# Définition des constantes pour les menus
UTILISATEUR = "Utilisateur"
ADMINISTRATEUR = "Administrateur"
QUITTER = "Quitter"
MODE_AUTOMATIQUE = "Mode automatique"
MODE_MANUEL = "Mode manuel"
MODE_IMAGE = "Mode reconaissance image"
SUIVEUR = "Mode suiveur de balle"
DETECTION = "Détection d'objet"
CHANGER_LANGUE = "Changer la langue"
AJOUTER_LANGUE = "Ajouter une langue"
CHANGER_MDP = "Changer le mot de passe"
ULTRASON = "Activer/Désactiver les ultrasons"
AVEC_MANETTE = "Avec la manette"
AVEC_VOIX = "Avec la voix"
RETOUR = "Retour"

class MenuApp:
    def __init__(self, root):
        """Initialisation de l'application et des menus"""
        self.root = root
        self.root.title("Menu de Navigation")
        self.root.geometry("800x300")

        self.help_frame = tk.Frame(self.root)
        self.help_label = tk.Label(self.help_frame, text="", font=("Arial", 14), justify=tk.LEFT, wraplength=700)
        self.help_label.pack(pady=10)

        self.help_buttons = tk.Frame(self.help_frame)
        self.retour_button = tk.Button(self.help_buttons, text="Retour", command=self.retour_depuis_aide)
        self.retour_button.pack(side=tk.LEFT, padx=20)
        self.quitter_button = tk.Button(self.help_buttons, text="Quitter", command=self.root.quit)
        self.quitter_button.pack(side=tk.RIGHT, padx=20)

        self.help_buttons.pack(pady=20)
        
        # Définition des menus
        self.main_menu = [UTILISATEUR, ADMINISTRATEUR, QUITTER]
        self.user_menu = [MODE_AUTOMATIQUE, MODE_MANUEL, MODE_IMAGE, CHANGER_LANGUE, RETOUR, QUITTER]
        self.manuel_menu = [AVEC_MANETTE, AVEC_VOIX, RETOUR, QUITTER]
        self.image_menu = [SUIVEUR, DETECTION, RETOUR, QUITTER]
        self.admin_menu = [CHANGER_MDP, AJOUTER_LANGUE, RETOUR, QUITTER]
        
        
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

    def retour_depuis_aide(self):
        """Revenir depuis le mode aide vers le menu précédent (admin)"""
        self.help_frame.pack_forget()
        self.label.pack(pady=50)  # Restaure le menu
        self.current_menu = self.admin_menu
        self.selected_index = 0
        self.update_menu()
    
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

        ### Gestion de la sélection d'une option UTILISATEUR ###
        elif choice == MODE_AUTOMATIQUE:
            print("Mode automatique activé")
            #subprocess.run(["python", os.getcwd()+ "\\Programmes\\test_automatique.py"])
        elif choice == MODE_MANUEL:
            self.current_menu = self.manuel_menu
            self.selected_index = 0
        elif choice == MODE_IMAGE:
            self.current_menu = self.image_menu
            self.selected_index = 0
        elif choice == CHANGER_LANGUE:
            print("Changer la langue sélectionné")

        ### Gestion de la sélection d'une option MANUEL ###
        elif choice == AVEC_MANETTE:
            print("Contrôle avec la manette activé")
            subprocess.run(["python", "Programmes\\test_pilotage.py"]) #os.getcwd()+ 
            #subprocess.run(["python", os.getcwd()+ "\\Programmes\\test_manuel.py"])
        elif choice == AVEC_VOIX:
            print("Contrôle avec la voix activé")
            #subprocess.run(["python", os.getcwd()+ "\\Programmes\\test_vocal.py"])

        ### Gestion de la sélection d'une option IMAGE ###
        elif choice == SUIVEUR:
            print("Recherche d'une balle...")
            print("Balle trouvé, suivie de la balle")
            #subprocess.run(["python", os.getcwd()+ "\\Programmes\\test_image.py"])
        elif choice == DETECTION:
            print("Contrôle avec la voix activé")
            #subprocess.run(["python", os.getcwd()+ "\\Programmes\\test_image.py"])

        ### Gestion de la sélection d'une option ADMINISTRATEUR ###
        elif choice == AJOUTER_LANGUE:
            print("Ajouter une langue")

            self.label.pack_forget()
            # Message d’aide
            aide_texte = (
                "📄 Ce fichier CSV contient les commandes vocales disponibles.\n"
                "Tu peux l’éditer avec Excel ou un éditeur de texte.\n"
                "➡️ Pour ajouter une langue, insère une nouvelle colonne avec la langue souhaitée.\n"
                "💾 N’oublie pas d’enregistrer avant de fermer le fichier."
            )
            self.help_label.config(text=aide_texte)
            self.help_frame.pack()


            fichier = "Casse_Noisette\\liste_commande_vocal.csv" #os.getcwd() +
            try:
                if platform.system() == "Windows":
                    os.startfile(fichier)
                #elif platform.system() == "Darwin":  # macOS
                #    subprocess.run(["open", fichier])
                #else:  # Linux
                #    subprocess.run(["xdg-open", fichier])
            except Exception as e:
                print(f"❌ Impossible d’ouvrir le fichier : {e}")

        elif choice == CHANGER_MDP:
            print("Changer le mot de passe sélectionné")
        elif choice == ULTRASON:
            print("Activation des Ultrasons")
            #subprocess.run(["python", os.getcwd()+ "\\Programmes\\test_ultrasons.py"])
            
        
        elif choice == RETOUR:
            if (self.current_menu == self.user_menu or self.current_menu == self.admin_menu):
                self.current_menu = self.main_menu
            elif (self.current_menu == self.image_menu or self.current_menu == self.manuel_menu):
                self.current_menu = self.user_menu
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
