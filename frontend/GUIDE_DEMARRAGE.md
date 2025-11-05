# 🚀 Guide de Démarrage du Frontend React

Ce guide vous aide à démarrer l'application frontend React de FPMsigm.

## 📋 Prérequis

- **Node.js** version 18 ou supérieure
- **npm** version 9 ou supérieure
- Le **backend Flask** doit être en cours d'exécution sur http://127.0.0.1:5000

## ⚙️ Technologies utilisées

- **React 18** - Framework UI
- **TypeScript** - Typage statique
- **Vite** - Build tool et dev server ultra-rapide
- **React Router** - Navigation
- **Zustand** - State management
- **Axios** - Client HTTP
- **Tailwind CSS** - Framework CSS
- **Lucide React** - Icônes
- **React Hook Form** - Gestion de formulaires
- **date-fns** - Manipulation de dates

## 🛠️ Installation

### Étape 1 : Vérifier Node.js

```powershell
node --version
npm --version
```

Vous devriez voir :
```
v18.x.x ou supérieur
9.x.x ou supérieur
```

### Étape 2 : Installer les dépendances

```powershell
cd C:\Users\SAHINO\Desktop\test\FPMsigm\frontend
npm install
```

Cette commande va installer toutes les dépendances listées dans `package.json`.

### Étape 3 : Vérifier la configuration

Le fichier `.env` a été créé automatiquement avec :

```env
VITE_API_URL=http://localhost:5000/api
```

Cette variable indique au frontend où se trouve le backend.

## 🚀 Démarrage

### Terminal 1 : Backend Flask (doit déjà tourner)

```powershell
cd C:\Users\SAHINO\Desktop\test\FPMsigm\backend
python autoapp.py
```

Vous devriez voir :
```
 * Running on http://127.0.0.1:5000
```

### Terminal 2 : Frontend React

```powershell
cd C:\Users\SAHINO\Desktop\test\FPMsigm\frontend
npm run dev
```

Vous devriez voir :

```
  VITE v5.0.8  ready in XXX ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h to show help
```

## 🌐 Accéder à l'application

Ouvrez votre navigateur et allez sur :

```
http://localhost:5173
```

Vous serez redirigé vers la page de connexion.

## 🔐 Se connecter

Utilisez les identifiants de l'utilisateur admin créé précédemment :

- **Email** : `admin@credef.com`
- **Mot de passe** : `admin123`

## 📂 Structure du Frontend

```
frontend/
├── src/
│   ├── components/         # Composants réutilisables
│   │   ├── Layout.tsx      # Layout principal avec navigation
│   │   ├── StatusBadge.tsx # Badge de statut
│   │   ├── WorkflowHistory.tsx  # Historique des transitions
│   │   ├── PiecesJointes.tsx    # Gestion des pièces jointes
│   │   └── TransitionModal.tsx  # Modal de transition
│   ├── pages/              # Pages de l'application
│   │   ├── Login.tsx       # Page de connexion
│   │   ├── Dashboard.tsx   # Tableau de bord
│   │   ├── Dossiers.tsx    # Liste des dossiers
│   │   └── DossierDetail.tsx # Détails d'un dossier
│   ├── services/           # Services API
│   │   └── api.ts          # Client API Axios
│   ├── stores/             # State management
│   │   └── authStore.ts    # Store d'authentification
│   ├── types/              # Types TypeScript
│   │   └── index.ts        # Définitions de types
│   ├── App.tsx             # Composant racine
│   └── main.tsx            # Point d'entrée
├── .env                    # Variables d'environnement
├── package.json            # Dépendances et scripts
├── vite.config.ts          # Configuration Vite
├── tailwind.config.js      # Configuration Tailwind
└── tsconfig.json           # Configuration TypeScript
```

## 🎨 Fonctionnalités de l'Interface

### 1. Page de Connexion
- Formulaire email/mot de passe
- Validation en temps réel
- Gestion des erreurs
- Design moderne avec Tailwind CSS

### 2. Dashboard
- Vue d'ensemble des dossiers
- Statistiques par statut
- Accès rapide aux fonctionnalités

### 3. Gestion des Dossiers
- Liste des dossiers avec filtres
- Création de nouveaux dossiers
- Détails et historique
- Transitions de workflow

### 4. Pièces Jointes
- Upload de fichiers
- Validation de complétude
- Téléchargement
- Suppression

## 🔧 Scripts Disponibles

### Développement
```powershell
npm run dev
```
Lance le serveur de développement avec hot-reload sur http://localhost:5173

### Build Production
```powershell
npm run build
```
Compile l'application pour la production dans le dossier `dist/`

### Preview Production
```powershell
npm run preview
```
Prévisualise le build de production localement

### Lint
```powershell
npm run lint
```
Vérifie le code avec ESLint

## 🔍 Débogage

### Le frontend ne se connecte pas au backend

**Vérifiez que :**
1. Le backend tourne sur http://127.0.0.1:5000
2. Le fichier `.env` contient `VITE_API_URL=http://localhost:5000/api`
3. Pas de CORS errors dans la console du navigateur

**Solution :** Le backend Flask a déjà CORS activé pour accepter les requêtes depuis n'importe quelle origine.

### Erreur "Cannot find module"

```powershell
# Supprimez node_modules et réinstallez
rm -rf node_modules package-lock.json
npm install
```

### Erreur de connexion 401 Unauthorized

**Cause :** Token JWT expiré ou invalide

**Solution :**
1. Ouvrez les DevTools du navigateur (F12)
2. Allez dans Application > Local Storage
3. Supprimez les clés `access_token`, `refresh_token`, et `user`
4. Rechargez la page et reconnectez-vous

### CORS Policy Error

Si vous voyez une erreur CORS dans la console :

```
Access to XMLHttpRequest at 'http://localhost:5000/api/auth/login' from origin
'http://localhost:5173' has been blocked by CORS policy
```

**Solution :** Vérifiez que le backend a bien Flask-CORS configuré (déjà fait dans notre cas).

## 🌐 URLs de l'API

Le frontend communique avec ces endpoints :

### Authentification
- `POST /api/auth/register` - Créer un compte
- `POST /api/auth/login` - Se connecter
- `GET /api/auth/me` - Obtenir l'utilisateur connecté
- `GET /api/auth/roles` - Liste des rôles

### Dossiers CREDEF
- `GET /api/credef/dossiers` - Liste des dossiers
- `POST /api/credef/dossiers` - Créer un dossier
- `POST /api/credef/dossiers/:id/transition` - Changer le statut
- `GET /api/credef/dossiers/:id/workflow` - Historique

### Pièces Jointes
- `POST /api/credef/dossiers/:id/pieces` - Upload
- `GET /api/credef/dossiers/:id/pieces` - Liste
- `GET /api/credef/dossiers/:id/pieces/validation` - Validation
- `DELETE /api/credef/pieces/:id` - Supprimer

## 🎯 Tester l'Application

### 1. Connexion
- Allez sur http://localhost:5173
- Connectez-vous avec admin@credef.com / admin123
- Vous devriez être redirigé vers le dashboard

### 2. Créer un Dossier
- Cliquez sur "Nouveau dossier"
- Remplissez le formulaire
- Le dossier est créé avec le statut "BROUILLON"

### 3. Transitions de Workflow
- Ouvrez un dossier
- Cliquez sur "Changer le statut"
- Sélectionnez un nouveau statut
- Ajoutez une note
- Validez

### 4. Upload de Pièces Jointes
- Dans un dossier
- Section "Pièces jointes"
- Cliquez sur "Ajouter une pièce"
- Sélectionnez un fichier
- Choisissez le type
- Upload

## 📝 Configuration Avancée

### Changer le port du frontend

Modifiez `vite.config.ts` :

```typescript
export default defineConfig({
  server: {
    port: 3000, // au lieu de 5173
  },
  // ...
})
```

### Activer HTTPS en développement

```typescript
export default defineConfig({
  server: {
    https: true,
  },
  // ...
})
```

## 🚨 Problèmes Courants

### Port 5173 déjà utilisé

```powershell
# Vite choisira automatiquement le prochain port disponible (5174, 5175, etc.)
npm run dev
```

### Build échoue avec des erreurs TypeScript

```powershell
# Vérifiez les types
npm run lint

# Si nécessaire, ignorez temporairement les erreurs de type (pas recommandé)
npm run build -- --no-type-check
```

## ✅ Checklist de Démarrage

- [ ] Node.js et npm installés
- [ ] Backend Flask en cours d'exécution sur http://127.0.0.1:5000
- [ ] Dépendances npm installées (`npm install`)
- [ ] Fichier `.env` créé avec `VITE_API_URL=http://localhost:5000/api`
- [ ] Frontend démarré (`npm run dev`)
- [ ] Navigateur ouvert sur http://localhost:5173
- [ ] Connexion réussie avec admin@credef.com / admin123

---

**Profitez de votre application FPMsigm ! 🎉**
