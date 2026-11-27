import json
import os
import random
import time
from donnees import animaux as animaux_base

FICHIER_JSON = "animaux.json"

questions = [
    ("domestique", "Est-il domestique ? (y/n) : "),
    ("aquatique", "Est-il aquatique ? (y/n) : "),
    ("carnivore", "Est-il carnivore ? (y/n) : ")
]

# Base de règles expertes (SI prémisses ALORS fait déduit)
REGLES_EXPERTES = [
    {"si": {"domestique": 0, "aquatique": 0, "carnivore": 1}, "alors": "Prédateur terrestre sauvage"},
    {"si": {"domestique": 0, "aquatique": 0, "carnivore": 0}, "alors": "Herbivore terrestre sauvage"},
    {"si": {"domestique": 0, "aquatique": 1, "carnivore": 1}, "alors": "Prédateur aquatique sauvage"},
    {"si": {"domestique": 0, "aquatique": 1, "carnivore": 0}, "alors": "Herbivore aquatique sauvage"},
    {"si": {"domestique": 1, "aquatique": 0, "carnivore": 1}, "alors": "Animal de compagnie carnivore"},
    {"si": {"domestique": 1, "aquatique": 0, "carnivore": 0}, "alors": "Animal de compagnie herbivore"},
    {"si": {"domestique": 1, "aquatique": 1, "carnivore": 1}, "alors": "Animal d'aquarium carnivore"},
    {"si": {"domestique": 1, "aquatique": 1, "carnivore": 0}, "alors": "Animal d'aquarium herbivore"},
]

#CREATION DE LA MEMOIRE
def memoire():
    if os.path.exists(FICHIER_JSON):
        with open(FICHIER_JSON, "r", encoding="utf-8") as f:
            return json.load(f)
    sauvegarde(animaux_base)
    return animaux_base.copy()

#CREATION DE LA SAUVEGARDE
def sauvegarde(animaux):
    with open(FICHIER_JSON, "w", encoding="utf-8") as f:
        json.dump(animaux, f, indent=4, ensure_ascii=False)

def moteur_inference(animal):
    for regle in REGLES_EXPERTES:
        if all(animal.get(cle) == val for cle, val in regle["si"].items()):
            conditions = " ET ".join([f"{k}={v}" for k, v in regle["si"].items()])
            return regle["alors"], f"Règle activée : SI ({conditions}) ALORS Catégorie = '{regle['alors']}'"
    return "Inconnue", "Aucune règle correspondante."


#BACKTRACKING
def backtracking(state, questions, stats):
    stats["etats_explores"] += 1

    if state["index"] == len(questions):
        print("\n" + "-" * 40)
        for animal in state["candidats"]:
            reponse = input(f"[PROPOSITION] Pensez-vous à : {animal['nom'].upper()} ? (y/n) : ").strip().lower()
            if reponse == 'y':
                return animal
        return None

    cle, texte = questions[state["index"]]
    reponse = input(texte).strip().lower()
    premier_choix = 1 if reponse == 'y' else 0
    choix_pos = [premier_choix, 1 - premier_choix]

    for i, choix in enumerate(choix_pos):
        if i == 1:
            stats["backtracks"] += 1

        nouveaux_candidats = [a for a in state["candidats"] if a[cle] == choix]
        if len(nouveaux_candidats) > 0:
            nouvelles_rep = state["reponses"].copy()
            nouvelles_rep[cle] = choix
            nouvel_etat = {
                "index": state["index"] + 1,
                "candidats": nouveaux_candidats,
                "reponses": nouvelles_rep
            }
            resultat = backtracking(nouvel_etat, questions, stats)
            if resultat is not None:
                return resultat

    return None

def main():
    animaux = memoire()

    while True:
        print("\n" + "=" * 48)
        print("SYSTÈME EXPERT D'IDENTIFICATION D'ANIMAUX")
        print("=" * 48)
        print("Pensez à un animal, je vais essayer de le deviner.\n")

        debut_temps = time.perf_counter()
        stats = {"etats_explores": 0, "backtracks": 0}

        animal_aleatoire = random.choice(animaux)
        reponse = input(f"[HYPOTHÈSE INITIALE] Pensez-vous à : {animal_aleatoire['nom'].upper()} ? (y/n) : ").strip().lower()

        if reponse == 'y':
            resultat = animal_aleatoire
            stats["etats_explores"] = 1

        else:
            candidats_restants = [a for a in animaux if a["nom"] != animal_aleatoire["nom"]]
            etat_initial = {"index": 0, "candidats": candidats_restants, "reponses": {}}
            resultat = backtracking(etat_initial, questions, stats)

        duree = time.perf_counter() - debut_temps


        if resultat is not None:
            categorie, trace_regle = moteur_inference(resultat)
            print("\n" + "=" * 48)
            print(f"[SUCCÈS] Animal identifié : {resultat['nom'].upper()}")
            print(f"[CATÉGORIE] {categorie}")
            print(f"[EXPLICATION] {trace_regle}")
            print(f"[PERFORMANCES] {stats['etats_explores']} états explorés | {stats['backtracks']} backtrack(s) | {duree:.2f}s")
            print("=" * 48 + "\n")
        else:
            print("\n" + "-" * 48)
            print("[ÉCHEC] Animal absent de la base de connaissances.")
            print("Phase d'acquisition de nouvelles connaissances :")
            print("-" * 48)

            nouveau_nom = input("Nom de l'animal recherché : ").strip().capitalize()
            nouvel_animal = {"nom": nouveau_nom}

            for cle, texte in questions:
                rep_carac = input(f"  -> {texte} ").strip().lower()
                nouvel_animal[cle] = 1 if rep_carac == 'y' else 0

            animaux.append(nouvel_animal)
            sauvegarde(animaux)
            print(f"\n[MÉMOIRE] '{nouveau_nom}' ajouté et sauvegardé dans {FICHIER_JSON}.")
            print(f"[PERFORMANCES] {stats['etats_explores']} états explorés | {stats['backtracks']} backtrack(s)\n")

        rejouer = input("Voulez-vous lancer une nouvelle session ? (y/n) : ").strip().lower()
        if rejouer != 'y':
            break

if __name__ == "__main__":
    main()