from donnees import animaux
import random







def main():
    animal_aleatoire = random.choice(animaux)
    reponse = input(f"Bonjour, est-ce que vous pensez à : {animal_aleatoire['nom']} ? (y/n) : ").strip().lower()
    if reponse == 'n':
        candidats = animaux.copy()
        candidats.remove(animal_aleatoire)
        questions = [
            ("domestique","est-ildomestique?"),
            ("aquatique","est-il aquatique?"),
            ("carnivore","est-il carnivore?")
        ]
       
        state = {
            "index":0,
            "candidats":candidats,
            "reponses":{}
        }
        
                
       resultat = backtacking(state, questions)

    else:
        return "Yes j'ai réussi a deviné du premier coup !!"    


   