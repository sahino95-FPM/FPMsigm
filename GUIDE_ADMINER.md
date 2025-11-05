# 🗄️ Guide d'Installation et Utilisation d'Adminer

Adminer est une interface web légère (un seul fichier PHP) pour gérer votre base de données MySQL.

---

## 🎯 Qu'est-ce qu'Adminer ?

- ✅ **Léger** : Un seul fichier PHP (~500 KB)
- ✅ **Rapide** : Interface moderne et réactive
- ✅ **Complet** : Toutes les fonctionnalités essentielles
- ✅ **Alternative à phpMyAdmin** : Plus simple et plus rapide

---

## 📥 Installation Rapide

### **Méthode 1 : Installation Automatique (Recommandé)**

Je vais créer un script PowerShell qui fait tout automatiquement !

```powershell
# Aller dans le dossier du projet
cd C:\Users\SAHINO\Desktop\test\FPMsigm

# Créer un dossier adminer
mkdir adminer
cd adminer

# Télécharger Adminer
Invoke-WebRequest -Uri "https://github.com/vrana/adminer/releases/download/v4.8.1/adminer-4.8.1-mysql.php" -OutFile "adminer.php"

# Lancer Adminer sur le port 8080
php -S localhost:8080
```

**✅ C'est fait !** Adminer tourne maintenant sur http://localhost:8080/adminer.php

---

### **Méthode 2 : Installation Manuelle**

#### **Étape 1 : Télécharger Adminer**

1. Allez sur : https://www.adminer.org/
2. Cliquez sur **"Adminer 4.8.1 for MySQL"** (fichier ~500 KB)
3. Sauvegardez le fichier dans : `C:\Users\SAHINO\Desktop\test\FPMsigm\adminer\`
4. Renommez-le en `adminer.php`

#### **Étape 2 : Lancer le serveur PHP**

```powershell
# Aller dans le dossier adminer
cd C:\Users\SAHINO\Desktop\test\FPMsigm\adminer

# Démarrer le serveur web PHP intégré
php -S localhost:8080
```

**Vous devriez voir :**
```
[Tue Nov 05 XX:XX:XX 2025] PHP 8.x.x Development Server (http://localhost:8080) started
```

---

## 🌐 Se Connecter à la Base de Données

### **Étape 1 : Ouvrir Adminer**

Dans votre navigateur, allez sur :
```
http://localhost:8080/adminer.php
```

### **Étape 2 : Remplir le Formulaire de Connexion**

Vous verrez un formulaire de connexion. Remplissez avec :

```
Système:        MySQL
Serveur:        127.0.0.1  (ou localhost)
Utilisateur:    credef
Mot de passe:   credef
Base de données: credef
```

### **Étape 3 : Cliquer sur "Connexion"**

**🎉 Vous êtes connecté !**

---

## 🎨 Interface Adminer

Une fois connecté, vous verrez :

### **Menu de Gauche : Tables**
- `user` - Utilisateurs
- `credef_dossier` - Dossiers CREDEF
- `workflow_log` - Historique des transitions
- `piece_jointe` - Pièces jointes
- `alembic_version` - Versions des migrations

### **Panneau Principal : Actions Disponibles**
- **Afficher** - Voir les données d'une table
- **Modifier** - Éditer les données
- **Requête SQL** - Exécuter des requêtes personnalisées
- **Exporter** - Exporter en CSV, SQL, etc.
- **Importer** - Importer des données
- **Structure** - Voir la structure des tables

---

## 📊 Opérations Courantes

### **1. Voir tous les utilisateurs**

1. Cliquez sur **"user"** dans le menu de gauche
2. Cliquez sur **"Afficher"** (ou "Select data")
3. Vous verrez la liste de tous les utilisateurs

### **2. Voir tous les dossiers CREDEF**

1. Cliquez sur **"credef_dossier"** dans le menu de gauche
2. Cliquez sur **"Afficher"**
3. Vous verrez tous les dossiers avec leurs détails

### **3. Exécuter une Requête SQL Personnalisée**

1. Cliquez sur **"Requête SQL"** en haut
2. Entrez votre requête, par exemple :
   ```sql
   SELECT * FROM credef_dossier WHERE statut = 'BROUILLON'
   ```
3. Cliquez sur **"Exécuter"**

### **4. Exporter des Données**

1. Cliquez sur **"Exporter"** en haut
2. Choisissez :
   - **Format** : SQL, CSV, CSV (Excel), JSON
   - **Tables** : Toutes ou sélection
   - **Options** : Structure et/ou données
3. Cliquez sur **"Exporter"**

### **5. Voir la Structure d'une Table**

1. Cliquez sur une table (ex: "user")
2. Cliquez sur **"Modifier la table"** ou **"Structure"**
3. Vous verrez tous les champs et leurs types

---

## 🔍 Requêtes SQL Utiles dans Adminer

Cliquez sur **"Requête SQL"** et essayez ces requêtes :

### **Statistiques globales**
```sql
SELECT
    (SELECT COUNT(*) FROM user) as nb_users,
    (SELECT COUNT(*) FROM credef_dossier) as nb_dossiers,
    (SELECT COUNT(*) FROM workflow_log) as nb_transitions,
    (SELECT COUNT(*) FROM piece_jointe) as nb_pieces;
```

### **Dossiers par statut**
```sql
SELECT statut, COUNT(*) as nombre
FROM credef_dossier
GROUP BY statut
ORDER BY nombre DESC;
```

### **Derniers dossiers créés**
```sql
SELECT id, ref, statut, montant_demande, mois_traitement
FROM credef_dossier
ORDER BY id DESC
LIMIT 10;
```

### **Historique d'un dossier spécifique**
```sql
SELECT
    w.id,
    w.statut_from,
    w.statut_to,
    w.role,
    w.created_at
FROM workflow_log w
WHERE w.dossier_id = 1
ORDER BY w.created_at;
```

### **Chercher un dossier par référence**
```sql
SELECT * FROM credef_dossier
WHERE ref LIKE '%2025%';
```

---

## 🎯 Avantages d'Adminer

✅ **Léger** : Un seul fichier PHP
✅ **Rapide** : Chargement instantané
✅ **Complet** : Toutes les fonctionnalités essentielles
✅ **Moderne** : Interface claire et intuitive
✅ **Multi-DB** : Supporte MySQL, PostgreSQL, SQLite, etc.
✅ **Sécurisé** : Protection contre les injections SQL
✅ **Export facile** : CSV, SQL, JSON
✅ **Thèmes** : Interface personnalisable

---

## 🚫 Arrêter Adminer

Pour arrêter le serveur PHP :

```powershell
# Dans le terminal où Adminer tourne
# Appuyez sur CTRL + C
```

Le serveur s'arrête immédiatement.

---

## 🔒 Sécurité

### **Pour le Développement Local**
- ✅ Adminer tourne uniquement sur localhost (127.0.0.1)
- ✅ Accessible seulement depuis votre PC
- ✅ Pas besoin de configuration supplémentaire

### **Pour la Production (NE PAS FAIRE)**
- ❌ Ne jamais déployer Adminer sur un serveur accessible publiquement
- ❌ Ne pas utiliser en production sans authentification forte
- ❌ Supprimer adminer.php après utilisation si déployé

---

## 🛠️ Astuces et Raccourcis

### **Astuce 1 : Favoris**
- Vous pouvez **sauvegarder vos requêtes favorites**
- Cliquez sur l'étoile ⭐ à côté d'une requête

### **Astuce 2 : Navigation Rapide**
- **Alt + Flèche Gauche** : Page précédente
- **Alt + Flèche Droite** : Page suivante
- **Ctrl + Entrée** : Exécuter la requête SQL

### **Astuce 3 : Édition Rapide**
- Cliquez directement sur une cellule pour l'éditer
- Cliquez sur "Sauvegarder" pour valider

### **Astuce 4 : Filtres**
- Dans l'affichage d'une table, utilisez les filtres en haut
- Par exemple : `WHERE statut = 'BROUILLON'`

---

## 🐛 Résolution de Problèmes

### **Erreur : "php" n'est pas reconnu**

**Problème :** PHP n'est pas dans le PATH

**Solution :**
```powershell
# Trouver où Python a été installé (car Python inclut parfois PHP)
# Ou télécharger PHP depuis : https://windows.php.net/download/

# Ajouter PHP au PATH temporairement :
$env:Path += ";C:\chemin\vers\php"

# Puis relancer :
php -S localhost:8080
```

### **Erreur : "Connexion refusée"**

**Problème :** MySQL n'est pas démarré

**Solution :**
```powershell
# Vérifier MySQL
Get-Service -Name MySQL*

# Démarrer MySQL
Start-Service -Name MySQL
```

### **Erreur : "Access denied for user"**

**Problème :** Mauvais identifiants

**Solution :**
- Vérifiez les identifiants : `credef` / `credef`
- Vérifiez la base de données : `credef`

### **Port 8080 déjà utilisé**

**Solution :** Changer de port
```powershell
# Utiliser le port 8081 au lieu de 8080
php -S localhost:8081
```

Puis allez sur : http://localhost:8081/adminer.php

---

## 📱 Alternatives à Adminer

Si vous voulez essayer d'autres outils :

| Outil | Avantages | Installation |
|-------|-----------|-------------|
| **Adminer** | Léger, rapide | 1 fichier PHP |
| **phpMyAdmin** | Complet, populaire | Plus complexe |
| **MySQL Workbench** | Professionnel, GUI native | Installation Desktop |
| **DBeaver** | Multi-DB, moderne | Installation Desktop |
| **HeidiSQL** | Léger, Windows | Installation Desktop |

---

## 🎯 Résumé Rapide

### **Installation**
```powershell
cd C:\Users\SAHINO\Desktop\test\FPMsigm
mkdir adminer
cd adminer
Invoke-WebRequest -Uri "https://github.com/vrana/adminer/releases/download/v4.8.1/adminer-4.8.1-mysql.php" -OutFile "adminer.php"
php -S localhost:8080
```

### **Connexion**
```
URL:            http://localhost:8080/adminer.php
Système:        MySQL
Serveur:        127.0.0.1
Utilisateur:    credef
Mot de passe:   credef
Base:           credef
```

### **Arrêt**
```
CTRL + C dans le terminal
```

---

## ✅ Checklist

- [ ] PHP est installé (`php --version`)
- [ ] MySQL est démarré (`Get-Service -Name MySQL*`)
- [ ] Adminer est téléchargé dans le dossier `adminer/`
- [ ] Serveur PHP lancé (`php -S localhost:8080`)
- [ ] Navigateur ouvert sur http://localhost:8080/adminer.php
- [ ] Connecté avec les identifiants `credef` / `credef`

---

**Vous êtes prêt à explorer votre base de données avec Adminer ! 🎉**
