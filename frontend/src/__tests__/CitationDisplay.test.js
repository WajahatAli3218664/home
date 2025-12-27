// Test for the CitationDisplay component
import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import CitationDisplay from '../components/CitationDisplay';

describe('CitationDisplay', () => {
  test('renders citations in inline style', () => {
    const citations = ['Chapter 3 - Embodied Cognition (p. 45)', 'Chapter 5 - Sensorimotor Learning (p. 78)'];
    
    render(<CitationDisplay citations={citations} />);
    
    const labelElement = screen.getByText(/Sources:/i);
    expect(labelElement).toBeInTheDocument();
    
    expect(screen.getByText('Chapter 3 - Embodied Cognition (p. 45)')).toBeInTheDocument();
    expect(screen.getByText('Chapter 5 - Sensorimotor Learning (p. 78)')).toBeInTheDocument();
  });

  test('renders citations in list style', () => {
    const citations = ['Chapter 3 - Embodied Cognition (p. 45)'];
    
    render(<CitationDisplay citations={citations} style="list" />);
    
    const headerElement = screen.getByText(/References:/i);
    expect(headerElement).toBeInTheDocument();
    
    expect(screen.getByText('Chapter 3 - Embodied Cognition (p. 45)')).toBeInTheDocument();
  });

  test('does not render when no citations provided', () => {
    render(<CitationDisplay citations={[]} />);
    
    const labelElement = screen.queryByText(/Sources:/i);
    expect(labelElement).not.toBeInTheDocument();
  });

  test('handles single citation', () => {
    const citations = ['Chapter 2 - Introduction (p. 15)'];
    
    render(<CitationDisplay citations={citations} />);
    
    expect(screen.getByText('Chapter 2 - Introduction (p. 15)')).toBeInTheDocument();
  });
});