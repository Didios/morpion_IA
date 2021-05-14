#-------------------------------------------------------------------------------
# Name:        interface finale morpion IA
# Purpose:     donner au morpion sur console une interface
#
# Author:      Didier Mathias
#
# Created:     23/04/2021
#-------------------------------------------------------------------------------

# importation des modules
from tkinter import Tk, Canvas, Button, Menu, Scale, Label, Radiobutton, StringVar
import module_lecture_fichier as read
from module_ABR import arbre
import datetime
from time import sleep


class morpion:
    """
    objet permettant de jouer au morpion via une interface Tkinter
    """
    def __init__(self):
        """
        constructeur de la classe
        on crée ici la barre de menu ainsi que les variables de bases nécessaires
        on lance directement le jeu
        """
        # On crée un fenêtre
        self.root = Tk()
        self.root.title("Morpion")

        self.turn = "J1" # on met le premier jouer comme étant J1 de base

        def turn(player):
            """
            sous-fonction permettant de modifier la valeur de self.turn ainsi que de déterminer si J1 est le premier joueur
            paramètres:
                player, une chaine de caractères, 'J1' ou 'J2' qui indique qui commence la partie
            """
            self.turn = player
            if self.turn == "J1":
                self.premier = True
            else:
                self.premier = False

        # on crée une barre de Menu
        menubar = Menu(self.root)

            # un sous-menu pour choisir qui joue en premier
        tour = Menu(menubar, tearoff = 0)
        tour.add_radiobutton(label = "Joueur 1", command = lambda x=None: turn("J1"))
        tour.add_radiobutton(label = "IA/ Joueur 2", command = lambda x=None: turn("J2"))
        menubar.add_cascade(label = "Tour", menu = tour)

        self.root.config(menu = menubar)

        # on lance l'interface
        self.lancement()
        self.root.mainloop()

    def lancement(self):
        """
        méthode permettant de lancer l'écran principal du morpion avec les choix de partie
        """
        self.log_contenu = "" # contient ce que l'on va mettre dans le log (fichier contenant information du jeu)

        self.vider_root("Menu") # on enlève ce qui se trouve sur le fenêtre

        # on initialise les variables (attributs)
        self.turn = "J1"
        self.premier = True
        self.fin = False

        # on affiche les différents choix de partie
        Button(self.root, text = "Humain VS Humain", command = self.partie_humaine, width = 20, height = 5).pack()
        Button(self.root, text = "Humain VS IA", command = self.partie_IA_renforcement, width = 20, height = 5).pack()
        Button(self.root, text = "IA VS IA", command = self.entrainement, width = 20, height = 5).pack()

    def dessiner_plateau(self):
        """
        méthode permettant de créer le plateau de jeu, tout autant visuel que digital
        """
        # plateau digital
        self.plateau = [
        ["_", "_", "_"],
        ["_", "_", "_"],
        ["_", "_", "_"]]

        # plateau visuel
        self.jeu = Canvas(self.root, width = 300, height = 300, bg = "white")

        self.jeu.create_line(0, 100, 300, 100)
        self.jeu.create_line(0, 200, 300, 200)
        self.jeu.create_line(100, 0, 100, 300)
        self.jeu.create_line(200, 0, 200, 300)


    def partie_humaine(self):
        """
        méthode permettant d'éxécuter un morpion entre 2 humain sur une grille de 3X3
        """
        # on met les premières informations dans le log
        date = datetime.datetime.now()
        self.log_contenu += "Partie du %d/%d/%d\n" %(date.day, date.month, date.year) # la date
        self.log_contenu += "à %d:%d:%d\n" %(date.hour, date.minute, date.second) # l'heure exacte
        self.log_contenu += "Partie Humain VS Humain\n\n" # le type de partie

        self.vider_root("Menu") # on enlève les boutons de choix de partie

        self.dessiner_plateau() # on crée le plateau

        def action(event):
            """
            sous-fonction permettant de jouer ou de retourner à l'écran titre selon le déroulement de la partie
            parametres:
                event, un event souris de clic
            """
            if self.fin: # si la partie est finie
                nom = "log_%s-%s-%s" %(date.day, date.month, date.year) # on détermine un nom de fichier pour le log
                if read.fichier_existe("enregistrements/%s.txt" %nom): # si le fichier existe déjà
                    # on cherche un nom avec un indice qui n'existe pas encore
                    numero = 1 # sert à déterminer l'indice
                    nouv_nom = nom + "(%d)" %numero # nom  du fichier avec l'indice
                    while read.fichier_existe("enregistrements/%s.txt" %nouv_nom): # tant que le fichier existe
                        numero += 1 # on passe à l'indice suivant
                        nouv_nom = nom + "(%d)" %numero # on change le nom de fichier avec le nouvelle indice
                    read.add_fichier("enregistrements", nouv_nom + ".txt", self.log_contenu) # on ajoute le fichier avec le nom choisi
                else:
                    read.add_fichier("enregistrements", nom + ".txt", self.log_contenu) # sinon on ajoute le fichier avec le nom selectionnez
                self.lancement() # on relance l'interface principale du jeu
            else: # la partie n'est donc pas finie
                self.coup(event) # on joue avec l'emplacement du clic

        self.jeu.bind("<1>", action) # on met un bind afin de détecter les clics
        self.jeu.pack() # on affiche le plateau de jeu

    def partie_IA_renforcement(self):
        """
        méthode permettant de faire une partie contre une IA à renforcement, elle apprend avec les parties précédentes joué
        elle devient donc de plus en plus forte au fur et à mesure des parties
        """
        # on met les premières informations dans le log
        date = datetime.datetime.now()
        self.log_contenu += "Partie du %d/%d/%d\n" %(date.day, date.month, date.year) # la date
        self.log_contenu += "à %d:%d:%d\n" %(date.hour, date.minute, date.second) # l'heure
        self.log_contenu += "Partie Humain VS IA\n\n" # le type de partie

        self.vider_root("Menu") # on enlève le contenu de la fenêtre

        self.dessiner_plateau() # on crée le plateau de jeu

        def action(event):
            """
            sous-fonction permettant de jouer ou de retourner à l'écran titre selon le déroulement de la partie
            parametres:
                event, un event souris de clic
            """
            if self.fin: # si la partie est finie
                # on s'occupe de choisir le nom du log et on l'enregistre dans le dossier prévu
                nom = "log_%s-%s-%s" %(date.day, date.month, date.year)
                if read.fichier_existe("enregistrements/%s.txt" %nom):
                    numero = 1
                    nouv_nom = nom + "(%d)" %numero
                    while read.fichier_existe("enregistrements/%s.txt" %nouv_nom):
                        numero += 1
                        nouv_nom = nom + "(%d)" %numero
                    read.add_fichier("enregistrements", nouv_nom + ".txt", self.log_contenu)
                else:
                    read.add_fichier("enregistrements", nom + ".txt", self.log_contenu)

                # on met fin à la partie pour l'IA, on lui indique le résultat de la partie
                if self.turn == "J1":
                    ordi.fin_partie(self.plateau, "IA")
                elif self.turn == "J2":
                    ordi.fin_partie(self.plateau, "J1")
                else:
                    ordi.fin_partie(self.plateau, "NUL")

                self.lancement() # on relance le jeu
            else: # sinon, la partie est en cours
                if self.turn == "J1": # si c'est à J1 de jouer
                    if self.coup(event) != "": # si le coup souhaiter par J1 est possible
                        self.coup(event) # on exécute ce coup
                        if not self.fin: # si la partie n'est pas fini
                            self.coup(ordi.jouer(self.plateau)) # on fait jouer l'IA
                else: # sinon, c'est à l'IA de jouer
                    self.coup(ordi.jouer(self.plateau)) # on fait jouer l'IA à l'emplacement qu'elle décide

        ordi = IA_2("cerveau_2.txt") # on crée un IA en indiquant le fichier de sauvegarde de ses données
        ordi.debut_partie() # on la prépare pour une nouvelle partie

        # on lance la partie en affichant le plateau et en mettant une action au clic du joueur
        self.jeu.bind("<1>", action)
        self.jeu.pack()


    def entrainement(self):
        """
        méthode permettant de faire jouer l'IA contre une autre IA semblable mais avec un autre cerveau
        """
        def entrainement_go():
            """
            sous-fonction permettant de lancer le processus d'entrainement
            """
            repet = repetitions.get() # on définit le nombre de parti choisite par l'utilisateur

            self.vider_root("Menu") # on vide l'écran de ce qu'il contient

            self.dessiner_plateau() # on crée le plateau sans l'afficher

            ordi = IA_2("cerveau.txt")
            ordi_2 = IA_2("cerveau_2.txt")

            # progression va indiquer le pourcentage de la demande effectué
            progression = Label(self.root, text =  "0.0% effectué", font = ('Times', -20, 'bold'))
            progression.pack()

            # on crée une barre de chargement, plus visuel
            progression_bar = Canvas(self.root, width = 1000, height = 20)
            progression_bar.create_rectangle(0, 0, 1000, 200, outline = "white", fill = "grey")
            progression_bar.pack()

            Label(self.root, text = "Partie en cours :", font = ("Times", -10, "bold")).pack()
            self.jeu.pack()

            for r in range(repet): # on répét le nombre de fois choisit

                # on réinitialise le plateau de jeu afin que les IA puisse jouer
                self.jeu.destroy()
                self.dessiner_plateau()
                self.jeu.pack()

                # On lance une partie en supposant que l'IA 1 est J1
                self.fin = False # la partie n'est pas finie de base
                # on fait en sorte que les IA joue alternativement en premier afin d'éviter de répéter les mêmes parties en boucles
                # on se sert de r qui est alternativement pair puis impair
                ordi.debut_partie()
                ordi_2.debut_partie()
                self.turn = "J1" # on détermine le premier jouer
                while not self.fin: # tant que la partie n'est pas finie
                    self.coup(ordi.jouer(self.plateau)) # l'IA 1 joue
                    if not self.fin: # si la partie n'est pas fini
                        self.coup(ordi_2.jouer(self.plateau)) # l'IA 2 joue

                # Quand la partie est finie, on enregistre les données en indiquant le résultat de la partie à chaque IA
                if self.turn == "J2":
                    ordi.fin_partie(self.plateau, "IA")
                    ordi_2.fin_partie(self.plateau, "J1")
                elif self.turn == "J1":
                    ordi.fin_partie(self.plateau, "J1")
                    ordi_2.fin_partie(self.plateau, "IA")
                else:
                    ordi.fin_partie(self.plateau, "NUL")
                    ordi_2.fin_partie(self.plateau, "NUL")
                """
                probleme de freeze du au fait que tkinter fonctionne avec des mainloop
                ce qui empeche la barre de progression de se mettre à jour tant que la boucle n'est pas finie

                utilisation de update pour régler le probleme
                """
                # on met à jour les informations de progression
                pourcentage = int(1000*r/repet)/10 # on obtient un pourcentage avec une décimal (ça évite d'avoir trop de décimal)
                progression.configure(text = str(pourcentage) + "% effectué")

                progression_bar.delete('chargement') # on évite d'avoir trop d'item dans le canvas on enlevent le rectangle précedent
                progression_bar.create_rectangle(0, 0, pourcentage * 10, 20, fill = "black", tags = "chargement") # on crée un rectangle qui rempli un certain pourcentage de la barre, ce qui crée une impression de progression (barre de chargement)
                self.root.update() # on rafraichit la fenêtre afin que les changements s'affichent

                sleep(0.1) # on attend 0.1s entre chaque partie à cause de problèmes d'écriture et de suppression des fichiers

            """
            il faudrait faire en sorte de mixer les deux fichiers cerveau.txt et cerveau_2.txt
            comme ça l'IA aura les connaissances des deux adversaires
            """
            self.lancement() # une fois l'entrainement terminés, on relance le jeu

        self.vider_root("Menu") # on enlève ce qu'il y a dans le fenêtre

        Label(self.root, text = "Nombres de partie d'entrainements :").pack() # on met un label pour indiquer ce que l'utilisateur doit faire
        # on met un scale afin de choisir un nombre de parties qui reste dans les limites du raisonnable
        repetitions = Scale(self.root, orient='horizontal', from_=50, to=1000, resolution=1, length=500)
        repetitions.pack()

        Button(self.root, text = "GO !", command = entrainement_go).pack() # on met un bouton afin de lancer l'entrainement une fois le nombre choisit

    def vider_root(self, *epargner):
        """
        méthode permettant de vider l'écran principal de tout ce qu'il contient, tout en épargnant une suite d'élémént choisit
        paramètres:
            epargner, une suite d'arguments, une chaine de caractères indiquant le type de l'élément à ne pas supprimer
        """
        for c in self.root.winfo_children(): # on parcours chaque éléments de la fenêtre
            if c.winfo_class() not in epargner: # si le type de l'élément ne fait partie de ceux à preserver
                c.destroy() # on le supprime


    def coup(self, event):
        """
        méthode permettant d'effectuer un coup sur le plateau, elle place le pion correspondant et annonce la fin de la partie
        parametres:
            event, un event souris avec les coordonnees de celle-ci sur le plateau, ou bien une liste indiaquant la position choisit dans le plateau virtuel
        """
        # on détermine si event est un event souris ou une liste afin d'en extraire correctement les informations
        if type(event) == list:
            x = event[1]
            y = event[0]
        else:
            x = event.x // 100
            y = event.y // 100

        # on place le pion dans le plateau virtuel
        if self.plateau[y][x] == "_": # si l'emplacement est libre
            # on place le pion correspondant en fonction de la personne qui joue et en fonction de si J1 et premier ou non
            if self.turn == "J1":
                if self.premier:
                    self.plateau[y][x] = "X"
                else:
                    self.plateau[y][x] = "O"
            else:
                if self.premier:
                    self.plateau[y][x] = "O"
                else:
                    self.plateau[y][x] = "X"
        else:
            return "" # on arrête la fonction ici si l'emplacement n'est pas libre

        def X(x, y):
            """
            sous-fonction permettant de placer un X sur le plateau visible à la position souhaiter sur le plateau digital
            """
            self.jeu.create_line(x*100 +15, y*100 +15, x*100 +85, y*100 +85)
            self.jeu.create_line(x*100 +85, y*100 +15, x*100 +15, y*100 +85)

        def O(x, y):
            """
            sous-fonction permettant de placer un O sur le plateau visible à la position souhaiter sur le plateau digital
            """
            self.jeu.create_oval(x*100 +15, y*100 +15, x*100 +85, y*100 +85)

        # on place le pion sur le plateau visible en fonction de la personne qui joue et en fonction de si J1 et premier ou non
        # puis on change le tour du joueur
        if self.turn == "J1":
            if self.premier:
                X(x, y)
            else:
                O(x, y)
            self.turn = "J2"
        else:
            if self.premier:
                O(x, y)
            else:
                X(x, y)
            self.turn = "J1"

        # selon le type de event, on peut savoir si c'est un humain ou une IA qui joue
        # grâce à cela et à self.turn (dit c'est au tour de qui de jouer), on ajoute au log  une ligne disant qui joue
        if type(event) == list:
            self.log_contenu += "IA :\n"
        elif self.turn == "J2":
            self.log_contenu += "Joueur 1 :\n"
        else:
            self.log_contenu += "Joueur 2 :\n"

        # on ajoute au log un représentation du plateau actuel
        self.log_contenu += "%s|%s|%s\n" %(self.plateau[0][0], self.plateau[0][1], self.plateau[0][2])
        self.log_contenu += "%s|%s|%s\n" %(self.plateau[1][0], self.plateau[1][1], self.plateau[1][2])
        self.log_contenu += "%s|%s|%s\n\n" %(self.plateau[2][0], self.plateau[2][1], self.plateau[2][2])

        # on vérifie si la partie est finie
        verif = self.verifier_plateau()

        if verif != None: # si verif est différent de None, cela signifie que la partie est finie
            def ecrire_fin(phrase):
                """
                sous-sous-fonction permettant d'afficher sur le plateau le résultat de la partie
                paramètres:
                    phrase, une chaine de caractères à marqué, indiquant le résultat de la partie
                """
                self.jeu.create_rectangle(75, 125, 225, 175, fill = "white")
                self.jeu.create_text(150, 150, font = ('Times', -20, 'bold'), text = phrase)

            self.fin = True # le jeu est fini
            # en fonction de quel possibilité à été faite, on crée un trait montrant la victoire
                # ligne
            if verif == "L1":
                self.jeu.create_line(15, 50, 285, 50, width = 10) # les lignes semblables à celle-ci permettent de faire un trait sur les trois symboles aligné (montrant ainsi comment le joueur à gagner
            elif verif == "L2":
                self.jeu.create_line(15, 150, 285, 150, width = 10)
            elif verif == "L3":
                self.jeu.create_line(15, 250, 285, 250, width = 10)
                # colonne
            elif verif == "C1":
                self.jeu.create_line(50, 15, 50, 285, width = 10)
            elif verif == "C2":
                self.jeu.create_line(150, 15, 150, 285, width = 10)
            elif verif == "C3":
                self.jeu.create_line(250, 15, 250, 285, width = 10)
                # diagonale
            elif verif == "D1":
                self.jeu.create_line(15, 15, 285, 285, width = 10)
            elif verif == "D2":
                self.jeu.create_line(15, 285, 285, 15, width = 10)
            # si aucune des condition précédente suivant n'est remplie, cela signifie que c'est un match nul
            else:
                self.turn = "NUL"
                ecrire_fin("Match NUL")

                self.log_contenu += "\nMATCH NUL" # on ajoute au log le résultat de la partie

            if verif != "PLEIN":
                if self.turn == "J1":
                    ecrire_fin("J2 a Gagner")
                else:
                    ecrire_fin("J1 a Gagner")

                # on ajoute au log le résultat de la partie
                if type(event) is list:
                    self.log_contenu += "\nVICTOIRE IA"
                elif self.turn == "J2":
                    self.log_contenu += "\nVICTOIRE JOUEUR 1"
                else:
                    self.log_contenu += "\nVICTOIRE JOUEUR 2"

    def verifier_plateau(self):
        """
        méthode permettant de connaitre l'etat du plateau : partie nul ou si quelqu'un a gagné
        renvoie une chaine de caracteres indiquant l'état du plateau
        si la partie n'est pas finie, renvoie None
        """
        # ligne
        l1 = self.plateau[0][0] == self.plateau[0][1] == self.plateau[0][2] and self.plateau[0][0] != "_"
        l2 = self.plateau[1][0] == self.plateau[1][1] == self.plateau[1][2] and self.plateau[1][0] != "_"
        l3 = self.plateau[2][0] == self.plateau[2][1] == self.plateau[2][2] and self.plateau[2][0] != "_"

        # colonne
        c1 = self.plateau[0][0] == self.plateau[1][0] == self.plateau[2][0] and self.plateau[0][0] != "_"
        c2 = self.plateau[0][1] == self.plateau[1][1] == self.plateau[2][1] and self.plateau[0][1] != "_"
        c3 = self.plateau[0][2] == self.plateau[1][2] == self.plateau[2][2] and self.plateau[0][2] != "_"

        # diagonale
        d1 = self.plateau[0][0] == self.plateau[1][1] == self.plateau[2][2] and self.plateau[0][0] != "_"
        d2 = self.plateau[0][2] == self.plateau[1][1] == self.plateau[2][0] and self.plateau[0][2] != "_"

        # plateau plein
        plein = "_" not in self.plateau[0] + self.plateau[1] + self.plateau[2]

        # on retourne une chaine de caractères en fonction des résultats précédent
        if l1:
            return "L1"
        elif l2:
            return "L2"
        elif l3:
            return "L3"
        elif c1:
            return "C1"
        elif c2:
            return "C2"
        elif c3:
            return "C3"
        elif d1:
            return "D1"
        elif d2:
            return "D2"
        elif plein:
            return "PLEIN"
        else:
            return None

################################################################################

"""
il existe un probleme lorsque 2 IA s'affrontent / du moins le bug n'a été repérée que là
il existe des choses insensée dans leur cerveau genre 022000000 ou bien 000200102, ou encore 010000000:000002000
    tentative de résolution en représentant O et X par des 1, mais configuration différentes possibles et pose problemes
    resolution partiel en prenant en compte la personne qui joue en premier

il y a aussi des problèmes d'accès aux fichiers, ce qui arrive de manière totalement aléatoire
    peut-être car main_interface.py est ouvert
    peut-être car le fichier est toujours en cours d'écriture   == trouver un moyen de détecter accès aux fichiers
"""
"""
chose incohérente:
    121212200:121212100     pas possible
"""
class IA:
    """
    objet permettant le contrôle d'une IA par renforcement pour jouer au morpion
    """
    def __init__(self, brain):
        """
        constructeur de la classe, elle définit le cerveau et met en place la mémoire de l'IA
        parametres:
            brain, une chaine de caracteres indiquant le chemin vers le fichier de mémoire, s'il n'existe pas, il est crée
        """
        if not read.fichier_existe(brain): # si le fichier censé contenir le cerveau n'existe pos
            read.add_fichier("", brain, "000000000:") # on le crée
        self.fichier_cerveau = brain

    def debut_partie(self, premier):
        """
        méthode permettant de préparer l'IA en vue d'une partie, on converti le fichier de mémoire en arbre
        """
        lecture = read.lire_fichier(self.fichier_cerveau) # on lit le fichier cerveau

        # on transforme le fichier en dictionnaire :
        # "000000000:100000000,010000000,001000000" => {000000000: [100000000, 010000000, 001000000]}
        dico = {}
        for ligne in lecture:
            ligne = ligne.split(":")
            l = ligne[1].split(",")
            dico[ligne[0]] = []
            for elmt in l:
                if elmt != ligne[0]:
                    dico[ligne[0]] += [elmt]

        def creation_arbre(dico, base):
            """
            sous-fonction permettant de creer un arbre des possibilité de jeu à partir d'un dictionnaire
            chaque clé de l'arbre devient une branche, chaque element dans la liste de valeur d'une clé devient soit une branche s'il existe en tant que clé, soit une feuille mais en tant que valeur
            parametres:
                dico, un dictionnaire récapitulant l'arbre
                racine, une clé du dictionnaire étant la racine de l'arbre
            """
            """
            doit être transformer en algo iteratif
            le recursif atteignant vote ses limites
            """
            """
            algo récursif :

            ABR = arbre(racine)
            if racine == "":
                return None
            for fils in dico[racine]:
                if fils in dico.keys():
                    sous_arbre = creation_arbre(dico, fils)
                    if sous_arbre is not None:
                        ABR.add_fils(sous_arbre)
                elif fils != "":
                    ABR.add_fils(arbre(int(fils)))
            return ABR
            """
            # on traite le cas ou le dico ne contient que les informations d'un cerveau vierge
            if dico == {"000000000":[""]}:
                return arbre("000000000")

            # on transforme chaque lignes en arbre :
            # {000000000: [100000000, 010000000, 001000000]} => {"000000000": arbre(000000000)}
            dico_arbre = {} # on definit un dico qui contiendrat les arbres à chaque éléments
            for keys in dico.keys(): # pour chaque clé (donc future noeud) du dico
                if dico[keys][0] not in dico.keys(): # si la valeur correspondante n'est pas présente dans les clé, cela signifie que c'est une feuille, une valeur à mettre
                    dico_arbre[keys] = arbre(keys, arbre(int(dico[keys][0]))) # on ajoute à dico_arbre l'arbre correspondant à la clé avec son unique feuille directement
                else: # sinon
                    dico_arbre[keys] = arbre(keys) # on ajoute à dico_arbre l'arbre avec comme racine sa clé correspondante

            # on assembles les arbres du dictionnaires :
            # {000000000: [100000000, 010000000, 001000000]} + {"000000000": arbre(000000000)} ==> {000000000: arbre(000000000, arbre(100000000, ...), arbre(010000000, ...), arbre(001000000, ...))}
            for racine, abr in dico_arbre.items(): # on parcourt chaque clé et arbre correspondant du dictionnaire d'arbre
                for fils in dico[racine]: # pour chaque élément présent dans le dictionnaire de base avec la même clé
                    if fils in dico_arbre.keys(): # si l'élément est dans les clé du dictionnaire d'arbre
                        abr.add_fils(dico_arbre[fils]) # on ajoute à l'arbre un fils qui est l'arbre avec l'élément comme racine (qui est stockée dans le dico d'arbre)
            # en faisant ainsi, on se retrouve avec des arbres qui pointent vers d'autres arbre du dictionnaire
            # donc quand on modifie un noeud, les noeuds qui pointent dessus se mettent à jour automatiquement

            return dico_arbre[base] # on renvoie l'arbre correspondant à la valeur racine souhaiter


        self.brain = creation_arbre(dico, "000000000") # on construit le cerveau sous la forme d'un arbre
        self.reflexion = self.brain # on définit le réflexion comme étant l'arbre entier
        self.premier = premier


    def deplacement_reflexion(self, situation):
        """
        méthode permettant de déplacer la reflexion de l'IA vers l'une des branches de celle-ci (on se déplace dans l'arbre des possibilité)
        paramètres:
            situation, une chaine de caractères indiquant la valeur du noeud dans lequel se rendre
        """
        for fils in self.reflexion.get_fils(): # pour chaque fils du noeud actuel
            if fils.get_racine() == situation: # si le fils à la bonne valeur
                self.reflexion = fils # on change le noeud actuel
                break # on met fin à la boucle

    def jouer(self, plateau):
        """
        méthode permettant de connaître le coup que va jouer l'IA
        parametres:
            plateau, une liste de liste représentant le plateau
        renvoie les coordonnées du plateau ou joue l'IA
        """
        situation = self.plateau_conversion_chaine(plateau) # on détermine la situation actuelle du plateau, de manière compréhensible pour l'IA
        scenarios = [x.get_racine() for x in self.reflexion.get_fils()] # on détermine les situations déjà exploré par l'IA

        if situation in scenarios: # si on connaît la situation actuelle
            self.deplacement_reflexion(situation) # on se déplace dans cette branche
        elif situation != self.reflexion.get_racine(): # sinon, si la situation est différente de la valeur du noeud dans lequel on est
            fils = arbre(situation) # on crée un arbre avec pour valeur la situation actuelle
            self.reflexion.add_fils(fils) # on ajoute ce noeud à l'arbre actuelle
            self.reflexion = fils # on déplace la réflexion dedans

        if not self.premier:
            choix = negamax(self.reflexion, 1) # on choisit le chemin le plus "rentable" pour l'IA (= avec un gain positif)
        else:
            choix = negamax(self.reflexion, -1)

        if choix[1] < 1 and len(self.reflexion.get_fils()) < self.nbr_possibilite(situation): # si la meilleure situation explorée est de perdre mais que toutes les possibilités actuelle n'ont pas été faites, on crée une nouvelle branche avec une autre possibilité
            scenarios = [x.get_racine() for x in self.reflexion.get_fils()] # on détermine les scénarios déjà connus, donc pas rentable

            situation = self.plateau_conversion_chaine(plateau) # on détermine la situation actuelle du plateau, de manière compréhensible pour l'IA
            i = 0
            while i < len(situation):
                if situation[i] == "0": # si l'emplacement en i est possible
                    s = situation # on met s comme étant la situation afin de le modifier
                    if self.premier: # si le nombre de possibilité est divisible par 2, cela signifie qu'il faut jouer X
                        s = s[:i] + "1" + s[i+1:]
                    else: # sinon, on joue O
                        s = s[:i] + "2" + s[i+1:]

                    if s not in scenarios: # si la possibilité supposé n'est pas encore explorée
                        break # on casse la boucle
                i += 1

            # on détermine les coordonnées du pion à jouer grâce à i
            x = 0
            while i > 2:
                x += 1
                i -= 3
            y = i

            # on crée une nouvelle branche avec pour valeur la situation trouvé et on s'y déplace
            fils = arbre(s)
            self.reflexion.add_fils(fils)
            self.reflexion = fils # on déplace la reflexion dans cette branche puisque c'est celle actuelle

        else: # sinon, cela signifie que l'on a trouvé un choix rentable, ou bien que toutes les possibilité ont été faites pour le moment
            self.deplacement_reflexion(choix[0]) # on déplace la réflexion à la situation trouvé

            # on détermine les situations future et actuelle
            situation_future = choix[0]
            situation_actuelle = self.plateau_conversion_chaine(plateau)

            # on détermine qu'elle est l'emplacement de leur différence
            rang = 0
            while situation_actuelle[rang] == situation_future[rang]:
                rang += 1

            # on en déduit l'emplecement à jouer sur le plateau
            x = rang % 3
            y = rang // 3

        return [x, y] # on renvoie les coordonnées trouvé

    def fin_partie(self, plateau, gagnant):
        """
        méthode permettant de sauvegarder l'arbre de connaissances posséder par l'IA dans le fichier de mémoire, tout en modifiant ce qui y est nécessaire
        paramètres:
            plateau, une liste de liste représentant le plateau de jeu de manière digitale
            gagnant, une chaine de caractères entre 'IA', 'J1' et 'NUL' indiquant le résultat finale de la partie
        """
        situation = self.plateau_conversion_chaine(plateau)
        scenarios = [x.get_racine() for x in self.reflexion.get_fils()]

        feuille = None

        def arbre_presence(gain):
            if situation not in scenarios and situation != self.reflexion.get_racine():
                return arbre(situation, arbre(gain))
            elif situation not in scenarios:
                return arbre(gain)
            else:
                return None

        if gagnant == "IA":
            if self.premier:
                feuille = arbre_presence(-1)
            else:
                feuille = arbre_presence(1)
        elif gagnant == "J1":
            if self.premier:
                feuille = arbre_presence(1)
            else:
                feuille = arbre_presence(-1)
        else:
            feuille = arbre_presence(0)

        if feuille is None:
            self.deplacement_reflexion(situation)
            valeur = self.reflexion.get_fils()[0].get_racine()
            if valeur > 0:
                valeur += 1
            elif valeur < 0:
                valeur -= 1
            self.reflexion.set_fils(arbre(valeur))
        elif feuille.est_feuille():
            self.reflexion.set_fils(feuille)
        else:
            self.reflexion.add_fils(feuille)

        def creation_dico(ABR):
            """
            sous-fonction permettant de transformer un arbre en dictionnaire dont chaque clé est un noeud interne et dont chaque élément correspondant et soit une branche, soit une feuille
            effectue l'inverse de la fonction creation-arbre(dico, racine)
            parametres:
                ABR, un arbre
            renvoie un dictionnaire contenant l'arbre dans sa globalité
            """

            """
            transformer algo récursif en algo itératif pour éviter les problemes de récursivité
            """
            """
            dico = {}

            dico[ABR.get_racine()] = []
            for fils in ABR.get_fils():
                if fils.est_feuille():
                    dico[ABR.get_racine()] += [fils.get_racine()]
                else:
                    nouv_dico = creation_dico(fils)
                    for keys, values in nouv_dico.items():
                        if keys in dico.keys():
                            for each in values:
                                if each not in dico[keys]:
                                    dico[keys] += [each]
                        else:
                            dico[keys] = values
                    dico[ABR.get_racine()] += [fils.get_racine()]

            return dico
            """

            """
            utilisation du parcours en largeur car celui-ci n'est pas récursif et permet d'obtenir chaque noeud de l'arbre
            ici, on enlève les feuilles car ce sont les valeur de score (donc on ne les enregistre pas comme des lignes à part entière
            """

            f = []
            f += [ABR]
            visiter = [ABR]
            while f != []:
                s = f[0]
                f = f[1:]
                for fils in s.get_fils():
                    if fils not in visiter:
                        f = f + [fils]
                        if not fils.est_feuille():
                            visiter += [fils]

            dico = {}
            for elmt in visiter:
                dico[elmt.get_racine()] = []
                for fils in elmt.get_fils():
                    dico[elmt.get_racine()] += [fils.get_racine()]

            return dico

        dico = creation_dico(self.brain)

        # transformation du dictionnaire en chaine de caracteres
        contenu = ""
        for keys, values in dico.items():
            contenu += keys
            contenu += ":"
            for indice in values:
                contenu += str(indice) + ","
            contenu = contenu[:-1]
            contenu += "\n"

        read.suppr_fichier(self.fichier_cerveau, False)
        read.add_fichier("", self.fichier_cerveau, contenu)

    def plateau_conversion_chaine(self, plateau):
        """
        fonction permettant de transformer le plateau de jeu d'un morpion en chaine de caracteres unique
        seule les 'X' et les 'O', tous autre caracteres sera représenté par un '0'
        parametres:
            plateau, une liste composé de liste qui représente le plateau
        renvoie une chaine de caracteres composé de '0' et '1'
        """
        assert type(plateau) in [list, tuple], "plateau doit être une liste"

        nbr = ""
        for i in range(len(plateau)):
            for j in range(len(plateau[i])):
                if plateau[i][j] == "X":
                    nbr += "1"
                elif plateau[i][j] == "O":
                    nbr += "2"
                else:
                    nbr += "0"
        return nbr

    def nbr_possibilite(self, situation):
        """
        fonction permettant de compter le nombre de positions possibles pour le prochain pion dans un jeu de morpion.
        C'est-à-dire qu'elle compte le nombre de 0 dans une chaine de caracteres
        parametres:
            situation, une chaine de caracteres représentant le plateau, voir fonction convertion_plateau(plateau)
        renvoie le nombre de possibilité (de cases vides) du plateau.
        """
        assert type(situation) == str, "situation doit être une chaine de caracteres"

        compteur = 0
        for i in situation:
            if i == "0":
                compteur += 1
        return compteur

def negamax(node, color, chemin = True):
    """
    fonction effectuant l'algorythme negamax, une version amélioré de minimax
    parametres:
        node, un arbre
        color, un nombre (-1 ou 1 en générale) indiquant si le joueur est maximiser ou minimiser
        chemin, optionnel, indique si la branche allant vers le résultat doit être indiqué, par defaut True
    Si chemin, renvoie une liste contenant le nom de la branche a prendre ainsi que la valeur finale
    Sinon, renvoie uniquement la valeur finale
    si l'arbre est une feuille et que chemin = True, renvoie ["", -1]
    sinon si l'arbre est une feuille, renvoie la racine de l'arbre multiplié par color
    """
    if chemin and node.est_feuille():
        return ["", -1]
    elif node.est_feuille():
        return color * node.get_racine()
    else:
        sous_chemin = None
        value = -999999999
        for fils in node.get_fils():
            v = -negamax(fils, -color, False)
            if value < v:
                value = v
                sous_chemin = fils.get_racine()

        if chemin:
            return [sous_chemin, value]
        else:
            return value


################################################################################
################################################################################


class IA_2:
    """
    objet permettant le contrôle d'une IA par renforcement pour jouer au morpion
    """
    def __init__(self, brain):
        """
        constructeur de la classe, elle définit le cerveau et met en place la mémoire de l'IA
        parametres:
            brain, une chaine de caracteres indiquant le chemin vers le fichier de mémoire, s'il n'existe pas, il est crée
        """
        if not read.fichier_existe(brain): # si le fichier censé contenir le cerveau n'existe pos
            read.add_fichier("", brain, "000000000:") # on le crée
        self.fichier_cerveau = brain

    def debut_partie(self):
        """
        méthode permettant de préparer l'IA en vue d'une partie, on converti le fichier de mémoire en arbre
        """
        lecture = read.lire_fichier(self.fichier_cerveau) # on lit le fichier cerveau

        # on transforme le fichier en dictionnaire :
        # "000000000:100000000,010000000,001000000" => {000000000: [100000000, 010000000, 001000000]}
        dico = {}
        for ligne in lecture:
            ligne = ligne.split(":")
            l = ligne[1].split(",")
            dico[ligne[0]] = []
            for elmt in l:
                if elmt != ligne[0]:
                    dico[ligne[0]] += [elmt]

        for key, value in dico.items():
            if value == [""]:
                dico[key] = []
            elif len(value) == 1 and value[0] not in dico.keys():
                dico[key] = int(value[0])


        self.brain = dico
        self.reflexion = "000000000" # on définit le réflexion comme étant l'arbre entier

    def jouer(self, plateau):
        """
        méthode permettant de connaître le coup que va jouer l'IA
        parametres:
            plateau, une liste de liste représentant le plateau
        renvoie les coordonnées du plateau ou joue l'IA
        """
        plateau_actuel = self.plateau_conversion_chaine(plateau)

        if plateau_actuel != self.reflexion:
            if plateau_actuel not in self.brain[self.reflexion]:
                self.brain[self.reflexion] += [plateau_actuel]

            if plateau_actuel not in self.brain.keys():
                self.brain[plateau_actuel] = []

            self.reflexion = plateau_actuel

        if self.compter_caracteres(self.reflexion, "2") == self.compter_caracteres(self.reflexion, "1"):
            choix = negamax_2(self.brain, self.reflexion, -1)
        else:
            choix = negamax_2(self.brain, self.reflexion, 1)

        if choix[1] < 1 and len(self.brain[self.reflexion]) < self.compter_caracteres(self.reflexion, "0"):
            rang = 0
            while rang < len(self.reflexion):
                if self.reflexion[rang] == "0":
                    futur = self.reflexion
                    if self.compter_caracteres(self.reflexion, "2") == self.compter_caracteres(self.reflexion, "1"):
                        futur = futur[:rang] + "1" + futur[rang+1:]
                    else:
                        futur = futur[:rang] + "2" + futur[rang+1:]

                    if futur not in self.brain[self.reflexion]:
                        break

                rang += 1

            x = rang % 3
            y = rang // 3

            self.brain[self.reflexion] += [futur]

            if futur not in self.brain.keys():
                self.brain[futur] = []

            self.reflexion = futur
        else:
            rang = 0
            while choix[0][rang] == self.reflexion[rang]:
                rang += 1

            x = rang % 3
            y = rang // 3

            self.reflexion = choix[0]

        return [y, x] # on renvoie les coordonnées trouvé

    def fin_partie(self, plateau, gagnant):
        """
        méthode permettant de sauvegarder l'arbre de connaissances posséder par l'IA dans le fichier de mémoire, tout en modifiant ce qui y est nécessaire
        paramètres:
            plateau, une liste de liste représentant le plateau de jeu de manière digitale
            gagnant, une chaine de caractères entre 'IA', 'J1' et 'NUL' indiquant le résultat finale de la partie
        """
        plateau_fin = self.plateau_conversion_chaine(plateau)

        nbr_1 = self.compter_caracteres(plateau_fin, "1")
        nbr_2 = self.compter_caracteres(plateau_fin, "2")
        if gagnant == "IA":
            if nbr_1 == nbr_2: # je suis les 2
                gain = 1
            else:
                gain = -1
        elif gagnant == "J1":
            if nbr_1 == nbr_2: # je suis les 1
                gain = 1
            else:
                gain = -1
        else:
            gain = 0

        if plateau_fin != self.reflexion:
            if plateau_fin not in self.brain[self.reflexion]:
                self.brain[self.reflexion] += [plateau_fin]

        if plateau_fin not in self.brain.keys():
            self.brain[plateau_fin] = gain
        elif self.brain[plateau_fin] == []:
            self.brain[plateau_fin] = gain
        else:
            self.brain[plateau_fin] += gain

        # transformation du dictionnaire en chaine de caracteres
        contenu = ""
        for keys, values in self.brain.items():
            contenu += keys
            contenu += ":"
            if type(values) == list:
                for indice in values:
                    contenu += str(indice) + ","
                contenu = contenu[:-1]
            else:
                contenu += str(values)
            contenu += "\n"

        read.suppr_fichier(self.fichier_cerveau, False)
        read.add_fichier("", self.fichier_cerveau, contenu)

    def plateau_conversion_chaine(self, plateau):
        """
        fonction permettant de transformer le plateau de jeu d'un morpion en chaine de caracteres unique
        seule les 'X' et les 'O', tous autre caracteres sera représenté par un '0'
        parametres:
            plateau, une liste composé de liste qui représente le plateau
        renvoie une chaine de caracteres composé de '0' et '1'
        """
        assert type(plateau) in [list, tuple], "plateau doit être une liste"

        nbr = ""
        for i in range(len(plateau)):
            for j in range(len(plateau[i])):
                if plateau[i][j] == "X":
                    nbr += "1"
                elif plateau[i][j] == "O":
                    nbr += "2"
                else:
                    nbr += "0"
        return nbr

    def compter_caracteres(self, situation, caracteres):
        """
        fonction permettant de compter le nombre de positions possibles pour le prochain pion dans un jeu de morpion.
        C'est-à-dire qu'elle compte le nombre de 0 dans une chaine de caracteres
        parametres:
            situation, une chaine de caracteres représentant le plateau, voir fonction convertion_plateau(plateau)
        renvoie le nombre de possibilité (de cases vides) du plateau.
        """
        assert type(situation) == str, "situation doit être une chaine de caracteres"

        compteur = 0
        for i in situation:
            if i == caracteres:
                compteur += 1
        return compteur

def negamax_2(dico, valeur, color, chemin = True):
    """
    fonction effectuant l'algorythme negamax, une version amélioré de minimax
    parametres:
        node, un arbre
        color, un nombre (-1 ou 1 en générale) indiquant si le joueur est maximiser ou minimiser
        chemin, optionnel, indique si la branche allant vers le résultat doit être indiqué, par defaut True
    Si chemin, renvoie une liste contenant le nom de la branche a prendre ainsi que la valeur finale
    Sinon, renvoie uniquement la valeur finale
    si l'arbre est une feuille et que chemin = True, renvoie ["", -1]
    sinon si l'arbre est une feuille, renvoie la racine de l'arbre multiplié par color
    """
    if chemin and dico[valeur] == []:
        return ["", -1]
    elif type(dico[valeur]) is int:
        return color * dico[valeur]
    else:
        sous_chemin = None
        value = -999999999
        for fils in dico[valeur]:
            if cpt_0(fils) < cpt_0(valeur):
                v = -negamax_2(dico, fils, -color, False)
                if value < v:
                    value = v
                    sous_chemin = fils

        if chemin:
            return [sous_chemin, value]
        else:
            return value

def cpt_0(chaine):
    cpt = 0
    for i in chaine:
        if i == "0":
            cpt += 1
    return cpt

if __name__ == "__main__":
    morpion()