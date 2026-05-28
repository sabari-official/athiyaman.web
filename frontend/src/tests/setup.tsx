import "@testing-library/jest-dom";
import { render, screen, waitFor } from "@testing-library/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import type { ReactNode } from "react";

export const createTestQueryClient = () =>
  new QueryClient({
    defaultOptions: {
      queries: {
        retry: false,
      },
      mutations: {
        retry: false,
      },
    },
  });

export const renderWithProviders = (ui: ReactNode, options = {}) => {
  const testQueryClient = createTestQueryClient();

  return render(
    <QueryClientProvider client={testQueryClient}>{ui}</QueryClientProvider>,
    options
  );
};

export const waitForLoadingToFinish = () =>
  waitFor(
    () => {
      expect(screen.queryByLabelText(/loading/i)).not.toBeInTheDocument();
    },
    { timeout: 4000 }
  );

export * from "@testing-library/react";
export { renderWithProviders as render };

