#!/bin/bash
# Script de test pour les Pièces Jointes
# Ce script démontre l'utilisation des endpoints de pièces jointes

BASE_URL="http://localhost:5000/api/credef"

echo "🧪 Test des Pièces Jointes"
echo "=========================="
echo ""

# 1. Créer un dossier de test
echo "1️⃣  Création d'un nouveau dossier..."
DOSSIER_ID=$(curl -s -X POST "$BASE_URL/dossiers" \
  -H "Content-Type: application/json" \
  -d '{
    "ref": "CREDEF-TEST-PIECES-001",
    "adherent_id": 888,
    "montant_demande": 75000.00,
    "duree_mois": 18
  }' | jq -r '.id')

echo "   ✅ Dossier créé avec ID: $DOSSIER_ID"
echo ""

# 2. Créer des fichiers de test
echo "2️⃣  Création de fichiers de test..."
mkdir -p /tmp/test_pieces
echo "Ceci est une CNI de test" > /tmp/test_pieces/cni.pdf
echo "Ceci est un bulletin de paie de test" > /tmp/test_pieces/bulletin.pdf
echo "Ceci est une attestation de travail de test" > /tmp/test_pieces/attestation.pdf
echo "   ✅ Fichiers de test créés"
echo ""

# 3. Upload CNI
echo "3️⃣  Upload CNI (pièce obligatoire)"
curl -s -X POST "$BASE_URL/dossiers/$DOSSIER_ID/pieces" \
  -F "file=@/tmp/test_pieces/cni.pdf" \
  -F "type_piece=CNI" \
  -F "uploaded_by=123" \
  -F "commentaire=Carte d'identité recto-verso" | jq '.'
echo ""

# 4. Upload Bulletin de paie
echo "4️⃣  Upload BULLETIN_PAIE (pièce obligatoire)"
curl -s -X POST "$BASE_URL/dossiers/$DOSSIER_ID/pieces" \
  -F "file=@/tmp/test_pieces/bulletin.pdf" \
  -F "type_piece=BULLETIN_PAIE" \
  -F "uploaded_by=123" \
  -F "commentaire=Bulletin de paie du mois de mai 2025" | jq '.'
echo ""

# 5. Vérifier la complétude (devrait manquer ATTESTATION_TRAVAIL et RIB)
echo "5️⃣  Vérification de la complétude des pièces"
curl -s "$BASE_URL/dossiers/$DOSSIER_ID/pieces/validation" | jq '.'
echo ""

# 6. Upload Attestation de travail
echo "6️⃣  Upload ATTESTATION_TRAVAIL (pièce obligatoire)"
curl -s -X POST "$BASE_URL/dossiers/$DOSSIER_ID/pieces" \
  -F "file=@/tmp/test_pieces/attestation.pdf" \
  -F "type_piece=ATTESTATION_TRAVAIL" \
  -F "uploaded_by=123" | jq '.'
echo ""

# 7. Lister toutes les pièces du dossier
echo "7️⃣  Liste de toutes les pièces du dossier"
curl -s "$BASE_URL/dossiers/$DOSSIER_ID/pieces" | jq '.'
echo ""

# 8. Vérifier à nouveau la complétude (devrait manquer RIB)
echo "8️⃣  Vérification finale de la complétude"
curl -s "$BASE_URL/dossiers/$DOSSIER_ID/pieces/validation" | jq '.'
echo ""

# 9. Test d'upload avec extension invalide
echo "9️⃣  Test d'upload avec extension invalide (doit échouer)"
echo "Texte invalide" > /tmp/test_pieces/test.txt
curl -s -X POST "$BASE_URL/dossiers/$DOSSIER_ID/pieces" \
  -F "file=@/tmp/test_pieces/test.txt" \
  -F "type_piece=CNI" | jq '.'
echo ""

# 10. Test d'upload avec type invalide
echo "🔟 Test d'upload avec type invalide (doit échouer)"
curl -s -X POST "$BASE_URL/dossiers/$DOSSIER_ID/pieces" \
  -F "file=@/tmp/test_pieces/cni.pdf" \
  -F "type_piece=TYPE_INVALIDE" | jq '.'
echo ""

echo "✅ Tests terminés !"
echo ""
echo "📋 Résumé:"
echo "   - Dossier créé: $DOSSIER_ID"
echo "   - 3 pièces uploadées: CNI, BULLETIN_PAIE, ATTESTATION_TRAVAIL"
echo "   - 1 pièce manquante: RIB"
echo "   - 2 tests d'erreur effectués (extension invalide, type invalide)"
echo ""
echo "🧹 Nettoyage des fichiers de test..."
rm -rf /tmp/test_pieces
echo "   ✅ Nettoyage effectué"
