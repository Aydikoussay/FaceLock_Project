# FaceLock : Authentification Faciale pour Windows

FaceLock est un système de sécurité intelligent conçu pour verrouiller automatiquement votre session Windows en cas d'absence et permettre un déverrouillage fluide par reconnaissance faciale.

## 🛡️ Privacy by Design (Respect de la Vie Privée)

Conformément aux principes du RGPD et aux recommandations de sécurité modernes :
- **Aucune image brute n'est stockée** : Le système transforme votre visage en un "embedding" (vecteur mathématique de 128 dimensions).
- **Traitement Local** : Toutes les opérations de reconnaissance sont effectuées localement sur votre machine. Aucune donnée ne quitte votre ordinateur.
- **Minimisation des données** : Les photos utilisées lors de l'enrôlement sont immédiatement supprimées après l'extraction des caractéristiques.

## 🚀 Installation

### 1. Prérequis
- Python 3.8 ou supérieur.
- Une webcam fonctionnelle.
- **Windows** (pour les fonctions de verrouillage système).

### 2. Installation des dépendances
Ouvrez un terminal (PowerShell ou CMD) dans le dossier du projet et exécutez :

```bash
pip install -r requirements.txt
```

> **Note sur dlib** : La bibliothèque `face_recognition` dépend de `dlib`. Si l'installation échoue, vous devrez peut-être installer [CMake](https://cmake.org/download/) et les outils de build C++ de [Visual Studio](https://visualstudio.microsoft.com/visual-cpp-build-tools/).

## 🛠️ Utilisation

### Étape 1 : Enrôlement des utilisateurs
Avant d'activer la protection, vous devez enregistrer votre visage.
```bash
python main.py --enroll
```
L'interface s'ouvrira. Cliquez sur "Enrôler un nouvel utilisateur", entrez votre nom et regardez la caméra.

### Étape 2 : Lancer FaceLock
Pour activer la surveillance en arrière-plan :
```bash
python main.py
```
Le système vérifiera votre présence toutes les secondes. Si aucun visage autorisé n'est détecté pendant 10 secondes (modifiable dans `main.py`), la session Windows sera verrouillée.

## 📂 Structure du Projet
- `main.py` : Point d'entrée principal.
- `modules/` : Contient la logique métier (caméra, détection, encodage, authentification, contrôle système).
- `gui/` : Interface graphique pour l'enrôlement.
- `data/` : Base de données SQLite stockant les embeddings.

## ⚖️ Conformité & Sécurité
Ce projet a été réalisé dans un cadre pédagogique pour démontrer l'intégration du Deep Learning avec les principes de protection des données. Pour une utilisation en production, il est recommandé de chiffrer la base de données `facelock.db` avec une clé liée au matériel.
