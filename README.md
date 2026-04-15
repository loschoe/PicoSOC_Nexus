<h1 align="center">📡 PicoSOC_Nexus</h1>

<p align="center">
  <img src="https://img.shields.io/badge/MicroPython-1.22-blue" />
  <img src="https://img.shields.io/badge/Hardware-Pico%20W-green" />
  <img src="https://img.shields.io/badge/Status-Stable-brightgreen" />
  <img src="https://img.shields.io/badge/License-MIT-lightgrey" />
</p>

<br>

<table>
  <tr>
    <td width="40%">
      <img src="https://github.com/user-attachments/assets/a99faf74-f6e9-4c69-84a0-a7d83dec78c1" width="100%" style="border-radius:12px;" />
    </td>
    <td width="60%" style="vertical-align:top; padding-left:15px;">
      <p>
        <strong>PicoSOC_Nexus</strong> est un dashboard réseau léger et autonome conçu pour le 
        <strong>Raspberry Pi Pico W</strong>.  
        Ce projet transforme votre microcontrôleur en une véritable machine de monitoring 
        (SOC - Security Operations Center) miniature.  
        Il permet d’explorer l’environnement WiFi, d’identifier les réseaux à proximité, 
        d’analyser les ports ouverts sur une cible spécifique, de collecter des informations 
        système essentielles et de visualiser l’ensemble via une interface web moderne, fluide 
        et entièrement embarquée.  
        L’objectif est d’offrir un outil compact, portable et polyvalent pour l’analyse réseau 
        passive, l’observation du trafic environnant et la supervision de petits environnements 
        techniques — le tout sans dépendre d’un ordinateur.
      </p>
    </td>
  </tr>
</table>


## 🚀 Fonctionnalités 
Le projet propose une interface web interactive, hébergée directement sur le Raspberry Pi Pico W, offrant un ensemble d’outils de supervision réseau :

🔍 Network Scanner — Analyse passive des réseaux WiFi environnants (SSID, BSSID, canal, RSSI).
<br>
| Champ | Description |
| --- | --- |
| SSID | Nom du réseau |
| BSSID | Adresse MAC AP (hex) |
| Canal | Canal WiFi |
| RSSI | Puissance du signal |
| Sécurité | Type de chiffrement |
<br>
<br>🛡️ Port Scanner — Vérification des ports critiques (22, 80, 443, 8080) sur une cible du réseau local.
<br><br><img src="https://github.com/user-attachments/assets/e9152c5a-bfb9-414e-8188-f5637f2da959" width="70%" /><br><br>
<br>📊 System Health — Monitoring en temps réel des ressources du microcontrôleur (RAM, CPU, uptime).
<br><br><img src="https://github.com/user-attachments/assets/f7054777-fcf1-4510-93b9-42c38e708d57" width="70%" /><br><br>
<br>📝 Log Engine — Système interne de journalisation des actions et événements.
<br><br><img src="https://github.com/user-attachments/assets/51756293-5b39-45a4-ab15-fa24dcc8aeec" width="70%" /><br><br>
<br>⚡ Smart Cache — Rafraîchissement intelligent des données toutes les SCAN_INTERVAL secondes = *120 secondes* pour préserver les ressources.

## 🛠️ Matériel Requis
- **Microcontrôleur** : Raspberry Pi Pico W (avec support WiFi)
- **Language** : MicroPython
- **Alimentation** : USB ou batterie externe 5V
- **Connexion internet stable**

## 📦 Installation & Utilisation
 **Prérequis** : Assurez-vous que votre Raspberry Pi Pico W possède le dernier firmware MicroPython.
 Téléchargement : https://micropython.org/download/RPI_PICO_W/
 
**Configuration** : Modifiez les variables `SSID`, `PASSWORD` et `TARGET` (IP de la cible à scanner) dans le fichier *PicoSOC_Nexus.py*.
```py
# =========================
# CONFIG
# =========================
SSID = '[Nom_du_reseau]'
PASSWORD = '[Mot_de_passe]'

TARGET = "[IP_Cible]"
SCAN_INTERVAL = 120

boot = time.ticks_ms()
LOGS = []

CACHE = {
    "ports": [],
    "wifi": [],
    "http": ""
}

last_scan = 0
```
**Upload** : Copiez le script sur votre Pico à l'aide de *Thonny*.

Accès : Une fois lancé, l'adresse IP du Pico s'affichera dans la console. Connectez-vous via votre navigateur sur le même réseau local.
⚠️ **Cela peit prendre 1 à 2 minutes la première fois le temps que le Raspberry fasse les différents scans** 

## 🤖 Développement & IA
Ce projet a été développé avec une approche hybride. La structure globale, l'architecture réseau et plus particulièrement la phase de débogage et d'optimisation de la gestion mémoire (Garbage Collection) ont été assistées par intelligence artificielle. Cette collaboration a permis d'assurer une stabilité système malgré les ressources limitées du microcontrôleur (gestion des erreurs ENOMEM et fermeture propre des sockets).

## 🤝 Contributions
Les améliorations sont les bienvenues ! Si vous souhaitez optimiser le code ou ajouter des fonctionnalités (scans plus larges, graphiques en JS, etc.)

## 📜 Licence & Propriété
Copyright (c) 2024 - loschoe
Tous droits réservés. Ce code est la propriété exclusive de son auteur.

Autorisations : Vous êtes autorisé à modifier et améliorer ce code dans le cadre de contributions via Pull Requests sur ce dépôt.

Restrictions : L'utilisation commerciale, la redistribution massive ou la réappropriation du projet sans mention de l'auteur original ne sont pas autorisées sans accord préalable.

