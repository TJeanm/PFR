import csv

historique_commandes = []

def lire_commande_fichier():
    fichier_path = "ligne_vocal.txt"
    try:
        with open(fichier_path, "r", encoding="utf-8") as fichier:
            print("Le fichier a bien été ouvert.")
            # On lit chaque ligne, on strippe, puis on split sur la virgule
            # et on ne conserve que le premier élément
            commandes = [ligne.strip().split(",")[0] for ligne in fichier]
            return commandes
    except FileNotFoundError:
        print(f"Erreur : fichier {fichier_path} introuvable.")
        return []  # On renvoie une liste vide pour éviter None dans parcourir_commande

def parcourir_commande(commande_texte):
    structure_commande = {}
    fichier_path = "liste_commande_vocal.csv"
    try:
        with open(fichier_path, "r", encoding="utf-8") as fichier:
            # On passe bien le handle 'fichier', pas le chemin
            reader = csv.reader(fichier, delimiter=';')
            
            # Si votre CSV a une entête, décommentez la ligne suivante
            # next(reader)

            # Pour chaque mot dicté
            for mot in commande_texte:
                # Si c'est un nombre entier (positif)
                if mot.isdigit():
                    structure_commande["angle_distance"] = int(mot)
                else:
                    # On parcourt tout le CSV à la recherche du mot
                    # (on peut aussi construire un dict en amont pour accélérer)
                    # Chaque 'ligne' est une liste : [col0, col1, col2, ...]
                    # Exemple : ligne[0] = nom de la commande, ligne[2] = type
                    # On remet le curseur au début du fichier à chaque mot
                    fichier.seek(0)
                    for ligne in reader:
                        if len(ligne) >= 3 and ligne[0] == mot:
                            if ligne[2] == "commande":
                                structure_commande["commande"] = mot
                            elif ligne[2] == "logiciel":
                                structure_commande["logiciel"] = mot
                            # Si vous n'avez besoin que du premier match :
                            # break

    except FileNotFoundError:
        print(f"Erreur : fichier {fichier_path} introuvable.")
        return {}

    historique_commandes.append(structure_commande)
    return structure_commande

if __name__ == "__main__":
    commandes = lire_commande_fichier()
    resultat = parcourir_commande(commandes)
    print(resultat)
