#Obtention des métadonnées pour un JDD à partir de l'id local
import librudiprod
import localFiles
import hashlib
import uuid
import time


#initialisation de l'API, utilise le fichier 'rudi_proxy.ini' pour l'ensemble des paramètres
np_api = librudiprod.Rudi_API()

if not np_api.checkServer():
    print("Le noeud bacasable ne peut être contacté")
    exit(1)

print("===================================")
metadata = np_api.getMetaFromId("README_INI",globalId = False)
print(metadata)
