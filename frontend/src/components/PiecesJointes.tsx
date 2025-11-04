import React, { useEffect, useState, useRef } from 'react';
import { api } from '../services/api';
import { Upload, File, Trash2, CheckCircle, XCircle, AlertCircle } from 'lucide-react';
import type { PieceJointe, TypePiece } from '../types';
import { useAuthStore } from '../stores/authStore';

interface PiecesJointesProps {
  dossierId: number;
}

export const PiecesJointes: React.FC<PiecesJointesProps> = ({ dossierId }) => {
  const { user } = useAuthStore();
  const [pieces, setPieces] = useState<PieceJointe[]>([]);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [selectedType, setSelectedType] = useState<TypePiece>('CNI');
  const [commentaire, setCommentaire] = useState('');
  const fileInputRef = useRef<HTMLInputElement>(null);

  const typePieceOptions: { value: TypePiece; label: string; obligatoire: boolean }[] = [
    { value: 'CNI', label: 'Carte Nationale d\'Identité', obligatoire: true },
    { value: 'BULLETIN_PAIE', label: 'Bulletin de Paie', obligatoire: true },
    { value: 'ATTESTATION_TRAVAIL', label: 'Attestation de Travail', obligatoire: true },
    { value: 'RIB', label: 'Relevé d\'Identité Bancaire', obligatoire: true },
    { value: 'JUSTIFICATIF_DOMICILE', label: 'Justificatif de Domicile', obligatoire: false },
    { value: 'PHOTO', label: 'Photo d\'Identité', obligatoire: false },
    { value: 'AUTRE', label: 'Autre Document', obligatoire: false },
  ];

  useEffect(() => {
    loadPieces();
  }, [dossierId]);

  const loadPieces = async () => {
    try {
      const data = await api.getPieces(dossierId);
      setPieces(data.pieces);
    } catch (error) {
      console.error('Erreur chargement pièces:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleFileSelect = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setUploading(true);
    try {
      await api.uploadPiece(dossierId, file, selectedType, user?.id, commentaire);
      await loadPieces();
      setCommentaire('');
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    } catch (error: any) {
      alert(error.response?.data?.error || 'Erreur lors de l\'upload');
    } finally {
      setUploading(false);
    }
  };

  const handleDelete = async (pieceId: number) => {
    if (!confirm('Êtes-vous sûr de vouloir supprimer cette pièce ?')) return;

    try {
      await api.deletePiece(pieceId);
      await loadPieces();
    } catch (error) {
      alert('Erreur lors de la suppression');
    }
  };

  const formatFileSize = (bytes: number) => {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
  };

  if (loading) {
    return (
      <div className="flex justify-center py-8">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Formulaire d'upload */}
      <div className="bg-gray-50 rounded-lg p-6 border-2 border-dashed border-gray-300">
        <div className="flex items-center gap-2 mb-4">
          <Upload className="h-5 w-5 text-gray-600" />
          <h3 className="font-semibold text-gray-900">Ajouter une pièce jointe</h3>
        </div>

        <div className="space-y-4">
          {/* Type de pièce */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Type de pièce *
            </label>
            <select
              value={selectedType}
              onChange={(e) => setSelectedType(e.target.value as TypePiece)}
              className="input-field"
            >
              {typePieceOptions.map((option) => (
                <option key={option.value} value={option.value}>
                  {option.label} {option.obligatoire && '(obligatoire)'}
                </option>
              ))}
            </select>
          </div>

          {/* Commentaire optionnel */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Commentaire (optionnel)
            </label>
            <input
              type="text"
              value={commentaire}
              onChange={(e) => setCommentaire(e.target.value)}
              className="input-field"
              placeholder="Ajouter une note..."
            />
          </div>

          {/* Sélection du fichier */}
          <div>
            <input
              ref={fileInputRef}
              type="file"
              onChange={handleFileSelect}
              disabled={uploading}
              className="block w-full text-sm text-gray-500
                file:mr-4 file:py-2 file:px-4
                file:rounded-lg file:border-0
                file:text-sm file:font-semibold
                file:bg-primary-50 file:text-primary-700
                hover:file:bg-primary-100
                disabled:opacity-50 disabled:cursor-not-allowed"
            />
            <p className="mt-1 text-xs text-gray-500">
              Taille max: 5 MB - Formats acceptés selon le type de pièce
            </p>
          </div>

          {uploading && (
            <div className="flex items-center gap-2 text-sm text-primary-600">
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-primary-600"></div>
              Upload en cours...
            </div>
          )}
        </div>
      </div>

      {/* Liste des pièces */}
      <div>
        <h3 className="font-semibold text-gray-900 mb-4">
          Pièces jointes ({pieces.length})
        </h3>

        {pieces.length === 0 ? (
          <p className="text-gray-500 text-center py-8">Aucune pièce jointe</p>
        ) : (
          <div className="space-y-3">
            {pieces.map((piece) => (
              <div
                key={piece.id}
                className="flex items-start gap-4 p-4 bg-white border border-gray-200 rounded-lg hover:shadow-md transition-shadow"
              >
                {/* Icône */}
                <div className="flex-shrink-0">
                  <File className="h-8 w-8 text-gray-400" />
                </div>

                {/* Informations */}
                <div className="flex-1 min-w-0">
                  <div className="flex items-start justify-between gap-2">
                    <div className="flex-1">
                      <p className="font-medium text-gray-900 truncate">
                        {piece.nom_fichier}
                      </p>
                      <div className="mt-1 flex flex-wrap items-center gap-2 text-xs text-gray-500">
                        <span className="font-medium text-gray-700">
                          {typePieceOptions.find((t) => t.value === piece.type_piece)?.label || piece.type_piece}
                        </span>
                        <span>•</span>
                        <span>{formatFileSize(piece.taille_octets)}</span>
                        {piece.est_obligatoire && (
                          <>
                            <span>•</span>
                            <span className="text-orange-600 font-medium">Obligatoire</span>
                          </>
                        )}
                      </div>
                      {piece.commentaire && (
                        <p className="mt-1 text-sm text-gray-600">{piece.commentaire}</p>
                      )}
                    </div>

                    {/* Statut et actions */}
                    <div className="flex items-center gap-2">
                      {piece.est_valide ? (
                        <CheckCircle className="h-5 w-5 text-green-600" title="Validé" />
                      ) : (
                        <XCircle className="h-5 w-5 text-red-600" title="Non validé" />
                      )}
                      <button
                        onClick={() => handleDelete(piece.id)}
                        className="p-1 text-red-600 hover:bg-red-50 rounded"
                        title="Supprimer"
                      >
                        <Trash2 className="h-4 w-4" />
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Message de complétude */}
      <ValidationComplétude dossierId={dossierId} />
    </div>
  );
};

// Composant pour afficher la validation de complétude
const ValidationComplétude: React.FC<{ dossierId: number }> = ({ dossierId }) => {
  const [validation, setValidation] = useState<{
    complet: boolean;
    pieces_manquantes: string[];
  } | null>(null);

  useEffect(() => {
    loadValidation();
  }, [dossierId]);

  const loadValidation = async () => {
    try {
      const data = await api.validateCompletude(dossierId);
      setValidation(data);
    } catch (error) {
      console.error('Erreur validation:', error);
    }
  };

  if (!validation) return null;

  if (validation.complet) {
    return (
      <div className="flex items-start gap-3 p-4 bg-green-50 border border-green-200 rounded-lg">
        <CheckCircle className="h-5 w-5 text-green-600 flex-shrink-0 mt-0.5" />
        <div>
          <p className="font-medium text-green-900">Dossier complet</p>
          <p className="text-sm text-green-700">Toutes les pièces obligatoires sont présentes</p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex items-start gap-3 p-4 bg-orange-50 border border-orange-200 rounded-lg">
      <AlertCircle className="h-5 w-5 text-orange-600 flex-shrink-0 mt-0.5" />
      <div>
        <p className="font-medium text-orange-900">Pièces manquantes</p>
        <ul className="mt-1 text-sm text-orange-700 list-disc list-inside">
          {validation.pieces_manquantes.map((piece) => (
            <li key={piece}>{piece.replace(/_/g, ' ')}</li>
          ))}
        </ul>
      </div>
    </div>
  );
};
