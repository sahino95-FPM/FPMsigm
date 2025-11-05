#!/usr/bin/env python3
"""
Script interactif pour interroger la base de données FPMsigm
Usage: python query_db.py
"""

import sys
from sqlalchemy import create_engine, text
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

                    # Calculer les largeurs de colonnes
                    col_widths = [len(col) for col in columns]
                    for row in rows:
                        for i, val in enumerate(row):
                            col_widths[i] = max(col_widths[i], len(str(val)) if val is not None else 4)

                    # Ligne de séparation
                    separator = "+" + "+".join(["-" * (w + 2) for w in col_widths]) + "+"

                    # Afficher l'en-tête
                    print("\n" + separator)
                    header = "|"
                    for col, width in zip(columns, col_widths):
                        header += f" {col:<{width}} |"
                    print(header)
                    print(separator)

                    # Afficher les données
                    for row in rows:
                        line = "|"
                        for val, width in zip(row, col_widths):
                            val_str = str(val) if val is not None else "NULL"
                            line += f" {val_str:<{width}} |"
                        print(line)

                    print(separator)
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
    print("  7. Statistiques globales")
    print("  8. Requête personnalisée")
    print("  0. Quitter")
    print("=" * 60)


def main():
    """Fonction principale"""
    queries = {
        "1": "SELECT id, email, nom, prenom, role, is_active FROM user ORDER BY id",
        "2": "SELECT id, ref, statut, montant_demande, duree_mois, mois_traitement FROM credef_dossier ORDER BY id DESC",
        "3": "SELECT statut, COUNT(*) as nombre FROM credef_dossier GROUP BY statut ORDER BY nombre DESC",
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
        "6": "SELECT type_piece, COUNT(*) as nombre, SUM(taille_octets) as taille_totale FROM piece_jointe GROUP BY type_piece",
        "7": """
            SELECT
                'Utilisateurs' as categorie,
                COUNT(*) as nombre
            FROM user
            UNION ALL
            SELECT
                'Dossiers' as categorie,
                COUNT(*) as nombre
            FROM credef_dossier
            UNION ALL
            SELECT
                'Transitions' as categorie,
                COUNT(*) as nombre
            FROM workflow_log
            UNION ALL
            SELECT
                'Pièces jointes' as categorie,
                COUNT(*) as nombre
            FROM piece_jointe
        """
    }

    print("\n" + "=" * 60)
    print("🗄️  OUTIL DE CONSULTATION BASE DE DONNÉES")
    print("=" * 60)
    print(f"\nConnexion : {DATABASE_URL}")
    print("Base de données : credef")

    while True:
        show_menu()
        choice = input("\nChoisissez une option : ").strip()

        if choice == "0":
            print("\nAu revoir ! 👋")
            break
        elif choice == "8":
            print("\nEntrez votre requête SQL (terminez par une ligne vide) :")
            print("Exemple: SELECT * FROM user WHERE role = 'ADMIN'")
            print()
            lines = []
            while True:
                line = input()
                if line == "":
                    break
                lines.append(line)

            if lines:
                query = " ".join(lines)
                execute_query(query)
            else:
                print("\n⚠ Requête vide")
        elif choice in queries:
            execute_query(queries[choice])
        else:
            print("\n⚠ Option invalide")

        input("\nAppuyez sur Entrée pour continuer...")


if __name__ == "__main__":
    main()
