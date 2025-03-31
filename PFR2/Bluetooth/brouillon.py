def lecture_manette():
    commande_manette = [[], []]
    with open("Com_to_Manette.txt", "r", encoding="utf-8") as fichier:
        lecture = fichier.readlines() 
        lecture.pop()
        for i, valeur in enumerate(lecture) :
            if i < 6 :
                commande_manette[0].append(bool(int(valeur.strip())))
            else:
                commande_manette[1].append(float(valeur.strip()))
    return commande_manette

def lecture_manette2():
    lecture = ""
    with open("Com_to_Manette.txt", "r", encoding="utf-8") as fichier:
        commande = fichier.readlines() 
        commande.pop()
        for valeur in commande :
            lecture = lecture + valeur.strip() + ","
        lecture = lecture  + "\n"
    return lecture

print(lecture_manette2())