import React, { useEffect, useState } from 'react';
import { useAuthStore } from '../stores/authStore';
import { api } from '../services/api';
import { FolderOpen, Clock, CheckCircle, XCircle, TrendingUp } from 'lucide-react';
import type { CredefDossier } from '../types';

interface KPICardProps {
  title: string;
  value: number;
  icon: React.ElementType;
  color: 'blue' | 'yellow' | 'green' | 'red';
  subtitle?: string;
}

const KPICard: React.FC<KPICardProps> = ({ title, value, icon: Icon, color, subtitle }) => {
  const colors = {
    blue: 'bg-blue-500',
    yellow: 'bg-yellow-500',
    green: 'bg-green-500',
    red: 'bg-red-500',
  };

  return (
    <div className="card">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-gray-600">{title}</p>
          <p className="text-3xl font-bold text-gray-900 mt-2">{value}</p>
          {subtitle && <p className="text-xs text-gray-500 mt-1">{subtitle}</p>}
        </div>
        <div className={`p-3 rounded-lg ${colors[color]}`}>
          <Icon className="h-6 w-6 text-white" />
        </div>
      </div>
    </div>
  );
};

export const Dashboard: React.FC = () => {
  const { user } = useAuthStore();
  const [dossiers, setDossiers] = useState<CredefDossier[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDossiers();
  }, []);

  const loadDossiers = async () => {
    try {
      const data = await api.getDossiers();
      setDossiers(data);
    } catch (error) {
      console.error('Erreur chargement dossiers:', error);
    } finally {
      setLoading(false);
    }
  };

  // Calcul des KPIs
  const totalDossiers = dossiers.length;
  const dossiersEnCours = dossiers.filter(
    (d) => !['CLOS', 'REJET_ADMIN'].includes(d.statut)
  ).length;
  const dossiersValides = dossiers.filter((d) => d.statut === 'VALIDÉ_COMITE').length;
  const dossiersClos = dossiers.filter((d) => d.statut === 'CLOS').length;

  // Dossiers récents
  const dossiersRecents = dossiers.slice(0, 5);

  const getStatutColor = (statut: string) => {
    if (statut === 'CLOS') return 'text-green-600 bg-green-50';
    if (statut === 'REJET_ADMIN') return 'text-red-600 bg-red-50';
    if (statut.includes('VALIDÉ')) return 'text-blue-600 bg-blue-50';
    return 'text-yellow-600 bg-yellow-50';
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
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p className="mt-2 text-gray-600">
          Bienvenue, {user?.prenom} {user?.nom} ({user?.role})
        </p>
      </div>

      {/* KPIs */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <KPICard
          title="Total Dossiers"
          value={totalDossiers}
          icon={FolderOpen}
          color="blue"
          subtitle="Tous les dossiers"
        />
        <KPICard
          title="En Cours"
          value={dossiersEnCours}
          icon={Clock}
          color="yellow"
          subtitle="Dossiers actifs"
        />
        <KPICard
          title="Validés"
          value={dossiersValides}
          icon={CheckCircle}
          color="green"
          subtitle="Validés par le comité"
        />
        <KPICard
          title="Clôturés"
          value={dossiersClos}
          icon={TrendingUp}
          color="blue"
          subtitle="Dossiers finalisés"
        />
      </div>

      {/* Dossiers récents */}
      <div className="card">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-bold text-gray-900">Dossiers Récents</h2>
          <a
            href="/dossiers"
            className="text-sm text-primary-600 hover:text-primary-700 font-medium"
          >
            Voir tout →
          </a>
        </div>

        {dossiersRecents.length === 0 ? (
          <p className="text-gray-500 text-center py-8">Aucun dossier pour le moment</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Référence
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Montant
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Statut
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Mois
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {dossiersRecents.map((dossier) => (
                  <tr key={dossier.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                      {dossier.ref}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-700">
                      {dossier.montant_demande?.toLocaleString('fr-FR')} €
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span
                        className={`px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full ${getStatutColor(
                          dossier.statut
                        )}`}
                      >
                        {dossier.statut}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {dossier.mois_traitement || '-'}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};
