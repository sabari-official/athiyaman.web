import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { Alert } from './index';

describe('Alert Component', () => {
  it('renders info alert', () => {
    render(<Alert type="info">Info message</Alert>);
    expect(screen.getByText('Info message')).toBeInTheDocument();
  });

  it('renders success alert', () => {
    render(<Alert type="success">Success message</Alert>);
    expect(screen.getByText('Success message')).toBeInTheDocument();
  });

  it('renders warning alert', () => {
    render(<Alert type="warning">Warning message</Alert>);
    expect(screen.getByText('Warning message')).toBeInTheDocument();
  });

  it('renders error alert', () => {
    render(<Alert type="error">Error message</Alert>);
    expect(screen.getByText('Error message')).toBeInTheDocument();
  });

  it('applies correct background color for info', () => {
    render(<Alert type="info">Message</Alert>);
    const alert = screen.getByText('Message').closest('div');
    expect(alert).toHaveClass('bg-blue-50');
  });

  it('applies correct background color for success', () => {
    render(<Alert type="success">Message</Alert>);
    const alert = screen.getByText('Message').closest('div');
    expect(alert).toHaveClass('bg-green-50');
  });

  it('applies correct background color for warning', () => {
    render(<Alert type="warning">Message</Alert>);
    const alert = screen.getByText('Message').closest('div');
    expect(alert).toHaveClass('bg-yellow-50');
  });

  it('applies correct background color for error', () => {
    render(<Alert type="error">Message</Alert>);
    const alert = screen.getByText('Message').closest('div');
    expect(alert).toHaveClass('bg-red-50');
  });

  it('renders with title', () => {
    render(
      <Alert type="info" title="Attention">
        Please read this
      </Alert>
    );
    expect(screen.getByText('Attention')).toBeInTheDocument();
  });

  it('renders with dismissible option', () => {
    const handleDismiss = vi.fn();
    render(
      <Alert type="info" onClose={handleDismiss} dismissible>
        Message
      </Alert>
    );
    
    const closeButton = screen.getByRole('button');
    closeButton.click();
    
    expect(handleDismiss).toHaveBeenCalled();
  });
});
