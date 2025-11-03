# FPMsigm - Système de Gestion CREDEF

Plateforme de gestion des dossiers de crédit CREDEF avec workflow complet et système de validation multi-acteurs.

## 📋 Table des matières

- [Architecture](#architecture)
- [Prérequis](#prérequis)
- [Installation](#installation)
- [Configuration](#configuration)
- [Lancement](#lancement)
- [API Endpoints](#api-endpoints)
- [Workflow CREDEF](#workflow-credef)
- [Développement](#développement)

---

## 🏗️ Architecture

### Stack Technique

**Backend:**
- Flask 3.0.3 (Framework web)
- SQLAlchemy 2.0.31 (ORM)
- Flask-Migrate 4.0.7 (Migrations)
- Flask-JWT-Extended 4.6.0 (Authentification)
- MySQL 8 (Base de données)

**Architecture:**
- Pattern MVC avec Clean Architecture
- Séparation: Controllers → Services → Repositories → Models
- Machine à états pour le workflow métier

### Structure du Projet

```
FPMsigm/
├── backend/
│   ├── app/
│   │   ├── controllers/         # Endpoints API
│   │   ├── domain/
│   │   │   ├── models/          # Modèles SQLAlchemy
│   │   │   ├── repositories/    # Couche d'accès aux données
│   │   │   └── services/        # Logique métier
│   │   ├── utils/               # Utilitaires (sécurité, etc.)
│   │   ├── migrations/          # Migrations Alembic
│   │   ├── extensions.py        # Configuration des extensions
│   │   ├── config.py            # Configuration Flask
│   │   └── blueprints.py        # Enregistrement des routes
│   ├── autoapp.py               # Point d'entrée
│   ├── requirements.txt         # Dépendances Python
│   ├── docker-compose.yml       # Docker MySQL + Adminer
│   └── setup.sh                 # Script d'installation
└── README.md                     # Ce fichier
```

---

## ✅ Prérequis

- **Python 3.11+**
- **Docker & Docker Compose** (pour MySQL)
- **pip3** (gestionnaire de paquets Python)

---

## 🚀 Installation

### 1. Cloner le repository

```bash
git clone <repository-url>
cd FPMsigm/backend
```

### 2. Installation automatique

```bash
./setup.sh
```

Le script setup.sh va:
- Créer le fichier `.env`
- Installer les dépendances Python
- Démarrer Docker (MySQL + Adminer)
- Exécuter les migrations de base de données

### 3. Installation manuelle (alternative)

```bash
# Copier .env.example vers .env
cp .env.example .env

# Installer les dépendances
pip3 install -r requirements.txt

# Démarrer Docker
docker compose up -d

# Attendre que MySQL soit prêt (5-10 secondes)
sleep 5

# Exécuter les migrations
export FLASK_APP=autoapp.py
flask db upgrade
```

---

## ⚙️ Configuration

Le fichier `.env` contient la configuration:

```env
DATABASE_URL=mysql+pymysql://credef:credef@localhost:3306/credef
JWT_SECRET_KEY=<generated-secret-key>
UPLOAD_DIR=/tmp/uploads
FLASK_APP=autoapp.py
FLASK_ENV=development
```

**Variables importantes:**
- `DATABASE_URL`: URL de connexion MySQL
- `JWT_SECRET_KEY`: Clé secrète pour les tokens JWT (générée automatiquement)
- `UPLOAD_DIR`: Répertoire pour les fichiers uploadés
- `FLASK_ENV`: Environnement (development/production)

---

## 🎯 Lancement

### Démarrer l'application

```bash
cd backend
python3 autoapp.py
```

L'API sera disponible sur: **http://localhost:5000**

### Accéder à Adminer (interface DB)

Ouvrir dans un navigateur: **http://localhost:8080**

**Identifiants MySQL:**
- Système: MySQL
- Serveur: mysql
- Utilisateur: credef
- Mot de passe: credef
- Base de données: credef

---

## 📡 API Endpoints

### Base URL
```
http://localhost:5000/api
```

### Endpoints disponibles

#### 1. Liste des dossiers CREDEF

```http
GET /api/credef/dossiers
GET /api/credef/dossiers?statut=DÉPOSÉ
GET /api/credef/dossiers?mois=2025-11
```

**Réponse (200):**
```json
[
  {
    "id": 1,
    "ref": "CREDEF-2025-001",
    "adherent_id": 123,
    "date_depot": "2025-11-03",
    "montant_demande": 50000.00,
    "montant_accorde": null,
    "taux": 10.00,
    "duree_mois": 12,
    "statut": "BROUILLON",
    "mois_traitement": "2025-11",
    "acteur_courant_id": 1,
    "commentaire_rejet": null
  }
]
```

#### 2. Créer un nouveau dossier

```http
POST /api/credef/dossiers
Content-Type: application/json

{
  "ref": "CREDEF-2025-001",
  "adherent_id": 123,
  "montant_demande": 50000.00,
  "duree_mois": 12
}
```

**Réponse (201):**
```json
{
  "id": 1,
  "ref": "CREDEF-2025-001",
  "statut": "BROUILLON",
  ...
}
```

#### 3. Transition de statut

```http
POST /api/credef/dossiers/1/transition
Content-Type: application/json

{
  "to": "DÉPOSÉ",
  "role": "SACV",
  "acteur_id": 123,
  "note": "Dossier validé par le SACV"
}
```

**Réponse (200):**
```json
{
  "id": 1,
  "ref": "CREDEF-2025-001",
  "statut": "DÉPOSÉ",
  ...
}
```

**Note:** La transition est automatiquement enregistrée dans le `workflow_log` pour traçabilité.

**Codes d'erreur:**
- `400`: Transition invalide
- `404`: Dossier non trouvé

#### 4. Historique des transitions (Workflow Log)

```http
GET /api/credef/dossiers/1/workflow
```

**Réponse (200):**
```json
{
  "dossier_id": 1,
  "dossier_ref": "CREDEF-2025-001",
  "statut_actuel": "DÉPOSÉ",
  "historique": [
    {
      "id": 2,
      "dossier_id": 1,
      "statut_from": "BROUILLON",
      "statut_to": "DÉPOSÉ",
      "acteur_id": 123,
      "role": "SACV",
      "commentaire": "Dossier validé par le SACV",
      "created_at": "2025-11-03T23:45:12.000000"
    },
    {
      "id": 1,
      "dossier_id": 1,
      "statut_from": null,
      "statut_to": "BROUILLON",
      "acteur_id": null,
      "role": "SYSTEM",
      "commentaire": null,
      "created_at": "2025-11-03T23:30:00.000000"
    }
  ]
}
```

**Codes d'erreur:**
- `404`: Dossier non trouvé

---

## 🔄 Workflow CREDEF

### Diagramme des états

```
BROUILLON
    ↓
DÉPOSÉ (par Adhérent)
    ↓
EN_CONTROLE_SACV (validation SACV)
    ↓
TRANSMIS_COURRIER (envoi courrier)
    ↓
EN_ETUDE_PRET (analyse technique)
    ↓
SOUMIS_COMITE (présentation comité)
    ↓
VALIDÉ_COMITE (décision positive)
    ↓
ETATS_EDITES (génération PDF)
    ↓
EN_SIGNATURE_DCFF_DCPRE (signature électronique)
    ↓
TRANSMIS_DTR (envoi DTR)
    ↓
DECAISSE_ECOBANK (décaissement)
    ↓
CLOS (dossier finalisé)

    ↕️
REJET_ADMIN (peut revenir à BROUILLON ou DÉPOSÉ)
```

### Transitions autorisées

Le service `CredefService` valide automatiquement les transitions selon les règles métier:

- **BROUILLON** → DÉPOSÉ
- **DÉPOSÉ** → EN_CONTROLE_SACV, REJET_ADMIN
- **EN_CONTROLE_SACV** → TRANSMIS_COURRIER, REJET_ADMIN
- **TRANSMIS_COURRIER** → EN_ETUDE_PRET
- **EN_ETUDE_PRET** → SOUMIS_COMITE, REJET_ADMIN
- **SOUMIS_COMITE** → VALIDÉ_COMITE, REJET_ADMIN
- **VALIDÉ_COMITE** → ETATS_EDITES
- **ETATS_EDITES** → EN_SIGNATURE_DCFF_DCPRE
- **EN_SIGNATURE_DCFF_DCPRE** → TRANSMIS_DTR
- **TRANSMIS_DTR** → DECAISSE_ECOBANK
- **DECAISSE_ECOBANK** → CLOS
- **REJET_ADMIN** → BROUILLON, DÉPOSÉ

---

## 🛠️ Développement

### Créer une nouvelle migration

```bash
export FLASK_APP=autoapp.py
flask db migrate -m "Description de la migration"
flask db upgrade
```

### Rollback d'une migration

```bash
flask db downgrade
```

### Lancer les tests (à venir)

```bash
pytest
```

### Structure d'un nouveau modèle

```python
from app.extensions import db

class NouveauModele(db.Model):
    __tablename__ = "nouveau_modele"

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
```

### Ajouter un endpoint

1. Créer le controller dans `app/controllers/`
2. Créer le service dans `app/domain/services/`
3. Enregistrer le blueprint dans `app/blueprints.py`

---

## 📝 Backlog (Prochaines étapes)

### ✅ Complété
- [x] API Dossiers (GET/POST)
- [x] Transitions Workflow
- [x] Migration Alembic initiale
- [x] Workflow Log (historique des transitions)

### 🔜 En cours
- [ ] Pièces jointes (upload & validation)
- [ ] Authentification JWT complète (login/register)

### ⏳ À venir
- [ ] Frontend React/Tailwind
- [ ] Kanban drag & drop
- [ ] Dashboard KPI
- [ ] Génération PDF
- [ ] Double signature électronique
- [ ] Export audit (CSV/PDF)

---

## 📞 Support

Pour toute question ou problème:
1. Vérifier les logs: `docker compose logs mysql`
2. Vérifier la connexion DB via Adminer
3. Consulter la documentation Flask: https://flask.palletsprojects.com/

---

## 📄 Licence

[À définir]
