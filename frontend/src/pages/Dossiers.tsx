import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { api } from '../services/api';
import { Search, Plus, Filter } from 'lucide-react';
import type { CredefDossier } from '../types';
import { CreateDossierModal } from '../components/CreateDossierModal';

export const Dossiers: React.FC = () => {
  const [dossiers, setDossiers] = useState<CredefDossier[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('');
  const [isModalOpen, setIsModalOpen] = useState(false);

  useEffect(() => {
    loadDossiers();
  }, [statusFilter]);

  const loadDossiers = async () => {
    try {
      const filters = statusFilter ? { statut: statusFilter } : {};
      const data = await api.getDossiers(filters);
      setDossiers(data);
    } catch (error) {
      console.error('Erreur chargement dossiers:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDossierCreated = (newDossier: CredefDossier) => {
    setDossiers([newDossier, ...dossiers]);
  };

  const filteredDossiers = dossiers.filter((dossier) =>
    dossier.ref.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const getStatutColor = (statut: string) => {
    if (statut === 'CLOS') return 'bg-green-100 text-green-800';
    if (statut === 'REJET_ADMIN') return 'bg-red-100 text-red-800';
    if (statut.includes('VALIDÉ')) return 'bg-blue-100 text-blue-800';
    return 'bg-yellow-100 text-yellow-800';
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* En-tête */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Dossiers CREDEF</h1>
          <p className="mt-2 text-gray-600">Gestion des dossiers de crédit</p>
        </div>
        <button
          onClick={() => setIsModalOpen(true)}
          className="btn-primary flex items-center gap-2"
        >
          <Plus className="h-5 w-5" />
          Nouveau Dossier
        </button>
      </div>

      {/* Filtres et recherche */}
      <div className="card">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {/* Recherche */}
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <Search className="h-5 w-5 text-gray-400" />
            </div>
            <input
              type="text"
              placeholder="Rechercher par référence..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="input-field pl-10"
            />
          </div>

          {/* Filtre par statut */}
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <Filter className="h-5 w-5 text-gray-400" />
            </div>
            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              className="input-field pl-10"
            >
              <option value="">Tous les statuts</option>
              <option value="BROUILLON">Brouillon</option>
              <option value="DÉPOSÉ">Déposé</option>
              <option value="EN_CONTROLE_SACV">En contrôle SACV</option>
              <option value="VALIDÉ_COMITE">Validé comité</option>
              <option value="CLOS">Clos</option>
              <option value="REJET_ADMIN">Rejeté</option>
            </select>
          </div>
        </div>
      </div>

      {/* Liste des dossiers */}
      <div className="card">
        {filteredDossiers.length === 0 ? (
          <p className="text-gray-500 text-center py-8">
            {searchTerm
              ? 'Aucun dossier ne correspond à votre recherche'
              : 'Aucun dossier pour le moment'}
          </p>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Référence
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Adhérent
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Montant Demandé
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Durée
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Statut
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Mois
                  </th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {filteredDossiers.map((dossier) => (
                  <tr key={dossier.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm font-medium text-gray-900">{dossier.ref}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-700">
                        {dossier.adherent_id || '-'}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-900">
                        {dossier.montant_demande?.toLocaleString('fr-FR')} €
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-700">
                        {dossier.duree_mois} mois
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span
                        className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${getStatutColor(
                          dossier.statut
                        )}`}
                      >
                        {dossier.statut}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {dossier.mois_traitement || '-'}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                      <Link
                        to={`/dossiers/${dossier.id}`}
                        className="text-primary-600 hover:text-primary-900"
                      >
                        Détails
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        <div className="mt-4 flex items-center justify-between border-t border-gray-200 pt-4">
          <div className="text-sm text-gray-700">
            <span className="font-medium">{filteredDossiers.length}</span> dossier(s)
          </div>
        </div>
      </div>

      {/* Modal de création */}
      <CreateDossierModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onSuccess={handleDossierCreated}
      />
    </div>
  );
};
