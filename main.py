#-------------------------------------------------------------------------------
# Name:        morpion IA
# Purpose:     donner au morpion sur console une interface
#              Créer une interface permettant de jouer au morpion entre 2 humain ou bien contre la machine
#
# Author:      Didier Mathias
#
# Created:     23/04/2021
#-------------------------------------------------------------------------------

# importation des modules
# on importe que les sous-modules nécessaires afin de ne pas importer l'intégralité de la bibliothèque
from tkinter import Tk, Canvas, Button, Menu, Scale, Label, filedialog, messagebox, Toplevel
import module_lecture_fichier as read
from datetime import datetime
from time import sleep
from PIL import ImageTk, Image


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
        self.X = "X" # le symbole de X par défaut
        self.O = "O" # le symbole de O par défaut

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

        def choice(signe):
            """
            sous-fonction permettant de choisir une image comme symbole
            paramètres:
                signe, une chaine de caracteres entre 'X' et 'O' indiquant l'image de quel pion doit être changé
            """
            fichier = filedialog.askopenfilename(initialdir = "bibliotheque_images/",title = "Select file",filetypes = (("PNG files", "*.png"), ("jpeg files", "*.jpg"), ("all files", "*.*"))) # on demande à l'utilisateur de choisir l'image dans l'appareil (placé par défaut dans le répertoire d'image du jeu
            img = Image.open(fichier) # on ouvre l'image afin de l'axaminer

            if messagebox.askokcancel("Validation", "Êtes-vous sûr de vouloir utiliser cette image ? (%s)" %(fichier)): # on demande une validation de l'image sélectionner
                nouv_nom = "bibliotheque_images/" + fichier.split("/")[-1] # on définit un nouveau chemin pour l'imge
                if nouv_nom not in fichier: # si le fichier n'est pas déjà dans la bibliothèque
                    read.mouv_fichier(fichier, nouv_nom) # on copie l'image choisit dans le dossier bibliothèque / pour un accès plus faciole les prochaines fois

                # on ouvre l'image et on lui donne la bonne résolution (afin qu'elle passe dans les cases du plateau de jeu)
                img = Image.open(nouv_nom) # on ouvre l'image
                coeff = max(img.size) / 80 # on définit le coefficient entre la taille actuel et la taille maximum souhaité
                resolution = (int(img.size[0] / coeff), int(img.size[1] / coeff)) # on définit la nouvelle résolution
                img = img.resize(resolution, Image.ANTIALIAS) # on applique cette résolution à l'image avec la meilleure qualité possible (éviter les bouillis de pixel)
                img = ImageTk.PhotoImage(img) # on transforme l'iamge en une image utilisable sur tkinter

                # on applique l'image au signe correspondant
                if signe == "X":
                    self.X = img
                else:
                    self.O = img

        def see(signe):
            """
            sous-fonction permettant de visualiser l'apparence d'un pion sur le terrain de jeu
            parametres:
                signe, une chaine de caracteres, 'X' ou 'O' indiquant le signe à afficher
            renvoi une sous-fenetre tkinter avec l'apparence du pion affiché
            """
            # on définit une sous-fenêtre tkinter
            visualisation = Toplevel(self.root)
            visualisation.title(signe)

            Label(visualisation, text = "Visualisation du signe : %s" %(signe)).pack() # on affiche quel signe est montré sur la fenêtre
            cadre = Canvas(visualisation, width = 100, height = 100, bg = "white") # on définit un canvas de la taille d'une case de morpion pour l'affichage

            # on affiche le signe correspondant dans le canvas
            if signe == "X": # si on doit afficher le symbole X
                if self.X == "X": # si on à l'image de base
                    cadre.create_line(15, 15, 85, 85) # on crée un simple X
                    cadre.create_line(85, 15, 15, 85)
                else: # sinon
                    cadre.create_image(50, 50, image = self.X) # on affiche l'image self.X
            else: # sinon, on doit afficher le symbole O
                if self.O == "O": # si on a l'image de base
                    cadre.create_oval(15, 15, 85, 85) # on crée un simple O
                else: # sinon
                    cadre.create_image(50, 50, image = self.O) # on affiche l'image self.O

            cadre.pack() # on affiche le canvas dans la sous-fenêtre
            visualisation.mainloop() # on affiche la sous-fenêtre

        # on crée une barre de Menu
        menubar = Menu(self.root)

            # un sous-menu pour choisir qui joue en premier
        tour = Menu(menubar, tearoff = 0)
        tour.add_radiobutton(label = "Joueur 1", command = lambda x=None: turn("J1"))
        tour.add_radiobutton(label = "IA/ Joueur 2", command = lambda x=None: turn("J2"))

            # un sous-menu pour visualiser et sélectionner l'apparence des pions
        symbole = Menu(menubar, tearoff = 0)
                # options pour X
        symbole_X = Menu(symbole, tearoff = 0)
        symbole_X.add_command(label = "Choisir", command = lambda x=None: choice("X"))
        symbole_X.add_command(label = "Visualiser", command = lambda x=None: see("X"))
                # options pour O
        symbole_O = Menu(symbole, tearoff = 0)
        symbole_O.add_command(label = "Choisir", command = lambda x=None: choice("O"))
        symbole_O.add_command(label = "Visualiser", command = lambda x=None: see("O"))
                # on ajoute les options
        symbole.add_cascade(label = "1er pion : X", menu = symbole_X)
        symbole.add_cascade(label = "2er pion : O", menu = symbole_O)

        # on ajoute les sous-menus au menu
        menubar.add_cascade(label = "Tour", menu = tour)
        menubar.add_cascade(label = "Selection symbole", menu = symbole)
        # on définit le menu comme menu de la fenêtre
        self.root.config(menu = menubar)

        # on lance l'interface et l'affichage de l'écran principal (self.lancement())
        self.lancement()
        self.root.mainloop()

    def lancement(self):
        """
        méthode permettant de lancer l'écran principal du morpion avec les choix des différentes parties
        """
        self.log_contenu = "" # contient ce que l'on va mettre dans le log (fichier contenant information du jeu)

        self.vider_root("Menu") # on enlève ce qui se trouve sur le fenêtre, sauf le menu

        # on initialise les variables (attributs) nécéssaires à chaque partie
        self.turn = "J1" # le joueur qui commence la partie
        self.premier = True # si J1 commence
        self.fin = False # si la partie est finie

        # on affiche les différents choix de partie
        Button(self.root, text = "Humain VS Humain", command = self.partie_humaine, width = 20, height = 5).pack()
        Button(self.root, text = "Humain VS IA", command = self.partie_IA_renforcement, width = 20, height = 5).pack()
        Button(self.root, text = "IA VS IA", command = self.entrainement, width = 20, height = 5).pack()

    def dessiner_plateau(self):
        """
        méthode permettant de créer le plateau de jeu, tout autant visuel que digital
        """
        # plateau digital, une matrice ne contenant que des '_', représentation d'une case vide
        self.plateau = [
        ["_", "_", "_"],
        ["_", "_", "_"],
        ["_", "_", "_"]]

        # plateau visuel
        self.jeu = Canvas(self.root, width = 300, height = 300, bg = "white") # on initialise le canvas
            # on dessine le plateau de jeu (2 traits verticaux et 2 trait horizontaux)
        self.jeu.create_line(0, 100, 300, 100)
        self.jeu.create_line(0, 200, 300, 200)
        self.jeu.create_line(100, 0, 100, 300)
        self.jeu.create_line(200, 0, 200, 300)


    def partie_humaine(self):
        """
        méthode permettant d'éxécuter un morpion entre 2 humain
        """
        # on met les premières informations dans le log, soit la date et le type de partie
        date = datetime.now()
        self.log_contenu += "Partie du %d/%d/%d\n" %(date.day, date.month, date.year) # la date
        self.log_contenu += "à %d:%d:%d\n" %(date.hour, date.minute, date.second) # l'heure exacte
        self.log_contenu += "Partie Humain VS Humain\n\n" # le type de partie

        self.vider_root("Menu") # on enlève les boutons de choix de partie

        self.dessiner_plateau() # on crée le plateau

        def action(event):
            """
            sous-fonction permettant de jouer ou de retourner à l'écran titre selon le déroulement de la partie
            parametres:
                event, un event souris de clic sur la canvas
            """
            if self.fin: # si la partie est finie
                nom = "log_%s-%s-%s" %(date.day, date.month, date.year) # on détermine le nom de fichier de base pour le log (log_jour-mois-année)

                i = 0 # i sert d'indice pour déterminer qu'elle nom de fichier n'est pas déjà pris
                while read.fichier_existe("enregistrements/%s(%d).txt" %(nom, i)): # tant que le nom de fichier avec l'indice existe déjà
                    i += 1 # on incrémente l'indice de 1

                read.add_fichier("enregistrements", "%s(%d).txt" %(nom, i), self.log_contenu) # on ajoute le fichier avec ce qu'il contient

                self.lancement() # on relance l'interface principale du jeu
            else: # sinon, la partie n'est pas finie
                self.coup(event) # on joue avec l'emplacement du clic

        self.jeu.bind("<1>", action) # on met un bind afin de détecter les clics sur le canvas
        self.jeu.pack() # on affiche le plateau de jeu

    def partie_IA_renforcement(self):
        """
        méthode permettant de faire une partie contre une IA à renforcement, elle apprend avec les parties précédentes joué
        elle devient donc de plus en plus forte au fur et à mesure des parties
        """
        # on met les premières informations dans le log
        date = datetime.now() # on utilise le module datetime afin de conna^tre la date actuel exacte
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
                nom = "log_%s-%s-%s" %(date.day, date.month, date.year) # on détermine le nom de fichier de base pour le log (log_jour-mois-année)

                i = 0 # i sert d'indice pour déterminer qu'elle nom de fichier n'est pas déjà pris
                while read.fichier_existe("enregistrements/%s(%d).txt" %(nom, i)): # tant que le nom de fichier avec l'indice existe déjà
                    i += 1 # on incrémente l'indice de 1

                read.add_fichier("enregistrements", "%s(%d).txt" %(nom, i), self.log_contenu) # on ajoute le fichier avec ce qu'il contient

                # on met fin à la partie pour l'IA, on lui indique le résultat de la partie
                if self.turn == "J1": # si c'est au tour de J1 et que la partie est finie, cela signifie que l'IA a gagné
                    ordi.fin_partie(self.plateau, "IA")
                elif self.turn == "J2": # sinon, si c'est au tour de J2, cela signifie que l'IA a perdu
                    ordi.fin_partie(self.plateau, "J1")
                else: # sinon, on est sur une partie nul
                    ordi.fin_partie(self.plateau, "NUL")

                self.lancement() # on relance le jeu
            else: # sinon, la partie est en cours
                if self.turn == "J1": # si c'est à J1 de jouer
                    if self.coup(event) != "": # si le coup souhaiter par J1 est possible, ainsi, on évite à l'IA de jouer 2 fois d'affiler si le joueur clique au maivais endroit
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
        méthode permettant de faire jouer l'IA contre une autre IA semblable mais avec un autre cerveau afin d'avoir des parties diversifiées
        """
        def entrainement_go():
            """
            sous-fonction permettant de lancer le processus d'entrainement
            """
            repet = repetitions.get() # on détecte le nombre de partie choisit par l'utilisateur

            self.vider_root("Menu") # on vide l'écran de ce qu'il contient

            self.dessiner_plateau() # on crée le plateau

            # on initialise les 2 IA en leur indiquant des fichiers différents
            ordi = IA_2("cerveau.txt")
            ordi_2 = IA_2("cerveau_2.txt")

            # progression va indiquer le pourcentage de la demande effectué
            progression = Label(self.root, text =  "0.0% effectué", font = ('Times', -20, 'bold'))
            progression.pack()

            # on crée une barre de chargement, plus visuel, qui représente le pourcentage affiché
            progression_bar = Canvas(self.root, width = 1000, height = 20)
            progression_bar.create_rectangle(0, 0, 1000, 200, outline = "white", fill = "grey")
            progression_bar.pack()

            # label indiquant ce que représente le canvas juste en dessous
            Label(self.root, text = "Partie en cours :", font = ("Times", -10, "bold")).pack()
            self.jeu.pack()

            for r in range(repet): # on répéte le nombre de fois choisit

                # on réinitialise le plateau de jeu afin que les IA puisse jouer sur un plateau vide
                self.jeu.destroy()
                self.dessiner_plateau()
                self.jeu.pack()

                # On lance une partie en supposant que l'IA 1 est J1
                self.fin = False # la partie n'est pas finie de base

                # on initialise les 2 IA pour une nouvelle partie
                ordi.debut_partie()
                ordi_2.debut_partie()
                self.turn = "J1" # on détermine le premier jouer, J1 = ordi, J2 = ordi_2

                while not self.fin: # tant que la partie n'est pas finie
                    self.coup(ordi.jouer(self.plateau)) # l'IA 1 joue
                    if not self.fin: # si la partie n'est pas fini
                        self.coup(ordi_2.jouer(self.plateau)) # l'IA 2 joue

                # Quand la partie est finie, on enregistre les données en indiquant le résultat de la partie à chaque IA, on utilise la même logique de sauvegarde que pour les parties IA VS Humain
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
                pourcentage = round(100*r/repet, 2) # on arrondit le chiffre de pourcentage à 2 décimal (comme le calcul renvoie un flottant, on évite qu'il y ait trop de décimal affiché)
                progression.configure(text = str(pourcentage) + "% effectué")

                progression_bar.delete('chargement') # on évite d'avoir trop d'item dans le canvas on enlevent le rectangle précedent
                progression_bar.create_rectangle(0, 0, pourcentage * 10, 20, fill = "black", tags = "chargement") # on crée un rectangle qui rempli un certain pourcentage de la barre, ce qui crée une impression de progression (barre de chargement)
                self.root.update() # on rafraichit la fenêtre afin que les changements s'affichent dans le canvas, ainsi, on voit les plateaux de jeu des IA quand la partie est finie

                sleep(0.1) # on attend 0.1s entre chaque partie à cause de problèmes d'écriture et de suppression des fichiers (des problèmes d'accès)

            self.lancement() # une fois l'entrainement terminés, on relance le jeu

        self.vider_root("Menu") # on enlève ce qu'il y a dans le fenêtre

        Label(self.root, text = "Nombres de partie d'entrainements :").pack() # on met un label pour indiquer ce que l'utilisateur doit faire
        # on met un scale afin de choisir un nombre de parties a effectué par les IA
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
            return "" # on arrête la fonction ici si l'emplacement n'est pas libre, si l'emplacement choisit n'est pas vide


        def X(x, y):
            """
            sous-fonction permettant de placer un pion X sur le plateau visible à la position souhaiter sur le plateau digital
            on respecte la représentation du symbole O
            """
            if self.X == "X":
                self.jeu.create_line(x*100 +15, y*100 +15, x*100 +85, y*100 +85)
                self.jeu.create_line(x*100 +85, y*100 +15, x*100 +15, y*100 +85)
            else:
                self.jeu.create_image(x*100 +50, y*100 +50, image = self.X)

        def O(x, y):
            """
            sous-fonction permettant de placer un pion O sur le plateau visible à la position souhaiter sur le plateau digital
            on respecte la représentation du symbole O
            """
            if self.O == "O":
                self.jeu.create_oval(x*100 +15, y*100 +15, x*100 +85, y*100 +85)
            else:
                self.jeu.create_image(x*100 +50, y*100 +50, image = self.O)


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
        # grâce à cela et à self.turn (dit c'est au tour de qui de jouer), on ajoute au log une ligne disant qui joue
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
                self.jeu.create_rectangle(75, 125, 225, 175, fill = "white") # on crée un rectangle blanc afin que le résultat de la partie reste visible
                self.jeu.create_text(150, 150, font = ('Times', -20, 'bold'), text = phrase) # on écrit le résultat de la partie au milieu du plateau de jeu

            self.fin = True # le jeu est fini
            # en fonction de quel possibilité à été faite, on crée un trait montrant la victoire, l'alignement des trois pions
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
                self.turn = "NUL" # on change le tour à 'NUL' afin d'indiquer que c'est un match nul
                ecrire_fin("Match NUL") # on affiche le résultat de la partie

                self.log_contenu += "\nMATCH NUL" # on ajoute au log le résultat de la partie

            if verif != "PLEIN": # si ce n'est pas un match nul
                if self.turn == "J1": # si c'est au tour de J1 de jouer
                    ecrire_fin("J2 a Gagner") # alors on affiche J2 comme vainqueur
                else: # sinon
                    ecrire_fin("J1 a Gagner") # on affiche J1 comme vainqueur

                # on ajoute au log le résultat de la partie en fonction de qui joue
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

        self.fichier_cerveau = brain # on définit le fichier de cerveau

    def debut_partie(self):
        """
        méthode permettant de préparer l'IA en vue d'une partie, on converti le fichier de mémoire en dictionnaire
        """
        lecture = read.lire_fichier(self.fichier_cerveau) # on lit le fichier cerveau

        # on transforme le fichier en dictionnaire :
        # "000000000:100000000,010000000,001000000" => {000000000: [100000000, 010000000, 001000000]}
        dico = {} # le dico est vide au début
        for ligne in lecture: # pour chaque ligne du fichier
            ligne = ligne.split(":") # on sépare la clé de ses valeurs (séparées par ':')
            l = ligne[1].split(",") # dans les valeurs, on sépare les differentes valeurs entre elles (séparées par ',')
            dico[ligne[0]] = [] # on définit le dictionnaire à la clé trouvé comme une liste vide
            for elmt in l: # pour chaque valeurs trouvé pour la clé
                if elmt != ligne[0]: # si la valeur est différentes de la clé (on prévient les potentielles boucles infinis qui pourrait survenir)
                    dico[ligne[0]] += [elmt] # alors on ajoute cette valeurs à la liste du dictionnaire à la clé correspondante

        # on change les scores présent dans le dictionnaire en nombre, car une fois extraites du fichier et transformé, se sont des listes de chaine de caracteres
        for key, value in dico.items(): # pour chaque clé et valeurs du dictionnaire
            if value == [""]: # si la valeur est quelque chose de vide, cela signifie que le cerveau vient d'être crée
                dico[key] = [] # alors on enlève cette élément "" car il pourrait causer des bugs
            elif len(value) == 1 and value[0] not in dico.keys(): # sinon si la clé ne contient qu'une valeurs est que celle-ci ne se trouve pas dans les clés du dictionnaire, cela signifie que c'est sensé être un score
                dico[key] = int(value[0]) # alors on transforme la liste en un score

        self.brain = dico # on définit le cerveau comme étant le dico, même si c'est plutôt l'ensemble de ses connaissances (mémoire)
        self.reflexion = "000000000" # on définit le réflexion comme étant le plateau vide (compréhensible pour l'IA)

    def jouer(self, plateau):
        """
        méthode permettant de connaître le coup que va jouer l'IA
        parametres:
            plateau, une liste de liste représentant le plateau
        renvoie les coordonnées du plateau ou joue l'IA
        """
        plateau_actuel = self.plateau_conversion_chaine(plateau) # on convertit la liste de liste en une chaine de caracteres compréhensibles par l'IA

        if plateau_actuel != self.reflexion: # si le plateau actuel n'est pas celui dans lequel réfléchit actuellement l'IA
            if plateau_actuel not in self.brain[self.reflexion]: # si c'est une nouvelle situation pour la situation précédente
                self.brain[self.reflexion] += [plateau_actuel] # on ajoute cette situation à la liste des situations connues pour la situation précédente

            if plateau_actuel not in self.brain.keys(): # si la situation est une toute nouvelle situation
                self.brain[plateau_actuel] = [] # on crée cette situation dans le cerveu avec comme valeur une liste vide

            self.reflexion = plateau_actuel # on déplace la réflexion de l'IA vers le plateau actuel

        if compter_caracteres(self.reflexion, "2") == compter_caracteres(self.reflexion, "1"): # s'il y a autant de X que de O sur le plateau
            choix = negamax_2(self.brain, self.reflexion, -1) # on doit réfléchir ainsi
        else: # sinon
            choix = negamax_2(self.brain, self.reflexion, 1) # on doit réfléchir ainsi

        if choix[1] < 1 and len(self.brain[self.reflexion]) < compter_caracteres(self.reflexion, "0"): # si le meilleure chose à faire est de perdre ET que toutes les situations possibles n'ont pas été explorées
            # alors, on joue une nouvelle situation pour essayer de gagner
            rang = 0 # indice permettant de déterminer quel coup n'as pas encore été fait
            while rang < len(self.reflexion): # tant que tout le plateau n'as pas été parcoure
                if self.reflexion[rang] == "0": # si la position actuelle est vide
                    futur = self.reflexion # on crée une supposition du futur plateau
                    if compter_caracteres(self.reflexion, "2") == compter_caracteres(self.reflexion, "1"): # s'il y a autant de X que de O, cela signifie qu'il faudrat jouer O
                        futur = futur[:rang] + "1" + futur[rang+1:] # on change l'emplacement dans le futur avec un X
                    else: # sinon
                        futur = futur[:rang] + "2" + futur[rang+1:] # on change l'emplacement choisit dans le futur par un O

                    if futur not in self.brain[self.reflexion]: # si la situation fitur supposé n'as pas encore été faite
                        break # on casse la boucle puisque son objectif est accompli

                rang += 1 # on incrémente l'indice de 1

            # on transforme l'indice rang en positions x et y sur un plateau normal
            x = rang % 3
            y = rang // 3

            self.brain[self.reflexion] += [futur] # on ajoute la position choisit au coup possible

            if futur not in self.brain.keys(): # si le coup choisit est une toute nouvelle situation
                self.brain[futur] = [] # on crée cette ssituation dans le cerveau

            self.reflexion = futur # on place la réflexion dans ce nouveau plateau
        else: # sinon, on joue le coup chosit
            rang = 0 # indice permettant de situé le coup sur le plateau
            while choix[0][rang] == self.reflexion[rang]:
                rang += 1

            # on transforme l'emplacement choisit en des coordonnées de plateau
            x = rang % 3
            y = rang // 3

            self.reflexion = choix[0] # on place la réflexion dans cette situation

        return [y, x] # on renvoie les coordonnées trouvé

    def fin_partie(self, plateau, gagnant):
        """
        méthode permettant de sauvegarder le dictionnaire de connaissances posséder par l'IA dans le fichier de mémoire, tout en modifiant le score final
        paramètres:
            plateau, une liste de liste représentant le plateau de jeu de manière digitale
            gagnant, une chaine de caractères entre 'IA', 'J1' et 'NUL' indiquant le résultat finale de la partie
        """
        plateau_fin = self.plateau_conversion_chaine(plateau) # on convertit le plateau actuel en une chaine de cracteres conpréhensible par l'IA

        nbr_1 = compter_caracteres(plateau_fin, "1") # on compte le nombre de X sur le plateau
        nbr_2 = compter_caracteres(plateau_fin, "2") # on compte le nombre de O sur le plateau
        if gagnant == "IA": # si le gagnant et l'IA
            if nbr_1 == nbr_2: # si on voit que l'IA jouait les O
                gain = 1 # on définit le gain comme étant à 1
            else: # sinon, c'est que l'on joue les X
                gain = -1 # on définit le gain comme étant de -1
        elif gagnant == "J1": # si le gagnant est l'adversaire
            if nbr_1 == nbr_2: # si l'IA joue les X
                gain = 1 # le gain est de 1
            else: # sinon, l'IA joue les O
                gain = -1 # le gain est de -1
        else: # sinon, c'est une partie nul
            gain = -1

        if plateau_fin != self.reflexion: # si le plateau actuel n'est pas celui dans lequel on réfléchit
            if plateau_fin not in self.brain[self.reflexion]: # si la plateau actuel n'est pas dans les situations possibles pour ma réfléxion
                self.brain[self.reflexion] += [plateau_fin] # on ajoute cette situation à la liste des situations déjà présentes

        if plateau_fin not in self.brain.keys(): # si la situation actuel est une toute nouvelle situation jamais vus auparavant
            self.brain[plateau_fin] = gain # on crée cette situation dans le dictionnaire en y indiquant le gain
        elif self.brain[plateau_fin] == []: # sinon, si cette situation existe mais qu'elle a pour valeur un liste vide
            self.brain[plateau_fin] = gain # on remplace la liste par le gain
        else: # sinon, cette situation existe déjà et sa valeur est un score
            self.brain[plateau_fin] += gain # on ajoute le gain aux score déjà présent

        # transformation du dictionnaire en chaine de caracteres en vue de son enregistrement
        contenu = "" # le contenu est vide au début
        for keys, values in self.brain.items(): # pour chaque clé et valeur dans le cerveau
            contenu += keys # on ajoute la clé au contenu
            contenu += ":" # on ajoute ':' au contenu
            if type(values) == list: # si la valeur est une liste
                for elmt in values: # pour chaque élément de cette liste
                    contenu += elmt + "," # on ajoute l'élément au contenu suivit de ','
                contenu = contenu[:-1] # on enlève le dernier caracteres, soit un ',' (ce qui pourrait causer des bugs)
            else: # sinon, on a ffaire à un score
                contenu += str(values) # on ajoute le score au contenu
            contenu += "\n" # on passe à la ligne suivante

        read.suppr_fichier(self.fichier_cerveau, False) # on enlève le fichier du cerveau sans demander l'avis à l'utilisateur
        read.add_fichier("", self.fichier_cerveau, contenu) # on crée le fichier cerveau en y mettant la chaine de caracteres représentant le cerveau

    def plateau_conversion_chaine(self, plateau):
        """
        méthode permettant de transformer le plateau de jeu d'un morpion en chaine de caracteres unique compréhensibles par l'IA
        parametres:
            plateau, une liste de liste qui représente le plateau
        renvoie une chaine de caracteres composé de '0', '1' et '2'
        """
        assert type(plateau) in [list, tuple], "plateau doit être une liste" # on vérifie que le plateau est bien un tableau

        nbr = "" # la chaine est vide au départ
        for i in range(len(plateau)): # pour i allant de 0 à la longueur de plateau
            for j in range(len(plateau[i])): # pour j allant de 0 à la longueur d'une sous-liste de plateau
                if plateau[i][j] == "X": # si l'élément est un 'X'
                    nbr += "1" # on ajoute un '1' à la chaine
                elif plateau[i][j] == "O": # sinon si l'élément est un 'O'
                    nbr += "2" # on ajoute un '2' à la chaine
                else: # sinon
                    nbr += "0" # on ajoute un '0' à la chaine
        return nbr # on retourne la chaine trouvé


def negamax_2(dico, valeur, coeff, chemin = True):
    """
    fonction permettant d'effectuer l'algorithme negamax (amélioration de minimax) dans un dictionnaire représentant un arbre, le tout pour choisir le meilleur choix à faire dans un morpion
    parametres:
        dico, un dictionnaire représentant un arbre dans sa globalité
        valeur, une clé du dictionnaire, représentant le point de départ de l'algorithme
        coeff, un nombre qui est le coefficient à appliquer aux score trouvé
        chemin, optionnel, un booléen indiquant s'il le chemin(seulement le prochain élément) doit être indiqué, par défaut sur True
    Renvoie:
        si chemin:
            une liste construite tel que [clé_de_la_prochaine_valeur, score_finale_atteignable]
        sinon:
            un nombre qui est le score finale atteignable
    """
    if chemin and dico[valeur] == []: # si chemin est que le dico en valeur est une liste vide
        return ["", -1] # on renvoie un résultat prédéfinis
    elif type(dico[valeur]) is int: # sinon, si le dico en valeur est un score
        return coeff * dico[valeur] # on renvoie le score multiplié par le coefficient
    else: # sinon
        sous_chemin = None # on définit le sous-chemin de base comme None
        value = -999999999 # on définit le meilleure score de base comme un nombre très bas, ainsi, tous nouveau score sera supérieur
        for fils in dico[valeur]: # pour chaque fils dans le dico en valeur
            if compter_caracteres(fils, "0") < compter_caracteres(valeur, "0"): # si le fils est possible (s'il y a moins de cases vide avec la situation valeur qu'avec la situation fils)
                v = -negamax_2(dico, fils, -coeff, False) # v est égale au négatif du negamax du fils avec avec le négatif du coefficient
                if value < v: # si le meilleure score actuel est plus petit que le score trouvé
                    value = v # le meilleure score devient le score actuel
                    sous_chemin = fils # le sous-chemin devient le fils

        if chemin: # si chemin est sur True
            return [sous_chemin, value] # on renvoie une liste avec [clé_de_la_prochaine_valeur, score_finale_atteignable]
        else: # sinon
            return value # on renvoie le score finale atteignable


def compter_caracteres(chaine, caractere):
    """
    fonction permettant de compter le nombre d'occurences d'un caractere dans une chaine de caracteres
    parametres:
        chaine, une chaine de caracteres dans laquelle cherché le caractere
        caractere, un caracteres à chercher dans chaine
    renvoie le nombre d'occurrences de 'caractere' dans 'chaine'
    """
    assert type(chaine) == str, "situation doit être une chaine de caracteres" # on vérifie que chaine est une chaine de caracteres

    compteur = 0 # on initialise le compteur a 0
    for i in chaine: # pour chaque caractere dans 'chaine'
        if i == caractere: # si le caractere vu et celui que l'on cherche
            compteur += 1 # on incrémente le compteur de 1

    return compteur # on renvoie le nombre d'occurrences trouvé


if __name__ == "__main__": # si on éxécute ce script directement
    morpion() # on lance la fonction morpion