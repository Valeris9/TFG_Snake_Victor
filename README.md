# Snake

Benvolguts al repositori del Treball de Fi de Grau. Aquí hi ha inclosos tots els documents, informes i imatges que he anat creant i realitzant durant tot el treball.
A continuació, comentaré les carpetes que hi ha en aquest directori per així poder aclarir-ho correctament.


# Files

 - grafics_resultats: Són tots els gràfics que hi ha a la part de resultats de l'informe però  més grans. Estan extrets de l'arxiu Resultats.xlsx.
 - img_informes: Són les imatges que hi ha a l'informe final. Hi ha versions normals i versions amb els colors invertits per millorar la visibilitat.
 - informes: Són tots els informes: El informe previ, el informe de progrés 1 i el informe de progrés 2.
 - src: Són tots els arxius referents a la implementació del Joc Snake amb control humà i amb IA. 
 - Informe final.pdf: És l'informe final corresponent.
 - Resultats.xlsx: Són els resultats de les 10.000 execucions de l'agent per entrenar-lo.

# /src
Parlaré del directori /src que és on està tot el codi, ja que serà interessant comentar una mica cada arxiu:

 - model: Carpeta on està el arxiu model.pth, que és el model de RL entrenat.
 - test: Carpeta on estan els arxius de testing realitzats.
 - agent.py: Arxiu que gestiona l'aprenentatge de l'agent, incloent la memòria, la selecció d'accions i l'entrenament a curt i llarg termini.
- evaluator.py: Arxiu responsable de l'avaluació del model entrenat jugant diverses partides i calculant les estadístiques com la puntuació mitjana i màxima. 
- food.py: Arxiu que gestiona la generació i el comportament dels aliments al joc.
- main.py: Arxiu principal que gestiona el flux del joc per a la interacció humana.
- model.py: Arxiu que defineix la xarxa neuronal utilitzada per al model de Q-Learning profund.
- printer.py (not in use): Arxiu no utilitzat que servia per printar un gràfic amb l'entrenament.
- snake.py: Arxiu que gestiona el comportament de la serp al joc.
- snake_ai.py: Arxiu que gestiona la lògica del joc per a la IA, incloent la inicialització del joc, el reinici, els passos del joc, la interfície d'usuari i la detecció de col·lisions.
