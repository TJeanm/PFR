import keyboard

def main():
    """Fonction principale pour détecter les touches pressées et afficher la direction."""
    print("Appuyez sur Z, Q, S, D pour piloter. Appuyez sur M pour quitter.")
    while True:
        if keyboard.is_pressed('z'):
            print("Avancer")
        elif keyboard.is_pressed('q'):
            print("Gauche")
        elif keyboard.is_pressed('s'):
            print("Reculer")
        elif keyboard.is_pressed('d'):
            print("Droite")
        elif keyboard.is_pressed('m'):
            print("Test fini")
            break

if __name__ == "__main__":
    main()