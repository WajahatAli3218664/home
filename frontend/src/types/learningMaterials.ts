export interface LearningMaterial {
  id: number;
  chapter_id: number;
  material_type: 'summary' | 'quiz' | 'learning_booster';
  content: string;
  version: string;
  metadata?: any;
  created_at: string;
  updated_at: string;
}

export interface QuizQuestion {
  id: number;
  question: string;
  options: string[];
  correctAnswer: number; // Index of the correct option
}