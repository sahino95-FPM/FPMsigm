import React from 'react';

interface LogoProps {
  className?: string;
  size?: 'small' | 'medium' | 'large';
}

export const Logo: React.FC<LogoProps> = ({ className = '', size = 'medium' }) => {
  const sizeClasses = {
    small: 'h-8',
    medium: 'h-12',
    large: 'h-16',
  };

  // Pour l'instant, afficher un placeholder
  // L'utilisateur pourra remplacer par le vrai logo FPM
  return (
    <div className={`flex items-center gap-2 ${className}`}>
      {/* Placeholder pour le logo FPM */}
      <div className={`${sizeClasses[size]} aspect-square bg-primary-600 rounded-lg flex items-center justify-center`}>
        <span className="text-white font-bold text-lg">FPM</span>
      </div>

      {/* Pour utiliser une vraie image, décommentez ceci et commentez le div ci-dessus :
      <img
        src="/logo-fpm.png"
        alt="Logo FPM"
        className={`${sizeClasses[size]} object-contain`}
      />
      */}
    </div>
  );
};

/**
 * Instructions pour ajouter le vrai logo FPM :
 *
 * 1. Placez votre fichier logo (logo-fpm.png, logo-fpm.svg, etc.) dans le dossier :
 *    frontend/public/
 *
 * 2. Dans ce fichier (Logo.tsx), décommentez la balise <img> et commentez le <div> placeholder
 *
 * 3. Ajustez le nom du fichier dans src="/logo-fpm.png" selon votre fichier
 *
 * Formats recommandés :
 * - PNG avec fond transparent (pour meilleure qualité)
 * - SVG (pour un logo vectoriel qui s'adapte à toutes les tailles)
 *
 * Taille recommandée : Au moins 200x200 pixels
 */
