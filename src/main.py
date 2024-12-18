""" File Manager Console Application 
    Generated with Claude 3.5 Haiku
    With 2 prompts : 
        Génère un programme console python qui permet d'explorer les fichiers, 
        en sélectionner pour copier, déplacer et supprimer les fichiers sélectionnés. 
        Une classe "métier" regroupe les fonctions de sélection, copie, déplacement 
        et suppression.

        Deux rectifications : il faudrait passer le code et l'interface en anglais 
        et sortir la sélection de la classe "métier"
"""

from app.components.menus.menu import Menu


def main():
    menu = Menu()

    menu.engine()

if __name__ == "__main__":
    main()