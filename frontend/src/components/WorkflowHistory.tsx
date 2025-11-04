import React, { useEffect, useState } from 'react';
import { api } from '../services/api';
import { Clock, User, MessageSquare, ArrowRight } from 'lucide-react';
import type { WorkflowLog } from '../types';
import { format } from 'date-fns';
import { fr } from 'date-fns/locale';

interface WorkflowHistoryProps {
  dossierId: number;
}

export const WorkflowHistory: React.FC<WorkflowHistoryProps> = ({ dossierId }) => {
  const [logs, setLogs] = useState<WorkflowLog[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadHistory();
  }, [dossierId]);

  const loadHistory = async () => {
    try {
      const data = await api.getWorkflowHistory(dossierId);
      setLogs(data.historique);
    } catch (error) {
      console.error('Erreur chargement historique:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center py-8">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  if (logs.length === 0) {
    return (
      <p className="text-gray-500 text-center py-8">Aucun historique de transition</p>
    );
  }

  return (
    <div className="space-y-4">
      {logs.map((log, index) => (
        <div key={log.id} className="relative">
          {/* Ligne de connexion */}
          {index < logs.length - 1 && (
            <div className="absolute left-4 top-12 bottom-0 w-0.5 bg-gray-200"></div>
          )}

          {/* Événement */}
          <div className="flex gap-4">
            {/* Icône */}
            <div className="flex-shrink-0">
              <div className="h-8 w-8 rounded-full bg-primary-100 flex items-center justify-center">
                <ArrowRight className="h-4 w-4 text-primary-600" />
              </div>
            </div>

            {/* Contenu */}
            <div className="flex-1 bg-gray-50 rounded-lg p-4 border border-gray-200">
              <div className="flex items-start justify-between flex-wrap gap-2">
                <div className="flex-1">
                  <div className="flex items-center gap-2 flex-wrap">
                    {log.statut_from && (
                      <>
                        <span className="text-sm font-medium text-gray-700">
                          {log.statut_from.replace(/_/g, ' ')}
                        </span>
                        <ArrowRight className="h-4 w-4 text-gray-400" />
                      </>
                    )}
                    <span className="text-sm font-bold text-gray-900">
                      {log.statut_to.replace(/_/g, ' ')}
                    </span>
                  </div>

                  {/* Métadonnées */}
                  <div className="mt-2 flex flex-wrap items-center gap-4 text-xs text-gray-500">
                    <div className="flex items-center gap-1">
                      <Clock className="h-3 w-3" />
                      {format(new Date(log.created_at), 'dd MMM yyyy HH:mm', { locale: fr })}
                    </div>
                    {log.role && (
                      <div className="flex items-center gap-1">
                        <User className="h-3 w-3" />
                        {log.role}
                      </div>
                    )}
                    {log.acteur_id && (
                      <span>Acteur #{log.acteur_id}</span>
                    )}
                  </div>

                  {/* Commentaire */}
                  {log.commentaire && (
                    <div className="mt-2 flex items-start gap-1 text-sm text-gray-700">
                      <MessageSquare className="h-4 w-4 text-gray-400 flex-shrink-0 mt-0.5" />
                      <p>{log.commentaire}</p>
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};
