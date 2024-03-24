import numpy as np
import random
from puissance4 import NB_COLONNES

class IA:
    def __init__(self, piece):
        self.piece = piece

    def choisir_coup(self, plateau):
        valides = [c for c in range(NB_COLONNES) if plateau[NB_LIGNES-1][c] == 0]
        return random.choice(valides) if valides else None
