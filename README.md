# Wawacity Downloader

Wawacity Downloader est un utilitaire pour télécharger des films depuis le site Wawacity. **LE PROGRAMME NE FONCTIONNE PAS AVEC LES SERIES (Pas encore).**

## Installation
### Package pré-installé
Vous pouvez trouver le package complet, contenant une version de Chrome portable et un driver Chrome pour Python
[sur cette page](https://github.com/teo-ldsm/Wawacity_Downloader/releases/latest). 
Il faut également installer [Python](https://www.python.org/downloads/).

### Construction manuelle
Pour faire fonctionner l'application à partir des sources:
1. Installer [Python](https://www.python.org/downloads/)
2. Installer [Chrome](https://www.google.com/intl/fr/chrome)
3. Installer les dépendances: `pip install -r requirements.txt` sous Windows ou `pip3 install -r requirements.txt` sous Linux.

## Utilisation
### Mode manuel
En mode manuel, le déroulement du programme est interactif avec des questions qui vous sont posées tout au long de l'exécution.

Pour lancer le programme en mode manuel, lancez dans un terminal:  
```python main.py``` (Windows)  
```python3 main.py```(Linux).

### Mode automatique
Vous pouvez également lancer le programme en mode automatique. Le mode automatique consiste à limiter au maximum les interractions : vous devez seulement renseigner le titre de votre film et le programme fait le reste seul. Vous devrez néanmoins valider manuellement un CAPTCHA (sauf avec la méthode 3).

Pour que le mode automatique soit efficace, il faut compléter correctement le fichier `config.txt`, ou faire un premier démarrage en mode manuel pour le laisser remplir ce fichier à votre place. Le fichier contient des explications sur comment compléter chaque valeur. (Les valeurs plex ne sont pas obligatoires.)

Pour lancer le programme en mode automatique, il faut entrer ceci dans un terminal :

```python main.py -f "Titre du film"``` (Windows)

```python3 main.py -f "Titre du film"``` (Linux).

N'oubliez pas les guillements.

### Mode debug
Si ```main.py``` ne fonctionne pas, lancez ```python main.py -d``` dans 
un terminal pour afficher les logs, les erreurs, et la fenêtre Chrome.


## Résolution des captchas
Les liens sur le site Wawacity sont protégés par le site https://dl-protect.link, qui demande à résoudre un CAPTCHA pour empêcher les bots de les extraire. Il existe 3 méthodes de résolution des CAPTCHAs dans le programme

### Méthode 1 : Application CaptchaSkipper
Si vous avez un téléphone Android, vous pouvez installer l'application Android Captcha Skipper sur votre téléphone. Elle vous permettra de passer le CAPTCHA sans avoir à subir les popups. Elle est indispensable si vous utilisez le programme sur un serveur sans interface graphique (Ex: Serveur NAS, Serveur Linux en ligne de commande, controle à distance en SSH, etc...) Vous pouvez trouver l'application [sur ce Github](https://github.com/teo-ldsm/CaptchaSkipper/releases/latest). Attention, le smartphone doit être sur le même réseau que l'ordinateur qui fait tourner Wawacity Downloader, sur le même point d'accès Wifi par exemple. Ou alors que cette machine soit accessible depuis Internet (un serveur VPS par exemple).

L'application présente la page du CAPTCHA. Il faut résoudre ce CAPTCHA, appuyer sur continuer, puis sur le lien du fournisseur (1fichier par exemple), et enfin sur le bouton en haut à droite de l'application.

La version iOS n'est pas encore disponible.

### Méthode 2 : Depuis le navigateur système
Cette méthode ouvre le navigateur par défaut, sur l'URL de lien. Vous devez résoudre le CAPTCHA, puis copier le lien de téléchargement  depuis le navigateur, et le coller dans la fenêtre de terminal.

### Méthode 3 : Résolution automatique avec Chrome
Cette méthode ouvre une fenêtre Chrome, puis clique automatiquement sur le bouton, récupère le lien et ferme la fenêtre. Cette méthode est expérimentale, et nécessite un environnement graphique.

## Téléchargement des films
Pour l'instant, le programme prend en charge les sites de téléchargements suivants :
- 1fichier


## Configuration
La configuration du programme est fonctionnelle, et elle se fait automatiquement au premier démarrage en posant des questions. Cette configuration peut néanmoins être également faite ou changée en modifiant le fichier config.txt. Le fichier contient des commentaires qui expliquent la signification de chaque propriété.

## Crédit
[wget.py](https://pypi.org/project/wget/) developé par techtonik.
