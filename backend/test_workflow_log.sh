#!/bin/bash
# Script de test pour le Workflow Log
# Ce script démontre l'utilisation des nouveaux endpoints

BASE_URL="http://localhost:5000/api/credef"

echo "🧪 Test du Workflow Log"
echo "========================"
echo ""

# 1. Créer un dossier de test
echo "1️⃣  Création d'un nouveau dossier..."
DOSSIER_ID=$(curl -s -X POST "$BASE_URL/dossiers" \
  -H "Content-Type: application/json" \
  -d '{
    "ref": "CREDEF-TEST-001",
    "adherent_id": 999,
    "montant_demande": 100000.00,
    "duree_mois": 24
  }' | jq -r '.id')

echo "   ✅ Dossier créé avec ID: $DOSSIER_ID"
echo ""

# 2. Faire une première transition
echo "2️⃣  Transition: BROUILLON → DÉPOSÉ"
curl -s -X POST "$BASE_URL/dossiers/$DOSSIER_ID/transition" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "DÉPOSÉ",
    "role": "ADHERENT",
    "acteur_id": 123,
    "note": "Dossier déposé par l'\''adhérent"
  }' | jq '.'
echo ""

# 3. Faire une deuxième transition
echo "3️⃣  Transition: DÉPOSÉ → EN_CONTROLE_SACV"
curl -s -X POST "$BASE_URL/dossiers/$DOSSIER_ID/transition" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "EN_CONTROLE_SACV",
    "role": "SACV",
    "acteur_id": 456,
    "note": "Prise en charge par le SACV pour contrôle"
  }' | jq '.'
echo ""

# 4. Faire une troisième transition
echo "4️⃣  Transition: EN_CONTROLE_SACV → TRANSMIS_COURRIER"
curl -s -X POST "$BASE_URL/dossiers/$DOSSIER_ID/transition" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "TRANSMIS_COURRIER",
    "role": "SACV",
    "acteur_id": 456,
    "note": "Contrôle validé, transmission du courrier"
  }' | jq '.'
echo ""

# 5. Récupérer l'historique complet
echo "5️⃣  Récupération de l'historique du workflow"
echo "   GET $BASE_URL/dossiers/$DOSSIER_ID/workflow"
echo ""
curl -s "$BASE_URL/dossiers/$DOSSIER_ID/workflow" | jq '.'
echo ""

echo "✅ Test terminé !"
echo ""
echo "💡 Le workflow_log contient maintenant 3 transitions:"
echo "   - BROUILLON → DÉPOSÉ (par ADHERENT)"
echo "   - DÉPOSÉ → EN_CONTROLE_SACV (par SACV)"
echo "   - EN_CONTROLE_SACV → TRANSMIS_COURRIER (par SACV)"
