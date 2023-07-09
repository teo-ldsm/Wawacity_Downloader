# Wawacity Downloader

Wawacity Downloader est un utilitaire pour télécharger des films depuis le site Wawacity.

### LE PROGRAMME NE FONCTIONNE PAS AVEC LES SERIES (Pas encore)

Vous pouvez trouver le package complet 
<a href="https://github.com/teo-ldsm/Wawacity_Downloader/releases/latest">
sur cette page
</a>

Pour lancer le programme normalement, lancez ```python main.py``` (Windows) ou ```python3 main.py```(Linux) dans un terminal.

Vous pouvez également lancer le programme en mode automatique. Le mode automatique consiste à limiter au maximum les interractions : vous devez seulement renseigner le titre de votre film et le programme fait le reste seul. Vous devez seulement valider manuellement un captcha.

Pour que le mode automatique soit éfficace, il faut compléter correctement le fichier ```config.txt```. Le fichier contiens des explixations qui explique comment compléter chaque valeur. (Les valeurs plex ne sont pas obligatoires.)

Pour lancer le programme en mode automatique, il faut entrer ceci dans un terminal :

```python main.py -f "Titre du film"``` (Windows)

```python3 main.py -f "Titre du film"``` (Linux)

N'oubliez pas les guillements


<br>
<br>
Le programme fonctionne avec Google Chrome. Il doit impérativement être installé.
<br>
<br>
Si vous avez un téléphone Android, vous pouvez installer l'application 
Android Captcha Skipper sur votre téléphone. Elle vous permettra de passer le captcha sans avoir à subir les popups. Elle est indispensable si vous utilisez le programme sur un serveur sans interface graphique (Ex: Serveur NAS, Serveur Linux en ligne de commande, controle à distance en SSH, etc...) Vous pouvez trouver l'appli 
<a href="https://github.com/teo-ldsm/CaptchaSkipper/releases/latest">sur ce 
Github</a>.

La version IOS n'est pas encore disponible.

<br>
Pour l'instant, le programme prend en charge les sites de téléchargements suivants :

- 1fichier
- ~~Uptobox (impossible de télécharger plusieurs films d'affilée)~~

**Uptobox est désactivé à cause d'un bug** 

Si ```main.py``` ne fonctionne pas, lancez ```python main.py debug``` dans 
un terminal pour afficher les logs et les erreurs

```plex_refresh.py``` peut être lancé seul. Il va actualiser les bibliothèques de votre serveur plex. Vous devez avoir complété ```config.txt``` pour le lancer.
<br>
<br>

wget.py developed by techtonik
