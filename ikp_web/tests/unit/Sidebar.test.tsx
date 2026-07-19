import { render, screen, fireEvent } from '@testing-library/react';
import { Sidebar } from '../../src/components/Sidebar';
import { describe, it, expect, vi } from 'vitest';

describe('Sidebar Component', () => {
  it('renders all navigation buttons', () => {
    const setActiveTab = vi.fn();
    render(<Sidebar activeTab="query" setActiveTab={setActiveTab} />);
    
    expect(screen.getByText('Solution Synthesis')).toBeInTheDocument();
    expect(screen.getByText('Graph Dashboard')).toBeInTheDocument();
    expect(screen.getByText('BOQ Validation')).toBeInTheDocument();
    expect(screen.getByText('Semantic Search')).toBeInTheDocument();
    expect(screen.getByText('Knowledge Transfer')).toBeInTheDocument();
    expect(screen.getByText('Validation Portal')).toBeInTheDocument();
  });

  it('calls setActiveTab when a button is clicked', () => {
    const setActiveTab = vi.fn();
    render(<Sidebar activeTab="query" setActiveTab={setActiveTab} />);
    
    const dashboardButton = screen.getByText('Graph Dashboard');
    fireEvent.click(dashboardButton);
    
    expect(setActiveTab).toHaveBeenCalledWith('dashboard');
  });

  it('highlights the active tab', () => {
    const setActiveTab = vi.fn();
    render(<Sidebar activeTab="boq" setActiveTab={setActiveTab} />);
    
    const boqButton = screen.getByText('BOQ Validation').closest('button');
    expect(boqButton).toHaveStyle({ background: 'rgba(255,255,255,0.1)' });
  });
});
