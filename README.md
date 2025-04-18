# 🩺 MediConnect

Application web médicale complète pour la gestion de patients, la visualisation d'images DICOM, et l'intégration de la téléradiologie et de l'intelligence artificielle.

---

## 👨‍💻 Développé par
- **Abdoulaye LAH** ([GitHub](https://github.com/layelah))

Projet réalisé dans le cadre du Master 1 Génie Logiciel et Systèmes d'Information.

---

## 📦 Prérequis

🔧 Avant de commencer, installez les outils suivants :

- [Python 3.10+](https://www.python.org/downloads/)
- [Node.js 18+](https://nodejs.org/en)
- [Docker](https://www.docker.com/products/docker-desktop/)
- [Git](https://git-scm.com/downloads)
- (Optionnel) [PostgreSQL local](https://www.postgresql.org/download/) si vous ne passez pas par Docker

---

## 🛠️ Installation et Configuration Complète

### 🧾 1. Cloner le projet

```bash
# Clonez le dépôt Git
git clone https://github.com/<votre-username>/pycrafted-mediconnect.git
cd pycrafted-mediconnect
```

### 🐘 2. Configurer PostgreSQL avec Docker

> ⚠️ C’est la base de données pour Django. Ne **PAS** sauter cette étape.

```bash
docker run -d --name mediconnect-pg -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=mediconnect_db -p 5432:5432 postgres
```

🧪 **Tester la connexion** :

```bash
psql -h localhost -U postgres -d mediconnect_db
```

✅ Si ça fonctionne, passez à l’étape suivante.  
❌ Si erreur : vérifier avec `docker ps` que le conteneur tourne, et que le port `5432` est libre.

### ⚙️ 3. Configurer le Backend Django

```bash
cd backend
```

🔹 Créer un environnement virtuel :

```bash
python -m venv venv
```

🔹 L’activer :

```bash
# Sous Windows :
venv\Scripts\activate

# Sous Linux/Mac :
source venv/bin/activate
```

🔹 Installer les dépendances :

```bash
pip install -r requirements.txt
```

🔹 Appliquer les migrations :

```bash
python manage.py migrate
```

🔹 Lancer le serveur :

```bash
python manage.py runserver
```

🔗 Accès : [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)

> 🛠️ Vérifiez `settings.py` si vous avez des soucis de connexion avec PostgreSQL.

### 🩻 4. Configurer Orthanc (pour les fichiers DICOM)

```bash
cd orthanc
```

🔹 Lancer Orthanc avec docker-compose :

```bash
docker-compose up -d
```

🔗 Accès à l’interface : [http://localhost:8042](http://localhost:8042)  
🔐 Identifiants : `orthanc` / `orthanc`

📋 Vérifier les logs :

```bash
docker logs orthanc-orthanc-1
```

### 🌐 5. Configurer le Frontend React

```bash
cd frontend
```

🔹 Installer les dépendances :

```bash
npm install
```

🔹 Lancer le frontend :

```bash
npm start
```

🔗 Interface web : [http://localhost:3000](http://localhost:3000)

---

## 🧾 Structure du Projet

```bash
pycrafted-mediconnect/
├── backend/     ← Backend Django (API, Auth, Models)
├── frontend/    ← Frontend React (interface utilisateur)
├── orthanc/     ← Configuration Orthanc (docker-compose.yml)
├── docs/        ← Documentation (à venir)
├── tests/       ← Tests unitaires (à venir)
```

---

## 🧪 Utilisation de l’Application

- 📁 **Orthanc** : Gérer les fichiers DICOM via [http://localhost:8042](http://localhost:8042)
- 🛠️ **Django** : Gérer les utilisateurs/admin via [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)
- 🖥️ **React** : Interface de gestion médicale via [http://localhost:3000](http://localhost:3000)

---

## 📚 Commandes Utiles

### 🛑 Arrêter Orthanc

```bash
cd orthanc
docker-compose down
```

### 🔍 Logs Django

```bash
cd backend
python manage.py runserver --verbosity 2
```

### 🧹 Nettoyer le cache npm (en cas de bug frontend)

```bash
cd frontend
npm cache clean --force
```

---

## 🔮 Prochaines Étapes

- ✅ Implémenter les modèles de gestion des patients en Django
- ✅ Créer les interfaces Patient / Médecin en React
- 🔄 Intégrer l’API REST de Django avec Orthanc pour synchroniser les données DICOM
- 🧠 Ajouter des fonctionnalités IA pour la lecture automatisée des images

---

## 🙋 Support & Questions

📩 Pour toute question, ouvrez une issue sur GitHub ou contactez **[Abdoulaye LAH](https://github.com/layelah)**.

---

🧠 Merci d’utiliser MediConnect ! Ensemble, digitalisons la santé. 💻🧬

