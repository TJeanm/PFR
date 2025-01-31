# Compilation des modules

main.o: main.c interface/interface.h pilotage_manuel/pilotage.h commande_vocale/commande_vocale.h
	gcc -c main.c

interface.o: interface/interface.c interface/interface.h pilotage_manuel/pilotage.h commande_vocale/commande_vocale.h
	gcc -c interface/interface.c

pilotage.o: pilotage_manuel/pilotage.c pilotage_manuel/pilotage.h
	gcc -c pilotage_manuel/pilotage.c

commande_vocale.o: commande_vocale/commande_vocale.c commande_vocale/commande_vocale.h
	gcc -c commande_vocale/commande_vocale.c

# Lier les objets pour créer l'exécutable
programme: main.o interface.o pilotage.o commande_vocale.o
	gcc main.o interface.o pilotage.o commande_vocale.o -o programme -lm

#Suppression des exécutables
clean:
	rm -rf *.o