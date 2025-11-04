import axios, { AxiosInstance, AxiosRequestConfig } from 'axios';
import type {
  User,
  LoginCredentials,
  RegisterData,
  AuthResponse,
  CredefDossier,
  WorkflowLog,
  PieceJointe,
} from '../types';

// Configuration de base d'axios
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';

class ApiService {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Intercepteur pour ajouter le token JWT
    this.client.interceptors.request.use((config) => {
      const token = localStorage.getItem('access_token');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    });

    // Intercepteur pour gérer les erreurs 401 (token expiré)
    this.client.interceptors.response.use(
      (response) => response,
      async (error) => {
        if (error.response?.status === 401) {
          // Token expiré, déconnecter l'utilisateur
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
          localStorage.removeItem('user');
          window.location.href = '/login';
        }
        return Promise.reject(error);
      }
    );
  }

  // ==================== AUTHENTIFICATION ====================

  async register(data: RegisterData): Promise<{ message: string; user: User }> {
    const response = await this.client.post('/auth/register', data);
    return response.data;
  }

  async login(credentials: LoginCredentials): Promise<AuthResponse> {
    const response = await this.client.post('/auth/login', credentials);
    const { access_token, refresh_token, user } = response.data;

    // Stocker les tokens et l'utilisateur
    localStorage.setItem('access_token', access_token);
    localStorage.setItem('refresh_token', refresh_token);
    localStorage.setItem('user', JSON.stringify(user));

    return response.data;
  }

  async getMe(): Promise<User> {
    const response = await this.client.get('/auth/me');
    return response.data;
  }

  async getRoles(): Promise<{ roles: string[] }> {
    const response = await this.client.get('/auth/roles');
    return response.data;
  }

  logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
  }

  // ==================== DOSSIERS CREDEF ====================

  async getDossiers(filters?: { statut?: string; mois?: string }): Promise<CredefDossier[]> {
    const params = new URLSearchParams();
    if (filters?.statut) params.append('statut', filters.statut);
    if (filters?.mois) params.append('mois', filters.mois);

    const response = await this.client.get(`/credef/dossiers?${params.toString()}`);
    return response.data;
  }

  async createDossier(data: Partial<CredefDossier>): Promise<CredefDossier> {
    const response = await this.client.post('/credef/dossiers', data);
    return response.data;
  }

  async transitionDossier(
    dossierId: number,
    data: { to: string; role?: string; note?: string; acteur_id?: number }
  ): Promise<CredefDossier> {
    const response = await this.client.post(`/credef/dossiers/${dossierId}/transition`, data);
    return response.data;
  }

  async getWorkflowHistory(dossierId: number): Promise<{
    dossier_id: number;
    dossier_ref: string;
    statut_actuel: string;
    historique: WorkflowLog[];
  }> {
    const response = await this.client.get(`/credef/dossiers/${dossierId}/workflow`);
    return response.data;
  }

  // ==================== PIÈCES JOINTES ====================

  async uploadPiece(
    dossierId: number,
    file: File,
    typePiece: string,
    uploadedBy?: number,
    commentaire?: string
  ): Promise<PieceJointe> {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('type_piece', typePiece);
    if (uploadedBy) formData.append('uploaded_by', uploadedBy.toString());
    if (commentaire) formData.append('commentaire', commentaire);

    const response = await this.client.post(`/credef/dossiers/${dossierId}/pieces`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  }

  async getPieces(dossierId: number): Promise<{
    dossier_id: number;
    dossier_ref: string;
    pieces: PieceJointe[];
  }> {
    const response = await this.client.get(`/credef/dossiers/${dossierId}/pieces`);
    return response.data;
  }

  async validateCompletude(dossierId: number): Promise<{
    dossier_id: number;
    dossier_ref: string;
    complet: boolean;
    pieces_manquantes: string[];
    types_obligatoires: string[];
  }> {
    const response = await this.client.get(`/credef/dossiers/${dossierId}/pieces/validation`);
    return response.data;
  }

  async deletePiece(pieceId: number): Promise<{ message: string }> {
    const response = await this.client.delete(`/credef/pieces/${pieceId}`);
    return response.data;
  }
}

export const api = new ApiService();
