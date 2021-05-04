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


"""
faire en sorte que l'IA puisse jouer contre elle-même
"""

class morpion:
    """
    objet permettant d'éxécuter un morpion
    """
    def __init__(self):
        """
        constructeur de la classe
        on crée ici la barre de menu ainsi que les variables de bases nécessaires
        on lance directement le jeu
        """
        self.root = Tk()
        self.root.title("Morpion")

        self.turn = "J1"
        self.symbole = "X"

        def turn(player):
            self.turn = player

        menubar = Menu(self.root)

        tour = Menu(menubar, tearoff = 0)
        tour.add_radiobutton(label = "Joueur 1", command = lambda x=None: turn("J1"))
        tour.add_radiobutton(label = "IA/ Joueur 2", command = lambda x=None: turn("J2"))
        menubar.add_cascade(label = "Tour", menu = tour)

        self.root.config(menu = menubar)

        self.lancement()
        self.root.mainloop()

    def lancement(self):
        """
        méthode permettant de lancer l'écran principal du morpion avec les choix de partie
        """
        self.vider_root("Menu") # on enlève ce qui se trouve sur le fenêtre

        # on initialise les variables (attributs)
        self.turn = "J1"
        self.symbole = "X"
        self.fin = False

        # on affiche les différents choix de partie
        Button(self.root, text = "2 joueurs", command = self.partie_humaine, width = 20, height = 5).pack()
        Button(self.root, text = "IA renforcement", command = self.partie_IA_renforcement, width = 20, height = 5).pack()
        Button(self.root, text = "entrainement IA", command = self.entrainement, width = 20, height = 5).pack()

    def dessiner_plateau(self):
        """
        méthode permettant de créer le plateau de jeu, tout autant visuel que digital
        """
        self.plateau = [
        ["_", "_", "_"],
        ["_", "_", "_"],
        ["_", "_", "_"]]

        self.jeu = Canvas(self.root, width = 300, height = 300, bg = "white")

        self.jeu.create_line(0, 100, 300, 100)
        self.jeu.create_line(0, 200, 300, 200)
        self.jeu.create_line(100, 0, 100, 300)
        self.jeu.create_line(200, 0, 200, 300)


    def partie_humaine(self):
        """
        méthode permettant d'éxécuter un morpion entre 2 humain sur une grille de 3X3
        """
        self.vider_root("Menu")

        self.dessiner_plateau()

        def action(event):
            """
            sous-fonction permettant de jouer ou de retourner à l'écran titre selon le déroulement de la partie
            parametres:
                event, un event souris de clic
            """
            if self.fin:
                self.lancement()
            else:
                self.coup(event)

        self.jeu.bind("<1>", action)
        self.jeu.pack()

    def partie_IA_renforcement(self):
        """
        méthode permettant de faire une partie contre une IA à renforcement, elle apprend avec les parties précédentes joué
        """
        self.vider_root("Menu")

        self.dessiner_plateau()

        def action(event):
            """
            sous-fonction permettant de jouer ou de retourner à l'écran titre selon le déroulement de la partie
            parametres:
                event, un event souris de clic
            """
            if self.fin:
                if self.turn == "J1":
                    ordi.fin_partie(self.plateau, "IA")
                elif self.turn == "J2":
                    ordi.fin_partie(self.plateau, "J1")
                else:
                    ordi.fin_partie(self.plateau, "NUL")
                self.lancement()
            else:
                if self.turn == "J1":
                    if self.coup(event) != "":
                        self.coup(event)
                        if not self.fin:
                            if self.symbole == "X":
                                self.coup(ordi.jouer(self.plateau, "O"))
                            else:
                                self.coup(ordi.jouer(self.plateau, "X"))
                else:
                    if self.symbole == "X":
                        self.coup(ordi.jouer(self.plateau, "O"))
                    else:
                        self.coup(ordi.jouer(self.plateau, "X"))

        ordi = IA("cerveau_2.txt")
        self.jeu.bind("<1>", action)
        self.jeu.pack()


    def entrainement(self):
        def entrainement_go():
            repet = repetitions.get()

            self.vider_root("Menu")

            self.dessiner_plateau()

            ordi = IA("cerveau.txt")
            ordi_2 = IA("cerveau_2.txt")

            # progression va indiquer le pourcentage de la demande effectué
            progression = Label(self.root, text =  "0.0% effectué", font = ('Times', -20, 'bold'))
            progression.pack()

            # on crée une barre de chargement, plus visuel
            progression_bar = Canvas(self.root, width = 1000, height = 20)
            progression_bar.create_rectangle(0, 0, 1000, 200, outline = "white", fill = "grey")
            progression_bar.pack()

            for r in range(repet):
                # on réinitialise le plateau de jeu afin que les IA puisse jouer
                self.plateau = [
                ["_", "_", "_"],
                ["_", "_", "_"],
                ["_", "_", "_"]]

                self.fin = False
                while not self.fin:
                    self.coup(ordi.jouer(self.plateau, "X"))
                    if not self.fin:
                        self.coup(ordi_2.jouer(self.plateau, "O"))

                # Quand la partie est finie, on enregistre les données
                if self.turn == "J1":
                    ordi.fin_partie(self.plateau, "IA")
                    ordi_2.fin_partie(self.plateau, "J1")
                elif self.turn == "J2":
                    ordi.fin_partie(self.plateau, "J1")
                    ordi_2.fin_partie(self.plateau, "IA")
                else:
                    ordi.fin_partie(self.plateau, "NUL")
                    ordi_2.fin_partie(self.plateau, "NUL")

                ordi.debut_partie()
                ordi_2.debut_partie()

                """
                probleme de freeze du au fait que tkinter fonctionne avec des mainloop
                utilisation de update pour régler le probleme
                """
                # on met à jour les informations de progression
                pourcentage = int(1000*r/repet)/10 # on obtient un pourcentage avec une décimal (ça évite d'avoir trop de décimal)
                progression.configure(text = str(pourcentage) + "% effectué")

                progression_bar.delete('chargement') # on évite d'avoir trop d'item dans le canvas
                progression_bar.create_rectangle(0, 0, pourcentage * 10, 20, fill = "black", tags = "chargement")
                self.root.update() # on rafraichit la fenêtre afin que les changements s'affichent

            """
            il faudrait faire en sorte de mixer les deux fichiers cerveau.txt et cerveau_2.txt
            comme ça l'IA aura les connaissances des deux adversaires
            """

            self.lancement()

        self.vider_root("Menu")

        Label(self.root, text = "Nombres de partie d'entrainements :").pack()
        repetitions = Scale(self.root, orient='horizontal', from_=50, to=10000, resolution=1, length=500)
        repetitions.pack()

        Button(self.root, text = "GO !", command = entrainement_go).pack()

    def vider_root(self, *epargner):
        for c in self.root.winfo_children():
            if c.winfo_class() not in epargner:
                c.destroy()


    def coup(self, event):
        """
        méthode permettant d'effectuer un coup sur le plateau, elle place le pion correspondant et annonce la fin de la partie
        parametres:
            event, un event souris avec les coordonnes de la souris sur le plateau
        """
        if type(event) == list:
            x = event[1]
            y = event[0]
        else:
            x = event.x // 100
            y = event.y // 100

        if self.plateau[y][x] == "_":
            if self.turn == "J1":
                self.plateau[y][x] = self.symbole
            else:
                if self.symbole == "X":
                    self.plateau[y][x] = "O"
                else:
                    self.plateau[y][x] = "X"
        else:
            return ""

        if self.turn == "J1":
            if self.symbole == "X":
                self.jeu.create_line(x*100 +15, y*100 +15, x*100 +85, y*100 +85)
                self.jeu.create_line(x*100 +85, y*100 +15, x*100 +15, y*100 +85)
            else:
                self.jeu.create_oval(x*100 +15, y*100 +15, x*100 +85, y*100 +85)
            self.turn = "J2"
        else:
            if self.symbole == "O":
                self.jeu.create_line(x*100 +15, y*100 +15, x*100 +85, y*100 +85)
                self.jeu.create_line(x*100 +85, y*100 +15, x*100 +15, y*100 +85)
            else:
                self.jeu.create_oval(x*100 +15, y*100 +15, x*100 +85, y*100 +85)
            self.turn = "J1"

        verif = self.verifier_plateau()

        if verif != None:
            self.fin = True # le jeu est fini
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
            # plein
            else:
                self.turn = "NUL"
                self.jeu.create_rectangle(75, 125, 225, 175, fill = "white")
                self.jeu.create_text(150, 150, font = ('Times', -20, 'bold'), text = "Match NUL")

            """
            faire en sorte de faire un rectangle blanc encadrant le texte afin qu'il reste visible
            """

            if verif != "PLEIN":
                if self.turn == "J1":
                    self.jeu.create_rectangle(75, 125, 225, 175, fill = "white")
                    self.jeu.create_text(150, 150, font = ('Times', -20, 'bold'), text = "J2 a Gagner")
                else:
                    self.jeu.create_rectangle(75, 125, 225, 175, fill = "white")
                    self.jeu.create_text(150, 150, font = ('Times', -20, 'bold'), text = "J1 a Gagner")

    def verifier_plateau(self):
        """
        méthode permettant de connaitre l'etat du plateau : partie nul ou si quelqu'un a gagné
        renvoie une chaine de caracteres indiquant l'état du plateau
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
        if not read.fichier_existe(brain):
            read.add_fichier("", brain, "000000000:")
        self.fichier_cerveau = brain

        self.debut_partie()

    def debut_partie(self):
        """
        méthode permettant de préparer l'IA en vue d'une partie, on converti le fichier de mémoire en arbre
        """
        lecture = read.lire_fichier(self.fichier_cerveau)

        # on transforme le fichier en dictionnaire
        dico = {}
        for ligne in lecture:
            ligne = ligne.split(":")
            l = ligne[1].split(",")
            dico[ligne[0]] = []
            for elmt in l:
                if elmt != ligne[0]:
                    dico[ligne[0]] += [elmt]

        def creation_arbre(dico, racine):
            """
            sous-fonction permettant de creer un arbre des possibilité de jeu à partir d'un dictionnaire
            chaque clé de l'arbre devient une branche, chaque element dans la liste de valeur d'une clé devient soit une branche s'il existe en tant que clé, soit une feuille mais en tant que valeur
            parametres:
                dico, un dictionnaire récapitulant l'arbre
                racine, une clé du dictionnaire étant la racine de l'arbre
            """

            """
            doit être transformer en algo iteratif
            le recursif n'etant pas assez puissant
            """


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
            dico_arbre = {}
            for keys in dico.keys():
                if len(dico[keys]) == 1 and dico[keys][0] not in dico.keys():
                    dico_arbre[keys] = arbre(keys, arbre(int(dico[keys][0])))
                else:
                    dico_arbre[keys] = arbre(keys)

            for racine, noeud in dico_arbre.items():
                for branche in dico[racine]:
                    if branche in dico.keys():
                        noeud.add_fils(dico_arbre[branche])

            return dico_arbre[racine]
            """

        self.brain = creation_arbre(dico, "000000000") # cerveau en entier
        self.reflexion = self.brain


    def deplacement_reflexion(self, situation):
        """
        méthode permettant de déplacer la reflexion de l'IA vers l'une des branches de celle-ci (on se déplace dans l'arbred es possibilité
        """
        for fils in self.reflexion.get_fils():
            if fils.get_racine() == situation:
                self.reflexion = fils
                break

    def jouer(self, plateau, pion):
        """
        méthode permettant de connaître le coup que va jouer l'IA
        parametres:
            plateau, une liste de liste représentant le plateau
            pion, le pion que joue l'IA : les X ou les O
            renvoie les coordonnées du plateau ou joue l'IA
        """
        situation = self.plateau_conversion_chaine(plateau)
        scenarios = [x.get_racine() for x in self.reflexion.get_fils()]

        if situation in scenarios:
            self.deplacement_reflexion(situation)
        elif situation != self.reflexion.get_racine():
            fils = arbre(situation)
            self.reflexion.add_fils(fils)
            self.reflexion = fils

        choix = negamax(self.reflexion, 1)

        if choix[1] < 1 and len(self.reflexion.get_fils()) < self.nbr_possibilite(situation):
            scenarios = [x.get_racine() for x in self.reflexion.get_fils()]

            situation = self.plateau_conversion_chaine(plateau)
            i = 0
            while i < len(situation):
                if situation[i] == "0":
                    s = situation
                    if pion == "O":
                        s = s[:i] + "2" + s[i+1:]
                    else:
                        s = s[:i] + "1" + s[i+1:]
                    if s not in scenarios:
                        break
                i += 1

            x = 0
            while i > 2:
                x += 1
                i -= 3
            y = i

            fils = arbre(s)
            self.reflexion.add_fils(fils)
            self.reflexion = fils # on déplace la reflexion dans cette branche puisque c'est celle actuelle

        else:
            self.deplacement_reflexion(choix[0])

            situation = self.chaine_conversion_plateau(choix[0])

            x = 0
            while situation[x] == plateau[x]:
                x += 1

            y = 0
            while situation[x][y] == plateau[x][y]:
                y += 1

        return [x, y]

    def fin_partie(self, plateau, gagnant):
        """
        méthode permettant de sauvegarder l'arbre de connaissances posséder par l'IA dans le fichier de mémoire

        changement de la valeur
        """
        situation = self.plateau_conversion_chaine(plateau)
        scenarios = [x.get_racine() for x in self.reflexion.get_fils()]

        feuille = None

        if gagnant == "IA":
            if situation not in scenarios and situation != self.reflexion.get_racine():
                feuille = arbre(situation, arbre(1))
            elif situation not in scenarios:
                feuille = arbre(1)
        elif gagnant == "J1":
            if situation not in scenarios and situation != self.reflexion.get_racine():
                feuille = arbre(situation, arbre(-1))
            elif situation not in scenarios:
                feuille = arbre(-1)
        elif situation not in scenarios:
            if situation != self.reflexion.get_racine():
                feuille = arbre(situation, arbre(0))
            else:
                feuille = arbre(0)

        if feuille != None:
            self.reflexion.set_fils(feuille)
        else:
            for fils in self.reflexion.get_fils():
                if fils.get_racine() == situation:
                    self.reflexion = fils
                    break
            valeur = self.reflexion.get_fils()[0].get_racine()
            if valeur > 0:
                self.reflexion.set_fils(arbre(valeur +1))
            elif valeur < 0:
                self.reflexion.set_fils(arbre(valeur -1))

        def creation_dico(ABR):
            """
            sous-fonction permettant de transformer un arbre en dictionnaire dont chaque clé est un noeud interne et dont chaque élément correspondant et soit une branche, soit une feuille
            effectue l'inverse de la fonction creation-arbre(dico, racine)
            parametres:
                ABR, un arbre
            renvoie un dictionnaire contenant l'arbre dans sa globalité
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
        seule les 'X' et les 'O' ainsi que les cases vide '' sont représenté, tous autre caracteres sera représenté par un '0'
        parametres:
            plateau, une liste composé de liste qui représente le plateau
        renvoie une chaine de caracteres composé de '0', '1' et '2'
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

    def chaine_conversion_plateau(self, chaine):
        """
        fonction permettant de transformer une chaine de caracteres en plateau de jeu d'un morpion
        parametres:
            nombre, une chaine de caracteres représentant le plateau de jeu
            x, optionnel, un entier indiquant la longueur du plateau, par defaut 3
            y, optionnel, un entier indiaquent la hauteur du plateau, par defaut 3
        renvoie une chaine de caracteres composé de '0', '1' et '2'
        """
        assert type(chaine) == str, "chaine doit être une chaine de caracteres"
        assert len(chaine) == 9, "la chaine n'est pas assez longue"

        plateau = [i for i in chaine]
        plat = [[plateau[i + j] for j in range(3)] for i in range(0, len(plateau), 3)]

        for i in range(len(plat)):
            for j in range(len(plat[i])):
                if plat[i][j] == "0":
                    plat[i][j] = "_"
                elif plat[i][j] == "1":
                    plat[i][j] = "X"
                else:
                    plat[i][j] = "O"

        return plat

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

if __name__ == "__main__":
    morpion()