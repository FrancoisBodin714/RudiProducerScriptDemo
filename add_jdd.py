#Ajoute les jeux de données déclarés dans le répertoire JDD
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

#Creation du contact et de l'organisation, sera utilisé pour la construction des métadonnées

c = librudiprod.Rudi_Contact()
cdld = np_api.getContactData("Bacasable")
cdld  = cdld[0]
print("Using contact ",cdld)
if cdld  == None:
    #take the one declared in the rudi_proxy.ini file
    c.create(email=np_api.email,contact_name=np_api.contact_name,contact_id=np_api.contact_id)
else:
    c.create(email=cdld["email"],contact_name=cdld["contact_name"],contact_id=cdld["contact_id"])

o = librudiprod.Rudi_Organization()
odld = np_api.getOrganisationData("RUDI")
odld = odld[0]
print("Using organisation ",odld)
if odld == None:
    #take the one declared in the rudi_proxy.ini file   
    o.create(organization_id = np_api.organization_id,organization_name = np_api.organization_name,organization_address = np_api.organization_address)
else:
    o.create(organization_id = odld["organization_id"],organization_name = odld["organization_name"],organization_address = odld["organization_address"])
    

#Accès aux jeux de données et métadata correspondantes, utilise le fichier 'localFiles.ini'
ori = localFiles.LocalFiles()
#Chargement des métadonnées dans le répertoire 'JDD'
ori.downloadMetadata()
jdds = ori.BrowseDataSet()
#affichage des jeux de données (identifiant local)
#construction des métadonnées
#chargement du JDD sur bacasable
for jdd in jdds:
    #Liste des média pour le jeu de données, dans le cas des fichiers locaux c'est 1 seul
    data = []
    data_type = []
    data_file_name = []
    digestmd5 = []
    media_id =[]
    data_file_name.append(ori.getFileNameFromLocalId(jdd))
    data_type.append(ori.getDataSetType(jdd))
    pth = ori.datasource_directory + ori.getFileNameFromLocalId(jdd)
    print("Chemin du fichier ", pth, " pour le JDD ",jdd, " qui est du type ",ori.getDataSetType(jdd))

    #chargement des données
    datafile = open(pth,"rb")
    data.append(datafile.read())
    datafile.close()
    dsm = ori.getDataSetMetaData(jdd)
    
    #Construction de la signature du fichier
    md5_hash = hashlib.md5() 
    md5_hash.update(data[-1])
    digestmd5.append(md5_hash.hexdigest())

    
    #print("Actions de publication sur média")
    #np_api.displayMediaStatus()     
    #get the media uuid already produced for avoiding the creation of a copie
    media_entry = np_api.getMediaStatus(ori.getFileNameFromLocalId(jdd))
    print(media_entry)
    if len(media_entry) > 0:
        #We already have created a media for the file
        uud = media_entry[-1][1]
        print("Reusing media",uud)
        media_id.append(uud)
    else:
        #Création d'un identifiant de média
        media_id.append(str(uuid.uuid4()))

    #création des métadonnées au format RUDI
    m = librudiprod.Rudi_Metadata()
    metadata = m.createFromOrigine(np_api,
                                  ori,
                                  jdd,
                                  dsm,
                                  data,
                                  c,
                                  o,
                                  digestmd5,
                                  "",
                                  data_type,
                                  data_file_name,
                                  media_id,
                                  origin="LFS",
                                  publish=False #do not publish on the portal
                                  )

    print(metadata)
    #Publication des métadonnées
    if np_api.publishMetadata(metadata):
        print("la publication des métadonnées a été faite avec succès")
        #Publication des données dans la zone média du
        for j in range(len(media_id)):
            if np_api.publishFile(data[j],media_id[j],data_file_name[j],len(data[j])):
                np_api.recordMediaStatus(data_file_name[j],media_id[j],np_api.STATUSMEDIA_ONLINE_OK,time.time())
            else:
                np_api.recordMediaStatus(data_file_name[j],media_id[j],np_api.STATUSMEDIA_ONLINE_FAILED,time.time())

#affichage du status des jdd
#print("Actions de publication de métadonnées")
#np_api.displayJDDStatus()

#Fermer la base de données qui conserve les liens entre les identifiants locaux et globaux
#utilisé par exemple pour les mises à jour afin de ne pas créer de doublons
#remise à zéro en supprimant le fichier 'bacasable_node.db' (déclaré dans 'rudi_proxy.ini')
np_api.closeLocalDB()


