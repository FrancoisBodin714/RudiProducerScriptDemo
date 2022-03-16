#metadata pour README / description du fichier de configuration
[METADATA]

#Le fichier de données (limité actuellement à un unique fichier)
descriptor_file = README.txt

#le titre qui apparaitra dans le titre du jeu de données
descriptor_resource_title = README des fichiers de configuration

#Date de création des métadata
descriptor_metadata_info_created = 02/10/2021
descriptor_metadata_info_updated = 02/10/2021

#Date de création 
descriptor_dataset_dates_created = 31/12/2020
descriptor_dataset_dates_updated = 31/12/2020

#Liste de mots clés, liste libre pour l'instant
descriptor_keywords = electricity, energy_consommation

#Le producteur doit être au préalable créé sur le noeud producteur, on reporte ici sont id au format uuid
descriptor_producer_organization_id = 99dc4101-97a5-43db-b3a3-f2eedefd8340

#Le contact doit être au préalable créé sur le noeud, on reporte ici sont id au format uuid
descriptor_contact_id = 941545a2-3f44-469d-a0e3-251b7a90f418

#Langage de la ressource, pour l'instant seul "fr" est considéré
descriptor_resource_languages = fr

#identifiant uuid voir https://docs.python.org/3/library/uuid.html
descriptor_global_id = a1fa1832-3979-445d-815b-2c49b8efd25f

#Le nom local de la ressource
descriptor_local_id = README_INI

#Ce champs est obligatoire
descriptor_synopsis = Fichier README avec la documentation des champs pour la configuration du moissonneur à partir de fichiers locaux

#ce champs est obligatoire mais son contenu n'est pas pris en compte si le champs descriptor_summary_file indique un fichier valide
descriptor_summary = Fichier README avec la documentation des champs pour la configuration du moissonneur à partir de fichiers locaux

#Indique le fichier qui contient la description du champs de données
#Le champs doit être présent, si aucun fichier n'est disponible le positionner sur 
#descriptor_summary_file = nofile
descriptor_summary_file = README.summary

#Choice of one theme in 
#     economy, citizenship, energyNetworks, culture, transportation,	children, environment,
#     townPlanning, location, education, publicSpace, health, housing, society
descriptor_theme = energyNetworks

#Type de la licence STANDARD (alors dans la liste ci-dessous) sinon la valeur est CUSTOM
descriptor_licence_type = STANDARD

#Choice of one licence in
#   etalab-2.0
#   etalab-1.0
#   gpl-3.0
#   public-domain-cc0
#   cc-by-nd-4.0
#   apache-2.0
#   odbl-1.0
#   mit
# si CUSTOM alors le champs suivant indique un lien vers la licence
descriptor_licence_label = etalab-1.0

#Use the MIME type here https://developer.mozilla.org/fr/docs/Web/HTTP/Basics_of_HTTP/MIME_types/Common_types
#When possible
#default application/octet-stream
#text is text/plain
descriptor_file_type = text/plain

#indicates if the data must be immediatly publish on the portal (valeur TRUE ou FALSE)
descriptor_ready_for_publication = FALSE

#indicates if the dataset is an update of previous version
descriptor_this_is_an_update = FALSE

