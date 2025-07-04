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
  thumbnail: string;
  genre: Genre;
  duration: string; // Django DurationField as string
  created_at: string;
  updated_at: string;
  is_featured: boolean;
}

export interface VideoFile {
  id: number;
  video: number;
  quality: '120p' | '360p' | '720p' | '1080p';
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
  last_watched: string;
  completed: boolean;
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
  genre: Genre;
  videos: Video[];
}

// Form Validation
export interface FormErrors {
  [key: string]: string[];
}
