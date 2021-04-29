#-------------------------------------------------------
# fait par Didier Mathias
#
# prjet de morpion en version console python
#-------------------------------------------------------

# importation des modules
from module_ABR import arbre_binaire as abr
from module_ABR import arbre
import module_lecture_fichier as read

################# algo minimax et variations ###################################

def minimax_binaire(node, maximizingPlayer):
    """
    fonction permettant d'effectuer l'algorithme minimax dans un arbre binaire
    parametres:
        node, un arbre binaire
        maximizingPlayer, un booléen indiquant si le joueur doit être maximisé (True) ou minimiser (False)
    renvoi la valeur maximisant ou minimisant les résultats du joueur
    """
    assert type(node) == arbre_binaire, "node doit être de type 'arbre_binaire'"
    assert type(maximizingPlayer) == bool, "maximizingPlayer doit être un booléen"

    if node.est_feuille():
        return node.get_racine()
    elif maximizingPlayer:
        if node.get_fg() is None:
            return minimax_binaire(node.get_fd(), False)
        elif node.get_fd() is None:
            return minimax_binaire(node.get_fg(), False)
        else:
            return max(minimax_binaire(node.get_fg(), False), minimax_binaire(node.get_fd(), False))
    else: # (* minimizing player *)
        if node.get_fg() is None:
            return minimax_binaire(node.get_fd(), True)
        elif node.get_fd() is None:
            return minimax_binaire(node.get_fg(), True)
        else:
            return min(minimax_binaire(node.get_fg(), True), minimax_binaire(node.get_fd(), True))


def minimax(node, maximizingPlayer, chemin = True):
    """
    fonction permettant d'effectuer l'algorithme minimax dans un arbre
    parametres:
        node, un arbre
        maximizingPlayer, un booléen indiquant si le joueur doit être maximisé (True) ou minimiser (False)
        chemin, optionnel, un booléen indiquant si la valeur de la branche permettant d'accéder aux chemin doit être indiqué, True par défaut
    Si chemin, renvoie une liste contenant le nom de la branche a prendre ainsi que la valeur finale
    Sinon, renvoie uniquement la valeur finale
    si l'arbre est une feuille et que chemin = True, renvoie ["", -1]
    sinon si l'arbre est une feuille, renvoie la racine de l'arbre
    """
    assert type(node) == arbre, "node doit être de type 'arbre'"
    assert type(maximizingPlayer) == bool, "maximizingPlayer doit être un booléen"
    assert type(chemin) == bool, "chemin doit être un booléen"

    if chemin and node.est_feuille():
        return ["", -1]

    sous_chemin = None
    nbr = None
    if node.est_feuille():
        return node.get_racine()
    elif maximizingPlayer:
        for f in node.get_fils():
            if type(f) == arbre:
                mmx = minimax(f, False, False)
                if nbr != None:
                    if nbr < mmx:
                        nbr = mmx
                        sous_chemin = f.get_racine()
                else:
                    nbr = mmx
                    sous_chemin = f.get_racine()
    else: # (* minimizing player *)
        for f in node.get_fils():
            if type(f) == arbre:
                mmx = minimax(f, True, False)
                if nbr != None:
                    if nbr > mmx:
                        nbr = mmx
                        sous_chemin = f.get_racine()
                else:
                    nbr = mmx
                    sous_chemin = f.get_racine()

    if chemin:
        return [sous_chemin, nbr]
    else:
        return nbr

"""
tentative pour faire des choix plus logique

def minimax_probabilité(node, maximizingPlayer):
    if node.est_feuille():
        return ["", -1]

    probabilite = {}
    for fils in node.get_fils():
        liste = liste_feuille(fils, maximizingPlayer)
        nbr = 0
        for i in liste:
            nbr += i
        probabilite[fils.get_racine()] = nbr

    chemin = fils.get_racine()
    maxi = probabilite[chemin]
    for fils, nombre in probabilite.items():
        if nombre > maxi:
            maxi = nombre
            chemin = fils

    return [chemin, maxi]

def liste_feuille(node, maximizingPlayer):
    if node.est_feuille():
        if maximizingPlayer:
            return [-node.get_racine()]
        else:
            return [node.get_racine()]
    else:
        liste = []
        for fils in node.get_fils():
            liste += liste_feuille(fils, not maximizingPlayer)
        return liste
"""
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
    assert type(node) == arbre, "node doit être de type 'arbre'"
    assert type(color) in [int, float], "color doit être un nombre"
    assert type(chemin) == bool, "chemin doit être un booléen"

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
# outils utiliser pour les morpions

def montrer_plateau(plateau):
    """
    fonction permettant d'imprimer une liste sous l'apparence d'un tableau de jeu dans la console
    parametres:
        plateau, une liste constitué de liste qui représente le plateau d'un jeu
    renvoi un print qui affiche le tableau dans la console
    """
    assert type(plateau) in [list, tuple], "plateau doit être une liste"

    texte = "-------\n"
    for ligne in plateau:
        assert type(ligne) in [list, tuple], "le plateau doit être composé de liste uniquement"

        texte += "|"
        for colonne in ligne:
            texte += colonne + "|"
        texte += "\n-------\n"
    print(texte)

def convertion_plateau(plateau):
    """
    fonction permettant de transformer le plateau de jeu d'un morpion en chaine de caracteres unique
    seule les 'X' et les 'O' ainsi que les cases vide '' sont représenté, tous autre caracteres sera représenté par un '0'
    parametres:
        plateau, une liste composé de liste qui représente le plateau
    renvoie une chaine de caracteres composé de '0', '1' et '2'

    exemple:
    >>> conversion_plateau([["X", "", "O"], ["", X", ""], ["O", "", "X"]])
    "102010201"
    """
    assert type(plateau) in [list, tuple], "plateau doit être une liste"

    nbr = ""
    for i in range(len(plateau)):
        assert type(plateau[i]) in [list, tuple], "le plateau doit être composé de liste uniquement"

        for j in range(len(plateau[i])):
            if plateau[i][j] == "X":
                nbr += "1"
            elif plateau[i][j] == "O":
                nbr += "2"
            else:
                nbr += "0"
    return nbr

def compter_pos(situation):
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

def convertion_chaine(nombre, x=3, y=3):
    """
    fonction permettant de transformer une chaine de caracteres en plateau de jeu d'un morpion
    elle fait l'exacte inverse de convertion_plateau(plateau)
    parametres:
        nombre, une chaine de caracteres représentant le plateau de jeu
        x, optionnel, un entier indiquant la longueur du plateau, par defaut 3
        y, optionnel, un entier indiaquent la hauteur du plateau, par defaut 3
    renvoie une chaine de caracteres composé de '0', '1' et '2'

    exemple:
    >>> conversion_chaine("102010201", 3, 3)
    [["X", "", "O"], ["", X", ""], ["O", "", "X"]]
    """
    assert type(nombre) == str, "nombre doit être une chaine de caracteres"
    assert x*y == len(nombre), "les valeurs renseigné ne correspondent pas au nombre"

    plateau = [i for i in nombre]
    plat = [[plateau[i + j] for j in range(x)] for i in range(0, len(plateau), y)]

    for i in range(len(plat)):
        for j in range(len(plat[i])):
            if plat[i][j] == "0":
                plat[i][j] = "_"
            elif plat[i][j] == "1":
                plat[i][j] = "X"
            else:
                plat[i][j] = "O"

    return plat

######################### les différents morpions ##############################

def morpion_humain(x = 3, y = 3):
    """
    fonction permettant de jouer au morpion (de la taille souhaité) sur un plateau de la taille de son choix entre 2 humains.
    Les cases sont renseigné ainsi : ligne_choisi.colonne_choisi
    parametres:
        x, un entier indiquant la longueur du plateau
        y, un entier représentant la hauteur du plateau
    """
    plateau = [["_" for i in range(x)] for j in range(y)]
    xtreme = [len(plateau[0]), len(plateau)]

    fin = [False, "J1"]
    while not fin[0]:
        montrer_plateau(plateau)

        placer = False
        while not placer:
            lieu = input("A quelle place veut-tu jouer %s ? (de 1.1 à 3.3)" % fin[1])
            if "." in lieu:
                lieu = lieu.split(".")
                x = int(lieu[0]) -1
                y = int(lieu[1]) -1
                if x > -1 and x < xtreme[0] and y > -1 and y < xtreme[1]:
                    if plateau[x][y] == "_":
                        placer = True

        if fin[1] == "J1":
            plateau[x][y] = "X"
        elif fin[1] == "J2":
            plateau[x][y] = "O"

        # toutes les possibilité d'arrêt
        ligne = False
        i = 0
        while i < 3 and not ligne:
            if (y+i-2 > -1 and y+i-2 < xtreme[1]) and (y+i > -1 and y+i < xtreme[1]):
                ligne = plateau[x][y + i -2] == plateau[x][y + i -1] == plateau[x][y + i] # colonnes

            if (x+i-2 > -1 and x+i-2 < xtreme[0]) and (x+i > -1 and x+i < xtreme[0]) and not ligne:
                ligne = plateau[x + i -2][y] == plateau[x + i -1][y] == plateau[x + i][y] # lignes

            if (y+i-2 > -1 and y+i-2 < xtreme[1]) and (y+i > -1 and y+i < xtreme[1]) and (x+i-2 > -1 and x+i-2 < xtreme[0]) and (x+i > -1 and x+i < xtreme[0]) and not ligne:
                ligne = plateau[x + i -2][y + i -2] == plateau[x + i -1][y + i -1] == plateau[x + i][y + i] # diagonale \

            if (y-i+2 > -1 and y-i+2 < xtreme[1]) and (y-i > -1 and y-i < xtreme[1]) and (x+i-2 > -1 and x+i-2 < xtreme[0]) and (x+i > -1 and x+i < xtreme[0]) and not ligne:
                ligne = plateau[x + i -2][y - i +2] == plateau[x + i -1][y - i +1] == plateau[x + i][y - i] # diagonale /
            i += 1

        plein = "_" not in plateau[0] + plateau[1] + plateau[2]

        if ligne:
            fin[0] = True
        elif fin[1] == "J1":
            fin[1] = "J2"
        else:
            fin[1] = "J1"

        if plein:
            fin[0] = True
            fin[1] = "0"

    montrer_plateau(plateau)

    if fin[1] == "0":
        print("Match nul")
    else:
        print("La joueur %s a gagné !" % fin[1])

"""
1er fonction permettant de jouer contre l'IA, abandonner à cause de trop nombreux probleme est repris dans morpion_IA_2()

def morpion_IA(fois = 1, aleatoire = True):
    score = {}
    score["IA"] = 0
    score["aleatoire"] = 0
    score["nul"] = 0
    for p in range(fois):
        # on transforme le fichier en dictionnaire
        lecture = read.lire_fichier("cerveau.txt")
        dico = {}
        for ligne in lecture:
            ligne = ligne.split(":")
            l = ligne[1].split(",")
            ####
            lors de la construction de l'arbre, des éléments se répètent
            ####
            dico[ligne[0]] = []
            for elmt in l:
                if elmt != ligne[0]:
                    dico[ligne[0]] += [elmt]

        def creation_arbre(dico, racine):
            ABR = arbre(racine)
            if racine == "":
                return None
            for fils in dico[racine]:
                ####
                repetitions des coups dans la chaine = bug de construction
                ####
                if fils in ["-1", "0", "1"]:
                    ABR.add_fils(arbre(int(fils)))
                else:
                    sous_arbre = creation_arbre(dico, fils)
                    if sous_arbre is not None:
                        ABR.add_fils(sous_arbre)
            return ABR

        brain = creation_arbre(dico, "000000000") # cerveau en entier

        reflexion = brain # zone de réfléxion

    ###--------------------------------------------------------------------------###

        plateau = [
        ["_", "_", "_"],
        ["_", "_", "_"],
        ["_", "_", "_"]
        ]

        fin = [False, "J1"] # sert à jouer en alternance et à arreter le jeu

        while not fin[0]: # tant qu'on a pas fini

            if fin[1] == "J1": # le joueur humain
                if aleatoire:
                    from random import randint

                    placer = False
                    while not placer:
                        x = randint(0, 2)
                        y = randint(0, 2)
                        situation = plateau
                        if plateau[x][y] == "_":
                            placer = True
                else:
                    montrer_plateau(plateau)

                    placer = False
                    while not placer:
                        lieu = input("A quelle place veut-tu jouer %s ? (de 1.1 à 3.3)" % fin[1])
                        if "." in lieu:
                            lieu = lieu.split(".")
                            x = int(lieu[0]) -1
                            y = int(lieu[1]) -1
                            if x > -1 and x < 3 and y > -1 and y < 3:
                                if plateau[x][y] == "_":
                                    placer = True
            ###------------------------------------------------------------------###
            elif fin[1] == "IA": # joueur IA
                situation = convertion_plateau(plateau)
                scenarios = [x.get_racine() for x in reflexion.get_fils()]

                if situation in scenarios:
                    for fils in reflexion.get_fils():
                        if fils.get_racine() == situation:
                            reflexion = fils
                            break
                elif situation == reflexion.get_racine():
                    pass
                else:
                    fils = arbre(situation)
                    reflexion.add_fils(fils)
                    reflexion = fils

                choix = minimax(reflexion, False)

                ####
                MAJ de l'arbre:

                    analyse situation
                    si nouvelle situation:
                        ajouter situation à l'arbre
                        ajouter un fils à l'arbre avec comme nom None et valeur 0

                    si la branche ou on est à déjà toutes les possibilitées de faites:
                        on enlève le fils None

                    reflexion devient la branche correspondante à situation
                ####

                if choix[1] < 0 and len(reflexion.get_fils()) < compter_pos(situation):
                    # on joue de manière aléatoire
                    from random import randint

                    placer = False
                    while not placer:
                        x = randint(0, 2)
                        y = randint(0, 2)

                        situation = convertion_chaine(convertion_plateau(plateau))
                        situation[x][y] = "O"

                        situation = convertion_plateau(situation)

                        if plateau[x][y] == "_" and situation not in [x.get_racine() for x in reflexion.get_fils()]:
                            placer = True

                    # on ajoute cette situation au cerveau puisqu'elle n'existe pas encore

                    fils = arbre(situation)

                    reflexion.add_fils(fils)
                    # on déplace la reflexion dans cette branche puisque c'est celle actuelle
                    reflexion = fils
                    ####
                    tant que x, y pas possible:
                        x, y = random entre 0 et 2
                    ajouter la nouvelle situation à reflexion
                    aller à la situation
                    ####
                else:
                    for fils in reflexion.get_fils():
                        if fils.get_racine() == choix[0]:
                            reflexion = fils
                            break

                    situation = convertion_chaine(choix[0])

                    x = 0
                    while situation[x] == plateau[x]:
                        x += 1

                    y = 0
                    while situation[x][y] == plateau[x][y]:
                        y += 1
                    # aller à choix[1]
                    # determiner x, y
                ####
                choix placement:
                    faire minmax(reflexion, False) pour connaitre la branche à prendre
                    si nom de la branche == "None":
                        x, y = -1, -1
                        tant que la position x y n'est pas possible ou que la situation correspondante est un fils de reflexion:
                            choisir x y au pif
                        ajouter la nouvelle situation à l'arbre
                        aller à la branche
                    sinon:
                        aller à la branche
                        prendre la racine de la branche
                        comparer la racine à l'analyse
                        donner le placement x y
                ####

        ###----------------------------------------------------------------------###
            # on place le pion au coordonnées selon le joueur
            if fin[1] == "J1":
                plateau[x][y] = "X"
            elif fin[1] == "IA":
                plateau[x][y] = "O"

            # toutes les possibilité de gagner sont ici
            ligne = False
            i = 0
            while i < 3 and not ligne:
                if (y+i-2 > -1 and y+i-2 < 3) and (y+i > -1 and y+i < 3):
                    ligne = plateau[x][y + i -2] == plateau[x][y + i -1] == plateau[x][y + i] # colonnes

                if (x+i-2 > -1 and x+i-2 < 3) and (x+i > -1 and x+i < 3) and not ligne:
                    ligne = plateau[x + i -2][y] == plateau[x + i -1][y] == plateau[x + i][y] # lignes

                if (y+i-2 > -1 and y+i-2 < 3) and (y+i > -1 and y+i < 3) and (x+i-2 > -1 and x+i-2 < 3) and (x+i > -1 and x+i < 3) and not ligne:
                    ligne = plateau[x + i -2][y + i -2] == plateau[x + i -1][y + i -1] == plateau[x + i][y + i] # diagonale \

                if (y-i+2 > -1 and y-i+2 < 3) and (y-i > -1 and y-i < 3) and (x+i-2 > -1 and x+i-2 < 3) and (x+i > -1 and x+i < 3) and not ligne:
                    ligne = plateau[x + i -2][y - i +2] == plateau[x + i -1][y - i +1] == plateau[x + i][y - i] # diagonale /
                i += 1

            plein = "_" not in plateau[0] + plateau[1] + plateau[2]

            # on regarde si le joueur a gagné et si le plateau n'est pas plein
            if ligne:
                fin[0] = True
            elif plein:
                fin[0] = True
                fin[1] = "0"
            # on change de joueur sinon
            elif fin[1] == "J1":
                fin[1] = "IA"
            else:
                fin[1] = "J1"
        ###----------------------------------------------------------------------###

        montrer_plateau(plateau) # on montre le plateau de fin

        situation = convertion_plateau(plateau)
        scenarios = [x.get_racine() for x in reflexion.get_fils()]

        if fin[1] == "IA":
            if situation not in scenarios and situation != reflexion.get_racine():
                fils = arbre(situation, arbre(1))
            elif situation not in scenarios:
                fils = arbre(1)
            reflexion.set_fils(fils)
        elif fin[1] == "J1":
            if situation not in scenarios and situation != reflexion.get_racine():
                fils = arbre(situation, arbre(-1))
            elif situation not in scenarios:
                fils = arbre(-1)
            reflexion.set_fils(fils)
        elif situation not in scenarios:
            if situation != reflexion.get_racine():
                fils = arbre(situation, arbre(0))
            else:
                fils = arbre(0)
            reflexion.set_fils(fils)

        ####
        analyse situation
        si IA perdu:
            si situation nouvelle:
                créer situation avec comme fils -1
            sinon:
                aller à situation
                prendre le fils et y enlever 1
        sinon si IA gagné:
            si situation nouvelle:
                creer situation avec comme fils 1
            sinon:
                aller à situation
                prendre le fils et y ajouter 1
        sinon si situation nouvelle:
                creer situation avec comme fils 0
        ####

        ###------------------------------------------------------------------###

        # enregistrement du nouvel arbre

        # on transforme l'arbre en dictionnaire
        ####
        def creation_dico(ABR):
            dico = {}
            l = []
            for fils in ABR.get_fils():
                try:
                    if fils.est_feuille():
                        l += [fils.get_racine()]
                    else:
                        l += [creation_dico(fils)]
                except:
                    l += [fils]
            dico[ABR.get_racine()] = l
            return dico
        ####
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

        dico = creation_dico(brain)

        ###----------------------------------------------------------------------###

        ####
        on transforme le dictionnaire en un dictionnaire unique
            il faut faire attention s'il y a plusieurs clé identique => assembler les valeur
        ####
        ####
        dico_unique = False
        while not dico_unique:
            nouv_dico = []
            # on enleve les sous_dico
            for keys, values in dico.items():
                nouv_values = []
                for elmt in values:
                    if type(elmt) == dict:
                        nouv_dico += [elmt]
                        nouv_values += [*elmt.keys()]
                    else:
                        nouv_values += [elmt]
                dico[keys] = nouv_values
            # on met les sous dico avec le dico
            for sous_dico in nouv_dico:
                sous_contenu = [*sous_dico.keys()]
                for keys in sous_contenu:
                    if keys in dico.keys():
                        for elmt in sous_dico[keys]:
                            if elmt not in dico[keys]:
                                dico[keys] = dico[keys] + [elmt]
                    else:
                        dico[keys] = sous_dico[keys]

            # on vérifie si le dico est unique
            if nouv_dico == []:
                dico_unique = True
        ####
        ###----------------------------------------------------------------------###
        # transformation du dictionnaire en chaine de caracteres
        contenu = ""
        for keys, values in dico.items():
            contenu += keys
            contenu += ":"
            ####
            values contient un arbre == impossible:
                PBM fonction arbre --> dictionnaire
            ####
            for indice in values:
                contenu += str(indice) + ","
            contenu = contenu[:-1]
            contenu += "\n"

        ###----------------------------------------------------------------------###
        # on indique le résultat de la partie
        if fin[1] == "0":
            score["nul"] += 1
        elif fin[1] == "IA":
            score["IA"] += 1
        else:
            score["aleatoire"] += 1
        print(score)

        ####
        il faut modifier le temps d'attente = creer une boucle  qui s'execute tant que le fichier n'est pas disponible
        os.system('TheCommand')

        il y a plusieurs fois le même nombre dans le dictionnaire
        {cle : [cle, cle_1, ...]}
        = ajouter verification, si pareil, pas ajouté
        ####

        import time
        time.sleep(5)

        read.suppr_fichier("cerveau.txt", False)
        read.add_fichier("", "cerveau.txt", contenu)
"""




def morpion_IA_2(fois = 1, aleatoire = True, J1_premier = True):
    """
    fonction permettant de jouer à un morpion classique sur la console contre une IA, celle_ci évolue au fur et à mesure des parties
    le score actuel est affiché à chaque fin de partie
    parametres:
        fois, optionnel, un entier positif supérieur à 0 permettant de définir le nombre de parties que l'on souhaite effectuée, par défaut 1
        aleatoire, optionnel, un booléen indiaquant si l'IA doit jouer contre un humain (False) ou contre un joueur aléatoire (True), par defaut True
        J1_premier, optionnel, un booléen indiquant qui est le premier joueur, False pour l'IA, True pour l'autre joueur, par defaut True
    """
    assert type(fois) == int, "fois doit être un entier"
    assert fois > 0, "fois doit être plus grand que 0"
    assert type(aleatoire) == bool, "aleatoire doit être un booléen"
    assert type(J1_premier) == bool, "J1_premier doit être un booléen"

    score = {}
    score["IA"] = 0
    score["aleatoire"] = 0
    score["nul"] = 0

    # si le fichier contenant la mémoire (la majorité de son "cerveau") n'existe pas, on le crée
    if not read.fichier_existe("cerveau_2.txt"):
        read.add_fichier("", "cerveau_2.txt", "000000000:")

    # on lit le contenu de la mémoire
    lecture = read.lire_fichier("cerveau_2.txt")

    # on transforme le fichier en dictionnaire
    dico = {}
    for ligne in lecture:
        ligne = ligne.split(":")
        l = ligne[1].split(",")
        """
        lors de la construction de l'arbre, des éléments se répètent
        probleme lors de l'enregistrement de l'arbre == mélange des dictionnaires lors de situation identique
        """
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
        assert type(dico) == dict, "dico doit être un dictionnaire"

        ABR = arbre(racine)
        if racine == "":
            return None

        for fils in dico[racine]:
            if racine in dico.keys():
                sous_arbre = creation_arbre(dico, fils)
                if sous_arbre is not None:
                    ABR.add_fils(sous_arbre)
            else:
                ABR.add_fils(arbre(int(fils)))

        return ABR

    brain = creation_arbre(dico, "000000000") # cerveau en entier

    reflexion = brain # zone de réfléxion
    for p in range(fois):

    ###--------------------------------------------------------------------------###

        plateau = [
        ["_", "_", "_"],
        ["_", "_", "_"],
        ["_", "_", "_"]
        ]

        if J1_premier:
            fin = [False, "J1"] # sert à jouer en alternance et à arreter le jeu
        else:
            fin = [False, "IA"]

        while not fin[0]: # tant qu'on a pas fini
            ###----------------------- joueur hors IA -----------------------###
            if fin[1] == "J1": # le 1er joueur
                if aleatoire: # le joueur aléatoire
                    from random import randint

                    placer = False
                    while not placer:
                        x = randint(0, 2)
                        y = randint(0, 2)
                        if plateau[x][y] == "_":
                            placer = True

                else: # le joueur humain
                    montrer_plateau(plateau)

                    placer = False
                    while not placer:
                        lieu = input("A quelle place veut-tu jouer %s ? (de 1.1 à 3.3)" % fin[1])
                        if "." in lieu:
                            lieu = lieu.split(".")
                            x = int(lieu[0]) -1
                            y = int(lieu[1]) -1
                            if x > -1 and x < 3 and y > -1 and y < 3:
                                if plateau[x][y] == "_":
                                    placer = True
            ###------------------------------------------------------------------###
            elif fin[1] == "IA": # joueur IA
                situation = convertion_plateau(plateau)
                scenarios = [x.get_racine() for x in reflexion.get_fils()]

                if situation in scenarios:
                    for fils in reflexion.get_fils():
                        if fils.get_racine() == situation:
                            reflexion = fils
                            break
                elif situation != reflexion.get_racine():
                    fils = arbre(situation)
                    reflexion.add_fils(fils)
                    reflexion = fils

                choix = negamax(reflexion, 1)
                # choix = minimax(reflexion, False)
                """
                MAJ de l'arbre:

                    analyse situation
                    si nouvelle situation:
                        ajouter situation à l'arbre
                        ajouter un fils à l'arbre avec comme nom None et valeur 0

                    si la branche ou on est à déjà toutes les possibilitées de faites:
                        on enlève le fils None

                    reflexion devient la branche correspondante à situation

                différents probleme existe:
                    minimax et negamax entrainent une trop importante récursivité
                    les actions de l'IA ne semble pas toujours logique quand on connait ses parties précédentes
                """

                if choix[1] < 0 and len(reflexion.get_fils()) < compter_pos(situation):
                    """
                    # on joue de manière aléatoire
                    from random import randint

                    placer = False
                    while not placer:
                        x = randint(0, 2)
                        y = randint(0, 2)

                        situation = convertion_chaine(convertion_plateau(plateau))
                        situation[x][y] = "O"

                        situation = convertion_plateau(situation)

                        if plateau[x][y] == "_" and situation not in [x.get_racine() for x in reflexion.get_fils()]:
                            placer = True

                    # on ajoute cette situation au cerveau puisqu'elle n'existe pas encore

                    fils = arbre(situation)

                    reflexion.add_fils(fils)
                    # on déplace la reflexion dans cette branche puisque c'est celle actuelle
                    reflexion = fils
                    """

                    """
                    tant que x, y pas possible:
                        x, y = random entre 0 et 2
                    ajouter la nouvelle situation à reflexion
                    aller à la situation

                    inutile de jouer aléatoirement, il suffit de prendre la premiere place libre que l'on n'as pas déjà fait
                    """
                    scenarios = [x.get_racine() for x in reflexion.get_fils()]

                    situation = convertion_plateau(plateau)
                    i = 0
                    while i < len(situation):
                        if situation[i] == "0":
                            s = situation
                            s = s[:i] + "2" + s[i+1:]
                            if s not in scenarios:
                                break
                        i += 1

                    x = 0
                    while i > 2:
                        x += 1
                        i -= 3
                    y = i

                    fils = arbre(s)
                    reflexion.add_fils(fils)
                    reflexion = fils # on déplace la reflexion dans cette branche puisque c'est celle actuelle

                else:
                    for fils in reflexion.get_fils():
                        if fils.get_racine() == choix[0]:
                            reflexion = fils
                            break

                    situation = convertion_chaine(choix[0])

                    x = 0
                    while situation[x] == plateau[x]:
                        x += 1

                    y = 0
                    while situation[x][y] == plateau[x][y]:
                        y += 1

                    # aller à choix[1]
                    # determiner x, y
                """
                choix placement:
                    faire minmax(reflexion, False) pour connaitre la branche à prendre
                    si nom de la branche == "None":
                        x, y = -1, -1
                        tant que la position x y n'est pas possible ou que la situation correspondante est un fils de reflexion:
                            choisir x y au pif
                        ajouter la nouvelle situation à l'arbre
                        aller à la branche
                    sinon:
                        aller à la branche
                        prendre la racine de la branche
                        comparer la racine à l'analyse
                        donner le placement x y
                """

        ###----------------------------------------------------------------------###
            # on place le pion au coordonnées selon le joueur
            if fin[1] == "J1":
                plateau[x][y] = "X"
            elif fin[1] == "IA":
                plateau[x][y] = "O"

            # toutes les possibilité de gagner sont ici
            ligne = False
            i = 0
            while i < 3 and not ligne:
                if (y+i-2 > -1 and y+i-2 < 3) and (y+i > -1 and y+i < 3):
                    ligne = plateau[x][y + i -2] == plateau[x][y + i -1] == plateau[x][y + i] # colonnes

                if (x+i-2 > -1 and x+i-2 < 3) and (x+i > -1 and x+i < 3) and not ligne:
                    ligne = plateau[x + i -2][y] == plateau[x + i -1][y] == plateau[x + i][y] # lignes

                if (y+i-2 > -1 and y+i-2 < 3) and (y+i > -1 and y+i < 3) and (x+i-2 > -1 and x+i-2 < 3) and (x+i > -1 and x+i < 3) and not ligne:
                    ligne = plateau[x + i -2][y + i -2] == plateau[x + i -1][y + i -1] == plateau[x + i][y + i] # diagonale \

                if (y-i+2 > -1 and y-i+2 < 3) and (y-i > -1 and y-i < 3) and (x+i-2 > -1 and x+i-2 < 3) and (x+i > -1 and x+i < 3) and not ligne:
                    ligne = plateau[x + i -2][y - i +2] == plateau[x + i -1][y - i +1] == plateau[x + i][y - i] # diagonale /
                i += 1

            plein = "_" not in plateau[0] + plateau[1] + plateau[2]

            # on regarde si le joueur a gagné et si le plateau n'est pas plein
            if ligne:
                fin[0] = True
            elif plein:
                fin[0] = True
                fin[1] = "0"
            # on change de joueur sinon
            elif fin[1] == "J1":
                fin[1] = "IA"
            else:
                fin[1] = "J1"
        ###----------------------------------------------------------------------###

        montrer_plateau(plateau) # on montre le plateau de fin

        situation = convertion_plateau(plateau)
        scenarios = [x.get_racine() for x in reflexion.get_fils()]

        feuille = None

        if fin[1] == "IA":
            if situation not in scenarios and situation != reflexion.get_racine():
                feuille = arbre(situation, arbre(1))
            elif situation not in scenarios:
                feuille = arbre(1)
        elif fin[1] == "J1":
            if situation not in scenarios and situation != reflexion.get_racine():
                feuille = arbre(situation, arbre(-1))
            elif situation not in scenarios:
                feuille = arbre(-1)
        elif situation not in scenarios:
            if situation != reflexion.get_racine():
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
            reflexion.set_fils(feuille)
        else:
            for fils in reflexion.get_fils():
                if fils.get_racine() == situation:
                    reflexion = fils
                    break
            valeur = reflexion.get_fils()[0].get_racine()
            if valeur > 0:
                reflexion.set_fils(arbre(valeur +1))
            elif valeur < 0:
                reflexion.set_fils(arbre(valeur -1))


        """
        feuille = fils
        fils était déjà utilisé avant ce qui fait que à cause de ce qui suit, l'arbre rebouclait sur lui même puisque reflexion = fils avant
        l'abcense de else fait que des fois, il remet la feuille précédente au mauvais endroits, d'ou des résultat incohérents
        """

        # on indique le résultat de la partie
        if fin[1] == "0":
            score["nul"] += 1
        elif fin[1] == "IA":
            score["IA"] += 1
        else:
            score["aleatoire"] += 1
        print(score)

        """
        probleme de recursivité
        raison inconnue

        probleme d'enregistrement de situation
        """

        reflexion = brain

        # onn met un temp d'attente entre chaque partie afin d'éviter les problemes du à la vitesse d'éxécution
        import time
        time.sleep(0.1)

        """
        analyse situation
        si IA perdu:
            si situation nouvelle:
                créer situation avec comme fils -1
            sinon:
                aller à situation
                prendre le fils et y enlever 1
        sinon si IA gagné:
            si situation nouvelle:
                creer situation avec comme fils 1
            sinon:
                aller à situation
                prendre le fils et y ajouter 1
        sinon si situation nouvelle:
                creer situation avec comme fils 0
        """

    ###------------------------------------------------------------------###

    # enregistrement du nouvel arbre

    # on transforme l'arbre en dictionnaire
    """
    def creation_dico(ABR):
        dico = {}
        l = []
        for fils in ABR.get_fils():
            try:
                if fils.est_feuille():
                    l += [fils.get_racine()]
                else:
                    l += [creation_dico(fils)]
            except:
                l += [fils]
        dico[ABR.get_racine()] = l
        return dico
    """
    def creation_dico(ABR):
        """
        sous-fonction permettant de transformer un arbre en dictionnaire dont chaque clé est un noeud interne et dont chaque élément correspondant et soit une branche, soit une feuille
        effectue l'inverse de la fonction creation-arbre(dico, racine)
        parametres:
            ABR, un arbre
        renvoie un dictionnaire contenant l'arbre dans sa globalité
        """
        """
        des fois, des feuille se mettent ensemble
        """
        dico = {}
        dico[ABR.get_racine()] = []
        for fils in ABR.get_fils():
            if fils.est_feuille():
                dico[ABR.get_racine()] = [fils.get_racine()]
            else:
                nouv_dico = creation_dico(fils)
                for keys, values in nouv_dico.items():
                    if keys in dico.keys():
                        for each in values:
                            if each not in dico[keys]:
                                if type(each) == int:
                                    if each > 0:
                                        dico[keys] = [max(dico[keys][0], each)]
                                    elif each < 0:
                                        dico[keys] = [min(dico[keys][0], each)]
                                    else:
                                        dico[keys] = [0]
                                else:
                                    dico[keys] += [each]
                    else:
                        dico[keys] = values
                dico[ABR.get_racine()] += [fils.get_racine()]
        return dico

    dico = creation_dico(brain)
    ###----------------------------------------------------------------------###

    ###----------------------------------------------------------------------###
    # transformation du dictionnaire en chaine de caracteres
    contenu = ""
    for keys, values in dico.items():
        contenu += keys
        contenu += ":"
        for indice in values:
            contenu += str(indice) + ","
        contenu = contenu[:-1]
        contenu += "\n"

        ###----------------------------------------------------------------------###

    """
    il faut modifier le temps d'attente = creer une boucle  qui s'execute tant que le fichier n'est pas disponible
    os.system('TheCommand')

    il y a plusieurs fois le même nombre dans le dictionnaire
    {cle : [cle, cle_1, ...]}
    = ajouter verification, si pareil, pas ajouté
    """

    read.suppr_fichier("cerveau_2.txt", False)
    read.add_fichier("", "cerveau_2.txt", contenu)