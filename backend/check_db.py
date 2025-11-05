#!/usr/bin/env python3
"""
Script de vérification de la configuration de la base de données
Utilisation: python check_db.py
"""

import sys
import os
from sqlalchemy import create_engine, text, inspect
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Configuration
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://credef:credef@localhost:3306/credef")


def check_database_connection():
    """Vérifie la connexion à la base de données"""
    print("\n" + "=" * 60)
    print("VÉRIFICATION DE LA CONNEXION À LA BASE DE DONNÉES")
    print("=" * 60)
    print(f"\nURL de connexion: {DATABASE_URL}")

    try:
        engine = create_engine(DATABASE_URL)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("\n✓ Connexion à la base de données réussie!")
            return engine
    except Exception as e:
        print(f"\n✗ ERREUR: Impossible de se connecter à la base de données")
        print(f"Détails: {str(e)}")
        print("\nVérifiez que:")
        print("  1. MySQL/MariaDB est démarré")
        print("  2. Les identifiants dans .env sont corrects")
        print("  3. La base de données 'credef' existe")
        print("\nPour créer la base de données:")
        print("  mysql -u root -p")
        print("  CREATE DATABASE credef;")
        print("  GRANT ALL ON credef.* TO 'credef'@'localhost' IDENTIFIED BY 'credef';")
        return None


def check_tables(engine):
    """Vérifie les tables existantes dans la base de données"""
    print("\n" + "=" * 60)
    print("VÉRIFICATION DES TABLES")
    print("=" * 60)

    inspector = inspect(engine)
    tables = inspector.get_table_names()

    expected_tables = ["user", "credef_dossier", "workflow_log", "piece_jointe", "alembic_version"]

    if not tables:
        print("\n⚠ Aucune table trouvée dans la base de données!")
        print("\nVous devez appliquer les migrations:")
        print("  flask db upgrade")
        return False

    print(f"\n✓ {len(tables)} table(s) trouvée(s):")
    for table in tables:
        if table in expected_tables:
            print(f"  ✓ {table}")
        else:
            print(f"  • {table}")

    # Vérifier les tables manquantes
    missing_tables = [t for t in expected_tables if t not in tables and t != "alembic_version"]

    if missing_tables:
        print(f"\n⚠ Tables manquantes: {', '.join(missing_tables)}")
        print("\nAppliquez les migrations pour créer les tables:")
        print("  flask db upgrade")
        return False

    return True


def check_user_table(engine):
    """Vérifie la structure de la table user"""
    print("\n" + "=" * 60)
    print("VÉRIFICATION DE LA TABLE USER")
    print("=" * 60)

    inspector = inspect(engine)

    if "user" not in inspector.get_table_names():
        print("\n⚠ La table 'user' n'existe pas!")
        return False

    columns = inspector.get_columns("user")
    column_names = [col["name"] for col in columns]

    expected_columns = ["id", "email", "password_hash", "nom", "prenom", "role", "is_active", "created_at", "updated_at"]

    print(f"\n✓ Colonnes de la table 'user':")
    for col in columns:
        print(f"  • {col['name']:20} {col['type']}")

    missing_columns = [c for c in expected_columns if c not in column_names]
    if missing_columns:
        print(f"\n⚠ Colonnes manquantes: {', '.join(missing_columns)}")
        return False

    return True


def check_users(engine):
    """Vérifie les utilisateurs existants"""
    print("\n" + "=" * 60)
    print("VÉRIFICATION DES UTILISATEURS")
    print("=" * 60)

    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT COUNT(*) as count FROM user"))
            count = result.fetchone()[0]

            print(f"\n✓ {count} utilisateur(s) dans la base de données")

            if count > 0:
                result = conn.execute(text("""
                    SELECT id, email, nom, prenom, role, is_active, created_at
                    FROM user
                    ORDER BY created_at DESC
                    LIMIT 10
                """))
                users = result.fetchall()

                print("\nUtilisateurs existants:")
                print("-" * 60)
                for user in users:
                    status = "Actif" if user[5] else "Inactif"
                    print(f"  • {user[1]:30} {user[3]} {user[2]:15} [{user[4]}] {status}")
            else:
                print("\n⚠ Aucun utilisateur trouvé.")
                print("\nCréez un utilisateur admin avec:")
                print("  python test_auth.py")
                print("\nOu avec PowerShell:")
                print('  $body = @{email="admin@credef.com"; password="admin123"; nom="Admin"; prenom="Systeme"; role="ADMIN"} | ConvertTo-Json')
                print('  Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/auth/register" -Method POST -Body $body -ContentType "application/json"')

            return True

    except Exception as e:
        print(f"\n✗ Erreur lors de la vérification des utilisateurs: {str(e)}")
        return False


def check_migrations(engine):
    """Vérifie l'état des migrations"""
    print("\n" + "=" * 60)
    print("VÉRIFICATION DES MIGRATIONS")
    print("=" * 60)

    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version_num FROM alembic_version"))
            version = result.fetchone()

            if version:
                print(f"\n✓ Version de migration actuelle: {version[0]}")
            else:
                print("\n⚠ Aucune migration appliquée")
                print("\nAppliquez les migrations:")
                print("  flask db upgrade")

            return True

    except Exception as e:
        print(f"\n⚠ Table alembic_version non trouvée (normal si jamais migré)")
        print("\nAppliquez les migrations:")
        print("  flask db upgrade")
        return False


def main():
    """Fonction principale"""
    print("\n" + "=" * 60)
    print("🔍 VÉRIFICATION DE LA CONFIGURATION DE LA BASE DE DONNÉES")
    print("=" * 60)

    # 1. Vérifier la connexion
    engine = check_database_connection()
    if not engine:
        sys.exit(1)

    # 2. Vérifier les migrations
    check_migrations(engine)

    # 3. Vérifier les tables
    tables_ok = check_tables(engine)

    if not tables_ok:
        print("\n" + "=" * 60)
        print("⚠ CONFIGURATION INCOMPLÈTE")
        print("=" * 60)
        print("\nÉtape suivante: Appliquer les migrations")
        print("  flask db upgrade")
        sys.exit(1)

    # 4. Vérifier la structure de la table user
    user_table_ok = check_user_table(engine)

    # 5. Vérifier les utilisateurs
    check_users(engine)

    # Résumé final
    print("\n" + "=" * 60)
    print("✓ VÉRIFICATION TERMINÉE")
    print("=" * 60)

    if tables_ok and user_table_ok:
        print("\n✓ La base de données est correctement configurée!")
        print("\nProchaines étapes:")
        print("  1. Démarrer le serveur: python autoapp.py")
        print("  2. Tester l'authentification: python test_auth.py")
    else:
        print("\n⚠ Configuration incomplète. Suivez les instructions ci-dessus.")


if __name__ == "__main__":
    main()
