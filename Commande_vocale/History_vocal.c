int test3()
{
  PILE liste_commande = init_PILE();
  liste_commande = choix_langue();
  affiche_PILE(liste_commande);

  return 0;
}

int detectMot1(PILE vocal, PILE commande, ELEMENT *action)
{
  printf("nbr mot de vocal = %d\n", vocal.tete);
  printf("nbr mot de commande = %d\n", commande.tete);
  affect_ELEMENT(*action, ELEMENT_VIDE);

  for(int i=0; i<vocal.tete; i++){
    for(int j=0;j<commande.tete; j++){
      if (compare_ELEMENT(vocal.tab[i], commande.tab[j]))
        affect_ELEMENT(*action, commande.tab[j]);
    }
  }

  affiche_ELEMENT(*action);
  return 0;
}

int detectMot2(PILE vocal, PILE commande, ELEMENT *action)
{
  printf("nbr mot de vocal = %d\n", vocal.tete);
  printf("nbr mot de commande = %d\n", commande.tete);
  affect_ELEMENT(*action, ELEMENT_VIDE);
  ELEMENT tempo;

  PILE vocal2mots = init_PILE();
  for(int i=0; i<vocal.tete-1; i++){
    fusion2ELEMENT(vocal.tab[i], vocal.tab[i+1], &tempo);
    vocal2mots = emPILE(vocal2mots, tempo);
  }

  for(int i=0; i<vocal2mots.tete; i++){
    for(int j=1;j<commande.tete; j++){
      if (compare_ELEMENT(vocal2mots.tab[i], commande.tab[j]))
        affect_ELEMENT(*action, commande.tab[j]);
    }
  }

  return 0;
}

int detectMot3(PILE vocal, PILE commande, ELEMENT *action)
{
  printf("nbr mot de vocal = %d\n", vocal.tete);
  printf("nbr mot de commande = %d\n", commande.tete);
  affect_ELEMENT(*action, ELEMENT_VIDE);
  ELEMENT tempo;

  PILE vocal3mots = init_PILE();
  for(int i=0; i<vocal.tete-2; i++){
    fusion2ELEMENT(vocal.tab[i], vocal.tab[i+1], &tempo);
    fusion2ELEMENT(tempo, vocal.tab[i+2], &tempo);
    vocal3mots = emPILE(vocal3mots, tempo);
  }

  for(int i=0; i<vocal3mots.tete; i++){
    for(int j=1;j<commande.tete; j++){
      if (compare_ELEMENT(vocal3mots.tab[i], commande.tab[j]))
        affect_ELEMENT(*action, commande.tab[j]);
    }
  }

  return 0;
}

int detectMot4(PILE vocal, PILE commande, ELEMENT *action)
{
  printf("nbr mot de vocal = %d\n", vocal.tete);
  printf("nbr mot de commande = %d\n", commande.tete);
  affect_ELEMENT(*action, ELEMENT_VIDE);
  ELEMENT tempo;

  PILE vocal4mots = init_PILE();
  for(int i=0; i<vocal.tete-3; i++){
    fusion2ELEMENT(vocal.tab[i], vocal.tab[i+1], &tempo);
    fusion2ELEMENT(tempo, vocal.tab[i+2], &tempo);
    fusion2ELEMENT(tempo, vocal.tab[i+3], &tempo);

    vocal4mots = emPILE(vocal4mots, tempo);
  }

  for(int i=0; i<vocal4mots.tete; i++){
    for(int j=1;j<commande.tete; j++){
      if (compare_ELEMENT(vocal4mots.tab[i], commande.tab[j]))
        affect_ELEMENT(*action, commande.tab[j]);
    }
  }

  return 0;
}

int detectMot5(PILE vocal, PILE commande, ELEMENT *action)
{
  printf("nbr mot de vocal = %d\n", vocal.tete);
  printf("nbr mot de commande = %d\n", commande.tete);
  affect_ELEMENT(*action, ELEMENT_VIDE);
  ELEMENT tempo;

  PILE vocal5mots = init_PILE();
  for(int i=0; i<vocal.tete-4; i++){
    fusion2ELEMENT(vocal.tab[i], vocal.tab[i+1], &tempo);
    fusion2ELEMENT(tempo, vocal.tab[i+2], &tempo);
    fusion2ELEMENT(tempo, vocal.tab[i+3], &tempo);
    fusion2ELEMENT(tempo, vocal.tab[i+4], &tempo);

    vocal5mots = emPILE(vocal5mots, tempo);
  }

  for(int i=0; i<vocal5mots.tete; i++){
    for(int j=1;j<commande.tete; j++){
      if (compare_ELEMENT(vocal5mots.tab[i], commande.tab[j]))
        affect_ELEMENT(*action, commande.tab[j]);
    }
  }

  return 0;
}

int detectMot_OLD(PILE vocal, PILE commande, ELEMENT *action, int nb_mot) // nb_mot max = 5
{
  printf("nbr mot de vocal = %d\n", vocal.tete);
  printf("nbr mot de commande = %d\n", commande.tete);
  affect_ELEMENT(*action, ELEMENT_VIDE);
  ELEMENT tempo;
  int detect = 0;

  if (nb_mot == 1){
    for(int i=0; i<vocal.tete; i++){
      for(int j=0;j<commande.tete; j++){
        if (compare_ELEMENT(vocal.tab[i], commande.tab[j])){
          affect_ELEMENT(*action, commande.tab[j]);
          detect = 1;
        }
      }
    }

  }else{
    PILE vocalmots = init_PILE();
    for(int i=0; i<vocal.tete-nb_mot-1; i++){

      if (nb_mot>=2){
        fusion2ELEMENT(vocal.tab[i], vocal.tab[i+1], &tempo);
        printf("test2\n");
        if (nb_mot>=3){
          fusion2ELEMENT(tempo, vocal.tab[i+2], &tempo);
          printf("test3\n");
          if (nb_mot>=4){
            fusion2ELEMENT(tempo, vocal.tab[i+3], &tempo);
            printf("test4\n");
            if (nb_mot>=5){
              fusion2ELEMENT(tempo, vocal.tab[i+4], &tempo);
              printf("test5\n");
            }
          }
        }
      }

      vocalmots = emPILE(vocalmots, tempo);
    }

    for(int i=0; i<vocalmots.tete; i++){
      for(int j=1;j<commande.tete; j++){
        if (compare_ELEMENT(vocalmots.tab[i], commande.tab[j])){
          affect_ELEMENT(*action, commande.tab[j]);
          detect = 1;
        }
      }
    }
  }
  
  return detect;
}

void historyTest()
{
  printf("TEST 1 : LIGNE TO PILE\n");
  char chaine_test0[] = "Avance de 20 centimètres";
  PILE p = init_PILE();
  p = ligne_to_PILE(p,chaine_test0, " ");
  affiche_PILE(p);


  printf("\nTEST 2 : LECTURE COMMANDE\n");
  PILE test_2 = init_PILE();
  test_2 = langue_FR1();
  affiche_PILE(test_2);


  printf("\nTEST 3 : LECTURE DE 2 COMMANDES\n");
  int test_3 = 0;
  test_3 = test3();
  

  printf("\nTEST 4 : COMPARAISON 1 MOT\n");
  char chaine_test1[] = "avance de 20 centimètres";
  PILE liste_vocal1 = init_PILE();
  PILE liste_commande = init_PILE();
  liste_vocal1 = ligne_to_PILE(liste_vocal1, chaine_test1, " ");
  liste_commande = langue_FR1(liste_commande);
  
  ELEMENT act1;
  int test_4 = 0;
  test_4 = detectMot1(liste_vocal1, liste_commande, &act1);
  

  printf("\nTEST 5 : COMPARAISON 2 MOTS\n");
  ELEMENT act2;
  int test_5 = 0;
  test_5 = detectMot2(liste_vocal1, liste_commande, &act2);
  affiche_ELEMENT(act2);


  printf("\nTEST 6 : COMPARAISON 3 MOTS\n");
  char chaine_test3[] = "robot fait un tour sur toi s'il te plait";
  PILE liste_vocal3 = init_PILE();
  liste_vocal3 = ligne_to_PILE(liste_vocal3, chaine_test3, " ");

  ELEMENT act3;
  int test_6 = 0;
  test_6 = detectMot3(liste_vocal3, liste_commande, &act3);
  affiche_ELEMENT(act3);


  printf("\nTEST 7 : COMPARAISON 4 MOTS\n");
  char chaine_test4[] = "robot tourne à droite de 20 degrès s'il te plait";
  PILE liste_vocal4 = init_PILE();
  liste_vocal4 = ligne_to_PILE(liste_vocal4, chaine_test4, " ");

  ELEMENT act4;
  int test_7 = 0;
  test_7 = detectMot4(liste_vocal4, liste_commande, &act4);
  affiche_ELEMENT(act4);


  printf("\nTEST 8 : COMPARAISON 5 MOTS\n");
  char chaine_test5[] = "robot tourne à droite sans fin s'il te plait";
  PILE liste_vocal5 = init_PILE();
  liste_vocal5 = ligne_to_PILE(liste_vocal5, chaine_test5, " ");

  ELEMENT act5;
  int test_8 = 0;
  test_8 = detectMot5(liste_vocal5, liste_commande, &act5);
  affiche_ELEMENT(act5);


  printf("\nTEST 9 : COMPARAISON NB_MOT\n");
  char chaine_test[] = "robot avance tourne à droite sans fin s'il recule te plait";
  PILE liste_vocal = init_PILE();
  PILE liste_commande_2 = init_PILE();
  liste_vocal = ligne_to_PILE(liste_vocal, chaine_test, " ");
  liste_commande_2 = langue_FR1(liste_commande_2);
  
  ELEMENT act;
  int test_9 = 0;
  test_9 = detectMot_OLD(liste_vocal, liste_commande_2, &act, 1);
  affiche_ELEMENT(act);


  printf("\nTEST 10 : RECEPTION VOCAL\n");
  PILE liste_vocal = init_PILE();
  liste_vocal = receptionVocal();


  printf("\nTEST 11 : RECURSIVITER\n");
  PILE liste_vocal_11 = init_PILE();
  PILE liste_commande_11 = init_PILE();
  ELEMENT action_11;
  liste_vocal_11 = receptionVocal();
  liste_commande_11 = langue_FR1(liste_commande_11);
  
  int test_11 = 0;
  test_11 = detectMot(liste_vocal_11, liste_commande_11, &action_11, 5);
  affiche_ELEMENT(action_11);
}