import pygame
import sys
import math
import random
from puissance4 import Puissance4, NB_LIGNES, NB_COLONNES

# Configurations
BLEU = (0, 0, 255)
NOIR = (0, 0, 0)
ROUGE = (255, 0, 0)
JAUNE = (255, 255, 0)
TAILLE_CASE = 100
RAYON = int(TAILLE_CASE / 2 - 5)

# Classe IA Simplifiée
class IA:
    def __init__(self, jeu):
        self.jeu = jeu

    def choisir_coup(self):
        coups_valides = [c for c in range(NB_COLONNES) if self.jeu.coup_valide(c)]
        return random.choice(coups_valides) if coups_valides else None

# Fonction pour dessiner le plateau
def dessiner_plateau(plateau):
    for c in range(NB_COLONNES):
        for r in range(NB_LIGNES):
            pygame.draw.rect(ecran, BLEU, (c * TAILLE_CASE, r * TAILLE_CASE + TAILLE_CASE, TAILLE_CASE, TAILLE_CASE))
            pygame.draw.circle(ecran, NOIR, (int(c * TAILLE_CASE + TAILLE_CASE / 2), int(r * TAILLE_CASE + TAILLE_CASE + TAILLE_CASE / 2)), RAYON)

    for c in range(NB_COLONNES):
        for r in range(NB_LIGNES):
            if plateau[r][c] == 1:
                pygame.draw.circle(ecran, ROUGE, (int(c * TAILLE_CASE + TAILLE_CASE / 2), hauteur - int(r * TAILLE_CASE + TAILLE_CASE / 2)), RAYON)
            elif plateau[r][c] == 2: 
                pygame.draw.circle(ecran, JAUNE, (int(c * TAILLE_CASE + TAILLE_CASE / 2), hauteur - int(r * TAILLE_CASE + TAILLE_CASE / 2)), RAYON)
    pygame.display.update()

# Initialisation du jeu
jeu = Puissance4()
ia = IA(jeu)
pygame.init()
largeur = NB_COLONNES * TAILLE_CASE
hauteur = (NB_LIGNES + 1) * TAILLE_CASE
taille = (largeur, hauteur)
ecran = pygame.display.set_mode(taille)
myfont = pygame.font.SysFont("monospace", 75)

# Choix du mode de jeu
mode_jeu = int(input("Choisissez le mode de jeu (1: Joueur vs Joueur, 2: Joueur vs IA, 3: IA vs IA): "))

tour = 0
game_over = False

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        
        if mode_jeu == 1 or (mode_jeu == 2 and tour % 2 == 0):
            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(ecran, NOIR, (0, 0, largeur, TAILLE_CASE))
                posx = event.pos[0]
                if tour % 2 == 0:
                    pygame.draw.circle(ecran, ROUGE, (posx, int(TAILLE_CASE / 2)), RAYON)
                else:
                    pygame.draw.circle(ecran, JAUNE, (posx, int(TAILLE_CASE / 2)), RAYON)
                pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                posx = event.pos[0]
                col = int(math.floor(posx / TAILLE_CASE))
                if jeu.coup_valide(col):
                    row = jeu.obtenir_prochaine_ligne_libre(col)
                    jeu.jouer_coup(row, col, 1 if tour % 2 == 0 else 2)
                    if jeu.gagnant(1 if tour % 2 == 0 else 2):
                        label = myfont.render(f"Le joueur {'1' if tour % 2 == 0 else '2'} gagne!", True, ROUGE if tour % 2 == 0 else JAUNE)
                        ecran.blit(label, (40, 10))
                        game_over = True
                    tour += 1
                    dessiner_plateau(jeu.plateau)
                    if game_over:
                        pygame.time.wait(3000)
        # IA joue son coup
        if (mode_jeu == 2 and tour % 2 != 0) or mode_jeu == 3 and not game_over:
            col = ia.choisir_coup()
            if col is not None:
                pygame.time.wait(500)  # Temps de "réflexion" pour l'IA
                row = jeu.obtenir_prochaine_ligne_libre(col)
                jeu.jouer_coup(row, col, 2 if mode_jeu == 2 else 1 if tour % 2 == 0 else 2)
                if jeu.gagnant(2 if mode_jeu == 2 else 1 if tour % 2 == 0 else 2):
                    label = myfont.render("L'IA gagne!" if mode_jeu == 2 else "IA 1 gagne!" if tour % 2 == 0 else "IA 2 gagne!", True, JAUNE if tour % 2 == 0 else ROUGE)
                    ecran.blit(label, (40, 10))
                    game_over = True
                tour += 1
                dessiner_plateau(jeu.plateau)
                if game_over:
                    pygame.time.wait(3000)
pygame.quit()

