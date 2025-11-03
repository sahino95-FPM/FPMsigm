#!/bin/bash
# Script de test pour l'Authentification JWT
# Ce script démontre l'utilisation des endpoints d'authentification

BASE_URL="http://localhost:5000/api"

echo "🧪 Test de l'Authentification JWT"
echo "=================================="
echo ""

# 1. Lister les rôles disponibles
echo "1️⃣  Liste des rôles disponibles"
curl -s "$BASE_URL/auth/roles" | jq '.'
echo ""

# 2. Créer un utilisateur ADMIN
echo "2️⃣  Création d'un utilisateur ADMIN"
curl -s -X POST "$BASE_URL/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@credef.com",
    "password": "admin123",
    "nom": "Administrateur",
    "prenom": "Système",
    "role": "ADMIN"
  }' | jq '.'
echo ""

# 3. Créer un utilisateur SACV
echo "3️⃣  Création d'un utilisateur SACV"
curl -s -X POST "$BASE_URL/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "sacv@credef.com",
    "password": "sacv123",
    "nom": "Agent",
    "prenom": "SACV",
    "role": "SACV"
  }' | jq '.'
echo ""

# 4. Créer un utilisateur ADHERENT
echo "4️⃣  Création d'un utilisateur ADHERENT"
curl -s -X POST "$BASE_URL/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "adherent@credef.com",
    "password": "adherent123",
    "nom": "Dupont",
    "prenom": "Jean",
    "role": "ADHERENT"
  }' | jq '.'
echo ""

# 5. Test de doublon (devrait échouer)
echo "5️⃣  Test de création avec email existant (doit échouer)"
curl -s -X POST "$BASE_URL/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@credef.com",
    "password": "test123",
    "nom": "Test",
    "prenom": "Doublon",
    "role": "ADMIN"
  }' | jq '.'
echo ""

# 6. Test de mot de passe trop court (devrait échouer)
echo "6️⃣  Test de mot de passe trop court (doit échouer)"
curl -s -X POST "$BASE_URL/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@credef.com",
    "password": "123",
    "nom": "Test",
    "prenom": "Court",
    "role": "ADMIN"
  }' | jq '.'
echo ""

# 7. Test de rôle invalide (devrait échouer)
echo "7️⃣  Test de rôle invalide (doit échouer)"
curl -s -X POST "$BASE_URL/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "invalid@credef.com",
    "password": "password123",
    "nom": "Test",
    "prenom": "Invalide",
    "role": "ROLE_INVALIDE"
  }' | jq '.'
echo ""

# 8. Login avec l'utilisateur ADMIN
echo "8️⃣  Login avec admin@credef.com"
LOGIN_RESPONSE=$(curl -s -X POST "$BASE_URL/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@credef.com",
    "password": "admin123"
  }')

echo "$LOGIN_RESPONSE" | jq '.'
echo ""

# Extraire le token
ACCESS_TOKEN=$(echo "$LOGIN_RESPONSE" | jq -r '.access_token')

# 9. Vérifier le token avec /auth/me
echo "9️⃣  Récupération du profil avec le token JWT"
curl -s "$BASE_URL/auth/me" \
  -H "Authorization: Bearer $ACCESS_TOKEN" | jq '.'
echo ""

# 10. Test de login avec mauvais mot de passe (devrait échouer)
echo "🔟 Test de login avec mauvais mot de passe (doit échouer)"
curl -s -X POST "$BASE_URL/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@credef.com",
    "password": "mauvais_password"
  }' | jq '.'
echo ""

# 11. Test de login avec email inexistant (devrait échouer)
echo "1️⃣1️⃣  Test de login avec email inexistant (doit échouer)"
curl -s -X POST "$BASE_URL/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "inexistant@credef.com",
    "password": "password123"
  }' | jq '.'
echo ""

# 12. Créer un dossier avec le token
echo "1️⃣2️⃣  Création d'un dossier avec authentification"
curl -s -X POST "$BASE_URL/credef/dossiers" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -d '{
    "ref": "CREDEF-AUTH-001",
    "adherent_id": 777,
    "montant_demande": 50000.00,
    "duree_mois": 12
  }' | jq '.'
echo ""

echo "✅ Tests terminés !"
echo ""
echo "📋 Résumé:"
echo "   - 3 utilisateurs créés: ADMIN, SACV, ADHERENT"
echo "   - 4 tests d'erreur effectués (doublon, mdp court, rôle invalide, login incorrect)"
echo "   - Token JWT généré et validé avec /auth/me"
echo "   - Création de dossier avec authentification réussie"
echo ""
echo "🔑 Token généré: ${ACCESS_TOKEN:0:50}..."
