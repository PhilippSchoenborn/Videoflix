import axios from 'axios';
import type { AxiosInstance } from 'axios';
import type {
  User,
  LoginCredentials,
  RegisterData,
  AuthResponse,
  PasswordResetRequest,
  PasswordReset,
  Video,
  VideoDetail,
  Genre,
  WatchProgress,
  GenreWithVideos,
  VideoStreamData,
  QualityOptions,
} from '../types';

class ApiService {
  private api: AxiosInstance;
  private baseURL = 'http://localhost:8000/api'; // Django backend URL

  constructor() {
    this.api = axios.create({
      baseURL: this.baseURL,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Add request interceptor to include auth token
    this.api.interceptors.request.use((config) => {
      const token = localStorage.getItem('auth_token');
      if (token) {
        config.headers.Authorization = `Token ${token}`;
      }
      return config;
    });

    // Add response interceptor for error handling
    this.api.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          // Unauthorized - clear token and redirect to login
          localStorage.removeItem('auth_token');
          window.location.href = '/login';
        }
        return Promise.reject(error);
      }
    );
  }

  // Authentication Methods
  async login(credentials: LoginCredentials): Promise<AuthResponse> {
    const response = await this.api.post<AuthResponse>('/auth/login/', credentials);
    if (response.data.token) {
      localStorage.setItem('auth_token', response.data.token);
    }
    return response.data;
  }

  async register(data: RegisterData): Promise<AuthResponse> {
    const response = await this.api.post<AuthResponse>('/auth/register/', data);
    if (response.data.token) {
      localStorage.setItem('auth_token', response.data.token);
    }
    return response.data;
  }

  async logout(): Promise<void> {
    try {
      await this.api.post('/auth/logout/');
    } finally {
      localStorage.removeItem('auth_token');
    }
  }

  async requestPasswordReset(data: PasswordResetRequest): Promise<{ message: string }> {
    const response = await this.api.post('/auth/password-reset/request/', data);
    return response.data;
  }

  async resetPassword(data: PasswordReset): Promise<{ message: string }> {
    const response = await this.api.post('/auth/password-reset/', data);
    return response.data;
  }

  async verifyEmail(token: string): Promise<{ message: string }> {
    const response = await this.api.get(`/auth/verify-email/${token}/`);
    return response.data;
  }

  async getUserProfile(): Promise<User> {
    const response = await this.api.get<User>('/auth/profile/');
    return response.data;
  }

  async updateUserProfile(data: Partial<User>): Promise<User> {
    const response = await this.api.patch<User>('/auth/profile/', data);
    return response.data;
  }

  // Video Methods
  async getVideos(params?: {
    genre?: number;
    search?: string;
    page?: number;
  }): Promise<Video[]> {
    const response = await this.api.get<Video[]>('/videos/', { params });
    return response.data;
  }

  async getVideoDetail(id: number): Promise<VideoDetail> {
    const response = await this.api.get<VideoDetail>(`/videos/${id}/`);
    return response.data;
  }

  async getFeaturedVideos(): Promise<Video[]> {
    const response = await this.api.get<Video[]>('/videos/featured/');
    return response.data;
  }

  async getVideosByGenre(): Promise<GenreWithVideos[]> {
    const response = await this.api.get<GenreWithVideos[]>('/videos/by-genre/');
    return response.data;
  }

  async getVideoStream(videoId: number, quality: string): Promise<VideoStreamData> {
    const response = await this.api.get<VideoStreamData>(`/videos/${videoId}/stream/${quality}/`);
    return response.data;
  }

  async getVideoQualityOptions(videoId: number): Promise<QualityOptions> {
    const response = await this.api.get<QualityOptions>(`/videos/${videoId}/quality-options/`);
    return response.data;
  }

  // Genre Methods
  async getGenres(): Promise<Genre[]> {
    const response = await this.api.get<Genre[]>('/videos/genres/');
    return response.data;
  }

  // Watch Progress Methods
  async getWatchProgress(): Promise<WatchProgress[]> {
    const response = await this.api.get<WatchProgress[]>('/videos/watch-progress/');
    return response.data;
  }

  async getContinueWatching(): Promise<WatchProgress[]> {
    const response = await this.api.get<WatchProgress[]>('/videos/continue-watching/');
    return response.data;
  }

  async updateWatchProgress(
    videoId: number,
    progressSeconds: number
  ): Promise<WatchProgress> {
    const response = await this.api.post<WatchProgress>(
      `/videos/${videoId}/watch-progress/`,
      { progress_seconds: progressSeconds }
    );
    return response.data;
  }

  // Utility Methods
  isAuthenticated(): boolean {
    return !!localStorage.getItem('auth_token');
  }

  getAuthToken(): string | null {
    return localStorage.getItem('auth_token');
  }

  clearAuth(): void {
    localStorage.removeItem('auth_token');
  }
}

// Create and export singleton instance
export const apiService = new ApiService();
export default apiService;
