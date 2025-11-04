import React from 'react';
import type { DossierStatut } from '../types';

interface StatusBadgeProps {
  statut: DossierStatut;
  size?: 'sm' | 'md' | 'lg';
}

export const StatusBadge: React.FC<StatusBadgeProps> = ({ statut, size = 'md' }) => {
  const getStatusColor = (s: DossierStatut) => {
    if (s === 'CLOS') return 'bg-green-100 text-green-800 border-green-200';
    if (s === 'REJET_ADMIN') return 'bg-red-100 text-red-800 border-red-200';
    if (s.includes('VALIDÉ')) return 'bg-blue-100 text-blue-800 border-blue-200';
    if (s === 'BROUILLON') return 'bg-gray-100 text-gray-800 border-gray-200';
    return 'bg-yellow-100 text-yellow-800 border-yellow-200';
  };

  const sizes = {
    sm: 'px-2 py-0.5 text-xs',
    md: 'px-2.5 py-1 text-sm',
    lg: 'px-3 py-1.5 text-base',
  };

  return (
    <span
      className={`inline-flex items-center font-semibold rounded-full border ${getStatusColor(
        statut
      )} ${sizes[size]}`}
    >
      {statut.replace(/_/g, ' ')}
    </span>
  );
};
