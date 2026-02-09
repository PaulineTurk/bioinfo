# 🧬 BioInfo - Analyse Bioinformatique

## Blsum-lab

Projet éducatif d'apprentissage en bioinformatique combinant analyse de séquences biologiques, alignement et visualisation avec des outils scientifiques.

### 📋 Description

Ce projet explore les fondamentaux de la bioinformatique à travers : #TODO
- **Gestion de données** : travail avec le formats Stockholm standards d'alignement multiple
- **Analyse de séquences protéiques** : parsing et traitement de [Pfam-A.seed](https://ftp.ebi.ac.uk/pub/databases/Pfam/current_release/Pfam-A.seed.gz)
- **Algorithmes de calcul de similitude pairwise** : #TODO
- **Algorithmes de clustering par similitude pairwise** : #TODO
- **Algorithmes de calcul de fréquence de co-occurence d'acides aminés**: sur colonne d'alignement multiple en tenant compte de la pondération par clusters 
- **Visualisation de données** : représentation graphique des résultats biologiques

### 🔬 Choix Scientifiques #TODO

##### Algorithmes Implémentés
- Calcul de similarité/distance entre séquences
- Analyse de composition (acides aminés)

#### Architecture 
#TODO
```
├── src/              # Code réutilisable
├── tests/            # Tests unitaires
└── pyproject.toml.   # Setup du projet
```

### 🚀 Installation et Utilisation Locale

#### Prérequis
- Python 3.12+
- pip

#### Étapes d'installation

1. **Cloner le repository**
```bash
## http better, no authentication required ?
git clone git@github.com:PaulineTurk/bioinfo.git
```

2. **Créer un environnement virtuel**
```bash 
# mac
python3 -m venv .venv 
source .venv/bin/activate

# windows
py -m venv .venv 
source .venv/Scripts/activate
```

3. **Installer les dépendances**
```bash
# mac
cd blosum_lab ; python3 -m pip install -e .

# windows
cd blosum_lab ; py -m pip install -e .
```

4. **Exécuter les analyses**
```bash
# Tests
#TODO

# Scripts spécifiques
#TODO
```


### 📚 Ressources Scientifiques

- [Biopython Documentation](https://biopython.org/)
- [NCBI Bioinformatics Toolkit](https://www.ncbi.nlm.nih.gov/)
-  **Amino acid substitution matrices from protein blocks**, Steven Hnikoff et Jorja Henikoff (10.1073/pnas.89.22.10915)
  

### 🛠️ Contribution

Suggestions pour étendre le projet:
- Implémentation d'algorithmes classiques
  - Alignement global (Needleman-Wunsch)
  - Alignement local (Smith-Waterman)

### 📝 Licence
#TODO
