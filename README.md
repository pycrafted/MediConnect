🩺 MediConnect
Application web médicale complète pour la gestion de patients, la visualisation d'images DICOM, et l'intégration de la téléradiologie et de l'intelligence artificielle.

👨‍💻 Développé par

Abdoulaye LAH (GitHub)

Projet réalisé dans le cadre du Master 1 Génie Logiciel et Systèmes d'Information.

📦 Prérequis
🔧 Avant de commencer, installez les outils suivants :

Python 3.10+
Node.js 18+
Docker
Git
Postman (pour tester les API)
(Optionnel) PostgreSQL local si vous ne passez pas par Docker


🛠️ Installation et Configuration Complète
🧾 1. Cloner le projet
# Clonez le dépôt Git
git clone https://github.com/layelah/pycrafted-mediconnect.git
cd pycrafted-mediconnect

🐘 2. Configurer PostgreSQL avec Docker

⚠️ C’est la base de données pour Django. Ne PAS sauter cette étape.

docker run -d --name mediconnect-pg -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=mediconnect_db -p 5432:5432 postgres

🧪 Tester la connexion :
psql -h localhost -U postgres -d mediconnect_db

✅ Si ça fonctionne, passez à l’étape suivante.❌ Si erreur : vérifier avec docker ps que le conteneur tourne, et que le port 5432 est libre.
⚙️ 3. Configurer le Backend Django
cd backend

🔹 Créer un environnement virtuel :
python -m venv venv

🔹 L’activer :
# Sous Windows :
venv\Scripts\activate

# Sous Linux/Mac :
source venv/bin/activate

🔹 Installer les dépendances :
pip install -r requirements.txt

🔹 Appliquer les migrations :
python manage.py migrate

🔹 Créer les groupes et permissions :
python manage.py create_groups

🔹 Lancer le serveur :
python manage.py runserver

🔗 Accès : http://127.0.0.1:8000/admin

🛠️ Vérifiez settings.py si vous avez des soucis de connexion avec PostgreSQL.

🩻 4. Configurer Orthanc (pour les fichiers DICOM)
cd orthanc

🔹 Lancer Orthanc avec docker-compose :
docker-compose up -d

🔗 Accès à l’interface : http://localhost:8042\🔐 Identifiants : mediconnect / securepassword123
📋 Vérifier les logs :
docker logs orthanc-orthanc-1

🌐 5. Configurer le Frontend React
cd frontend

🔹 Installer les dépendances :
npm install

🔹 Installer les dépendances DICOM :
npm install cornerstone-core cornerstone-wado-image-loader dicom-parser

🔹 Lancer le frontend :
npm start

🔗 Interface web : http://localhost:3000

🧾 Structure du Projet
pycrafted-mediconnect/
├── backend/              ← Backend Django (API, Auth, Models)
│   ├── core/             ← Modèles et vues pour patients, médecins, etc.
│   ├── orthanc_integration/ ← Intégration avec Orthanc (API DICOM)
├── frontend/             ← Frontend React (interface utilisateur)
├── orthanc/              ← Configuration Orthanc (docker-compose.yml)
├── docs/                 ← Documentation (à venir)
├── tests/                ← Tests unitaires (à venir)
└── README.md             ← Instructions setup


🧪 Utilisation de l’Application

📁 Orthanc : Gérer les fichiers DICOM via http://localhost:8042
🛠️ Django Admin : Gérer les utilisateurs et patients via http://127.0.0.1:8000/admin
🖥️ React : Interface de gestion médicale via http://localhost:3000
🩻 DICOM : Uploader et visualiser les images DICOM via http://localhost:3000/dicom-viewer

Tester l’API DICOM avec Postman
Obtenir un token JWT :

Méthode : POST

URL : http://127.0.0.1:8000/api/token/

Headers : Content-Type: application/json

Body (raw, JSON) :
{
  "username": "oumy",
  "password": "Bocar@97"
}


Copiez le champ access de la réponse.


Lister les images DICOM :

Méthode : GET
URL : http://127.0.0.1:8000/api/orthanc/images/
Authorization : Bearer <access_token>
Headers : Content-Type: application/json

Uploader un fichier DICOM :

Méthode : POST
URL : http://127.0.0.1:8000/api/orthanc/dicom-to-png/
Authorization : Bearer <access_token>
Body : form-data
Clé : file, Valeur : sélectionnez un fichier .dcm
Clé : description, Valeur : (facultatif, par exemple, "Radio thorax")



Visualiser une image DICOM :

Méthode : GET
URL : http://127.0.0.1:8000/api/orthanc/dicom-to-png/?id=<instance_id>
Authorization : Bearer <access_token>


📚 Commandes Utiles
🛑 Arrêter Orthanc
cd orthanc
docker-compose down

🔍 Logs Django
cd backend
python manage.py runserver --verbosity 2

🧹 Nettoyer le cache npm
cd frontend
npm cache clean --force


✅ Progrès Réalisés

✅ Gestion des utilisateurs : Modèles Django pour Patient, Médecin, Assistant, Hôpital, RendezVous.
✅ Authentification : Système JWT avec groupes (Patient, Médecin, Assistant) et permissions.
✅ Intégration Orthanc : Upload et visualisation des fichiers DICOM avec persistance dans Orthanc.
✅ Frontend : Interface React pour la gestion des profils, rendez-vous, et visualisation DICOM.


🔮 Prochaines Étapes

🖥️ Améliorer l’interface téléradiologie (zoom, annotations sur les images DICOM).
🔒 Ajouter l’authentification multi-facteurs (MFA).
🧠 Intégrer des fonctionnalités IA pour l’analyse automatisée des images DICOM.
📊 Ajouter des statistiques pour les médecins (nombre de patients, rendez-vous, etc.).


🙋 Support & Questions
📩 Pour toute question, ouvrez une issue sur GitHub ou contactez Abdoulaye LAH.

🧠 Merci d’utiliser MediConnect ! Ensemble, digitalisons la santé. 💻🧬
