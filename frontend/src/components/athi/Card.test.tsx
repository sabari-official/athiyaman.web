import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { Card } from './index';

describe('Card Component', () => {
  it('renders card with children', () => {
    render(<Card>Card content</Card>);
    expect(screen.getByText('Card content')).toBeInTheDocument();
  });

  it('renders with title', () => {
    render(
      <Card>
        <Card.Header>
          <Card.Title>My Title</Card.Title>
        </Card.Header>
        Content
      </Card>
    );
    expect(screen.getByText('My Title')).toBeInTheDocument();
  });

  it('applies custom className', () => {
    const { container } = render(
      <Card className="custom-class">Content</Card>
    );
    const card = container.querySelector('.bg-white');
    expect(card).toHaveClass('custom-class');
  });

  it('renders header section', () => {
    render(
      <Card>
        <Card.Header>Header content</Card.Header>
        Body
      </Card>
    );
    expect(screen.getByText('Header content')).toBeInTheDocument();
  });

  it('renders body section', () => {
    render(
      <Card>
        <Card.Body>Body content</Card.Body>
      </Card>
    );
    expect(screen.getByText('Body content')).toBeInTheDocument();
  });

  it('renders footer section', () => {
    render(
      <Card>
        <Card.Footer>Footer content</Card.Footer>
      </Card>
    );
    expect(screen.getByText('Footer content')).toBeInTheDocument();
  });
});
