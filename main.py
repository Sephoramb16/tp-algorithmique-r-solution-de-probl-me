from donnees import animaux
import random

def backtracking(state, questions):
    if state["index"] == len(questions):
        for animal in state["candidats"]:
            reponse = input(f"pensez vous à : {animal['nom']} ? ").strip().lower()
            if reponse == 'y':
                return animal

        return None
    
    cle, texte = questions[state["index"]]
    reponse = input(texte).strip().lower()
    
    premier_choix=0

    if reponse == 'y':
        premier_choix=1

    choix_pos = [premier_choix,1-premier_choix]

    for choix in choix_pos:
        nouveaux_candidats = [a for a in state["candidats"] if a[cle]== choix]
        if len(nouveaux_candidats)>0:
            nouvelles_rep = state["reponses"].copy()
            nouvelles_rep[cle]=choix
            nouvel_etat = {
                "index" : state["index"]+1,
                "candidats" : nouveaux_candidats,
                "reponses" : nouvelles_rep
            }
            resultat = backtracking(nouvel_etat, questions)
            if resultat is not None:
                return resultat






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
        
                
        resultat = backtracking(state, questions)

    else:
        return "Yes j'ai réussi a deviné du premier coup !!"    


   