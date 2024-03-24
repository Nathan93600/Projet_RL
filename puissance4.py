import numpy as np

NB_LIGNES = 6
NB_COLONNES = 7

class Puissance4:
    def __init__(self):
        self.plateau = np.zeros((NB_LIGNES, NB_COLONNES))

    def jouer_coup(self, row, col, piece):
        self.plateau[row][col] = piece

    def coup_valide(self, col):
        return self.plateau[NB_LIGNES-1][col] == 0

    def obtenir_prochaine_ligne_libre(self, col):
        for r in range(NB_LIGNES):
            if self.plateau[r][col] == 0:
                return r

    def gagnant(self, piece):
        # Vérifier les victoires horizontales
        for c in range(NB_COLONNES - 3):
            for r in range(NB_LIGNES):
                if self.plateau[r][c] == piece and self.plateau[r][c + 1] == piece and \
                   self.plateau[r][c + 2] == piece and self.plateau[r][c + 3] == piece:
                    return True

        # Vérifier les victoires verticales
        for c in range(NB_COLONNES):
            for r in range(NB_LIGNES - 3):
                if self.plateau[r][c] == piece and self.plateau[r + 1][c] == piece and \
                   self.plateau[r + 2][c] == piece and self.plateau[r + 3][c] == piece:
                    return True

        # Vérifier les victoires diagonales (positives et négatives)
        for c in range(NB_COLONNES - 3):
            for r in range(NB_LIGNES - 3):
                if self.plateau[r][c] == piece and self.plateau[r + 1][c + 1] == piece and \
                   self.plateau[r + 2][c + 2] == piece and self.plateau[r + 3][c + 3] == piece:
                    return True

        for c in range(NB_COLONNES - 3):
            for r in range(3, NB_LIGNES):
                if self.plateau[r][c] == piece and self.plateau[r - 1][c + 1] == piece and \
                   self.plateau[r - 2][c + 2] == piece and self.plateau[r - 3][c + 3] == piece:
                    return True

        return False
