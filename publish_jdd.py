#Obtention des métadonnées pour un JDD à partir de l'id local
#et publication sur le portail
import librudiprod
import localFiles
import hashlib
import uuid
import json
import time

#initialisation de l'API, utilise le fichier 'rudi_proxy.ini' pour l'ensemble des paramètres
np_api = librudiprod.Rudi_API()

if not np_api.checkServer():
    print("Le noeud bacasable ne peut être contacté")
    exit(1)

print("===================================")
jdd = "README_INI"
gid = np_api.getGlobalIdFromLocalId(jdd)
print(gid)
metadata = np_api.getMetaFromId(jdd,globalId = False)
print(metadata)

if metadata != None:
    try:
        del metadata[0]['collection_tag']
        print("PUBLISHING")
        print(metadata[0])
        metadata_str = json.dumps(metadata[0])
        np_api.publishMetadata(metadata_str)
    except:
        print('collection_tag not present')

    ir = np_api.getIntegrationReport(gid)
    print(ir)

