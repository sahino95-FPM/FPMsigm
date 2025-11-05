# 🔐 Guide de Test d'Authentification

Ce guide vous aide à tester le système d'authentification de l'application CREDEF.

## 📋 Prérequis

### 1. MySQL/MariaDB

La base de données doit être en cours d'exécution avec :
- **Utilisateur** : `credef`
- **Mot de passe** : `credef`
- **Base de données** : `credef`
- **Port** : `3306`

### 2. Python et dépendances

Assurez-vous d'avoir Python 3.9+ installé.

## 🚀 Installation et Configuration

### Étape 1 : Installer les dépendances

```powershell
cd C:\Users\SAHINO\Desktop\test\FPMsigm\backend
pip install -r requirements.txt
```

### Étape 2 : Vérifier la configuration

Le fichier `.env` doit contenir :

```env
DATABASE_URL=mysql+pymysql://credef:credef@localhost:3306/credef
JWT_SECRET_KEY=c9ab4e58a20f13e471b36822e6147bc0f4fb181e7f16eb62b9632e924e013649
UPLOAD_DIR=/tmp/uploads
FLASK_APP=autoapp.py
FLASK_ENV=development
```

### Étape 3 : Appliquer les migrations de base de données

```powershell
# Depuis le dossier backend
flask db upgrade
```

## 🧪 Tester l'Authentification

### Option 1 : Script Python automatique (Recommandé ✅)

**Terminal 1** - Démarrer le serveur Flask :
```powershell
cd C:\Users\SAHINO\Desktop\test\FPMsigm\backend
python autoapp.py
```

Vous devriez voir :
```
 * Running on http://127.0.0.1:5000
```

**Terminal 2** - Lancer le script de test :
```powershell
cd C:\Users\SAHINO\Desktop\test\FPMsigm\backend
python test_auth.py
```

Le script va :
- ✅ Lister les rôles disponibles
- ✅ Créer un utilisateur admin (email: admin@credef.com, password: admin123)
- ✅ Se connecter et obtenir un token JWT
- ✅ Récupérer les informations de l'utilisateur

### Option 2 : Tests manuels avec PowerShell

**Terminal 1** - Démarrer le serveur Flask :
```powershell
cd C:\Users\SAHINO\Desktop\test\FPMsigm\backend
python autoapp.py
```

**Terminal 2** - Effectuer les tests manuels :

#### 1️⃣ Lister les rôles disponibles

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/auth/roles" -Method GET
```

#### 2️⃣ Créer un utilisateur admin

```powershell
$registerBody = @{
    email = "admin@credef.com"
    password = "admin123"
    nom = "Admin"
    prenom = "Systeme"
    role = "ADMIN"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/auth/register" -Method POST -Body $registerBody -ContentType "application/json"
```

#### 3️⃣ Se connecter

```powershell
$loginBody = @{
    email = "admin@credef.com"
    password = "admin123"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/auth/login" -Method POST -Body $loginBody -ContentType "application/json"

# Afficher les résultats
Write-Host "✅ Connexion réussie!"
Write-Host "Token: $($response.access_token.Substring(0, 50))..."
Write-Host "Utilisateur: $($response.user.prenom) $($response.user.nom)"
Write-Host "Rôle: $($response.user.role)"

# Sauvegarder le token pour les prochaines requêtes
$token = $response.access_token
```

#### 4️⃣ Récupérer les infos de l'utilisateur connecté

```powershell
$headers = @{
    "Authorization" = "Bearer $token"
    "Content-Type" = "application/json"
}

$userInfo = Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/auth/me" -Method GET -Headers $headers

Write-Host "Informations utilisateur:"
$userInfo
```

### Option 3 : Tests avec curl (si disponible)

#### Lister les rôles
```bash
curl http://127.0.0.1:5000/api/auth/roles
```

#### Créer un utilisateur
```bash
curl -X POST http://127.0.0.1:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@credef.com",
    "password": "admin123",
    "nom": "Admin",
    "prenom": "Systeme",
    "role": "ADMIN"
  }'
```

#### Se connecter
```bash
curl -X POST http://127.0.0.1:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@credef.com",
    "password": "admin123"
  }'
```

## 🎭 Rôles Disponibles

Le système supporte les rôles suivants :
- **ADMIN** - Administrateur système
- **SACV** - Service d'Action Culturelle et de Valorisation
- **SCR** - Service Commercial et Relations
- **SG** - Secrétariat Général
- **PRESIDENT** - Président
- **DAF** - Directeur Administratif et Financier
- **DG** - Directeur Général

## ❌ Résolution des Problèmes

### Erreur : "Connection refused"
**Cause** : Le serveur Flask n'est pas démarré.
**Solution** : Lancez `python autoapp.py` dans le dossier backend.

### Erreur : "Can't connect to MySQL server"
**Cause** : MySQL/MariaDB n'est pas en cours d'exécution ou mauvaise configuration.
**Solution** :
- Vérifiez que MySQL est démarré
- Vérifiez les identifiants dans le fichier `.env`
- Créez la base de données si elle n'existe pas : `CREATE DATABASE credef;`

### Erreur : "Un utilisateur avec cet email existe déjà"
**Cause** : L'utilisateur a déjà été créé.
**Solution** : C'est normal ! Passez directement à l'étape de connexion.

### Erreur : "Table 'credef.user' doesn't exist"
**Cause** : Les migrations n'ont pas été appliquées.
**Solution** : Lancez `flask db upgrade` dans le dossier backend.

### Erreur : "ModuleNotFoundError: No module named 'X'"
**Cause** : Dépendances manquantes.
**Solution** : Réinstallez les dépendances : `pip install -r requirements.txt`

## 📝 Créer d'Autres Utilisateurs de Test

Pour créer des utilisateurs avec différents rôles :

```powershell
# Utilisateur SACV
$body = @{
    email = "sacv@credef.com"
    password = "sacv123"
    nom = "Culturel"
    prenom = "Service"
    role = "SACV"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/auth/register" -Method POST -Body $body -ContentType "application/json"

# Utilisateur SCR
$body = @{
    email = "scr@credef.com"
    password = "scr123"
    nom = "Commercial"
    prenom = "Service"
    role = "SCR"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/auth/register" -Method POST -Body $body -ContentType "application/json"
```

## ✅ Résultats Attendus

Après avoir exécuté les tests avec succès, vous devriez avoir :

1. ✅ Un utilisateur admin créé dans la base de données
2. ✅ Un token JWT valide pour l'authentification
3. ✅ La possibilité de récupérer les infos de l'utilisateur connecté
4. ✅ Une liste complète des rôles disponibles

## 🔗 Endpoints API Disponibles

- `GET /api/auth/roles` - Liste les rôles disponibles
- `POST /api/auth/register` - Créer un nouveau compte
- `POST /api/auth/login` - Se connecter et obtenir un token JWT
- `GET /api/auth/me` - Récupérer les infos de l'utilisateur connecté (nécessite authentification)

## 🎉 Prochaines Étapes

Une fois l'authentification testée, vous pouvez :
- Tester le frontend React avec la connexion
- Créer des dossiers CREDEF
- Tester les workflows et transitions
- Ajouter des pièces jointes

---

**Bon test ! 🚀**
