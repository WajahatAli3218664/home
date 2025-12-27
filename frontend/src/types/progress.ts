export interface ProgressRecord {
  id: number;
  user_id: number;
  chapter_id: number;
  chapter_title: string; // This would be populated by the backend
  content_version: string;
  progress_percentage: number; // 0-100
  last_accessed: string; // ISO date string
  completed: boolean;
  quiz_score?: any; // JSON object for quiz scores
  time_spent: number; // in seconds
}