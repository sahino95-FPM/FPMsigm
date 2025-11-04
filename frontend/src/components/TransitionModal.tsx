import React, { useState } from 'react';
import { X, ArrowRight } from 'lucide-react';
import { api } from '../services/api';
import { useAuthStore } from '../stores/authStore';
import type { DossierStatut } from '../types';

interface TransitionModalProps {
  dossierId: number;
  currentStatut: DossierStatut;
  onClose: () => void;
  onSuccess: () => void;
}

// Transitions autorisées selon le statut actuel
const TRANSITIONS_AUTORISEES: Record<DossierStatut, DossierStatut[]> = {
  BROUILLON: ['DÉPOSÉ'],
  DÉPOSÉ: ['EN_CONTROLE_SACV', 'REJET_ADMIN'],
  EN_CONTROLE_SACV: ['TRANSMIS_COURRIER', 'REJET_ADMIN'],
  TRANSMIS_COURRIER: ['EN_ETUDE_PRET'],
  EN_ETUDE_PRET: ['SOUMIS_COMITE', 'REJET_ADMIN'],
  SOUMIS_COMITE: ['VALIDÉ_COMITE', 'REJET_ADMIN'],
  'VALIDÉ_COMITE': ['ETATS_EDITES'],
  ETATS_EDITES: ['EN_SIGNATURE_DCFF_DCPRE'],
  EN_SIGNATURE_DCFF_DCPRE: ['TRANSMIS_DTR'],
  TRANSMIS_DTR: ['DECAISSE_ECOBANK'],
  DECAISSE_ECOBANK: ['CLOS'],
  CLOS: [],
  REJET_ADMIN: ['BROUILLON', 'DÉPOSÉ'],
};

export const TransitionModal: React.FC<TransitionModalProps> = ({
  dossierId,
  currentStatut,
  onClose,
  onSuccess,
}) => {
  const { user } = useAuthStore();
  const [selectedStatut, setSelectedStatut] = useState<DossierStatut | ''>('');
  const [note, setNote] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const transitionsPossibles = TRANSITIONS_AUTORISEES[currentStatut] || [];

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedStatut) return;

    setLoading(true);
    setError(null);

    try {
      await api.transitionDossier(dossierId, {
        to: selectedStatut,
        role: user?.role,
        note,
        acteur_id: user?.id,
      });
      onSuccess();
      onClose();
    } catch (err: any) {
      setError(err.response?.data?.error || 'Erreur lors de la transition');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-lg max-w-md w-full p-6">
        {/* Header */}
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-bold text-gray-900">Changer le statut</h2>
          <button
            onClick={onClose}
            className="p-1 hover:bg-gray-100 rounded"
          >
            <X className="h-5 w-5 text-gray-500" />
          </button>
        </div>

        {/* Statut actuel */}
        <div className="mb-6 p-4 bg-gray-50 rounded-lg">
          <p className="text-sm text-gray-600 mb-1">Statut actuel</p>
          <p className="font-medium text-gray-900">{currentStatut.replace(/_/g, ' ')}</p>
        </div>

        {/* Formulaire */}
        <form onSubmit={handleSubmit} className="space-y-4">
          {/* Sélection du nouveau statut */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Nouveau statut *
            </label>
            {transitionsPossibles.length === 0 ? (
              <p className="text-sm text-gray-500 italic">
                Aucune transition possible depuis ce statut
              </p>
            ) : (
              <select
                value={selectedStatut}
                onChange={(e) => setSelectedStatut(e.target.value as DossierStatut)}
                required
                className="input-field"
              >
                <option value="">Sélectionner...</option>
                {transitionsPossibles.map((statut) => (
                  <option key={statut} value={statut}>
                    {statut.replace(/_/g, ' ')}
                  </option>
                ))}
              </select>
            )}
          </div>

          {/* Note/Commentaire */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Note (optionnel)
            </label>
            <textarea
              value={note}
              onChange={(e) => setNote(e.target.value)}
              rows={3}
              className="input-field"
              placeholder="Ajouter un commentaire sur cette transition..."
            />
          </div>

          {/* Informations */}
          <div className="text-xs text-gray-500 bg-blue-50 p-3 rounded">
            <p>Cette transition sera effectuée par :</p>
            <p className="mt-1 font-medium text-gray-700">
              {user?.prenom} {user?.nom} ({user?.role})
            </p>
          </div>

          {/* Erreur */}
          {error && (
            <div className="p-3 bg-red-50 border border-red-200 rounded text-sm text-red-800">
              {error}
            </div>
          )}

          {/* Actions */}
          <div className="flex gap-3 pt-4">
            <button
              type="button"
              onClick={onClose}
              className="flex-1 btn-secondary"
            >
              Annuler
            </button>
            <button
              type="submit"
              disabled={loading || !selectedStatut || transitionsPossibles.length === 0}
              className="flex-1 btn-primary flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                  Traitement...
                </>
              ) : (
                <>
                  <ArrowRight className="h-4 w-4" />
                  Valider
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
