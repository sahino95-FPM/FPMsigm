# 🗄️ Guide de Consultation de la Base de Données FPMsigm

Ce guide vous montre comment consulter et interroger la base de données MySQL de l'application.

---

## 📊 Informations de Connexion

**Configuration de la base de données :**
- **Hôte :** `localhost` (ou `127.0.0.1`)
- **Port :** `3306`
- **Base de données :** `credef`
- **Utilisateur :** `credef`
- **Mot de passe :** `credef`

---

## 🎯 Méthode 1 : Ligne de Commande MySQL (Recommandé)

### **Connexion à MySQL**

```powershell
# Se connecter à la base de données
mysql -u credef -p credef

# Quand demandé, entrez le mot de passe : credef
```

OU avec le mot de passe dans la commande :

```powershell
mysql -u credef -pcredef credef
```

### **Commandes SQL Utiles**

Une fois connecté, vous pouvez utiliser ces commandes :

#### **Lister toutes les tables**
```sql
SHOW TABLES;
```

**✅ Résultat attendu :**
```
+------------------------+
| Tables_in_credef       |
+------------------------+
| alembic_version        |
| credef_dossier         |
| piece_jointe           |
| user                   |
| workflow_log           |
+------------------------+
```

#### **Voir la structure d'une table**
```sql
DESCRIBE user;
DESCRIBE credef_dossier;
DESCRIBE workflow_log;
DESCRIBE piece_jointe;
```

#### **Consulter les utilisateurs**
```sql
-- Tous les utilisateurs
SELECT * FROM user;

-- Juste les infos essentielles
SELECT id, email, nom, prenom, role, is_active FROM user;

-- Compter les utilisateurs
SELECT COUNT(*) as total_users FROM user;

-- Utilisateurs par rôle
SELECT role, COUNT(*) as nombre FROM user GROUP BY role;
```

#### **Consulter les dossiers CREDEF**
```sql
-- Tous les dossiers
SELECT * FROM credef_dossier;

-- Colonnes essentielles
SELECT id, ref, statut, montant_demande, duree_mois, mois_traitement
FROM credef_dossier;

-- Dossiers par statut
SELECT statut, COUNT(*) as nombre FROM credef_dossier GROUP BY statut;

-- Dossiers d'un mois spécifique
SELECT * FROM credef_dossier WHERE mois_traitement = '2025-11';

-- Dossiers triés par date de création
SELECT * FROM credef_dossier ORDER BY id DESC;

-- Le dernier dossier créé
SELECT * FROM credef_dossier ORDER BY id DESC LIMIT 1;
```

#### **Consulter l'historique des workflows**
```sql
-- Toutes les transitions
SELECT * FROM workflow_log;

-- Historique d'un dossier spécifique (remplacez 1 par l'ID)
SELECT * FROM workflow_log WHERE dossier_id = 1 ORDER BY created_at;

-- Dernières transitions
SELECT w.*, d.ref as dossier_ref
FROM workflow_log w
JOIN credef_dossier d ON w.dossier_id = d.id
ORDER BY w.created_at DESC
LIMIT 10;
```

#### **Consulter les pièces jointes**
```sql
-- Toutes les pièces
SELECT * FROM piece_jointe;

-- Pièces d'un dossier spécifique
SELECT * FROM piece_jointe WHERE dossier_id = 1;

-- Statistiques des pièces
SELECT type_piece, COUNT(*) as nombre
FROM piece_jointe
GROUP BY type_piece;
```

#### **Requêtes avancées (Jointures)**
```sql
-- Dossiers avec leur nombre de pièces jointes
SELECT
    d.id,
    d.ref,
    d.statut,
    COUNT(p.id) as nb_pieces
FROM credef_dossier d
LEFT JOIN piece_jointe p ON d.id = p.dossier_id
GROUP BY d.id, d.ref, d.statut;

-- Dernières actions par dossier
SELECT
    d.ref as dossier,
    d.statut as statut_actuel,
    w.statut_from,
    w.statut_to,
    w.role,
    w.created_at
FROM workflow_log w
JOIN credef_dossier d ON w.dossier_id = d.id
ORDER BY w.created_at DESC
LIMIT 20;
```

#### **Quitter MySQL**
```sql
EXIT;
```
ou
```sql
QUIT;
```

---

## 🎨 Méthode 2 : MySQL Workbench (Interface Graphique)

### **Installation**
1. Téléchargez MySQL Workbench : https://dev.mysql.com/downloads/workbench/
2. Installez-le sur votre PC

### **Connexion**
1. Ouvrez MySQL Workbench
2. Cliquez sur "+" pour créer une nouvelle connexion
3. Remplissez :
   - **Connection Name:** FPMsigm
   - **Hostname:** 127.0.0.1
   - **Port:** 3306
   - **Username:** credef
   - **Password:** credef (cliquez sur "Store in Vault")
   - **Default Schema:** credef
4. Cliquez sur "Test Connection"
5. Si OK, cliquez sur "OK"

### **Utilisation**
- Double-cliquez sur la connexion "FPMsigm"
- Vous verrez les tables dans le panneau de gauche
- Écrivez vos requêtes SQL dans l'éditeur
- Appuyez sur ⚡ pour exécuter

---

## 🌐 Méthode 3 : phpMyAdmin (Interface Web)

### **Installation**

#### **Option A : Avec XAMPP (si vous l'avez)**
1. Démarrez XAMPP Control Panel
2. Cliquez sur "Admin" à côté de MySQL
3. phpMyAdmin s'ouvre dans le navigateur

#### **Option B : Installation standalone**
1. Téléchargez phpMyAdmin : https://www.phpmyadmin.net/downloads/
2. Extrayez dans `C:\phpmyadmin`
3. Configurez selon la doc officielle

### **Connexion**
1. Allez sur http://localhost/phpmyadmin
2. Connectez-vous avec :
   - **Utilisateur :** credef
   - **Mot de passe :** credef
3. Sélectionnez la base "credef" dans le panneau de gauche

---

## 🐍 Méthode 4 : Script Python (Recommandé pour les développeurs)

J'ai créé un script Python pour vous !

### **Script : `query_db.py`**

```python
#!/usr/bin/env python3
"""
Script interactif pour interroger la base de données
Usage: python query_db.py
"""

import sys
from sqlalchemy import create_engine, text
from tabulate import tabulate
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://credef:credef@localhost:3306/credef")


def execute_query(query):
    """Exécute une requête SQL et affiche les résultats"""
    engine = create_engine(DATABASE_URL)

    try:
        with engine.connect() as conn:
            result = conn.execute(text(query))

            # Si c'est une requête SELECT
            if query.strip().upper().startswith('SELECT'):
                rows = result.fetchall()
                if rows:
                    # Obtenir les noms de colonnes
                    columns = result.keys()
                    # Afficher avec tabulate
                    print("\n" + tabulate(rows, headers=columns, tablefmt="grid"))
                    print(f"\n✓ {len(rows)} ligne(s) retournée(s)")
                else:
                    print("\n⚠ Aucun résultat")
            else:
                # Pour INSERT, UPDATE, DELETE
                conn.commit()
                print("\n✓ Requête exécutée avec succès")

    except Exception as e:
        print(f"\n✗ Erreur: {str(e)}")


def show_menu():
    """Affiche le menu des requêtes prédéfinies"""
    print("\n" + "=" * 60)
    print("CONSULTATION BASE DE DONNÉES FPMSIGM")
    print("=" * 60)
    print("\nRequêtes prédéfinies :")
    print("  1. Lister tous les utilisateurs")
    print("  2. Lister tous les dossiers")
    print("  3. Compter les dossiers par statut")
    print("  4. Voir le dernier dossier créé")
    print("  5. Historique des workflows (10 derniers)")
    print("  6. Statistiques des pièces jointes")
    print("  7. Requête personnalisée")
    print("  0. Quitter")
    print("=" * 60)


def main():
    """Fonction principale"""
    queries = {
        "1": "SELECT id, email, nom, prenom, role, is_active FROM user",
        "2": "SELECT id, ref, statut, montant_demande, duree_mois, mois_traitement FROM credef_dossier ORDER BY id DESC",
        "3": "SELECT statut, COUNT(*) as nombre FROM credef_dossier GROUP BY statut",
        "4": "SELECT * FROM credef_dossier ORDER BY id DESC LIMIT 1",
        "5": """
            SELECT
                w.id,
                d.ref as dossier,
                w.statut_from,
                w.statut_to,
                w.role,
                w.created_at
            FROM workflow_log w
            JOIN credef_dossier d ON w.dossier_id = d.id
            ORDER BY w.created_at DESC
            LIMIT 10
        """,
        "6": "SELECT type_piece, COUNT(*) as nombre, SUM(taille_octets) as taille_totale FROM piece_jointe GROUP BY type_piece"
    }

    while True:
        show_menu()
        choice = input("\nChoisissez une option : ").strip()

        if choice == "0":
            print("\nAu revoir ! 👋")
            break
        elif choice == "7":
            print("\nEntrez votre requête SQL (terminez par une ligne vide) :")
            lines = []
            while True:
                line = input()
                if line == "":
                    break
                lines.append(line)

            if lines:
                query = " ".join(lines)
                execute_query(query)
        elif choice in queries:
            execute_query(queries[choice])
        else:
            print("\n⚠ Option invalide")

        input("\nAppuyez sur Entrée pour continuer...")


if __name__ == "__main__":
    main()
```

### **Utilisation**

```powershell
cd C:\Users\SAHINO\Desktop\test\FPMsigm\backend

# Installer tabulate si nécessaire
pip install tabulate

# Lancer le script
python query_db.py
```

---

## 📱 Méthode 5 : Via DBeaver (Moderne et Gratuit)

### **Installation**
1. Téléchargez DBeaver Community : https://dbeaver.io/download/
2. Installez-le

### **Connexion**
1. Ouvrez DBeaver
2. Cliquez sur "Nouvelle connexion" (icône prise)
3. Sélectionnez "MySQL"
4. Remplissez :
   - **Host:** localhost
   - **Port:** 3306
   - **Database:** credef
   - **Username:** credef
   - **Password:** credef
5. Testez la connexion
6. Cliquez sur "Terminer"

### **Avantages de DBeaver**
- ✅ Interface moderne et intuitive
- ✅ Coloration syntaxique
- ✅ Auto-complétion SQL
- ✅ Export facile (CSV, Excel, JSON)
- ✅ Visualisation des données
- ✅ Éditeur de schéma visuel

---

## 🔍 Requêtes SQL Utiles par Cas d'Usage

### **Cas 1 : Vérifier qu'un dossier a été créé**
```sql
-- Chercher par référence
SELECT * FROM credef_dossier WHERE ref = 'CREDEF-2025-001';

-- Les 5 derniers dossiers
SELECT * FROM credef_dossier ORDER BY id DESC LIMIT 5;
```

### **Cas 2 : Suivre un dossier dans le workflow**
```sql
-- Voir l'historique complet d'un dossier
SELECT
    w.id,
    w.statut_from,
    w.statut_to,
    w.role,
    w.commentaire,
    w.created_at
FROM workflow_log w
WHERE w.dossier_id = 1  -- Remplacez par l'ID du dossier
ORDER BY w.created_at;
```

### **Cas 3 : Vérifier les pièces jointes d'un dossier**
```sql
-- Pièces d'un dossier
SELECT
    p.id,
    p.type_piece,
    p.nom_fichier,
    p.taille_octets,
    p.est_obligatoire,
    p.est_valide,
    p.created_at
FROM piece_jointe p
WHERE p.dossier_id = 1;  -- Remplacez par l'ID du dossier
```

### **Cas 4 : Statistiques globales**
```sql
-- Vue d'ensemble
SELECT
    (SELECT COUNT(*) FROM user) as nb_users,
    (SELECT COUNT(*) FROM credef_dossier) as nb_dossiers,
    (SELECT COUNT(*) FROM workflow_log) as nb_transitions,
    (SELECT COUNT(*) FROM piece_jointe) as nb_pieces;
```

### **Cas 5 : Nettoyer les données de test**
```sql
-- ⚠️ ATTENTION : Cela supprime TOUTES les données !

-- Supprimer un dossier spécifique et ses données liées
DELETE FROM piece_jointe WHERE dossier_id = 1;
DELETE FROM workflow_log WHERE dossier_id = 1;
DELETE FROM credef_dossier WHERE id = 1;

-- Supprimer tous les dossiers (⚠️ DANGER)
DELETE FROM piece_jointe;
DELETE FROM workflow_log;
DELETE FROM credef_dossier;

-- Supprimer tous les utilisateurs sauf admin
DELETE FROM user WHERE email != 'admin@credef.com';
```

---

## 🛠️ Outils de Diagnostic Rapide

### **Script : `check_db.py` (Déjà disponible)**

```powershell
cd C:\Users\SAHINO\Desktop\test\FPMsigm\backend
python check_db.py
```

Ce script vous montre :
- ✅ État de la connexion
- ✅ Tables existantes
- ✅ Structure de la table user
- ✅ Nombre d'utilisateurs
- ✅ État des migrations

---

## 📊 Export des Données

### **Export en CSV (via ligne de commande)**

```sql
-- Dans MySQL
SELECT * FROM credef_dossier
INTO OUTFILE 'C:/temp/dossiers.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n';
```

### **Export via MySQL Workbench**
1. Exécutez votre requête
2. Cliquez sur "Export" (icône disquette)
3. Choisissez le format (CSV, JSON, SQL)
4. Sauvegardez

---

## 🔒 Sécurité et Bonnes Pratiques

### **À FAIRE ✅**
- Toujours utiliser des `SELECT` pour consulter
- Tester vos `UPDATE/DELETE` avec un `WHERE` précis
- Faire des backups avant les modifications

### **À NE PAS FAIRE ❌**
- Ne JAMAIS exécuter `DROP TABLE` ou `DROP DATABASE`
- Ne JAMAIS exécuter `DELETE` sans `WHERE`
- Ne pas partager les identifiants de la base

### **Backup de la base**

```powershell
# Backup complet
mysqldump -u credef -pcredef credef > backup_credef.sql

# Backup d'une seule table
mysqldump -u credef -pcredef credef credef_dossier > backup_dossiers.sql

# Restaurer un backup
mysql -u credef -pcredef credef < backup_credef.sql
```

---

## 📝 Résumé des Méthodes

| Méthode | Difficulté | Avantages | Usage |
|---------|-----------|-----------|-------|
| **MySQL CLI** | ⭐⭐ | Rapide, léger | Consultation rapide |
| **MySQL Workbench** | ⭐⭐⭐ | Interface complète | Développement |
| **phpMyAdmin** | ⭐⭐ | Web, facile | Administration |
| **Script Python** | ⭐⭐ | Automatisation | Développement |
| **DBeaver** | ⭐⭐ | Moderne, polyvalent | Tout usage |

---

## 🆘 Problèmes Courants

### **Erreur : Access denied for user**
```
Solution : Vérifiez les identifiants (credef / credef)
```

### **Erreur : Can't connect to MySQL server**
```powershell
# Vérifier que MySQL tourne
Get-Service -Name MySQL*

# Démarrer MySQL
Start-Service -Name MySQL
```

### **Erreur : Unknown database 'credef'**
```sql
-- Créer la base
CREATE DATABASE credef;
GRANT ALL ON credef.* TO 'credef'@'localhost' IDENTIFIED BY 'credef';
```

---

**Vous avez maintenant tous les outils pour consulter votre base de données ! 🎉**
