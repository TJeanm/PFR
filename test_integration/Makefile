# Compilation des modules

main.o: main.c interface.h pilotage.h
	gcc -c main.c

interface.o: interface.c interface.h pilotage.h
	gcc -c interface.c

pilotage.o: pilotage.c pilotage.h
	gcc -c pilotage.c

# Lier les objets pour créer l'exécutable
programme: main.o interface.o pilotage.o
	gcc main.o interface.o pilotage.o -o programme -lm
