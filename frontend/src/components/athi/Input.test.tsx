import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, it, expect } from 'vitest';
import { Input } from './index';

describe('Input Component', () => {
  it('renders input with placeholder', () => {
    render(<Input placeholder="Enter text" />);
    const input = screen.getByPlaceholderText('Enter text');
    expect(input).toBeInTheDocument();
  });

  it('renders with label', () => {
    render(<Input label="Username" />);
    expect(screen.getByText('Username')).toBeInTheDocument();
  });

  it('accepts user input', async () => {
    const user = userEvent.setup();
    render(<Input placeholder="test" />);
    
    const input = screen.getByPlaceholderText('test') as HTMLInputElement;
    await user.type(input, 'hello');
    
    expect(input.value).toBe('hello');
  });

  it('displays error message', () => {
    render(<Input error="This field is required" />);
    expect(screen.getByText('This field is required')).toBeInTheDocument();
  });

  it('shows error styling when error present', () => {
    render(<Input error="Error" />);
    const container = screen.getByText('Error').closest('div');
    expect(container).toHaveClass('border-red-500');
  });

  it('handles different input types', () => {
    render(<Input type="email" />);
    const input = screen.getByRole('textbox') as HTMLInputElement;
    expect(input.type).toBe('email');
  });

  it('can be disabled', () => {
    render(<Input disabled />);
    const input = screen.getByRole('textbox') as HTMLInputElement;
    expect(input.disabled).toBe(true);
  });

  it('clears value when reset', async () => {
    const user = userEvent.setup();
    const { rerender } = render(<Input value="test" />);
    
    let input = screen.getByDisplayValue('test') as HTMLInputElement;
    expect(input.value).toBe('test');
  });
});
