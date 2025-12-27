export interface Chapter {
  id: number;
  title: string;
  slug: string;
  content: string;
  version: string;
  position: number;
  word_count: number;
  estimated_reading_time: number; // in minutes
  metadata?: any; // JSON string for additional metadata
}