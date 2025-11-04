# FPMsigm Frontend

Interface utilisateur moderne pour la gestion des dossiers CREDEF.

## 🚀 Technologies

- **React 18** - Bibliothèque UI
- **TypeScript** - Typage statique
- **Vite** - Build tool ultra-rapide
- **Tailwind CSS** - Framework CSS utility-first
- **React Router** - Routing
- **Zustand** - State management
- **Axios** - HTTP client
- **Lucide React** - Icônes

## 📋 Prérequis

- Node.js 18+
- npm ou yarn
- Backend FPMsigm lancé sur http://localhost:5000

## 🔧 Installation

```bash
# Installer les dépendances
npm install

# Copier le fichier d'environnement
cp .env.example .env

# Lancer le serveur de développement
npm run dev
```

L'application sera disponible sur **http://localhost:3000**

## 🏗️ Structure du projet

```
frontend/
├── src/
│   ├── components/       # Composants réutilisables
│   │   └── Layout.tsx    # Layout principal avec navigation
│   ├── pages/            # Pages de l'application
│   │   ├── Login.tsx     # Page de connexion
│   │   ├── Dashboard.tsx # Dashboard avec KPIs
│   │   └── Dossiers.tsx  # Liste des dossiers
│   ├── services/         # Services API
│   │   └── api.ts        # Client API avec Axios
│   ├── stores/           # State management
│   │   └── authStore.ts  # Store d'authentification
│   ├── types/            # Types TypeScript
│   │   └── index.ts      # Interfaces et types
│   ├── App.tsx           # Composant principal + routing
│   ├── main.tsx          # Point d'entrée
│   └── index.css         # Styles globaux + Tailwind
├── index.html            # Template HTML
├── package.json          # Dépendances
├── tsconfig.json         # Configuration TypeScript
├── vite.config.ts        # Configuration Vite
└── tailwind.config.js    # Configuration Tailwind
```

## 🎨 Features Implémentées

### Authentification ✅
- Page de connexion avec validation
- Gestion JWT (access_token + refresh_token)
- Store Zustand pour l'état utilisateur
- Routes protégées avec redirection automatique
- Déconnexion

### Dashboard ✅
- KPIs en temps réel (Total, En cours, Validés, Clôturés)
- Liste des dossiers récents
- Design responsive

### Dossiers ✅
- Liste complète des dossiers
- Recherche par référence
- Filtre par statut
- Badges colorés selon le statut
- Table responsive

### Layout ✅
- Navigation sidebar responsive
- Header avec profil utilisateur
- Menu mobile avec overlay
- Déconnexion rapide

## 🔌 API Integration

Le frontend communique avec le backend via `src/services/api.ts` qui expose :

### Authentification
- `register(data)` - Créer un compte
- `login(credentials)` - Se connecter
- `getMe()` - Récupérer le profil
- `logout()` - Se déconnecter

### Dossiers
- `getDossiers(filters)` - Liste des dossiers
- `createDossier(data)` - Créer un dossier
- `transitionDossier(id, data)` - Changer le statut
- `getWorkflowHistory(id)` - Historique des transitions

### Pièces Jointes
- `uploadPiece(dossierId, file, ...)` - Upload
- `getPieces(dossierId)` - Liste des pièces
- `validateCompletude(dossierId)` - Vérifier complétude
- `deletePiece(pieceId)` - Supprimer

## 🎯 Commandes disponibles

```bash
# Développement
npm run dev

# Build de production
npm run build

# Preview du build
npm run preview

# Lint
npm run lint
```

## 🔐 Authentification

Le système utilise JWT avec stockage dans localStorage :
- `access_token` - Token d'accès
- `refresh_token` - Token de rafraîchissement
- `user` - Objet utilisateur

En cas de token expiré (401), l'utilisateur est automatiquement redirigé vers /login.

## 🎨 Customisation Tailwind

Les couleurs primaires sont définies dans `tailwind.config.js` :

```js
primary: {
  50: '#eff6ff',
  // ... jusqu'à 900
}
```

Classes CSS custom dans `src/index.css` :
- `.btn-primary` - Bouton primaire
- `.btn-secondary` - Bouton secondaire
- `.input-field` - Champ de saisie
- `.card` - Carte blanche avec ombre

## 📱 Responsive Design

L'interface est entièrement responsive avec breakpoints Tailwind :
- Mobile first
- Sidebar pliable sur mobile
- Tables scrollables horizontalement
- Grid adaptatif pour les KPIs

## 🚧 À venir

- [ ] Page de détail d'un dossier
- [ ] Formulaire de création de dossier
- [ ] Upload de pièces jointes avec drag & drop
- [ ] Kanban board pour le workflow
- [ ] Graphiques pour les statistiques
- [ ] Notifications temps réel
- [ ] Dark mode

## 🐛 Debugging

### Backend non accessible
Vérifier que le backend tourne sur http://localhost:5000

### CORS errors
Le backend doit autoriser l'origine http://localhost:3000

### Token expiré
Les tokens sont automatiquement supprimés et l'utilisateur redirigé vers /login

## 📄 Licence

[À définir]
