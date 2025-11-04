// Types pour l'application FPMsigm

export interface User {
  id: number;
  email: string;
  nom: string;
  prenom: string;
  role: UserRole;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export type UserRole = 'ADMIN' | 'SACV' | 'DCFF' | 'DCPRE' | 'DTR' | 'ADHERENT';

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData {
  email: string;
  password: string;
  nom: string;
  prenom: string;
  role: UserRole;
}

export interface AuthResponse {
  access_token: string;
  refresh_token: string;
  user: User;
}

export interface CredefDossier {
  id: number;
  ref: string;
  adherent_id?: number;
  date_depot?: string;
  montant_demande?: number;
  montant_accorde?: number;
  taux?: number;
  duree_mois?: number;
  statut: DossierStatut;
  mois_traitement?: string;
  acteur_courant_id?: number;
  commentaire_rejet?: string;
}

export type DossierStatut =
  | 'BROUILLON'
  | 'DÉPOSÉ'
  | 'EN_CONTROLE_SACV'
  | 'TRANSMIS_COURRIER'
  | 'EN_ETUDE_PRET'
  | 'SOUMIS_COMITE'
  | 'VALIDÉ_COMITE'
  | 'ETATS_EDITES'
  | 'EN_SIGNATURE_DCFF_DCPRE'
  | 'TRANSMIS_DTR'
  | 'DECAISSE_ECOBANK'
  | 'CLOS'
  | 'REJET_ADMIN';

export interface WorkflowLog {
  id: number;
  dossier_id: number;
  statut_from: DossierStatut | null;
  statut_to: DossierStatut;
  acteur_id?: number;
  role?: string;
  commentaire?: string;
  created_at: string;
}

export interface PieceJointe {
  id: number;
  dossier_id: number;
  type_piece: TypePiece;
  nom_fichier: string;
  taille_octets: number;
  mime_type?: string;
  est_obligatoire: boolean;
  est_valide: boolean;
  uploaded_by?: number;
  commentaire?: string;
  created_at: string;
}

export type TypePiece =
  | 'CNI'
  | 'BULLETIN_PAIE'
  | 'ATTESTATION_TRAVAIL'
  | 'RIB'
  | 'JUSTIFICATIF_DOMICILE'
  | 'PHOTO'
  | 'AUTRE';

export interface ApiError {
  error: string;
}
