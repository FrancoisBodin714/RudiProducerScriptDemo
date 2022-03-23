#A propos de la librudiprod

Cette bibliothèque propose un empactage d'un sous-ensemble de l'API RUDI.
Elle comporte deux fonctionnalités principales :

1) la contruction des métadonnées
2) l'accès au noeud producteur (https://bacasable.fenix.rudi-univ-rennes1.fr/prodmanager/)

Le répertoire contient aussi une bibliothèque (localFiles.py) pour déclarer des
fichiers locaux (ici dans le répertoire JDD).

Une documentation du lien noeud-producteur <-> portail est
disponible ici : http://doc.rudi.bzh/api/contrat-portail-noeud-producteur/

La documentation de l'API est disponible ici :
https://app.swaggerhub.com/apis/OlivierMartineau/RUDI-PRODUCER/1.2.0#/Connector

#Noeud de test

https://bacasable.fenix.rudi-univ-rennes1.fr/prodmanager/
user = bacasable
passwd = bacasable

Ce noeud est remis en configuration initiale toutes les nuits.
Il comporte deux éléments principaux :

1) l'interface et l'API de gestion des métadonnées
2) la partie média qui s'occupe du stockage des JDD

#Installing the library

virtualenv -p /usr/bin/python3 venv
source venv/bin/activate
pip  install -r requirements.txt --upgrade

#Running the demo

python add_jdd.py

#Ajouts JDD

Pour ajouter un jeu de données, mettre le fichier dans le
répertoire JDD et créer le fichier .ini correspondant.
Un jeu supplémentaire est disponible dans JDD_Sup.

#Remise à zéro

La bibliothèque garde trace des identifiants créés pour éviter
les doublons sur le noeud et la multiplication des copies sur média.
La remise à zéro est effectuée en effacant le fichier bacasable_node.db. 
