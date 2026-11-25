from donnees import animaux
import random


def backtracking(state, questions):
    if state["index"] == len(questions):
        for animal in state["candidats"]:
            reponse = input(f"pensez vous à : {animal['nom']} ? ").strip().lower()
            if reponse == 'y':
                print(state)
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
            ("domestique","Est-il domestique ? (y/n) : "),
            ("aquatique","Est-il aquatique ? (y/n) : "),
            ("carnivore","Est-il carnivore ? (y/n) : ")
        ]
       
        state = {
            "index":0,
            "candidats":candidats,
            "reponses":{}
        }
        
                
        resultat = backtracking(state, questions)
        if resultat is not None:
            print("Yes j'ai réussi a deviner !!" )
        else:
            nouveau_nom=input("Mince je n'ai pas réussi à deviner l'animal auquel tu pensais! Quel est le nom de ce nouvel animal ? : ")
            nouvel_animal = {"nom": nouveau_nom }
            questions_nv = [
                        ("domestique","Le nouvel animal est domestique ? (y/n) : "),
                        ("aquatique","Le nouvel animal est aquatique ? (y/n) : "),
                        ("carnivore","Le nouvel animal est carnivore ? (y/n) : ")
                    ]
                   
            for cle, texte in questions_nv:
                reponse_nv = input(texte).strip().lower()

                if reponse_nv == 'y':
                    nouvel_animal[cle] = 1 
                else:
                    nouvel_animal[cle] = 0
            animaux.append(nouvel_animal)
    else:
        print("Yes j'ai réussi a deviné du premier coup !!")
main()
   