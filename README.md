MediConnect
Application web médicale pour gérer les patients, les données DICOM, et intégrer télé-radiologie et IA.
Prérequis

Python 3.10+
Node.js 18+
PostgreSQL
Docker
Git

Installation
1. Cloner le projet
git clone <URL_DU_REPOSITOIRE>
cd MediConnect

2. Configurer Orthanc

Naviguer dans le dossier Orthanc :cd orthanc


Créer le fichier docker-compose.yml avec le contenu suivant :services:
  orthanc:
    image: jodogne/orthanc
    ports:
      - "4242:4242"
      - "8042:8042"
    volumes:
      - ./orthanc-db:/var/lib/orthanc/db


Lancer Orthanc :docker-compose up -d


Accéder à l’interface web :
URL : http://localhost:8042
Identifiants : orthanc/orthanc



3. Configurer le Frontend React
(À compléter après configuration du frontend)
4. Configurer le Backend Django
(À compléter)
5. Configurer PostgreSQL
(À compléter)
Structure

backend/ : Projet Django
frontend/ : Projet React
orthanc/ : Configuration Orthanc
docs/ : Documentation
tests/ : Tests unitaires

Utilisation

Orthanc :
Accéder à http://localhost:8042 pour gérer les fichiers DICOM.
Utiliser les identifiants orthanc/orthanc.
API REST disponible à http://localhost:8042 (ex. : GET /studies pour lister les études).


Frontend React : (À compléter)
Backend Django : (À compléter)

Commandes utiles

Lancer Orthanc :cd orthanc
docker-compose up -d


Vérifier les logs d’Orthanc :docker logs orthanc-orthanc-1


Arrêter Orthanc :docker-compose down



Prochaines étapes

Configurer le frontend React pour interagir avec l’API REST d’Orthanc.
Intégrer le backend Django avec PostgreSQL.
Rédiger la documentation complète.

