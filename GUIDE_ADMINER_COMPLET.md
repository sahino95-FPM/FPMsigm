# 🗄️ Guide Complet Adminer pour FPMsigm

Guide pratique pour gérer votre base de données MySQL avec Adminer.

---

## 📖 Table des Matières

1. [Introduction](#introduction)
2. [Installation en 3 Minutes](#installation)
3. [Première Connexion](#premiere-connexion)
4. [Tutoriels Pas à Pas](#tutoriels)
5. [Cas d'Usage Spécifiques](#cas-dusage)
6. [Requêtes SQL Essentielles](#requetes-sql)
7. [Export et Backup](#export-backup)
8. [Dépannage](#depannage)
9. [Astuces et Raccourcis](#astuces)

---

## 🎯 Introduction {#introduction}

### Qu'est-ce qu'Adminer ?

Adminer est une **interface web légère** pour gérer votre base de données MySQL. C'est une alternative moderne et plus simple que phpMyAdmin.

**Avantages :**
- ✅ **Un seul fichier** (~500 KB)
- ✅ **Rapide** et réactif
- ✅ **Interface moderne** et intuitive
- ✅ **Toutes les fonctionnalités** essentielles
- ✅ **Sans installation** complexe

### Pourquoi utiliser Adminer pour FPMsigm ?

Avec Adminer, vous pouvez :
- 👀 **Voir** tous vos utilisateurs et dossiers
- 🔍 **Rechercher** des données spécifiques
- ✏️ **Modifier** des enregistrements
- 📊 **Analyser** les statistiques
- 💾 **Exporter** vos données
- 🔧 **Déboguer** l'application

---

## ⚡ Installation en 3 Minutes {#installation}

### Prérequis

Avant de commencer, vérifiez que vous avez :
- ✅ PHP installé (`php --version`)
- ✅ MySQL/MariaDB en cours d'exécution
- ✅ Les identifiants de la base (credef/credef)

### Méthode Ultra-Rapide (Recommandé)

**Étape 1 : Récupérer les scripts**

```powershell
cd C:\Users\SAHINO\Desktop\test\FPMsigm
git pull
```

**Étape 2 : Lancer Adminer**

Double-cliquez sur le fichier :
```
start_adminer.bat
```

**Étape 3 : Ouvrir le navigateur**

Allez sur :
```
http://localhost:8080/adminer.php
```

**✅ C'est fait ! Adminer est prêt !**

---

### Méthode Manuelle (Alternative)

Si le script ne fonctionne pas, suivez ces étapes :

**Étape 1 : Créer le dossier**

```powershell
cd C:\Users\SAHINO\Desktop\test\FPMsigm
mkdir adminer
cd adminer
```

**Étape 2 : Télécharger Adminer**

```powershell
Invoke-WebRequest -Uri "https://github.com/vrana/adminer/releases/download/v4.8.1/adminer-4.8.1-mysql.php" -OutFile "adminer.php"
```

Ou téléchargez manuellement depuis : https://www.adminer.org/

**Étape 3 : Lancer le serveur PHP**

```powershell
php -S localhost:8080
```

**Étape 4 : Ouvrir le navigateur**

```
http://localhost:8080/adminer.php
```

---

## 🔐 Première Connexion {#premiere-connexion}

### Page de Connexion

Quand vous ouvrez http://localhost:8080/adminer.php, vous voyez un formulaire.

**Remplissez avec ces informations :**

```
┌─────────────────────────────────────┐
│ Système:        [MySQL        ▼]   │
│ Serveur:        [127.0.0.1       ]  │
│ Utilisateur:    [credef          ]  │
│ Mot de passe:   [credef          ]  │
│ Base de données:[credef          ]  │
│                                      │
│          [Se connecter]              │
└─────────────────────────────────────┘
```

**Cliquez sur "Se connecter"** (ou "Connexion" selon la langue)

### Interface Principale

Après connexion, vous voyez :

```
┌─────────────────────────────────────────────────┐
│ Adminer         [Base: credef ▼]    Déconnexion│
├──────────────┬──────────────────────────────────┤
│              │                                   │
│ Tables:      │ Sélectionner une table           │
│              │                                   │
│ ☐ user       │ Tables de la base credef:        │
│ ☐ credef_... │                                   │
│ ☐ workflow...│ - user                           │
│ ☐ piece_j... │ - credef_dossier                 │
│              │ - workflow_log                   │
│              │ - piece_jointe                   │
│              │ - alembic_version                │
│              │                                   │
└──────────────┴──────────────────────────────────┘
```

**Menu de gauche :** Liste des tables
**Panneau principal :** Actions et données

---

## 📚 Tutoriels Pas à Pas {#tutoriels}

### Tutoriel 1 : Voir tous les utilisateurs

**Objectif :** Consulter la liste des utilisateurs de l'application

**Étapes :**

1. **Cliquer sur "user"** dans le menu de gauche
2. **Cliquer sur "Afficher"** (ou "Select data")
3. **Voir le résultat** : Tableau avec tous les utilisateurs

**Ce que vous voyez :**

```
┌────┬──────────────────────┬────────┬──────────┬────────┬───────────┐
│ id │ email                │ nom    │ prenom   │ role   │ is_active │
├────┼──────────────────────┼────────┼──────────┼────────┼───────────┤
│ 1  │ admin@credef.com     │ Admin  │ Systeme  │ ADMIN  │ 1         │
└────┴──────────────────────┴────────┴──────────┴────────┴───────────┘
```

**Actions possibles :**
- 👁️ Cliquer sur "modifier" pour éditer un utilisateur
- ➕ Cliquer sur "Nouvel enregistrement" pour créer un utilisateur
- 🗑️ Cocher et supprimer des utilisateurs

---

### Tutoriel 2 : Consulter les dossiers CREDEF

**Objectif :** Voir tous les dossiers créés dans l'application

**Étapes :**

1. **Cliquer sur "credef_dossier"** dans le menu de gauche
2. **Cliquer sur "Afficher"**
3. **Parcourir les résultats**

**Ce que vous voyez :**

```
┌────┬─────────────────┬────────────┬──────────────────┬─────────────┐
│ id │ ref             │ statut     │ montant_demande  │ duree_mois  │
├────┼─────────────────┼────────────┼──────────────────┼─────────────┤
│ 1  │ CREDEF-2025-001 │ BROUILLON  │ 50000.00         │ 24          │
│ 2  │ CREDEF-2025-002 │ DÉPOSÉ     │ 75000.00         │ 36          │
└────┴─────────────────┴────────────┴──────────────────┴─────────────┘
```

**Astuces :**
- 🔍 Utilisez la barre de recherche en haut pour filtrer
- 📊 Cliquez sur les en-têtes de colonnes pour trier
- 📄 Changez le nombre de lignes affichées (10, 50, 100...)

---

### Tutoriel 3 : Chercher un dossier spécifique

**Objectif :** Trouver un dossier par sa référence

**Méthode 1 : Avec le filtre (Simple)**

1. Cliquer sur "credef_dossier"
2. Cliquer sur "Afficher"
3. Dans la zone de filtre en haut, taper :
   ```
   WHERE ref = 'CREDEF-2025-001'
   ```
4. Cliquer sur "Afficher"

**Méthode 2 : Avec SQL (Flexible)**

1. Cliquer sur **"Requête SQL"** en haut
2. Taper :
   ```sql
   SELECT * FROM credef_dossier
   WHERE ref LIKE '%2025%'
   ORDER BY id DESC;
   ```
3. Cliquer sur **"Exécuter"**

**Résultat :** Tous les dossiers contenant "2025" dans la référence

---

### Tutoriel 4 : Voir l'historique d'un dossier

**Objectif :** Consulter toutes les transitions d'un dossier

**Étapes :**

1. **Trouver l'ID du dossier** (ex: dossier #1)
2. Cliquer sur **"Requête SQL"**
3. Taper cette requête :
   ```sql
   SELECT
       w.id,
       w.statut_from AS 'De',
       w.statut_to AS 'Vers',
       w.role,
       w.commentaire,
       w.created_at AS 'Date'
   FROM workflow_log w
   WHERE w.dossier_id = 1
   ORDER BY w.created_at;
   ```
4. Cliquer sur **"Exécuter"**

**Résultat :**

```
┌────┬────────────┬─────────────┬────────┬──────────────┬─────────────────────┐
│ id │ De         │ Vers        │ role   │ commentaire  │ Date                │
├────┼────────────┼─────────────┼────────┼──────────────┼─────────────────────┤
│ 1  │ NULL       │ BROUILLON   │ ADMIN  │ Création     │ 2025-11-05 10:00:00 │
│ 2  │ BROUILLON  │ DÉPOSÉ      │ SACV   │ Validé       │ 2025-11-05 11:30:00 │
└────┴────────────┴─────────────┴────────┴──────────────┴─────────────────────┘
```

---

### Tutoriel 5 : Modifier un utilisateur

**Objectif :** Changer le rôle d'un utilisateur

**⚠️ ATTENTION :** Soyez prudent lors des modifications !

**Étapes :**

1. Cliquer sur **"user"**
2. Cliquer sur **"Afficher"**
3. Sur la ligne de l'utilisateur, cliquer sur **"modifier"**
4. Modifier le champ **"role"** (ex: SACV → ADMIN)
5. Cliquer sur **"Sauvegarder"**

**Vérification :**
- Rafraîchissez la page
- Le rôle devrait être changé
- Connectez-vous à l'application pour tester

---

### Tutoriel 6 : Créer un nouvel utilisateur

**Objectif :** Ajouter un utilisateur via Adminer

**Étapes :**

1. Cliquer sur **"user"**
2. Cliquer sur **"Nouvel enregistrement"**
3. Remplir le formulaire :
   ```
   email:         sacv@credef.com
   nom:           Service
   prenom:        SACV
   password_hash: (voir note ci-dessous)
   role:          SACV
   is_active:     1
   ```

**⚠️ Note sur le mot de passe :**

Le mot de passe doit être hashé ! Utilisez plutôt l'API ou Python :

```python
from werkzeug.security import generate_password_hash
hash = generate_password_hash("motdepasse123")
print(hash)
```

**Alternative recommandée :** Créez les utilisateurs via l'API (`/api/auth/register`) ou le frontend.

---

### Tutoriel 7 : Supprimer un dossier

**Objectif :** Supprimer un dossier de test

**⚠️ DANGER :** La suppression est PERMANENTE !

**Étapes :**

1. **D'abord, supprimer les données liées** (très important !)

   ```sql
   -- Requête SQL pour tout supprimer en ordre
   DELETE FROM piece_jointe WHERE dossier_id = 1;
   DELETE FROM workflow_log WHERE dossier_id = 1;
   DELETE FROM credef_dossier WHERE id = 1;
   ```

2. Aller dans **"Requête SQL"**
3. Coller les requêtes ci-dessus
4. Remplacer `1` par l'ID du dossier à supprimer
5. Cliquer sur **"Exécuter"**

**Vérification :**
```sql
SELECT * FROM credef_dossier WHERE id = 1;
```
Résultat : Aucune ligne (le dossier est supprimé)

---

## 💼 Cas d'Usage Spécifiques {#cas-dusage}

### Cas 1 : Vérifier qu'un dossier a été créé

**Situation :** Vous créez un dossier via le frontend, vous voulez vérifier qu'il est en base.

**Solution :**

```sql
-- Voir les 5 derniers dossiers créés
SELECT id, ref, statut, created_at
FROM credef_dossier
ORDER BY id DESC
LIMIT 5;
```

---

### Cas 2 : Compter les dossiers par statut

**Situation :** Vous voulez des statistiques sur les dossiers.

**Solution :**

```sql
SELECT
    statut,
    COUNT(*) as nombre,
    SUM(montant_demande) as montant_total
FROM credef_dossier
GROUP BY statut
ORDER BY nombre DESC;
```

**Résultat :**

```
┌──────────────────────┬────────┬────────────────┐
│ statut               │ nombre │ montant_total  │
├──────────────────────┼────────┼────────────────┤
│ BROUILLON            │ 15     │ 750000.00      │
│ DÉPOSÉ               │ 8      │ 400000.00      │
│ EN_CONTROLE_SACV     │ 3      │ 150000.00      │
│ CLOS                 │ 2      │ 100000.00      │
└──────────────────────┴────────┴────────────────┘
```

---

### Cas 3 : Trouver les dossiers sans pièces jointes

**Situation :** Vous cherchez les dossiers incomplets.

**Solution :**

```sql
SELECT
    d.id,
    d.ref,
    d.statut,
    COUNT(p.id) as nb_pieces
FROM credef_dossier d
LEFT JOIN piece_jointe p ON d.id = p.dossier_id
GROUP BY d.id, d.ref, d.statut
HAVING nb_pieces = 0;
```

---

### Cas 4 : Voir l'activité récente

**Situation :** Vous voulez voir les dernières actions sur les dossiers.

**Solution :**

```sql
SELECT
    d.ref as dossier,
    w.statut_from as de,
    w.statut_to as vers,
    w.role,
    w.created_at as date
FROM workflow_log w
JOIN credef_dossier d ON w.dossier_id = d.id
ORDER BY w.created_at DESC
LIMIT 20;
```

---

### Cas 5 : Réinitialiser un dossier à BROUILLON

**Situation :** Un dossier est dans un mauvais état, vous voulez le remettre en BROUILLON.

**Solution :**

```sql
-- Méthode 1 : Simple
UPDATE credef_dossier
SET statut = 'BROUILLON'
WHERE id = 1;

-- Méthode 2 : Avec vérification
UPDATE credef_dossier
SET statut = 'BROUILLON',
    commentaire_rejet = 'Remis à zéro pour test'
WHERE id = 1 AND statut != 'CLOS';
```

---

### Cas 6 : Exporter les dossiers d'un mois

**Situation :** Vous voulez exporter tous les dossiers de novembre 2025.

**Solution :**

```sql
SELECT
    ref,
    adherent_id,
    statut,
    montant_demande,
    duree_mois,
    taux,
    mois_traitement
FROM credef_dossier
WHERE mois_traitement = '2025-11'
ORDER BY ref;
```

Puis **Exporter** en CSV :
1. Exécuter la requête
2. Cliquer sur **"Exporter"** en bas
3. Choisir **"CSV"**
4. Télécharger

---

## 📊 Requêtes SQL Essentielles {#requetes-sql}

### Vue d'Ensemble Rapide

```sql
-- Tableau de bord complet
SELECT
    'Utilisateurs' as categorie,
    COUNT(*) as total,
    COUNT(CASE WHEN is_active = 1 THEN 1 END) as actifs
FROM user

UNION ALL

SELECT
    'Dossiers' as categorie,
    COUNT(*) as total,
    COUNT(CASE WHEN statut = 'CLOS' THEN 1 END) as clos
FROM credef_dossier

UNION ALL

SELECT
    'Transitions' as categorie,
    COUNT(*) as total,
    COUNT(DISTINCT dossier_id) as dossiers_avec_historique
FROM workflow_log

UNION ALL

SELECT
    'Pièces jointes' as categorie,
    COUNT(*) as total,
    SUM(taille_octets) / 1024 / 1024 as taille_mb
FROM piece_jointe;
```

---

### Recherches Avancées

**Dossiers avec montant > 50000 €**
```sql
SELECT * FROM credef_dossier
WHERE montant_demande > 50000
ORDER BY montant_demande DESC;
```

**Dossiers créés cette semaine**
```sql
SELECT * FROM credef_dossier
WHERE created_at >= DATE_SUB(NOW(), INTERVAL 7 DAY)
ORDER BY created_at DESC;
```

**Utilisateurs par rôle**
```sql
SELECT
    role,
    COUNT(*) as nombre,
    GROUP_CONCAT(email SEPARATOR ', ') as emails
FROM user
GROUP BY role;
```

**Pièces jointes manquantes (types obligatoires)**
```sql
SELECT
    d.id,
    d.ref,
    COUNT(p.id) as pieces_actuelles
FROM credef_dossier d
LEFT JOIN piece_jointe p ON d.id = p.dossier_id
GROUP BY d.id, d.ref
HAVING pieces_actuelles < 5;  -- Si 5 pièces obligatoires
```

---

### Modifications en Masse

**⚠️ DANGER : Testez d'abord avec SELECT !**

**Désactiver tous les utilisateurs sauf admin**
```sql
-- TEST d'abord :
SELECT id, email, is_active FROM user
WHERE role != 'ADMIN';

-- Puis exécuter :
UPDATE user
SET is_active = 0
WHERE role != 'ADMIN';
```

**Mettre à jour le mois de traitement**
```sql
-- TEST :
SELECT id, ref, mois_traitement FROM credef_dossier
WHERE mois_traitement IS NULL;

-- Exécution :
UPDATE credef_dossier
SET mois_traitement = '2025-11'
WHERE mois_traitement IS NULL;
```

---

## 💾 Export et Backup {#export-backup}

### Exporter une Table en CSV

1. Afficher la table (ex: credef_dossier)
2. Cliquer sur **"Exporter"** en bas
3. Choisir :
   - **Format** : CSV
   - **Sortie** : save
   - **Format** : CSV (ou CSV avec point-virgule pour Excel)
4. Cliquer sur **"Exporter"**

**Fichier téléchargé :** `credef_dossier.csv`

---

### Exporter toute la Base en SQL

1. Ne sélectionner aucune table (écran d'accueil)
2. Cliquer sur **"Exporter"** en haut
3. Choisir :
   - **Sortie** : save
   - **Format** : SQL
   - **Base de données** : ☑
   - **Tables** : ☑ Tout sélectionner
   - **Données** : ☑ INSERT
4. Cliquer sur **"Exporter"**

**Fichier téléchargé :** `credef-YYYY-MM-DD.sql`

---

### Importer des Données

**⚠️ Attention :** Cela peut écraser des données existantes !

1. Cliquer sur **"Importer"** en haut
2. Cliquer sur **"Choisir un fichier"**
3. Sélectionner votre fichier SQL ou CSV
4. Cliquer sur **"Exécuter"**

---

### Backup Complet via Ligne de Commande

**Plus sûr et plus rapide :**

```powershell
# Backup complet
mysqldump -u credef -pcredef credef > backup_$(Get-Date -Format 'yyyy-MM-dd_HHmmss').sql

# Backup d'une seule table
mysqldump -u credef -pcredef credef credef_dossier > backup_dossiers.sql

# Restaurer un backup
mysql -u credef -pcredef credef < backup_2025-11-05.sql
```

---

## 🔧 Dépannage {#depannage}

### Problème : "PHP command not found"

**Cause :** PHP n'est pas installé ou pas dans le PATH

**Solution :**

1. Vérifier l'installation :
   ```powershell
   php --version
   ```

2. Si erreur, installer PHP :
   - Télécharger : https://windows.php.net/download/
   - Extraire dans `C:\php`
   - Ajouter au PATH

3. Ou utiliser Python à la place :
   ```powershell
   cd adminer
   python -m http.server 8080
   # Puis aller sur http://localhost:8080/adminer.php
   ```

---

### Problème : "Connexion refusée"

**Cause :** MySQL n'est pas démarré

**Solution :**

```powershell
# Vérifier MySQL
Get-Service -Name MySQL*

# Démarrer MySQL
Start-Service -Name MySQL

# Si toujours une erreur, redémarrer
Restart-Service -Name MySQL
```

---

### Problème : "Access denied for user 'credef'"

**Cause :** Mauvais identifiants ou permissions

**Solution :**

1. Vérifier les identifiants dans `backend/.env`
2. Se connecter en root pour réinitialiser :
   ```sql
   mysql -u root -p
   CREATE USER 'credef'@'localhost' IDENTIFIED BY 'credef';
   GRANT ALL PRIVILEGES ON credef.* TO 'credef'@'localhost';
   FLUSH PRIVILEGES;
   ```

---

### Problème : "Unknown database 'credef'"

**Cause :** La base de données n'existe pas

**Solution :**

```sql
mysql -u root -p
CREATE DATABASE credef CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
SHOW DATABASES;
```

Puis appliquer les migrations :
```powershell
cd backend
flask db upgrade
```

---

### Problème : Port 8080 déjà utilisé

**Solution :** Changer de port

```powershell
php -S localhost:8081
# Puis aller sur http://localhost:8081/adminer.php
```

---

### Problème : Erreur lors d'une requête SQL

**Cause courante :** Erreur de syntaxe

**Solutions :**

1. Vérifier les points-virgules `;` à la fin
2. Vérifier les guillemets (simples ' pour les valeurs)
3. Vérifier les noms de tables et colonnes
4. Tester avec une requête simple d'abord :
   ```sql
   SELECT * FROM user LIMIT 1;
   ```

---

## 💡 Astuces et Raccourcis {#astuces}

### Raccourcis Clavier

- **Ctrl + Entrée** : Exécuter la requête SQL
- **Alt + ←** : Page précédente
- **Alt + →** : Page suivante
- **Échap** : Annuler une action

---

### Sauvegarder vos Requêtes Favorites

1. Exécuter une requête SQL
2. Cliquer sur l'étoile ⭐ à côté de la requête
3. Donner un nom (ex: "Stats mensuelles")
4. La requête est sauvegardée !

Pour la réutiliser :
- Cliquer sur **"Requête SQL"**
- Choisir dans la liste déroulante

---

### Édition Rapide

**Dans l'affichage d'une table :**
- Cliquer directement sur une cellule pour l'éditer
- Appuyer sur **Tab** pour passer à la cellule suivante
- Cliquer sur **"Sauvegarder"** en bas

---

### Filtrage Avancé

Dans l'affichage d'une table, utilisez les opérateurs :

```
=          Égal
!=         Différent
>          Supérieur
>=         Supérieur ou égal
<          Inférieur
<=         Inférieur ou égal
LIKE       Contient (utiliser % comme joker)
IS NULL    Est vide
IS NOT NULL Est non vide
```

**Exemples :**

```
WHERE statut = 'BROUILLON'
WHERE montant_demande > 50000
WHERE ref LIKE '%2025%'
WHERE adherent_id IS NOT NULL
```

---

### Copier des Résultats

Pour copier les résultats d'une requête :
1. Exécuter la requête
2. **Ctrl + A** (tout sélectionner)
3. **Ctrl + C** (copier)
4. Coller dans Excel ou un éditeur de texte

---

### Thèmes et Apparence

Adminer supporte différents thèmes !

1. Télécharger un thème depuis : https://www.adminer.org/en/
2. Placer le fichier `adminer.css` dans le même dossier que `adminer.php`
3. Rafraîchir la page

---

### Auto-complétion SQL

Quand vous tapez dans l'éditeur SQL :
- Les noms de tables apparaissent automatiquement
- Utilisez **Tab** pour compléter
- Les colonnes sont suggérées après `SELECT` et `WHERE`

---

## 🎓 Bonnes Pratiques

### ✅ À FAIRE

- **Toujours tester** avec `SELECT` avant `UPDATE` ou `DELETE`
- **Faire des backups** réguliers
- **Utiliser des filtres WHERE** pour limiter les modifications
- **Vérifier les résultats** après chaque modification
- **Fermer Adminer** quand vous ne l'utilisez plus (CTRL+C)

### ❌ À NE PAS FAIRE

- **Ne jamais** exécuter `DROP TABLE` ou `DROP DATABASE`
- **Ne jamais** exécuter `DELETE` sans `WHERE`
- **Ne pas** modifier `password_hash` directement (utiliser l'API)
- **Ne pas** laisser Adminer accessible publiquement
- **Ne pas** partager vos identifiants

---

## 📚 Ressources Supplémentaires

### Documentation Officielle
- Site officiel : https://www.adminer.org/
- GitHub : https://github.com/vrana/adminer

### Autres Guides du Projet
- `GUIDE_CONSULTATION_DB.md` - Méthodes alternatives (CLI, Workbench)
- `RITUEL_DEMARRAGE.md` - Démarrage de l'application
- `backend/GUIDE_TEST_AUTH.md` - Tests d'authentification

---

## 🎯 Résumé Rapide

### Lancer Adminer
```powershell
# Méthode 1 : Double-clic
start_adminer.bat

# Méthode 2 : PowerShell
.\start_adminer.ps1

# Méthode 3 : Manuel
cd adminer
php -S localhost:8080
```

### Connexion
```
URL:      http://localhost:8080/adminer.php
Système:  MySQL
Serveur:  127.0.0.1
User:     credef
Pass:     credef
Base:     credef
```

### Requêtes Essentielles
```sql
-- Voir tout
SELECT * FROM user;
SELECT * FROM credef_dossier;

-- Statistiques
SELECT statut, COUNT(*) FROM credef_dossier GROUP BY statut;

-- Recherche
SELECT * FROM credef_dossier WHERE ref LIKE '%2025%';

-- Historique
SELECT * FROM workflow_log WHERE dossier_id = 1;
```

---

**Vous êtes maintenant un expert Adminer ! 🎉**

**Besoin d'aide ? Consultez la section [Dépannage](#depannage) ou demandez de l'aide !**
