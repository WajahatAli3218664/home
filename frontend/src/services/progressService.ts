import { ProgressRecord } from '../types/progress';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

export const getProgressForUser = async (userId: number): Promise<ProgressRecord[]> => {
  try {
    const response = await fetch(`${API_BASE_URL}/progress/?user_id=${userId}`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error(`Error fetching progress for user ${userId}:`, error);
    throw error;
  }
};