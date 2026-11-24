from donnees import animaux
import random
def main():
    animal_aleatoire = random.choice(animaux)
    reponse = input(f"Bonjour, est-ce que vous pensez à : {animal_aleatoire['nom']} ? (y/n) : ").strip().lower()
    if reponse == 'n':
        candidats = animaux.copy().remove(animal_aleatoire)
        
    else:
        return "Yes j'ai réussi a deviné du premier coup !!"    