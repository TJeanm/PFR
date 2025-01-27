# Compilation des modules

main.o: main.c interface.h pilotage.h Commande_vocal.h
	gcc -c main.c

interface.o: interface.c interface.h pilotage.h Commande_vocal.h
	gcc -c interface.c

pilotage.o: pilotage.c pilotage.h
	gcc -c pilotage.c

Commande_vocal.o: Commande_vocal.c Commande_vocal.h
	gcc -c Commande_vocal.c

# Lier les objets pour créer l'exécutable
programme: main.o interface.o pilotage.o Commande_vocal.o
	gcc main.o interface.o pilotage.o Commande_vocal.o -o programme -lm

clean:
	rm -rf *.o