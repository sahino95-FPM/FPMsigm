#!/usr/bin/env python3
"""
Script de test pour l'authentification API
Utilisation: python test_auth.py
"""

import requests
import json

# Configuration
BASE_URL = "http://127.0.0.1:5000/api/auth"


def test_register():
    """Test de l'enregistrement d'un utilisateur admin"""
    print("\n" + "=" * 60)
    print("TEST: Enregistrement d'un utilisateur admin")
    print("=" * 60)

    data = {
        "email": "admin@credef.com",
        "password": "admin123",
        "nom": "Admin",
        "prenom": "Systeme",
        "role": "ADMIN"
    }

    try:
        response = requests.post(
            f"{BASE_URL}/register",
            json=data,
            headers={"Content-Type": "application/json"}
        )

        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")

        if response.status_code == 201:
            print("\n✓ Utilisateur créé avec succès!")
            return True
        elif response.status_code == 400:
            response_data = response.json()
            if "existe déjà" in response_data.get("error", ""):
                print("\n⚠ L'utilisateur existe déjà. Passons au test de connexion...")
                return True
            else:
                print(f"\n✗ Erreur lors de l'enregistrement: {response_data.get('error')}")
                return False
        else:
            print(f"\n✗ Erreur lors de l'enregistrement (Status: {response.status_code})")
            print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
            return False

    except requests.exceptions.ConnectionError:
        print("\n✗ ERREUR: Impossible de se connecter au serveur!")
        print("Assurez-vous que le serveur Flask est démarré:")
        print("  cd backend")
        print("  python autoapp.py")
        return False
    except Exception as e:
        print(f"\n✗ Erreur: {str(e)}")
        return False


def test_login():
    """Test de la connexion"""
    print("\n" + "=" * 60)
    print("TEST: Connexion avec l'utilisateur admin")
    print("=" * 60)

    data = {
        "email": "admin@credef.com",
        "password": "admin123"
    }

    try:
        response = requests.post(
            f"{BASE_URL}/login",
            json=data,
            headers={"Content-Type": "application/json"}
        )

        print(f"Status: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            print(f"\n✓ Connexion réussie!")
            print(f"\nUtilisateur: {result['user']['prenom']} {result['user']['nom']}")
            print(f"Email: {result['user']['email']}")
            print(f"Rôle: {result['user']['role']}")
            print(f"\n🔑 Token d'accès:")
            print(result['access_token'][:50] + "...")
            return result
        else:
            print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
            print("\n✗ Erreur lors de la connexion")
            return None

    except requests.exceptions.ConnectionError:
        print("\n✗ ERREUR: Impossible de se connecter au serveur!")
        return None
    except Exception as e:
        print(f"\n✗ Erreur: {str(e)}")
        return None


def test_get_me(access_token):
    """Test de récupération des infos utilisateur"""
    print("\n" + "=" * 60)
    print("TEST: Récupération des informations utilisateur")
    print("=" * 60)

    try:
        response = requests.get(
            f"{BASE_URL}/me",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
        )

        print(f"Status: {response.status_code}")

        if response.status_code == 200:
            user = response.json()
            print(f"\n✓ Informations récupérées avec succès!")
            print(f"\nUtilisateur: {user['prenom']} {user['nom']}")
            print(f"Email: {user['email']}")
            print(f"Rôle: {user['role']}")
            return True
        else:
            print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
            print("\n✗ Erreur lors de la récupération")
            return False

    except Exception as e:
        print(f"\n✗ Erreur: {str(e)}")
        return False


def test_get_roles():
    """Test de récupération des rôles disponibles"""
    print("\n" + "=" * 60)
    print("TEST: Récupération des rôles disponibles")
    print("=" * 60)

    try:
        response = requests.get(f"{BASE_URL}/roles")

        print(f"Status: {response.status_code}")

        if response.status_code == 200:
            roles = response.json()
            print(f"\n✓ Rôles disponibles:")
            for role in roles['roles']:
                print(f"  - {role}")
            return True
        else:
            print(f"\n✗ Erreur: {response.text}")
            return False

    except Exception as e:
        print(f"\n✗ Erreur: {str(e)}")
        return False


def main():
    print("\n" + "=" * 60)
    print("TESTS D'AUTHENTIFICATION API")
    print("=" * 60)

    # Test 1: Récupérer les rôles disponibles
    test_get_roles()

    # Test 2: Enregistrer un utilisateur
    if not test_register():
        print("\n⚠ Les tests suivants nécessitent que le serveur soit démarré.")
        return

    # Test 3: Se connecter
    login_result = test_login()

    if login_result and 'access_token' in login_result:
        # Test 4: Récupérer les infos utilisateur
        test_get_me(login_result['access_token'])

    print("\n" + "=" * 60)
    print("TESTS TERMINÉS")
    print("=" * 60)


if __name__ == "__main__":
    main()
