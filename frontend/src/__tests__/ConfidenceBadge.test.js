// Basic test for the ConfidenceBadge component
import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import ConfidenceBadge from '../components/ConfidenceBadge';

describe('ConfidenceBadge', () => {
  test('renders with HIGH confidence', () => {
    render(<ConfidenceBadge level="HIGH" />);
    const badgeElement = screen.getByText(/High Confidence/i);
    expect(badgeElement).toBeInTheDocument();
    expect(badgeElement).toHaveClass('confidence-high');
  });

  test('renders with MEDIUM confidence', () => {
    render(<ConfidenceBadge level="MEDIUM" />);
    const badgeElement = screen.getByText(/Medium Confidence/i);
    expect(badgeElement).toBeInTheDocument();
    expect(badgeElement).toHaveClass('confidence-medium');
  });

  test('renders with LOW confidence', () => {
    render(<ConfidenceBadge level="LOW" />);
    const badgeElement = screen.getByText(/Low Confidence/i);
    expect(badgeElement).toBeInTheDocument();
    expect(badgeElement).toHaveClass('confidence-low');
  });

  test('renders with unknown confidence level', () => {
    render(<ConfidenceBadge level="UNKNOWN" />);
    const badgeElement = screen.getByText(/Unknown Confidence/i);
    expect(badgeElement).toBeInTheDocument();
    expect(badgeElement).toHaveClass('confidence-unknown');
  });

  test('renders without level prop', () => {
    render(<ConfidenceBadge />);
    const badgeElement = screen.getByText(/Unknown Confidence/i);
    expect(badgeElement).toBeInTheDocument();
    expect(badgeElement).toHaveClass('confidence-unknown');
  });
});