# Wawacity Downloader

Wawacity Downloader est un utilitaire pour télécharger des films depuis le site Wawacity.

Vous pouvez trouver le package complet 
<a href="https://github.com/teo-ldsm/Wawacity_Downloader/releases/latest">
sur cette page
</a>

Pour lancer le programme normalement, lancez ```python main.py``` dans un terminal.


<br>
<br>
Le programme fonctionne avec Google Chrome. Il doit impérativement être installé.
<br>
<br>
Si vous avez un téléphone android, vous pouvez installer l'application 
android Captcha Skipper sur votre téléphone. Elle vous permettra de passer le captcha sans avoir a subir les popups. Elle est indispensable si vous utilisez le programme sur un serveur sans interface graphique (Ex: Serveur NAS, Serveur Linux en ligne de commande, controle a distance en SSH, etc...) Vous pouvez trouver l'appli 
<a href="https://github.com/teo-ldsm/CaptchaSkipper/releases/latest">sur ce 
Github</a>.

La version IOS n'est pas encore disponible.

<br>
Pour l'instant, le programme prend en charge les sites de téléchargements suivants :

- 1fichier
- Uptobox (impossible de télécharger plusieurs films d'affilée)

Si ```main.py``` ne fonctionne pas, lancez ```python main.py debug``` dans 
un terminal pour afficher les logs et les erreurs

```plex_refresh.py``` peut être lancé seul. Il va actualiser les bibliothèques de votre serveur plex. Vous devez avoir complété ```config.txt``` pour le lancer.
<br>
<br>

wget.py developed by techtonik
