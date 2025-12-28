import { Chapter } from '../types/chapter';

const API_BASE_URL = (typeof window !== 'undefined' && window.REACT_APP_API_BASE_URL) || 'http://localhost:8000';

export const getAllChapters = async (): Promise<Chapter[]> => {
  try {
    const response = await fetch(`${API_BASE_URL}/chapters/`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error('Error fetching chapters:', error);
    throw error;
  }
};

export const getChapterById = async (id: number): Promise<Chapter> => {
  try {
    const response = await fetch(`${API_BASE_URL}/chapters/${id}`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error(`Error fetching chapter with id ${id}:`, error);
    throw error;
  }
};