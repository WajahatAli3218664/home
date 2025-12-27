import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import QdrantSearch from './QdrantSearch';

// Mock fetch API for testing
global.fetch = jest.fn();

describe('QdrantSearch Component', () => {
  beforeEach(() => {
    fetch.mockClear();
  });

  test('renders search input and button', () => {
    render(<QdrantSearch />);
    
    const inputElement = screen.getByPlaceholderText('Enter your search query...');
    const buttonElement = screen.getByRole('button', { name: /Search/i });
    
    expect(inputElement).toBeInTheDocument();
    expect(buttonElement).toBeInTheDocument();
  });

  test('updates input value on change', () => {
    render(<QdrantSearch />);
    
    const inputElement = screen.getByPlaceholderText('Enter your search query...');
    fireEvent.change(inputElement, { target: { value: 'test query' } });
    
    expect(inputElement.value).toBe('test query');
  });

  test('submits search query when button is clicked', async () => {
    const mockResults = [
      {
        content: 'Test content snippet',
        source: 'https://example.com/test',
        score: 0.92
      }
    ];
    
    fetch.mockResolvedValueOnce({
      json: () => Promise.resolve({ results: mockResults }),
      ok: true
    });

    render(<QdrantSearch />);
    
    const inputElement = screen.getByPlaceholderText('Enter your search query...');
    fireEvent.change(inputElement, { target: { value: 'test query' } });
    
    const buttonElement = screen.getByRole('button', { name: /Search/i });
    fireEvent.click(buttonElement);
    
    await waitFor(() => {
      expect(screen.getByText('Test content snippet')).toBeInTheDocument();
    });
  });

  test('shows error message when API call fails', async () => {
    fetch.mockRejectedValueOnce(new Error('Network error'));
    
    render(<QdrantSearch />);
    
    const inputElement = screen.getByPlaceholderText('Enter your search query...');
    fireEvent.change(inputElement, { target: { value: 'test query' } });
    
    const buttonElement = screen.getByRole('button', { name: /Search/i });
    fireEvent.click(buttonElement);
    
    await waitFor(() => {
      expect(screen.getByText(/Failed to retrieve results/i)).toBeInTheDocument();
    });
  });
});