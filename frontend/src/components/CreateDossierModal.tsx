import React, { useState } from 'react';
import { X } from 'lucide-react';
import { api } from '../services/api';
import type { CredefDossier } from '../types';

interface CreateDossierModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess: (dossier: CredefDossier) => void;
}

export const CreateDossierModal: React.FC<CreateDossierModalProps> = ({
  isOpen,
  onClose,
  onSuccess,
}) => {
  const [formData, setFormData] = useState({
    ref: '',
    adherent_id: '',
    montant_demande: '',
    duree_mois: '',
    taux: '10',
    mois_traitement: '',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      // Préparer les données
      const data: any = {
        ref: formData.ref,
        statut: 'BROUILLON',
      };

      // Ajouter les champs optionnels s'ils sont remplis
      if (formData.adherent_id) data.adherent_id = parseInt(formData.adherent_id);
      if (formData.montant_demande) data.montant_demande = parseFloat(formData.montant_demande);
      if (formData.duree_mois) data.duree_mois = parseInt(formData.duree_mois);
      if (formData.taux) data.taux = parseFloat(formData.taux);
      if (formData.mois_traitement) data.mois_traitement = formData.mois_traitement;

      // Créer le dossier
      const dossier = await api.createDossier(data);
      onSuccess(dossier);

      // Réinitialiser le formulaire
      setFormData({
        ref: '',
        adherent_id: '',
        montant_demande: '',
        duree_mois: '',
        taux: '10',
        mois_traitement: '',
      });

      onClose();
    } catch (err: any) {
      setError(err.response?.data?.error || 'Erreur lors de la création du dossier');
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-200">
          <h2 className="text-2xl font-bold text-gray-900">Nouveau Dossier CREDEF</h2>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 transition-colors"
          >
            <X className="h-6 w-6" />
          </button>
        </div>

        {/* Body */}
        <form onSubmit={handleSubmit} className="p-6 space-y-4">
          {error && (
            <div className="bg-red-50 border border-red-200 rounded-lg p-4">
              <p className="text-sm text-red-800">{error}</p>
            </div>
          )}

          {/* Référence (obligatoire) */}
          <div>
            <label htmlFor="ref" className="block text-sm font-medium text-gray-700 mb-2">
              Référence du dossier <span className="text-red-500">*</span>
            </label>
            <input
              type="text"
              id="ref"
              name="ref"
              value={formData.ref}
              onChange={handleChange}
              required
              placeholder="Ex: CREDEF-2025-001"
              className="input-field"
            />
            <p className="mt-1 text-xs text-gray-500">
              Format recommandé : CREDEF-YYYY-XXX
            </p>
          </div>

          {/* ID Adhérent */}
          <div>
            <label htmlFor="adherent_id" className="block text-sm font-medium text-gray-700 mb-2">
              ID Adhérent
            </label>
            <input
              type="number"
              id="adherent_id"
              name="adherent_id"
              value={formData.adherent_id}
              onChange={handleChange}
              placeholder="Ex: 12345"
              className="input-field"
            />
          </div>

          {/* Montant demandé */}
          <div>
            <label htmlFor="montant_demande" className="block text-sm font-medium text-gray-700 mb-2">
              Montant demandé (€)
            </label>
            <input
              type="number"
              id="montant_demande"
              name="montant_demande"
              value={formData.montant_demande}
              onChange={handleChange}
              step="0.01"
              min="0"
              placeholder="Ex: 50000"
              className="input-field"
            />
          </div>

          {/* Durée en mois */}
          <div>
            <label htmlFor="duree_mois" className="block text-sm font-medium text-gray-700 mb-2">
              Durée (mois)
            </label>
            <input
              type="number"
              id="duree_mois"
              name="duree_mois"
              value={formData.duree_mois}
              onChange={handleChange}
              min="1"
              placeholder="Ex: 24"
              className="input-field"
            />
          </div>

          {/* Taux */}
          <div>
            <label htmlFor="taux" className="block text-sm font-medium text-gray-700 mb-2">
              Taux (%)
            </label>
            <input
              type="number"
              id="taux"
              name="taux"
              value={formData.taux}
              onChange={handleChange}
              step="0.01"
              min="0"
              max="100"
              placeholder="Ex: 10"
              className="input-field"
            />
          </div>

          {/* Mois de traitement */}
          <div>
            <label htmlFor="mois_traitement" className="block text-sm font-medium text-gray-700 mb-2">
              Mois de traitement
            </label>
            <input
              type="month"
              id="mois_traitement"
              name="mois_traitement"
              value={formData.mois_traitement}
              onChange={handleChange}
              className="input-field"
            />
            <p className="mt-1 text-xs text-gray-500">
              Format : YYYY-MM
            </p>
          </div>

          {/* Info */}
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <p className="text-sm text-blue-800">
              <strong>Note :</strong> Le dossier sera créé avec le statut <strong>BROUILLON</strong>.
              Vous pourrez ensuite le compléter et le faire évoluer dans le workflow.
            </p>
          </div>

          {/* Buttons */}
          <div className="flex justify-end gap-3 pt-4 border-t border-gray-200">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
              disabled={loading}
            >
              Annuler
            </button>
            <button
              type="submit"
              className="btn-primary"
              disabled={loading || !formData.ref}
            >
              {loading ? (
                <span className="flex items-center">
                  <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Création...
                </span>
              ) : (
                'Créer le dossier'
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
