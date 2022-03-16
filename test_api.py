#Ajoute les jeux de données déclarés dans le répertoire JDD
import librudiprod
import localFiles
import hashlib
import uuid
import time

#initialisation de l'API, utilise le fichier 'rudi_proxy.ini' pour l'ensemble des paramètres
np_api = librudiprod.Rudi_API()

if not np_api.checkServer():
    print("Le noeud  ne peut être contacté")
    exit(1)

print("============== Enum de l'API ===========")
enum = np_api.getListEnum()
print(enum)

o = np_api.getOrganisationData("RUDI")
print(o)

c = np_api.getContactData("Bacasable")
print(c)




