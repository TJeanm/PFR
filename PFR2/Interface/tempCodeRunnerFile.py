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