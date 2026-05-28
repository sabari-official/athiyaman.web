# Athiyaman Platform - Frontend Implementation Document
## Phase 1 – Digital India React SPA Development & Engineering Guidelines

---

## 1. Frontend Development Strategy

*   **Engineering Focus:** To construct a highly performant, fully accessible (WCAG 2.1 AA compliant), and responsive React Single Page Application (SPA).
*   **Architecture Standard:** Decouple Presentation components from Feature modules, using standard Page templates and custom hooks.
*   **Core Engineering Principles:** Enforce strict type safety, visual theme consistency, and secure token management.
*   **Performance Benchmarks:** Target a $1.5\text{-second}$ initial bundle load limit under normal $3\text{G}$ cellular connections.

---

## 2. React Setup

Configure the React application runtime using Vite:

### 2.1 Project Initialization
```bash
# 1. Initialize React project using Vite and TypeScript
npx -y create-vite@latest athiyaman-frontend --template react-ts

# 2. Install core dependencies
cd athiyaman-frontend
npm install react-router-dom @tanstack/react-query axios lucide-react jwt-decode
```

### 2.2 Core Entrypoint (`src/main.tsx`)
```typescript
import React from 'react'
import ReactDOM from 'react-dom/client'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { BrowserRouter } from 'react-router-dom'
import App from './App'
import './index.css'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
      staleTime: 5 * 60 * 1000, // 5 minutes cache
    },
  },
})

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <App />
      </BrowserRouter>
    </QueryClientProvider>
  </React.StrictMode>
)
```

---

## 3. TypeScript Setup

Configure strict TypeScript parameters to ensure type safety across the client application:

### 3.1 Strict Configuration (`tsconfig.json`)
```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["DOM", "DOM.Iterable", "ES2020"],
    "module": "ESNext",
    "skipLibCheck": true,
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx"
  },
  "include": ["src"]
}
```

---

## 4. Tailwind Setup

*   **Utility-first CSS:** Install and configure Tailwind CSS to generate a lightweight CSS footprint.
*   **Government-Style Theme:** Map design system tokens (Deep Blue, Environmental Green) directly in `tailwind.config.js`.
*   **Tailwind Configuration (`tailwind.config.js`):**
    ```javascript
    /** @type {import('tailwindcss').Config} */
    export default {
      content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
      ],
      theme: {
        extend: {
          colors: {
            primary: {
              blue: '#0B3C5D',     // Trust, Technology, Identity
              lightBlue: '#328CC1' // Active elements, overlays
            },
            secondary: {
              green: '#98D7C2',    // Environment, Waste, Growth
              darkGreen: '#167D7F' // High-contrast green text
            },
            neutral: {
              bg: '#F9F9F9',       // Body background
              border: '#E2E8F0'    // Gray borders
            },
            alert: {
              red: '#D9534F',      // Errors, rejections
              amber: '#F0AD4E'     // Pending, audits
            }
          },
          fontFamily: {
            sans: ['Inter', 'sans-serif'],
          }
        },
      },
      plugins: [],
    }
    ```

---

## 5. Folder Creation Order

To avoid dependency blocks, modules must be developed in this strict order:

```
┌────────────────────────────────────────────────────────┐
│  1. Base: Folder layout creations and imports          │
├────────────────────────────────────────────────────────┤
│  2. Contexts: Session state and token caching          │
├────────────────────────────────────────────────────────┤
│  3. Layouts: Shell configurations and sidebars         │
├────────────────────────────────────────────────────────┤
│  4. Components: Base inputs, buttons, and loading slots│
├────────────────────────────────────────────────────────┤
│  5. Features: Core modules (Auth, Waste, Teams)        │
└────────────────────────────────────────────────────────┘
```
```bash
# Create shared sub-folders in workspace
mkdir -p src/assets src/components src/constants src/contexts src/features src/hooks src/layouts src/pages src/routes src/services src/types src/utils

# Create base feature modules
cd src/features
mkdir -p auth profiles teams referrals levels waste collection_centers claims payments notifications audit analytics admin developer
```

---

## 6. Layout Implementation

The client application configures five visual layout shells to govern structural layouts across different pages:

*   **Public Layout:** Sticky top navigation menu and central footer block. Used on all unprotected public pages.
*   **Dashboard Layout:** Left-docked navigation sidebar ($260\text{px}$ width) with the main content panel rendering in a fluid grid ($1180\text{px}$). Enforces locks if profile completion is under $100\%$.
*   **Admin Layout:** High-contrast sidebar navigation, exposing verification queues and global platform aggregates to authenticated administrators.
*   **Developer Layout:** System control console. Displays diagnostic metrics, log outputs, backups, and feature flags to developers.
*   **Authentication Layout:** Focused layout shell featuring a clean, centered container box, used on login, signup, and OTP verification screens.

---

## 7. Routing Implementation

Verify endpoint permissions dynamically by parsing JWT role payloads at the router layer:

```typescript
import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';

interface ProtectedRouteProps {
  allowedRoles: string[];
  userRole: string | null;
  profileComplete: boolean;
}

export const ProtectedRoute: React.FC<ProtectedRouteProps> = ({
  allowedRoles,
  userRole,
  profileComplete,
}) => {
  // 1. Session verification
  if (!userRole) {
    return <Navigate to="/login" replace />;
  }

  // 2. Role permission validation
  if (!allowedRoles.includes(userRole)) {
    return <Navigate to="/unauthorized" replace />;
  }

  // 3. Profile completeness lock check
  if (!profileComplete && userRole !== 'ADMIN' && userRole !== 'DEVELOPER') {
    return <Navigate to="/profile-completion" replace />;
  }

  return <Outlet />;
};
```

---

## 8. Authentication Pages

*   **Login Screen:** Centered login box containing *Username* and *Password* inputs, displaying descriptive error warnings.
*   **Register Screen:** Registration wizard requiring a valid referral code, phone number, password, and mobile OTP.
*   **Forgot/Reset Password Screen:** Enter mobile number to verify an OTP, enabling password reset inputs.
*   **OTP Verification Screen:** Renders a $6$-digit number entry grid with an active countdown timer.
*   **Profile Completion Screen:** Multi-step form tracking biography details, encrypted Aadhaar entries, validated bank details, and nominee information.
*   **Rules Acceptance Screen:** Full-screen terms window. Users must scroll to the bottom and select the click-wrap checkbox to unlock dashboards.

---

## 9. Public Website Pages

*   **Home:** Renders standard Hero banner, mission metrics, initiative highlights, and real-time statistics cards.
*   **About:** Displays organization profile, platform goals, and core design principles.
*   **Initiatives:** Exposes informative segments for Digital India (active) and Phase 2 & 3 modules (disabled).
*   **Waste Info:** Educational grids listing allowed/prohibited items and collection workflows.
*   **Become Leader:** Registration form capturing biographical details, geocodes, and leader application reasons.
*   **Contact:** Official phone, email, support details, and active support inbox contact form.

---

## 10. Leader Dashboard Pages

*   **Overview:** Displays profile completeness meters, team/personal levels cards, notifications, and recent activities.
*   **My Profile:** Profile completion wizard, showing bank verification and nominee logs.
*   **Team Details:** Renders team profiles, district coordinates, and statistics grids.
*   **Team Members:** Member roster table with search, filter, and pagination options.
*   **Referral Management:** Active referral code generator, usage logs, and referral capacity charts.
*   **Team Progress:** Milestone tracker for Levels 1–6 with claim triggers.
*   **My Progress:** Personal progression gauge for Levels 7–11.
*   **Level Tree:** Visual diagram of progress milestones.
*   **Waste Management:** Upload tool and history list.
*   **Payment Transactions:** Claim states and transaction receipts.
*   **Collection Centers:** Nearest center finder and map routes.
*   **Settings:** Password changes and alert choices.

---

## 11. Member Dashboard Pages

*   **Overview:** Individual dashboard status, personal progress levels (7-11), and notifications.
*   **Team Details:** Renders team details, showing leader contacts.
*   **Level Tree:** Personal progression tree for Levels 7–11.
*   **Waste Management:** Upload tool and collection receipt queue.
*   **Payment Transactions:** Payout status list and bank receipts.
*   **Collection Centers:** Map routing to regional centers.
*   **Settings:** Security updates.

---

## 12. Admin Dashboard Pages

*   **Dashboard Overview:** Exposes platform metrics (users, teams, collections, claims) and analytical growth trend charts.
*   **Leader Applications:** Queue table displaying candidate details with approve and reject buttons.
*   **User Management:** Roster with user suspension features.
*   **Team Management:** Roster with team suspension features.
*   **Referral Management:** Codes audit engine and leader invitation setup.
*   **Waste Verification:** Photo queue and weight audit tools.
*   **Reward Claims:** Payout audit approvals.
*   **Payments:** Transaction code recorder.
*   **Collection Centers:** Tools to add, edit, and toggle centers.
*   **Notifications:** Broadcast editor.
*   **Analytics:** Exportable reports.
*   **Documents:** Document verification checks.
*   **Audit Logs:** System activity explorer.
*   **Settings:** Operational variables manager.

---

## 13. Developer Dashboard Pages

*   **Overview:** Displays diagnostic metrics, active connection pools, API status, and database health.
*   **System Monitoring:** Interactive charts displaying CPU and Memory usage trends.
*   **Security Center:** System logs for failed logins and access blocks.
*   **Logs:** Real-time runtime outputs.
*   **Audit Explorer:** Advanced SQL logs inspector.
*   **Backup Center:** Database dump and restore triggers.
*   **Data Management:** Data cleanups and maintenance tools.
*   **Feature Controls:** Toggle flags for modular features.
*   **Announcements:** Technical notification creator.
*   **Settings:** System configurations.

---

## 14. API Integration Layer

Use Axios client interceptors to inject authorization tokens and handle expired sessions automatically:

```typescript
import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  timeout: 10000,
});

// Request Interceptor: Inject JWT token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token && config.headers) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
}, (error) => {
  return Promise.reject(error);
});

// Response Interceptor: Catch expired tokens
api.interceptors.response.use((response) => response, async (error) => {
  const originalRequest = error.config;
  if (error.response?.status === 401 && !originalRequest._retry) {
    originalRequest._retry = true;
    try {
      // Execute token refresh using HTTP-only cookies
      const { data } = await axios.post(`${import.meta.env.VITE_API_URL}/auth/refresh`, {}, { withCredentials: true });
      localStorage.setItem('access_token', data.access_token);
      originalRequest.headers.Authorization = `Bearer ${data.access_token}`;
      return api(originalRequest);
    } catch (refreshError) {
      // Invalidate session on failure
      localStorage.removeItem('access_token');
      window.location.href = '/login?expired=true';
    }
  }
  return Promise.reject(error);
});

export default api;
```

---

## 15. React Query Integration

*   **Server State Caching:** Use React Query hooks to fetch API data, keeping cache states synchronized.
*   **Data Fetching Standard:** Wrap standard data queries in custom hooks, handling loading, error, and cached states:
    ```typescript
    import { useQuery } from '@tanstack/react-query';
    import api from '../services/api';
    
    export const useWasteRecords = () => {
      return useQuery({
        queryKey: ['waste_records'],
        queryFn: async () => {
          const { data } = await api.get('/waste');
          return data;
        },
      });
    };
    ```

---

## 16. Form Validation Strategy

*   **Client Validation:** Enforce strict client-side validation rules on form fields before submitting payloads.
*   **Error Indicators:** Validation failures display below the affected input field in red text, disabling the submit button.
*   **Prevent Double Submits:** Enforce disabled loading states on buttons during form processing.

---

## 17. Error Handling Strategy

*   **React Error Boundaries:** Wrap component grids in React Error Boundaries to catch rendering failures, displaying clean fallback screens.
*   **Network Errors:** Axios interceptors capture network timeouts and connection losses, displaying informative toast notifications.

---

## 18. Loading State Strategy

*   **Skeleton Skeletons:** Renders skeleton placeholder containers during data loading, matching structural card shapes to reduce perceived latency.
*   **Spinners & Progress Bars:** Renders loading spinners on buttons and progress overlays during fullscreen operations.

---

## 19. Responsive Design Strategy

*   **Tailwind Breakpoints:** Enforces standard responsive breakpoints: Mobile (`max-w-md` under $768\text{px}$), Tablet (`md:` from $768\text{px}$), and Desktop (`lg:` from $1024\text{px}$).
*   **Adaptive Grids:** Dashboard rosters transition from multi-column tables on desktop to vertical grid lists on mobile layouts.

---

## 20. Accessibility Strategy

*   **Keyboard Operations:** Users can navigate forms, active links, and buttons using standard `Tab` inputs.
*   **Screen Reader Integration:** Enforce explicit `aria-label` and role properties on all interactive component tags.
*   **Visual contrast:** Use high-contrast color balances, checking contrast targets to exceed WCAG 2.1 AA limits.

---

## 21. Performance Optimization

*   **Lazy Loading:** Implement dynamic code-splitting (`React.lazy`) to load feature modules on demand, keeping initial bundle sizes optimized.
*   **Local Caches:** React Query caches static lookups locally, reducing redundant network requests.

---

## 22. Security Standards

*   **Access Token Security:** Keep access tokens in memory variables, using refresh cookies to handle persistence.
*   **Route Protection Guards:** Protected route guards check active roles and user statuses before rendering dashboards.
*   **Input Sanitization:** Escape input variables to prevent XSS injection exploits.

---

## 23. Testing Strategy

*   **Vitest & React Testing Library:** Unit test reusable components and form validation checks.
*   **Route Verification:** Verify that route protection wrappers intercept access requests.
*   **Mock Network Responses:** Mock API responses using MSW (Mock Service Worker) during development.

---

## 24. Frontend Readiness Checklist

Before deploying the frontend application, verify all items on this readiness checklist are completed:

*   [ ] **React Build:** Verify initial bundle sizes are optimized and lazy-loading routes load successfully.
*   [ ] **Accessibility Standards:** Confirm contrast ratios meet WCAG 2.1 AA requirements and inputs have explicit `aria-label` tags.
*   [ ] **Protected Routes:** Verify route guards protect dashboards, redirecting unauthorized traffic.
*   [ ] **Axios Interceptors:** Verify interceptors handle expired access tokens.
*   [ ] **Form Validations:** Confirm all form fields check inputs before submissions.

---

## 25. Conclusion

This Frontend Implementation Guide (`13_FRONTEND_IMPLEMENTATION.md`) establishes the absolute technical setups, folder structures, component interfaces, state caches, responsive grids, error checking, and readiness checklists for the Athiyaman Platform – Digital India Phase 1. By detailing code architectures and providing complete SQL and TypeScript snippets, it serves as a complete technical guide for frontend developers, enabling independent development cycles.
