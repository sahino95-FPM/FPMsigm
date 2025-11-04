import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { api } from '../services/api';
import {
  ArrowLeft,
  Calendar,
  DollarSign,
  Clock,
  User,
  FileText,
  GitBranch,
  Paperclip,
  RefreshCw,
} from 'lucide-react';
import type { CredefDossier } from '../types';
import { StatusBadge } from '../components/StatusBadge';
import { WorkflowHistory } from '../components/WorkflowHistory';
import { PiecesJointes } from '../components/PiecesJointes';
import { TransitionModal } from '../components/TransitionModal';
import { format } from 'date-fns';
import { fr } from 'date-fns/locale';

export const DossierDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [dossier, setDossier] = useState<CredefDossier | null>(null);
  const [loading, setLoading] = useState(true);
  const [showTransitionModal, setShowTransitionModal] = useState(false);
  const [activeTab, setActiveTab] = useState<'infos' | 'workflow' | 'pieces'>('infos');

  useEffect(() => {
    if (id) {
      loadDossier();
    }
  }, [id]);

  const loadDossier = async () => {
    if (!id) return;

    try {
      const dossiers = await api.getDossiers();
      const found = dossiers.find((d) => d.id === parseInt(id));
      if (found) {
        setDossier(found);
      } else {
        alert('Dossier introuvable');
        navigate('/dossiers');
      }
    } catch (error) {
      console.error('Erreur chargement dossier:', error);
      alert('Erreur lors du chargement');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  if (!dossier) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500">Dossier introuvable</p>
        <button onClick={() => navigate('/dossiers')} className="mt-4 btn-primary">
          Retour à la liste
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* En-tête */}
      <div className="flex items-start justify-between flex-wrap gap-4">
        <div className="flex items-center gap-4">
          <button
            onClick={() => navigate('/dossiers')}
            className="p-2 hover:bg-gray-100 rounded-lg"
          >
            <ArrowLeft className="h-5 w-5 text-gray-600" />
          </button>
          <div>
            <h1 className="text-3xl font-bold text-gray-900">{dossier.ref}</h1>
            <p className="mt-1 text-gray-600">Détails du dossier CREDEF</p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <StatusBadge statut={dossier.statut} size="lg" />
          <button
            onClick={() => setShowTransitionModal(true)}
            className="btn-primary flex items-center gap-2"
          >
            <RefreshCw className="h-4 w-4" />
            Changer le statut
          </button>
        </div>
      </div>

      {/* Onglets */}
      <div className="border-b border-gray-200">
        <nav className="-mb-px flex space-x-8">
          {[
            { id: 'infos', label: 'Informations', icon: FileText },
            { id: 'workflow', label: 'Historique', icon: GitBranch },
            { id: 'pieces', label: 'Pièces jointes', icon: Paperclip },
          ].map((tab) => {
            const Icon = tab.icon;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as any)}
                className={`
                  flex items-center gap-2 py-4 px-1 border-b-2 font-medium text-sm transition-colors
                  ${
                    activeTab === tab.id
                      ? 'border-primary-500 text-primary-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }
                `}
              >
                <Icon className="h-4 w-4" />
                {tab.label}
              </button>
            );
          })}
        </nav>
      </div>

      {/* Contenu des onglets */}
      <div>
        {activeTab === 'infos' && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Informations générales */}
            <div className="card">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">
                Informations Générales
              </h2>
              <dl className="space-y-3">
                <InfoRow
                  icon={FileText}
                  label="Référence"
                  value={dossier.ref}
                />
                <InfoRow
                  icon={User}
                  label="ID Adhérent"
                  value={dossier.adherent_id?.toString() || '-'}
                />
                <InfoRow
                  icon={Calendar}
                  label="Date de dépôt"
                  value={
                    dossier.date_depot
                      ? format(new Date(dossier.date_depot), 'dd MMMM yyyy', { locale: fr })
                      : '-'
                  }
                />
                <InfoRow
                  icon={Calendar}
                  label="Mois de traitement"
                  value={dossier.mois_traitement || '-'}
                />
              </dl>
            </div>

            {/* Informations financières */}
            <div className="card">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">
                Informations Financières
              </h2>
              <dl className="space-y-3">
                <InfoRow
                  icon={DollarSign}
                  label="Montant demandé"
                  value={
                    dossier.montant_demande
                      ? `${dossier.montant_demande.toLocaleString('fr-FR')} €`
                      : '-'
                  }
                />
                <InfoRow
                  icon={DollarSign}
                  label="Montant accordé"
                  value={
                    dossier.montant_accorde
                      ? `${dossier.montant_accorde.toLocaleString('fr-FR')} €`
                      : '-'
                  }
                />
                <InfoRow
                  icon={FileText}
                  label="Taux d'intérêt"
                  value={dossier.taux ? `${dossier.taux}%` : '-'}
                />
                <InfoRow
                  icon={Clock}
                  label="Durée"
                  value={dossier.duree_mois ? `${dossier.duree_mois} mois` : '-'}
                />
              </dl>
            </div>

            {/* Statut et acteur */}
            <div className="card lg:col-span-2">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">
                Statut et Workflow
              </h2>
              <dl className="space-y-3">
                <InfoRow
                  icon={GitBranch}
                  label="Statut actuel"
                  value={<StatusBadge statut={dossier.statut} />}
                />
                <InfoRow
                  icon={User}
                  label="Acteur courant"
                  value={dossier.acteur_courant_id?.toString() || '-'}
                />
                {dossier.commentaire_rejet && (
                  <div className="pt-2">
                    <p className="text-sm font-medium text-gray-700 mb-1">
                      Commentaire de rejet
                    </p>
                    <div className="p-3 bg-red-50 border border-red-200 rounded-lg">
                      <p className="text-sm text-red-800">{dossier.commentaire_rejet}</p>
                    </div>
                  </div>
                )}
              </dl>
            </div>
          </div>
        )}

        {activeTab === 'workflow' && (
          <div className="card">
            <h2 className="text-lg font-semibold text-gray-900 mb-6">
              Historique des Transitions
            </h2>
            <WorkflowHistory dossierId={dossier.id} />
          </div>
        )}

        {activeTab === 'pieces' && (
          <div className="card">
            <h2 className="text-lg font-semibold text-gray-900 mb-6">
              Gestion des Pièces Jointes
            </h2>
            <PiecesJointes dossierId={dossier.id} />
          </div>
        )}
      </div>

      {/* Modal de transition */}
      {showTransitionModal && (
        <TransitionModal
          dossierId={dossier.id}
          currentStatut={dossier.statut}
          onClose={() => setShowTransitionModal(false)}
          onSuccess={loadDossier}
        />
      )}
    </div>
  );
};

// Composant helper pour afficher une ligne d'information
const InfoRow: React.FC<{
  icon: React.ElementType;
  label: string;
  value: React.ReactNode;
}> = ({ icon: Icon, label, value }) => (
  <div className="flex items-start gap-3">
    <Icon className="h-5 w-5 text-gray-400 flex-shrink-0 mt-0.5" />
    <div className="flex-1 min-w-0">
      <dt className="text-sm font-medium text-gray-500">{label}</dt>
      <dd className="mt-0.5 text-sm text-gray-900">{value}</dd>
    </div>
  </div>
);
