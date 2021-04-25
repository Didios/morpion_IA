#-------------------------------------------------------------------------------
# Name:        interface finale morpion IA
# Purpose:     donner au morpion précédent une interface
#
# Author:      Didier Mathias
#
# Created:     23/04/2021
#-------------------------------------------------------------------------------
from tkinter import Tk, Canvas, Button, Menu, Scale, Label, Radiobutton, StringVar
import module_lecture_fichier as read
from module_ABR import arbre
"""
faire en sorte que l'IA puisse jouer contre elle-même
"""

class morpion:
    def __init__(self):
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

    def lancement(self, event = None):
        for c in self.root.winfo_children():
            if c.winfo_class() == "Canvas":
                c.destroy()

        self.plateau = [
        ["_", "_", "_"],
        ["_", "_", "_"],
        ["_", "_", "_"]]
        self.turn = "J1"
        self.symbole = "X"
        self.fin = False

        Button(self.root, text = "2 joueurs", command = self.partie_humaine, width = 20, height = 5).pack()
        Button(self.root, text = "IA renforcement", command = self.partie_IA_renforcement, width = 20, height = 5).pack()
        #        Button(self.root, text = "entrainement IA", command = self.entrainement).pack()


    def partie_humaine(self):
        for c in self.root.winfo_children():
            if c.winfo_class() == "Button":
                c.destroy()

        self.jeu = Canvas(self.root, width = 300, height = 300, bg = "white")

        self.jeu.create_line(0, 100, 300, 100)
        self.jeu.create_line(0, 200, 300, 200)
        self.jeu.create_line(100, 0, 100, 300)
        self.jeu.create_line(200, 0, 200, 300)

        def action(event):
            if self.fin:
                self.lancement()
            else:
                self.coup(event)

        self.jeu.bind("<1>", action)
        self.jeu.pack()

    def partie_IA_renforcement(self):
        for c in self.root.winfo_children():
            if c.winfo_class() == "Button":
                c.destroy()

        self.jeu = Canvas(self.root, width = 300, height = 300, bg = "white")

        self.jeu.create_line(0, 100, 300, 100)
        self.jeu.create_line(0, 200, 300, 200)
        self.jeu.create_line(100, 0, 100, 300)
        self.jeu.create_line(200, 0, 200, 300)

        def action(event):
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
                            self.coup(ordi.jouer(self.plateau))
                else:
                    self.coup(ordi.jouer(self.plateau))
        ordi = IA("cerveau_2.txt")
        self.jeu.bind("<1>", action)
        self.jeu.pack()

    """
    Ne fonctionne pas pour une raison inconnue

    def entrainement(self):
        def entrainement_go():
            repet = repetitions.get()

            for c in self.root.winfo_children():
                if c.winfo_class() in ["Button", "Label", "Scale", "Radiobutton"]:
                    c.destroy()

            for r in range(1, repet+1):
                self.jeu = Canvas(self.root, height = 20, width = 1000)
                self.jeu.pack()

                ordi = IA("cerveau.txt")
                ordi_2 = IA("cerveau_2.txt")
                self.fin = False
                while not self.fin:
                    self.coup(ordi.jouer(self.plateau))
                    if not self.fin:
                        self.coup(ordi_2.jouer(self.plateau))

                if self.turn == "J1":
                    ordi.fin_partie(self.plateau, "IA")
                    ordi_2.fin_partie(self.plateau, "J1")
                elif self.turn == "J2":
                    ordi.fin_partie(self.plateau, "J1")
                    ordi_2.fin_partie(self.plateau, "IA")
                else:
                    ordi.fin_partie(self.plateau, "NUL")
                    ordi_2.fin_partie(self.plateau, "NUL")

                self.jeu.create_rectangle(0, 0, 1000*repet/r, 20)

        for c in self.root.winfo_children():
            if c.winfo_class() == "Button":
                c.destroy()

        Label(self.root, text = "Nombres d'entrainements :").pack()
        repetitions = Scale(self.root, orient='horizontal', from_=50, to=10000, resolution=1, length=500)
        repetitions.pack()

        choix = StringVar()
        choix.set("IA")
        Radiobutton(self.root, text = "IA VS IA", variable = choix, value = "IA").pack()
        Radiobutton(self.root, text = "IA VS aléatoire", variable = choix, value = "alea").pack()
        Button(self.root, text = "GO !", command = entrainement_go).pack()

    def entrainement(self):
        def entrainement_go():
            ordi = IA("cerveau_2.txt")
            if choix.get() == "IA":
                ordi_2 = IA("cerveau_2.txt")
            else:
                from random import randint

            for repet in range(repetitions.get()):
                print(repet)
                for c in self.root.winfo_children():
                    if c.winfo_class() in ["Button", "Scale", "Label", "Canvas", "Radiobutton"]:
                        c.destroy()

                self.jeu = Canvas(self.root, width = 300, height = 300, bg = "white")
                self.jeu.create_line(0, 100, 300, 100)
                self.jeu.create_line(0, 200, 300, 200)
                self.jeu.create_line(100, 0, 100, 300)
                self.jeu.create_line(200, 0, 200, 300)
                self.jeu.pack()

                self.turn = "J1"
                self.fin = False
                while not self.fin:
                    self.coup(ordi.jouer(self.plateau))

                    if choix.get() == "IA" and not self.fin:
                        self.coup(ordi_2.jouer(self.plateau))
                    elif not self.fin:
                        test_coup = ""
                        while test_coup == "":
                            test_coup = self.coup([randint(0,2), randint(0,2)])

                if self.turn == "J1":
                    ordi.fin_partie(self.plateau, "IA")
                    if choix.get() == "IA":
                        ordi_2.fin_partie(self.plateau, "J1")
                elif self.turn == "J2":
                    ordi.fin_partie(self.plateau, "J1")
                    if choix.get() == "IA":
                        ordi_2.fin_partie(self.plateau, "IA")
                else:
                    ordi.fin_partie(self.plateau, "NUL")
                    if choix.get() == "IA":
                        ordi_2.fin_partie(self.plateau, "NUL")

        for c in self.root.winfo_children():
            if c.winfo_class() == "Button":
                c.destroy()

        Label(self.root, text = "Nombres d'entrainements :").pack()
        repetitions = Scale(self.root, orient='horizontal', from_=50, to=10000, resolution=1, length=500)
        repetitions.pack()

        choix = StringVar()
        choix.set("IA")
        Radiobutton(self.root, text = "IA VS IA", variable = choix, value = "IA").pack()
        Radiobutton(self.root, text = "IA VS aléatoire", variable = choix, value = "alea").pack()
        Button(self.root, text = "GO !", command = entrainement_go).pack()
    """

    def coup(self, event):
        try:
            x = event.x // 100
            y = event.y // 100
        except:
            x = event[1]
            y = event[0]

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
            self.fin = True
            # ligne
            if verif == "L1":
                self.jeu.create_line(15, 50, 285, 50, width = 10)
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
                self.jeu.create_text(150, 150, font = ('Times', -20, 'bold'), text = "Match NUL")

            if verif != "PLEIN":
                if self.turn == "J1":
                   self.jeu.create_text(150, 150, font = ('Times', -20, 'bold'), text = "J2 a Gagner")
                else:
                    self.jeu.create_text(150, 150, font = ('Times', -20, 'bold'), text = "J1 a Gagner")

    def verifier_plateau(self):
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
    def __init__(self, brain):
        if not read.fichier_existe(brain):
            read.add_fichier("", brain, "000000000:")
        self.fichier_cerveau = brain

        self.debut_partie()

    def debut_partie(self):
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
            ABR = arbre(racine)
            if racine == "":
                return None
            for fils in dico[racine]:
                try:
                    sous_arbre = creation_arbre(dico, fils)
                    if sous_arbre is not None:
                        ABR.add_fils(sous_arbre)
                except:
                    ABR.add_fils(arbre(int(fils)))
            return ABR

        self.brain = creation_arbre(dico, "000000000") # cerveau en entier
        self.reflexion = self.brain

    def deplacement_reflexion(self, situation):
        for fils in self.reflexion.get_fils():
            if fils.get_racine() == situation:
                self.reflexion = fils
                break

    def jouer(self, plateau):
        situation = self.plateau_conversion_chaine(plateau)
        scenarios = [x.get_racine() for x in self.reflexion.get_fils()]

        if situation in scenarios:
            self.deplacement_reflexion(situation)
        elif situation != self.reflexion.get_racine():
            fils = arbre(situation)
            self.reflexion.add_fils(fils)
            self.reflexion = fils

        choix = negamax(self.reflexion, 1)

        if choix[1] < 0 and len(self.reflexion.get_fils()) < self.nbr_possibilite(situation):
            scenarios = [x.get_racine() for x in self.reflexion.get_fils()]

            situation = self.plateau_conversion_chaine(plateau)
            i = 0
            while i < len(situation):
                if situation[i] == "0":
                    s = situation
                    s = s[:i] + "2" + s[i+1:]
                    """
                    changer selon si l'IA joue en premier ou en deuxieme = X ou O
                    """
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

        """
        il faut changer le score si la situation a déjà été fait
        else:
            aller à situation
            prendre la valeur du fils
            changer la valeur
            remettre la nouvelle valeur
        """

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
        compteur = 0
        for i in situation:
            if i == "0":
                compteur += 1
        return compteur

def negamax(node, color, chemin = True):
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