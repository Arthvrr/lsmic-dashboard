# LSMIC-DASHBOARD

## Présentation

Ce dépôt contient le code source de l'application web du **LSM Investment Club**, un outil essentiel pour le suivi et l'analyse du portefeuille boursier du club. Développé avec le framework **Django**, ce tableau de bord a pour objectif de transformer la théorie financière en pratique concrète, en offrant une plateforme dynamique et transparente pour évaluer la stratégie d'investissement du club.

Ce guide sert de référence technique pour le déploiement continu et la maintenance de l'application sur la plateforme d'hébergement PythonAnywhere.

### 📊 Fonctionnalités et Onglets Principaux

L'application est structurée autour des fonctionnalités suivantes pour répondre aux besoins d'analyse et de gestion du club :

* **Portefeuille** : Cet onglet présente une vue détaillée du portefeuille boursier du club. Il affiche le portefeuille dans les moindres détails, incluant les positions titre par titre, des données clés telles que le prix d'achat, le prix actuel, la valeur totale, le ROI en valeur et en pourcentage. Un graphique intégré offre une visualisation synthétique de la répartition et de l'évolution des actifs.
* **Performance** : Cette section est dédiée à l'évaluation de la performance personnelle de chaque membre du club.
* **Actualités** : Affiche les nouvelles et informations pertinentes pour les marchés financiers.
* **Profil** (ou Espace Utilisateur) : Permet à chaque membre de gérer ses paramètres personnels. Les fonctionnalités incluent la possibilité de changer le mot de passe, l'identifiant (username), ainsi que de s'abonner ou de se désabonner à la newsletter du club.


## 🔄 Routine de Mise à Jour du Projet Django (LSM Investment Club)

Ce guide décrit la procédure standard à suivre dans la console Bash de PythonAnywhere pour déployer les dernières modifications (code, dépendances, ou modèles de base de données).

### 1. 💻 Préparation et Récupération du Code

Ces commandes doivent être exécutées dans votre console **Bash** pour récupérer les changements effectués en local et publiés sur Git.
 
| Étape | Commande | Description |
| :--- | :--- | :--- |
| **Activer l'Environnement** | `workon mon-env-final` | Active l'environnement virtuel où Django est installé. |
| **Se positionner** | `cd lsmic-dashboard/lsm_investment` | Se déplace dans le répertoire de l'application qui contient le fichier `manage.py`. |
| **Récupérer les Changements** | `git pull` | Télécharge le dernier code de la branche Git vers le serveur. |

### 2. 🛠️ Mise à Jour du Système Django

Ces commandes garantissent que l'environnement serveur est synchronisé avec le nouveau code.

* **Mise à jour des Dépendances (si le fichier `requirements.txt` a été modifié)** :
    ```bash
    pip install -r requirements.txt
    ```

* **Mise à jour des Modèles (si des changements ont été faits dans `models.py`)** :
    ```bash
    python manage.py makemigrations lsm_investment
    python manage.py migrate
    ```

* **Mise à jour des Statiques (si vous avez ajouté ou modifié CSS/JS/images)** :
    ```bash
    python manage.py collectstatic
    ```

### 3. 🚀 Lancement de l'Application

La dernière étape est obligatoire pour forcer le serveur à charger le nouveau code Python.

* **Redémarrer l'Application** :
    1.  Aller à l'onglet **Web** de votre tableau de bord PythonAnywhere.
    2.  Cliquer sur le bouton vert **Reload** (Recharger).
