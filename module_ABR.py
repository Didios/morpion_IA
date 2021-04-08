#-------------------------------------------------------------------------------
# module_ABR
#
# fait par Didier Mathias
#
# ce module permet de crée et manipulé des arbres
#-------------------------------------------------------------------------------

class arbre_binaire:
    def __init__(self, racine, fg = None, fd = None):
        self.racine = racine
        self.fg = fg
        self.fd = fd

    def get_fg(self):
        return self.fg

    def get_fd(self):
        return self.fd

    def get_racine(self):
        return self.racine

    def est_feuille(self):
        return self.fg == None and self.fd == None

    def set_fg(self, fg):
        self.fg = fg

    def set_fd(self, fd):
        self.fd = fd

    def set_racine(self, racine):
        self.racine = racine

    def existe_noeud(self, valeur):
        return valeur in self.parcours_infixe()

    def parcours_largeur(self):
      if self.est_feuille():
        return self.racine
      else:
        f = [self]
        visiter = [self.racine]
        while f != []:
            v = f[0]
            if type(v) is arbre_binaire:
                if v.get_fg() is not None:
                    if v.get_fg().get_racine() not in visiter:
                        f += [v.get_fg()]
                        visiter += [v.get_fg().get_racine()]
                if v.get_fd() is not None:
                    if v.get_fd().get_racine() not in visiter:
                        f += [v.get_fd()]
                        visiter += [v.get_fd().get_racine()]
            f = f[1:]
        return visiter

    def parcours_prefixe(self):
        if self.est_feuille():
            return [self.racine]
        else:
            if self.fg is None:
                return [self.racine] + self.fd.parcours_prefixe()
            elif self.fd is None:
                return [self.racine] + self.fg.parcours_prefixe()
            else:
                return [self.racine] + self.fg.parcours_prefixe() + self.fd.parcours_prefixe()

    def parcours_infixe(self):
        if self.est_feuille():
            return [self.racine]
        else:
            if self.fg is None:
                return [self.racine] + self.fd.parcours_infixe()
            elif self.fd is None:
                return [self.racine] + self.fg.parcours_infixe()
            else:
                return [self.racine] + self.fg.parcours_infixe() + self.fd.parcours_infixe()

    def parcours_suffixe(self):
        if self.est_feuille():
            return [self.racine]
        else:
            if self.fg is None:
                return [self.racine] + self.fd.parcours_suffixe()
            elif self.fd is None:
                return [self.racine] + self.fg.parcours_suffixe()
            else:
                return [self.racine] + self.fg.parcours_suffixe() + self.fd.parcours_suffixe()

    def parcours_postfixe(self):
        return self.parcours_suffixe()

    def taille(self):
        return len(self.parcours_infixe())

    def hauteur(self):
        if self.est_feuille():
            return 1
        else:
            if self.fg == None:
                return 1 + self.fd.hauteur()
            elif self.fd == None:
                return 1 + self.fd.hauteur()
            else:
                return 1 + max(self.fd.hauteur(), self.fg.hauteur())

    """
    nombre feuille
    """
    def suppr_noeud(self, valeur):
        pass

class arbre_recherche():
    pass

class arbre:
    def __str__(self):
        ch = str(self.racine) + ":["
        for f in self.fils:
            ch += str(f) + " ; "
        ch += "]"
        return ch

    def __init__(self, racine, *fils):
        self.racine = racine
        self.fils = [*fils]

    def arite(self):
        return len(self.fils)

    def get_racine(self):
        return self.racine

    def get_fils(self):
        return self.fils

    def set_fils(self, *fils):
        self.fils = [*fils]

    def est_feuille(self):
        return self.fils == []

    def existe_noeud(self, valeur):
        return valeur in self.fils + [self.racine]

    def taille(self):
        nbr = 1
        for f in self.fils:
            if type(f) == arbre:
                nbr += f.taille()
            else:
                nbr += 1
        return nbr

    def hauteur(self):
        nbr = 1
        for f in self.fils:
            if type(f) == arbre:
                nbr = max(nbr, 1 + f.hauteur())
        return nbr

    def add_fils(self, fils):
        self.fils += [fils]