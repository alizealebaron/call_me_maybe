<p align="center">
  <img src="https://github.com/alizealebaron/alizealebaron/blob/main/assets/call_me_maybe.png" width="120"/>
</p>
<h3 align="center">
  <em>Introduction to function calling in LLMs.</em>
</h3>

---

<div align="center">
  <p>
      <img src="https://img.shields.io/badge/score-106%20%2F%20100-success?style=for-the-badge" />
      <img src="https://img.shields.io/github/languages/count/alizealebaron/call_me_maybe?style=for-the-badge&logo=" />
      <img src="https://img.shields.io/github/languages/top/alizealebaron/call_me_maybe?style=for-the-badge" />
      <img src="https://img.shields.io/github/last-commit/alizealebaron/call_me_maybe?style=for-the-badge" />
  </p>
</div>

## ⚠️ Avant propos

- **Portfolio :** Ce repertoire se concentre sur un seul sujet. Vous pouvez retrouver tous mes projets sur mon [profil](https://github.com/alizealebaron).
- **Sujet :** Conformément aux règles de 42, vous ne trouverez pas le sujet de l'exercice dans ce répertoire.
- **État du projet:** Le code est exactement le même que lorsqu'il a été validé. Il ne sera pas mis à jour même s'il contient des erreurs.
- **Aide & Licence :** Ce repertoire est principalement là pour vous aider à faire votre propre code. Évitez de copier / coller sans comprendre le code.

## 🦆 Status

**Commencé le :** 02/04/2026

**Rendu le :** 14/04/2026.

## Description

**Call Me Maybe** est un projet d'apprentissage sur le "function calling" avec les Large Language Models (LLM). Plutôt que de demander directement au modèle de générer une réponse, ce projet entraîne le LLM à :

1. **Identifier la fonction appropriée** à appeler parmi une liste prédéfinie
2. **Générer les paramètres corrects** pour cette fonction
3. **Retourner le résultat** sous forme structurée en JSON

### Cas d'usage

- **Assistants IA conversationnels** : Permettre aux chatbots de décider quelles API appeler
- **Systèmes d'automatisation** : Transformer des instructions en actions précises
- **Intégration d'outils** : Connecter les LLMs avec des services externes (calculatrices, bases de données, etc.)

## Installation

```bash
# Cloner le projet
git clone https://github.com/alizealebaron/call_me_maybe.git
cd call_me_maybe

# Installation des dépendances
uv sync
# Ou avec le makefile
make install
```

### Commandes du Makefile

```bash
# Installe les dépendances et créer un environnement
make install

# Lance le programme
make run

# Vérifie et renvoie les erreurs de normes strictes
make lint-strict

# Vérifie et renvoie les erreurs de normes
make lint

# Nettoie les fichiers créés par python
make clean

# Lance un environnement de test
make debug
```

### Exécution Basique

```bash
# Utiliser les fichiers par défaut
uv run python -m src
# Ou avec le makefil
make run

# Résultat : data/output/function_calling_results.json
cat data/output/function_calling_results.json
```

### Exécution Personnalisée

```bash
# Avec fichiers custom
uv run python -m src \
  --functions_definition data/input/functions_definition.json \
  --input data/input/function_calling_tests.json \
  --output data/output/custom_results.json
```

### Exemple de fichiers

**Entrée** (`data/input/function_calling_tests.json`) :
```json
[
  {
    "prompt": "What are Palkia's weaknesses ?"
  }
  ...
]
```

**Définitions de Fonctions** (`data/input/functions_definition.json`) :
```json
[
  {
    "name": "fn_find_weakness",
    "description": "Find Pokémon's type weaknesses",
    "parameters": {
      "pokemon": {
        "type": "string"
      }
    },
    "returns": {
      "type": "string"
    }
  }
  ...
]
```

**Sortie** (`data/output/function_calling_results.json`) :
```json
[
  {
    "prompt": "What are Palkia's weaknesses ?",
    "name": "fn_find_weakness",
    "parameters": {
      "pokemon": "Palkia",
    }
  }
  ...
]
```

## Architecture du code

### Arborescence des fichiers
```
call_me_maybe/
├── pyproject.toml            # Fichier de configuration
├── Makefile                  # Automatisation des commandes
├── README.md                 # Explications du projet en anglais
├── README_FR.md              # Explications du projet en français
└── src/
    ├── algorithm/          
    │   └── calling_llm.py    # Appel à la LLM
    ├── models/
    │   ├── functionModel.py  # Modèle des fonctions
    │   └── promptModel.py    # Modèles des prompts
    ├── parsing/            
    │   ├── parsing_args.py   # Parse les arguments passés
    │   ├── parsing_json.py   # Récupère les données JSON
    │   └── parsing_name.py   # Récupère le nom et le dossier de l'output
    ├── utils/              
    │   └── error.py          # Gestion des erreurs
    └── __main__.py           # Point d'entré du programme
```

## Explication de l'Algorithme : Constrained Decoding

### Concept Fondamental

Le constrained decoding est une technique qui force le LLM à générer uniquement à partir d'un ensemble prédéfini de tokens valides. Au lieu de laisser le modèle générer n'importe quel token, on masque les logits (scores de probabilité) des tokens invalides, les rendant impossibles à sélectionner.

### Algorithme pour la Génération de Noms de Fonction

```python
1. Pour chaque position dans le nom de fonction :
   a. Récupérer les logits du LLM
   b. Calculer les tokens valides :
      - Pour chaque fonction disponible
      - Si la fonction commence par le texte généré jusqu'à présent
      - Le prochain token du nom est valide
   c. Masquer les logits : 
      - Tous les tokens invalides → -∞
      - Tous les tokens valides → leur logit original
   d. Sélectionner le meilleur token valide (argmax)
   e. Ajouter le token à la sortie
   f. Arrêter si un nom complet est trouvé
```

**Exemple concret** :
```
Fonctions disponibles : [fn_add_numbers, fn_greet, fn_reverse_string]

Prompt initial généré : "function name: "

Étape 1 (Premier token) :
  - Logits masqués pour tokens : ['f', 'g', 'r']
  - Meilleur : 'f' (très probable pour "fn_")
  - Sortie : "f"

Étape 2 (Deuxième token) :
  - Logits masqués pour se continuer en "fn_"
  - Meilleur : 'n'
  - Sortie : "fn"

... (continue jusqu'à un nom complet détecté)
```

### Algorithme pour la Génération de Paramètres

#### Pour les paramètres numériques

```python
1. Ensemble valide = {'-', '0'-'9', '.', '\n'}
2. Boucle jusqu'à max_tokens ou '\n' rencontré :
   a. Logits masqués pour caractères numériques
   b. Sélectionner le meilleur token valide
   c. Valider les règles numériques :
      - Maximum 1 point décimal
      - Maximum 1 moins, au début seulement
   d. Si invalide : rejeter ce token
   e. Si '\n' rencontré : extraire et convertir en float
3. Retourner le float validé
```

#### Pour les paramètres strings

```python
1. Pas de masquage de logits (tous les tokens autorisés)
2. Boucle jusqu'à max_tokens :
   a. Récupérer le meilleur token (argmax normal)
   b. Ajouter à la sortie
   c. Arrêter si :
      - Caractère d'arrêt rencontré ('\n', espaces multiples, etc.)
      - Token vide
3. Nettoyer et retourner la string
```

## Défis Rencontrés et Solutions

### Défi 1 : Hallucinations du Modèle

**Problème** :
```
Input: "Appelle la fonction..."
Output: "appelle la fonction que j'imagine"
        (fonction inexistante)
```

**Solution Implémentée** :
```python
# Masquer tous les tokens sauf les valides
logits_masked = np.full_like(logits, -np.inf)
for token_id in valid_tokens:
    logits_masked[token_id] = logits[token_id]
```

---

### Défi 2 : Génération Infinie de Tokens

**Problème** :
```
Boucle infinie si pas d'arrêt clair
Temps d'exécution devient énorme
```

**Solution Implémentée** :
- Max tokens par phase (20 pour fonction, 100 pour params strings)
- Détection de caractères spéciaux d'arrêt
- Rejet de tokens vides

---

### Défi 3 : Tokenisation Incomprise

**Problème** :
```
LLM encode parfois "fn_add" en 1 token
Mais parfois en 4 tokens : ['f', 'n', '_', 'add']
Inconsistance crée des erreurs
```

**Solution Implémentée** :
```python
# Flatten tous les tokens
token_seq = [t for sublist in encoding for t in sublist]
# Assurer cohérence
```

## Ressources

### Aide à l'utilisation de JSON

- [Analyser les données JSON en Python](https://brightdata.fr/blog/savoir-faire/parse-json-data-with-python)
- [Utiliser JSON avec Python](https://www.docstring.fr/glossaire/json/)

## Compréhension des LLMs

- [Qu'est-ce qu'une LLM ?](https://www.cloudflare.com/fr-fr/learning/ai/what-is-large-language-model/)
- [Message et token spéciaux](https://huggingface.co/learn/agents-course/fr/unit1/messages-and-special-tokens)

### Autres projets Call Me Maybe

- [Projet de shadox254](https://github.com/shadox254/Call-Me-Maybe)
- [Projet de Sousampere](https://github.com/sousampere/42_call_me_maybe_v1.2)

### Utilisation de l'IA dans ce projet

1. **Algorithme (calling_llm.py)**
   - Explication vulgarisée du principe à implémenter
   - Génération de pseudos codes illustrer l'explication
   - Débuggage des boucles infinis

2. **Checking Norm**
   - Correction des erreurs mypy trouvées

3. **Documentation and Comments**
   - Génération de certains docstring et documentation de classe
   - Correction des erreurs d'orthographe et reformulation
   - Aide pour structurer le readme
   - Aide à la traduction en anglais

## License

Ce projet est sous licence CC0 1.0 Universal (domaine public).

---

**Dernière modification**: 11 avril 2026
