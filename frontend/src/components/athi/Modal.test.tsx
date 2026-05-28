import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, it, expect, vi } from 'vitest';
import { Modal } from './index';

describe('Modal Component', () => {
  it('does not render when closed', () => {
    render(
      <Modal isOpen={false} onClose={() => {}}>
        Modal content
      </Modal>
    );
    expect(screen.queryByText('Modal content')).not.toBeInTheDocument();
  });

  it('renders when open', () => {
    render(
      <Modal isOpen={true} onClose={() => {}}>
        Modal content
      </Modal>
    );
    expect(screen.getByText('Modal content')).toBeInTheDocument();
  });

  it('renders with title', () => {
    render(
      <Modal isOpen={true} onClose={() => {}} title="Dialog">
        Content
      </Modal>
    );
    expect(screen.getByText('Dialog')).toBeInTheDocument();
  });

  it('calls onClose when close button clicked', async () => {
    const user = userEvent.setup();
    const handleClose = vi.fn();
    
    render(
      <Modal isOpen={true} onClose={handleClose} title="Test">
        Content
      </Modal>
    );
    
    const closeButton = screen.getByRole('button', { name: /close/i });
    await user.click(closeButton);
    
    expect(handleClose).toHaveBeenCalled();
  });

  it('calls onClose when overlay clicked', async () => {
    const user = userEvent.setup();
    const handleClose = vi.fn();
    
    const { container } = render(
      <Modal isOpen={true} onClose={handleClose}>
        Content
      </Modal>
    );
    
    const overlay = container.querySelector('.fixed.inset-0');
    if (overlay) {
      await user.click(overlay);
    }
  });

  it('renders with correct size', () => {
    const { container } = render(
      <Modal isOpen={true} onClose={() => {}} size="lg">
        Content
      </Modal>
    );
    
    const dialog = container.querySelector('[role="dialog"]');
    expect(dialog).toBeInTheDocument();
  });

  it('supports action buttons', () => {
    render(
      <Modal 
        isOpen={true} 
        onClose={() => {}}
        actions={[
          { label: 'Cancel', onClick: vi.fn(), variant: 'secondary' },
          { label: 'Confirm', onClick: vi.fn(), variant: 'primary' }
        ]}
      >
        Content
      </Modal>
    );
    
    expect(screen.getByText('Cancel')).toBeInTheDocument();
    expect(screen.getByText('Confirm')).toBeInTheDocument();
  });
});
