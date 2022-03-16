#Obtention des métadonnées pour un JDD à partir de l'id local
import librudiprod
import localFiles
import hashlib
import uuid
import time
import json

#initialisation de l'API, utilise le fichier 'rudi_proxy.ini' pour l'ensemble des paramètres
np_api = librudiprod.Rudi_API()

if not np_api.checkServer():
    print("Le noeud bacasable ne peut être contacté")
    exit(1)

print("==============Get the metadata===============")
metadata = np_api.getMetaFromId("README_INI",globalId = False)
print(metadata)
if metadata == None or len(metadata) == 0:
    print("Could not get the metadata ... exiting")
    exit(1)
print("==============Change the metadata===============")

print(metadata[0]["resource_title"])
metadata[0]["resource_title"] = "Nouveau titre des metadonnées"
print(metadata)
print("==============Re-publish the metadata===============")
metadata_str = json.dumps(metadata[0])
if np_api.publishMetadata(metadata_str):
    print("Republishing ok")
else:
    print("Fail to send the metadata")


