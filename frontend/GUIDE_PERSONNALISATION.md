# 🎨 Guide de Personnalisation du Design FPMsigm

Ce document explique comment personnaliser l'apparence de l'application FPMsigm.

---

## ✅ Modifications Appliquées

### 1. Couleur Principale : #006b01 (Vert FPM)

La couleur bleue a été remplacée par le vert FPM (#006b01) dans toute l'application.

**Fichiers modifiés :**
- `frontend/tailwind.config.js` - Configuration des couleurs Tailwind

**Palette de couleurs générée :**
```javascript
primary: {
  50: '#e6f5e6',   // Très clair
  100: '#c2e6c2',  // Clair
  200: '#9dd69d',
  300: '#78c678',
  400: '#53b653',
  500: '#2ea62e',
  600: '#006b01',  // ← Couleur principale FPM
  700: '#005501',  // Foncé
  800: '#004001',
  900: '#002a01',  // Très foncé
}
```

---

### 2. Police : Tahoma

La police par défaut est maintenant **Tahoma** sur toute l'application.

**Fichiers modifiés :**
- `frontend/tailwind.config.js` - Configuration de la police par défaut
- `frontend/src/index.css` - Application de la police sur tous les éléments

**Hiérarchie des polices :**
```css
font-family: 'Tahoma', Arial, sans-serif;
```

Si Tahoma n'est pas disponible, le navigateur utilisera Arial, puis une police sans-serif générique.

---

### 3. Logo FPM

Un composant Logo a été créé et ajouté sur toutes les pages.

**Fichiers créés/modifiés :**
- `frontend/src/components/Logo.tsx` - Composant Logo
- `frontend/src/components/Layout.tsx` - Logo dans l'en-tête
- `frontend/src/pages/Login.tsx` - Logo sur la page de connexion

**Emplacement du logo :**
- ✅ En-tête de toutes les pages (à côté de "FPMsigm")
- ✅ Page de connexion (au-dessus du titre)

---

## 🖼️ Comment Ajouter le Vrai Logo FPM

Actuellement, le logo est un **placeholder** (carré vert avec "FPM"). Voici comment le remplacer par le vrai logo :

### Étape 1 : Préparer votre Logo

**Formats recommandés :**
- **PNG** avec fond transparent (meilleure qualité)
- **SVG** (vectoriel, s'adapte à toutes les tailles)

**Taille recommandée :**
- Au moins **200x200 pixels**
- Format carré ou rectangulaire horizontal

### Étape 2 : Placer le Logo

Copiez votre fichier logo dans le dossier :
```
frontend/public/
```

Nommez-le par exemple :
- `logo-fpm.png`
- `logo-fpm.svg`

### Étape 3 : Modifier le Composant Logo

Ouvrez le fichier `frontend/src/components/Logo.tsx`

**Commentez le placeholder** (lignes 16-19) :
```tsx
{/* Placeholder pour le logo FPM */}
{/*
<div className={`${sizeClasses[size]} aspect-square bg-primary-600 rounded-lg flex items-center justify-center`}>
  <span className="text-white font-bold text-lg">FPM</span>
</div>
*/}
```

**Décommentez la balise image** (lignes 21-26) :
```tsx
<img
  src="/logo-fpm.png"
  alt="Logo FPM"
  className={`${sizeClasses[size]} object-contain`}
/>
```

**Ajustez le nom du fichier** selon votre logo :
```tsx
src="/logo-fpm.png"  // Pour PNG
src="/logo-fpm.svg"  // Pour SVG
```

### Étape 4 : Tester

1. Sauvegardez le fichier
2. Le frontend se recharge automatiquement (si `npm run dev` tourne)
3. Vérifiez que le logo s'affiche correctement
4. Testez sur différentes pages

---

## 🎨 Personnalisations Supplémentaires

### Changer la Couleur Principale

Si vous voulez une autre couleur que #006b01 :

**Fichier :** `frontend/tailwind.config.js`

```javascript
colors: {
  primary: {
    600: '#VOTRE_COULEUR',  // Remplacez par votre code couleur
    // Générez les autres teintes sur : https://uicolors.app/
  },
},
```

Utilisez cet outil pour générer toutes les teintes : https://uicolors.app/create

---

### Changer la Police

Pour utiliser une autre police :

**Fichier :** `frontend/tailwind.config.js`

```javascript
fontFamily: {
  sans: ['Nouvelle-Police', 'Arial', 'sans-serif'],
},
```

**Et dans :** `frontend/src/index.css`

```css
* {
  font-family: 'Nouvelle-Police', Arial, sans-serif;
}
```

**Polices disponibles par défaut sur Windows :**
- Arial
- Times New Roman
- Courier New
- Verdana
- Georgia
- Tahoma ← (actuellement utilisée)
- Trebuchet MS
- Comic Sans MS
- Impact

**Pour utiliser des polices Google Fonts :**

1. Allez sur https://fonts.google.com/
2. Sélectionnez votre police
3. Copiez le code `<link>` dans `frontend/index.html`
4. Utilisez le nom de la police dans la config

---

### Modifier le Titre de l'Application

**Fichier :** `frontend/index.html`

```html
<title>FPMsigm - Nouveau Titre</title>
```

---

### Changer le Favicon (Icône du Navigateur)

1. Créez un favicon.ico (16x16 ou 32x32 pixels)
2. Placez-le dans `frontend/public/favicon.ico`
3. Le navigateur le chargera automatiquement

---

## 🌈 Couleurs Utilisées dans l'Application

### Couleurs Principales (Vert FPM)

- **Background gradient login** : `from-primary-600 to-primary-800`
- **Boutons principaux** : `bg-primary-600 hover:bg-primary-700`
- **Texte principal** : `text-primary-600`
- **Fond actif (sidebar)** : `bg-primary-50 text-primary-700`

### Couleurs Secondaires

- **Fond de page** : `bg-gray-50`
- **Texte** : `text-gray-900`, `text-gray-700`, `text-gray-500`
- **Bordures** : `border-gray-200`
- **Hover** : `hover:bg-gray-50`

---

## 📱 Design Responsive

L'application est entièrement responsive et s'adapte à :
- 📱 Mobile (< 640px)
- 📱 Tablette (640px - 1024px)
- 💻 Desktop (> 1024px)

Le logo s'adapte automatiquement grâce aux tailles :
- `small` (h-8) - En-tête
- `medium` (h-12) - Par défaut
- `large` (h-16) - Page de connexion

---

## 🔄 Appliquer les Changements

### Si le serveur de développement tourne :

Les changements sont appliqués **automatiquement** (hot reload).

### Si le serveur ne tourne pas :

```powershell
cd frontend
npm run dev
```

### Pour un build de production :

```powershell
cd frontend
npm run build
```

Les fichiers sont générés dans `frontend/dist/`

---

## ✅ Checklist de Personnalisation

- [x] Couleur principale changée en #006b01
- [x] Police changée en Tahoma
- [x] Composant Logo créé
- [x] Logo ajouté dans l'en-tête
- [x] Logo ajouté sur la page de connexion
- [ ] Logo FPM réel ajouté (à faire)
- [ ] Favicon personnalisé (optionnel)

---

## 🎯 Résultat Visuel

### Page de Connexion
```
┌───────────────────────────────────────┐
│                                       │
│          [Logo FPM]                   │
│                                       │
│         FPMsigm                       │
│   Gestion des dossiers CREDEF         │
│                                       │
│  ┌─────────────────────────────────┐ │
│  │      Connexion                  │ │
│  │                                 │ │
│  │  Email: [________________]      │ │
│  │  Pass:  [________________]      │ │
│  │                                 │ │
│  │  [Se connecter] (vert #006b01)  │ │
│  └─────────────────────────────────┘ │
│                                       │
└───────────────────────────────────────┘
```

### En-tête de l'Application
```
┌────────────────────────────────────────────────────┐
│ [FPM] FPMsigm            User Name    [👤] [⎋]   │
└────────────────────────────────────────────────────┘
```

---

## 📞 Support

Si vous rencontrez des problèmes :

1. Vérifiez que tous les fichiers sont bien modifiés
2. Redémarrez le serveur de développement (`npm run dev`)
3. Videz le cache du navigateur (Ctrl + Shift + R)
4. Vérifiez la console pour les erreurs (F12)

---

**Votre application FPMsigm est maintenant personnalisée avec les couleurs et le style FPM ! 🎉**
