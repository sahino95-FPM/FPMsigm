# 🚀 Rituel de Démarrage de l'Application FPMsigm

Ce guide contient toutes les commandes nécessaires pour démarrer l'application complète (Backend + Frontend).

## 📋 Prérequis

Avant de commencer, vérifiez que :
- ✅ MySQL/MariaDB est démarré
- ✅ Python 3.9+ est installé
- ✅ Node.js 18+ est installé
- ✅ Vous êtes dans le bon répertoire

---

## 🎯 Démarrage Rapide (2 Terminaux)

### **Terminal 1️⃣ : Backend Flask**

```powershell
# Aller dans le dossier backend
cd C:\Users\SAHINO\Desktop\test\FPMsigm\backend

# Activer l'environnement virtuel (si vous en avez un)
# .venv\Scripts\Activate.ps1

# Démarrer le serveur Flask
python autoapp.py
```

**✅ Résultat attendu :**
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

⚠️ **Laissez ce terminal ouvert !**

---

### **Terminal 2️⃣ : Frontend React**

```powershell
# Ouvrir un NOUVEAU terminal PowerShell

# Aller dans le dossier frontend
cd C:\Users\SAHINO\Desktop\test\FPMsigm\frontend

# Démarrer le serveur de développement Vite
npm run dev
```

**✅ Résultat attendu :**
```
  VITE v5.x.x  ready in XXX ms

  ➜  Local:   http://localhost:3001/
  ➜  Network: use --host to expose
```

⚠️ **Laissez ce terminal ouvert aussi !**

---

## 🌐 Accéder à l'Application

Ouvrez votre navigateur sur :
```
http://localhost:3001
```

**Identifiants de connexion :**
- Email : `admin@credef.com`
- Mot de passe : `admin123`

---

## 📝 Script PowerShell Complet (Copier-Coller)

Vous pouvez copier-coller ces blocs de commandes directement !

### **Pour le Backend (Terminal 1)**

```powershell
# Navigation et démarrage
cd C:\Users\SAHINO\Desktop\test\FPMsigm\backend
python autoapp.py
```

### **Pour le Frontend (Terminal 2)**

```powershell
# Navigation et démarrage
cd C:\Users\SAHINO\Desktop\test\FPMsigm\frontend
npm run dev
```

---

## 🔄 Rituel Complet (Jour après jour)

### **Chaque fois que vous démarrez votre PC :**

#### **Étape 1 : Vérifier MySQL** (⏱️ 10 secondes)
```powershell
# Vérifier que MySQL tourne
Get-Service -Name MySQL*
```

Si MySQL n'est pas démarré :
```powershell
Start-Service -Name MySQL
```

#### **Étape 2 : Mise à jour du code** (⏱️ 30 secondes)
```powershell
# Aller dans le dossier du projet
cd C:\Users\SAHINO\Desktop\test\FPMsigm

# Récupérer les dernières modifications
git pull origin claude/dev-011CUiKQBZqunHCXf6VuqJof
```

#### **Étape 3 : Démarrer le Backend** (⏱️ 5 secondes)
```powershell
# Ouvrir Terminal 1
cd C:\Users\SAHINO\Desktop\test\FPMsigm\backend
python autoapp.py
```

Attendez de voir :
```
✅ * Running on http://127.0.0.1:5000
```

#### **Étape 4 : Démarrer le Frontend** (⏱️ 10 secondes)
```powershell
# Ouvrir Terminal 2 (NOUVEAU terminal)
cd C:\Users\SAHINO\Desktop\test\FPMsigm\frontend
npm run dev
```

Attendez de voir :
```
✅ ➜  Local:   http://localhost:3001/
```

#### **Étape 5 : Ouvrir le Navigateur** (⏱️ 5 secondes)
```
http://localhost:3001
```

**Temps total : ~1 minute** ⚡

---

## 🛠️ Commandes de Maintenance

### **Mettre à jour les dépendances Python**
```powershell
cd C:\Users\SAHINO\Desktop\test\FPMsigm\backend
pip install -r requirements.txt --upgrade
```

### **Mettre à jour les dépendances npm**
```powershell
cd C:\Users\SAHINO\Desktop\test\FPMsigm\frontend
npm install
```

### **Appliquer les migrations de base de données**
```powershell
cd C:\Users\SAHINO\Desktop\test\FPMsigm\backend
flask db upgrade
```

### **Vérifier l'état de la base de données**
```powershell
cd C:\Users\SAHINO\Desktop\test\FPMsigm\backend
python check_db.py
```

### **Tester l'authentification API**
```powershell
cd C:\Users\SAHINO\Desktop\test\FPMsigm\backend
python test_auth.py
```

---

## ⚠️ Résolution de Problèmes

### **Problème 1 : Port déjà utilisé**

**Backend (port 5000 occupé) :**
```
Error: Address already in use
```

**Solution :**
```powershell
# Trouver le processus qui utilise le port 5000
netstat -ano | findstr :5000

# Tuer le processus (remplacez PID par le numéro trouvé)
taskkill /PID <PID> /F
```

**Frontend (port 3001 occupé) :**
- Vite choisira automatiquement un autre port (3002, 3003, etc.)
- Utilisez simplement le port affiché dans le terminal

---

### **Problème 2 : Erreur "Module not found"**

**Python :**
```powershell
cd C:\Users\SAHINO\Desktop\test\FPMsigm\backend
pip install -r requirements.txt
```

**Node.js :**
```powershell
cd C:\Users\SAHINO\Desktop\test\FPMsigm\frontend
rm -rf node_modules package-lock.json
npm install
```

---

### **Problème 3 : MySQL ne démarre pas**

```powershell
# Vérifier le statut
Get-Service -Name MySQL*

# Redémarrer MySQL
Restart-Service -Name MySQL

# Si ça ne fonctionne toujours pas, vérifiez les logs MySQL
```

---

### **Problème 4 : "Can't connect to MySQL server"**

**Vérifications :**
1. MySQL est-il démarré ?
   ```powershell
   Get-Service -Name MySQL*
   ```

2. Les identifiants sont-ils corrects dans `.env` ?
   ```powershell
   cd C:\Users\SAHINO\Desktop\test\FPMsigm\backend
   cat .env
   ```

3. La base de données existe-t-elle ?
   ```sql
   mysql -u root -p
   SHOW DATABASES;
   ```

---

### **Problème 5 : Frontend ne se connecte pas au Backend**

**Vérifications :**
1. Le backend tourne-t-il sur http://127.0.0.1:5000 ?
2. Le fichier `frontend/.env` existe-t-il avec `VITE_API_URL=http://localhost:5000/api` ?
3. Y a-t-il des erreurs CORS dans la console du navigateur (F12) ?

**Solution :**
```powershell
# Recréer le fichier .env
cd C:\Users\SAHINO\Desktop\test\FPMsigm\frontend
"VITE_API_URL=http://localhost:5000/api" | Out-File -FilePath .env -Encoding UTF8

# Redémarrer le frontend
npm run dev
```

---

## 🧹 Arrêter l'Application

### **Méthode propre :**

**Backend (Terminal 1) :**
```
Appuyez sur CTRL + C
```

**Frontend (Terminal 2) :**
```
Appuyez sur CTRL + C
```

### **Méthode force (si bloqué) :**

```powershell
# Tuer tous les processus Python
taskkill /F /IM python.exe

# Tuer tous les processus Node
taskkill /F /IM node.exe
```

---

## 📊 Vérifier que Tout Fonctionne

### **Checklist de démarrage :**

```powershell
# 1. MySQL est démarré
Get-Service -Name MySQL*
# ✅ Status = Running

# 2. Backend répond
curl http://127.0.0.1:5000/api/auth/roles
# ✅ Retourne la liste des rôles

# 3. Frontend est accessible
# Ouvrir http://localhost:3001
# ✅ Page de connexion s'affiche

# 4. Connexion fonctionne
# Se connecter avec admin@credef.com / admin123
# ✅ Redirection vers le dashboard
```

---

## 🎯 Version Ultra-Rapide (Expert)

Pour les utilisateurs avancés qui connaissent déjà l'application :

**Terminal 1 :**
```powershell
cd C:\Users\SAHINO\Desktop\test\FPMsigm\backend && python autoapp.py
```

**Terminal 2 :**
```powershell
cd C:\Users\SAHINO\Desktop\test\FPMsigm\frontend && npm run dev
```

**Navigateur :**
```
http://localhost:3001
```

**⏱️ Temps total : 15 secondes !**

---

## 📝 Notes Importantes

1. **Toujours démarrer le Backend AVANT le Frontend**
   - Le frontend a besoin de l'API pour fonctionner

2. **Ne fermez pas les terminaux pendant que vous travaillez**
   - Le Backend doit rester actif
   - Le Frontend doit rester actif

3. **Le Frontend se recharge automatiquement**
   - Quand vous modifiez le code React
   - Pas besoin de redémarrer

4. **Le Backend ne se recharge PAS automatiquement**
   - Si vous modifiez le code Python
   - Redémarrez avec CTRL+C puis `python autoapp.py`

5. **Les logs sont vos amis**
   - Terminal Backend : voir les requêtes API
   - Terminal Frontend : voir les erreurs de compilation
   - Console navigateur (F12) : voir les erreurs JavaScript

---

## 🆘 Aide Supplémentaire

### **Documentation disponible :**
- `backend/GUIDE_TEST_AUTH.md` - Guide d'authentification
- `backend/check_db.py` - Script de vérification DB
- `backend/test_auth.py` - Script de test API
- `frontend/GUIDE_DEMARRAGE.md` - Guide frontend complet

### **Commandes de diagnostic :**
```powershell
# Vérifier Python
python --version

# Vérifier Node.js
node --version

# Vérifier npm
npm --version

# Vérifier MySQL
Get-Service -Name MySQL*

# Vérifier l'état git
cd C:\Users\SAHINO\Desktop\test\FPMsigm
git status
```

---

## ✅ Résumé des URLs

| Service | URL | Utilisation |
|---------|-----|-------------|
| **Frontend React** | http://localhost:3001 | Interface utilisateur - **UTILISEZ CELUI-CI** |
| **Backend API** | http://127.0.0.1:5000/api/* | API REST (utilisé par le frontend) |
| **Documentation Swagger** | ❌ Non configuré | - |
| **Base de données** | localhost:3306 | MySQL/MariaDB |

---

## 🎉 Vous êtes Prêt !

Suivez ces étapes et votre application FPMsigm sera opérationnelle en moins d'une minute !

**Bon développement ! 🚀**
