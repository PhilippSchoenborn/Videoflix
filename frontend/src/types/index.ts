// User and Authentication Types
export interface User {
  id: number;
  email: string;
  username: string;
  first_name: string;
  last_name: string;
  is_email_verified: boolean;
  date_of_birth?: string;
  profile_image?: string;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData {
  email: string;
  username: string;
  password: string;
  password_confirm: string;
  first_name?: string;
  last_name?: string;
}

export interface AuthResponse {
  token: string;
  user: User;
}

export interface PasswordResetRequest {
  email: string;
}

export interface PasswordReset {
  token: string;
  password: string;
  password_confirm: string;
}

// Video Types
export interface Genre {
  id: number;
  name: string;
  description?: string;
}

export interface Video {
  id: number;
  title: string;
  description: string;
  thumbnail: string | null;
  genre: Genre;
  duration: string; // Django DurationField as string
  age_rating: 'FSK 0' | 'FSK 6' | 'FSK 12' | 'FSK 16' | 'FSK 18';
  created_at: string;
  updated_at?: string;
  is_featured: boolean;
  video_files?: VideoFile[];
}

export interface VideoFile {
  id: number;
  video: number;
  quality: '120p' | '360p' | '480p' | '720p' | '1080p';
  file: string;
  file_size: number;
  is_processed: boolean;
}

export interface VideoDetail extends Video {
  video_files: VideoFile[];
}

export interface WatchProgress {
  id: number;
  user: number;
  video: Video;
  progress_seconds: number;
  progress_percentage?: number;
  last_resolution?: string;
  last_watched: string;
  completed: boolean;
}

// Pagination Types
export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

// API Response Types
export interface ApiResponse<T> {
  data: T;
  message?: string;
}

export interface ApiError {
  error: string;
  detail?: string;
}

// Video Player Types
export interface VideoQuality {
  quality: string;
  file_size: number;
}

export interface VideoStreamData {
  video_url: string;
  quality: string;
  file_size: number;
}

export interface QualityOptions {
  available_qualities: VideoQuality[];
  recommended_quality: string;
}

// Dashboard Types
export interface GenreWithVideos {
  id: number;
  name: string;
  description?: string;
  videos: Video[];
}

export interface VideoUploadData {
  title: string;
  description: string;
  genre: number;
  age_rating: 'FSK 0' | 'FSK 6' | 'FSK 12' | 'FSK 16' | 'FSK 18';
  video_file: File;
}

export interface SearchFilters {
  genre?: number;
  search?: string;
  age_rating?: string;
  featured?: boolean;
}

export interface DashboardStats {
  total_videos: number;
  total_genres: number;
  watch_progress_count: number;
  completed_videos: number;
}

// Form Validation
export interface FormErrors {
  [key: string]: string[];
}
