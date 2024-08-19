# ShellValley Reverse Shell Generator

Le générateur de reverse shells ShellValley permet de créer des scripts de reverse shell dans divers langages de programmation et de les enregistrer pour une utilisation ultérieure. Ce projet prend en charge plusieurs types de shells, y compris Bash, Python, PHP, et bien d'autres.

<h1 align="center">
 <a href="#"><img src="./img/shell_valley.png"></a>

## Fonctionnalités

- Génération de reverse shells dans divers langages de programmation.
- Enregistrement des reverse shells générés dans un répertoire spécifié.
- Interface en ligne de commande (CLI) et interface graphique utilisateur (GUI) pour faciliter l'utilisation.

## Installation

1. Clonez le dépôt :

   ```bash
   git clone https://github.com/tucommenceapousser/ShellValley.git
   ```

2. Accédez au répertoire du projet :

   ```bash
   cd ShellValley
   ```

3. Assurez-vous que Python 3 est installé sur votre système. Installez les dépendances requises avec pip :

   ```bash
   pip install -r requirements.txt
   ```

## Utilisation

### Interface en Ligne de Commande (CLI)

Le script `run.py` permet de générer des reverse shells et de les enregistrer dans un répertoire spécifié.

#### Commandes de Base

```bash
python3 run.py -i [IP] -p [PORT] -s [SHELL] -d [DIRECTORY]
```

- `-i`, `--ip` : Adresse IP à laquelle le reverse shell se connectera. (Obligatoire)
- `-p`, `--port` : Port sur lequel le reverse shell se connectera. (Obligatoire)
- `-s`, `--shell` : Type de shell à générer. Les options disponibles sont : `bash`, `php`, `python`, `perl`, `java`, `javascript`, `node`, etc. (Facultatif, par défaut `bash`)
- `-d`, `--download` : Répertoire où enregistrer les scripts de reverse shell générés. (Facultatif)

#### Exemples

- **Générer un reverse shell en Bash et l'enregistrer dans un répertoire spécifique** :

  ```bash
  python3 run.py -i 192.168.1.100 -p 1234 -s bash -d /chemin/vers/repertoire
  ```

- **Générer un reverse shell en PHP et l'enregistrer dans un répertoire spécifique** :

  ```bash
  python3 run.py -i 192.168.1.100 -p 1234 -s php -d /chemin/vers/repertoire
  ```

- **Générer des reverse shells pour tous les types disponibles et les enregistrer dans un répertoire** :

  ```bash
  python3 run.py -i 192.168.1.100 -p 1234 -d /chemin/vers/repertoire
  ```

### Interface Graphique Utilisateur (GUI)

Le script `rungui.py` fournit une interface graphique pour générer des reverse shells.

#### Lancer l'Interface Graphique

Assurez-vous que vous avez installé les dépendances requises, puis exécutez :

```bash
python3 run.py
```

L'interface graphique vous guidera à travers les étapes pour sélectionner le type de shell, entrer l'adresse IP et le port, et choisir un répertoire pour enregistrer les fichiers.

### Options Avancées

- **Lister les types de shells disponibles en CLI** :

  ```bash
  python3 run.py -l
  ```

  Cette commande affiche tous les types de shells disponibles pour la génération.

this Mod'Z is made by Trhacknon from this repo:
***https://github.com/Nabil-Official/ShellValley***

Merci d'utiliser ShellValley ! 😊
