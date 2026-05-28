# Athiyaman Platform - Frontend Specification Document
## Phase 1 – Digital India Screen-by-Screen & UI Engineering standards

---

## 1. Frontend Overview

This document defines the Frontend Specification and UI Engineering Standards for the Athiyaman Platform - Digital India Phase 1. It details the component models, routing architectures, page layouts, state managers, responsive designs, security guidelines, and testing criteria to ensure frontend developers can construct a highly consistent, accessible, and performant user experience.

*   **Purpose:** To establish a central visual and technical design guide that aligns client-side assets directly with the platform's core business workflows.
*   **Goals:**
    *   *High Performance:* Target a $1.5\text{-second}$ initial bundle load limit under normal $3\text{G}$ cellular connections.
    *   *Accessibility First:* Complete compliance with WCAG 2.1 AA contrast and screen-reader keyboard controls.
    *   *Visual Consistency:* Enforce government-style layouts to build trust and ensure clear utility interfaces.
*   **Responsibilities:** Renders views, handles client validations, manages local caches, isolates routes based on active roles, and prevents user action bottlenecks during calculations.
*   **Frontend Scope:** Home pages, OTP signup screens, $100\%$ profile completion forms, level trees, waste logging dashboards, and queues for administrators.
*   **User Experience (UX) Goals:** High readability, fast page loads, simple interactions, clear progress tracking, and friendly error indicators.
*   **Performance Goals:** Light bundle footprint, dynamic component loading, state caching, and fast asset delivery.
*   **Security Goals:** Native protection against XSS exploits, secure token managers in local memories, and client-side RBAC route blocks.

---

## 2. Frontend Technology Stack

The client application utilizes a modern, light-weight tech-stack configured for high compatibility and performant delivery.

*   **React (v18+):** Leveraged as our SPA component library. Chosen for its performance, Virtual DOM rendering efficiency, and rich component ecosystem.
*   **TypeScript:** Enforces strict static typing, eliminating type mismatch errors during development.
*   **Tailwind CSS:** Utility-first CSS engine. Provides rapid responsive styling and compiles into a tiny, high-contrast visual footprint.
*   **React Router (v6+):** Client-side router. Handles nested layout routes, protecting administrative routes natively.
*   **React Query (TanStack):** Handles server-state caching, background queries, error states, and mutations.

---

## 3. Frontend Architecture

The client application separates layout duties from state synchronization engines using a Clean Architecture design:

```
[ Router Guards ] ──► [ Page Container ] ──► [ Layout Shell ] ──► [ Business Hook ] ──► [ UI Components ]
```

*   **Application Structure:** Code folders are grouped by business feature directories rather than technical layer classes, keeping resources modular.
*   **Page Architecture:** Page templates act as structural layout shells, rendering feature grids and loading skeletons while delegating data fetching to custom hooks.
*   **Component Architecture:** Isolates shared presentation components (buttons, input fields) from custom feature components, ensuring high styling consistency.
*   **Routing Architecture:** Configured via React Router, using role-based routing guards to block unauthorized page requests.
*   **State Architecture:** Separates server states (managed by React Query) from local UI states (managed by local hooks or contexts), keeping runtime overhead low.
*   **Service Architecture:** Manages network communication using **Axios** clients, injecting tokens automatically and processing HTTP error codes cleanly.
*   **Authentication Architecture:** Connects token validation steps to user contexts, tracking session lifetimes and unlocking locked dashboards once profiles are complete.

---

## 4. Project Folder Structure

The client application uses a clean, standardized workspace structure:

```
src/
├── assets/             # Static visual media (logos, branding, icons)
├── components/         # Shared presentation elements (buttons, inputs)
├── constants/          # Application variables (IFSC dictionaries, level metrics)
├── contexts/           # Unified contexts managing active user sessions
├── features/           # Modular business feature directories
│   ├── auth/           # Login screens, OTP challenges, and signup forms
│   ├── teams/          # Team profiles, rosters, and validation forms
│   └── waste/          # Waste log forms, collections tables, and maps
├── hooks/              # Global custom hooks (useMediaQuery, useDebounce)
├── layouts/            # Page shell containers (menus, sidebars)
├── pages/              # Unprotected info displays (Home, About, Initiatives)
├── routes/             # Client-side router configurations and guards
├── services/           # Network API adapters (Axios clients)
├── types/              # Unified TypeScript definitions (.ts files)
└── utils/              # Helper utilities (IFSC verification, date formatters)
```

---

## 5. Layout Architecture

The client application configures five visual layout shells to govern structural layouts across different pages:

*   **Public Layout:** Simple layout shell containing the sticky top navigation menu and central footer block. Used on all unprotected public pages.
*   **Dashboard Layout:** Left-docked navigation sidebar ($260\text{px}$ width) with the main content panel rendering in a fluid grid ($1180\text{px}$). Enforces locks if profile completion is under $100\%$.
*   **Admin Layout:** High-contrast sidebar navigation, exposing verification queues and global platform aggregates to authenticated administrators.
*   **Developer Layout:** System control console. Displays diagnostic metrics, log outputs, backups, and feature flags to developers.
*   **Authentication Layout:** Focused layout shell featuring a clean, centered container box, used on login, signup, and OTP verification screens.

---

## 6. Routing Architecture

The client application implements role-based routing guards to block unauthorized page requests at the gateway level:

```
┌────────────────────────────────────────────────────────┐
│             Frontend Route Protection Guards           │
├────────────────────────────────────────────────────────┤
│  Public Routes:    [VISITOR] (Unprotected access)      │
│  Member Routes:    [MEMBER, LEADER, ADMIN, DEVELOPER]  │
│  Leader Routes:    [LEADER, ADMIN, DEVELOPER]          │
│  Admin Routes:     [ADMIN, DEVELOPER]                  │
│  Developer Routes: [DEVELOPER]                         │
└────────────────────────────────────────────────────────┘
```

*   **Route Guards:** Enforces route permissions by checking user contexts before rendering views, redirecting unauthorized requests to the login screen.
*   **Role Validation:** Checks JWT access token payloads, verifying active role classifications and user statuses.
*   **Navigation Rules:** Authenticated logouts wipe tokens from memory, clear local cache pools, and redirect users to the public landing page.
*   **Unauthorized Handling:** Access violations route users immediately to the `403 Forbidden` error screen, logging the security event in the audit trail.

---

## 7. Authentication Frontend Flow

*   **Login Workflow:** Users enter credentials $\rightarrow$ Client validates formats $\rightarrow$ Submits payloads $\rightarrow$ Receives JWT access token in memory $\rightarrow$ Registers secure HTTP-only refresh cookies $\rightarrow$ Redirects to appropriate dashboard.
*   **Logout Workflow:** Wipes tokens from memory $\rightarrow$ Clears cached queries $\rightarrow$ Calls logout endpoints $\rightarrow$ Wipes refresh cookies $\rightarrow$ Redirects to landing page.
*   **Session Validation:** Dashboard shells call session endpoints automatically on page loads, checking token permissions before rendering views.
*   **Token Refresh Handling:** Axios interceptors catch expired access token errors, requesting new tokens using refresh cookies to prevent session interruptions.
*   **Profile Completion Overlay:** Non-dismissible popup modal that locks dashboards, displaying the profile completion checklist and progress bar.
*   **Rules Acceptance Checkpoint:** Full-screen terms window. Users must scroll to the bottom and select the click-wrap checkbox to unlock dashboards.
*   **Dashboard Access:** Access is unlocked once the profile reaches $100\%$ and terms are accepted.

---

## 8. State Management Strategy

*   **Global State:** Managed using React's native `useContext` hook to share user credentials, roles, and theme settings.
*   **Local State:** Managed using the `useState` hook, isolating component-specific parameters (e.g., drawer toggles, text fields) from global states.
*   **Server State Caching:** Synchronized using **React Query** (TanStack), managing active cache values, automated background updates, and request states.
*   **Caching Expirations:** Dynamic lookups (such as profiles and team lists) are cached for $5\text{ minutes}$. Aggregated metrics use $15\text{-minute}$ caches.
*   **Cache Invalidation Rules:** Mutating records triggers cache invalidations automatically, updating dashboards on next page loads.

---

## 9. API Communication Layer

*   **Service Integrations:** Services group API adapters by modular feature areas, using Axios clients to manage network queries.
*   **Request Interceptors:** Inject JWT access tokens automatically into request authorization headers.
*   **Response Interceptors:** Parse API responses, catching network timeouts and handling expired tokens.
*   **Error Catching:** Maps backend error payloads to descriptive frontend toast warnings.
*   **Retry Protocols:** Retries failed GET queries up to $3\text{ times}$ under poor network conditions, using exponential backoff to reduce server load.
*   **Credentials Handlers:** Enforces token checks on all non-public APIs, blocking unauthorized calls at the router layer.

---

## 10. UI Design Philosophy

*   **Simple Layouts:** Prioritizes flat layouts, clean borders, and clear text spacing, avoiding heavy graphics or distracting animations.
*   **Government-Style Interface:** Uses high-contrast, professional layouts featuring deep blues for trust, rich greens for environmental focus, and clear borders.
*   **Minimalistic Framework:** Limits styling assets, optimizing resources to ensure fast page loads on low-end budget smartphones.
*   **Professional Integrity:** Implements data masking natively, showing truncated characters for sensitive data.
*   **Accessibility Standards:** Complete compliance with WCAG 2.1 AA standards, enforcing $4.5:1$ contrast minimums and full keyboard navigability.
*   **Mobile Responsiveness:** A single responsive layout that resizes smoothly from desktop viewports ($1440\text{px}$) to tablets ($768\text{px}$) and mobile screens ($360\text{px}$).

---

## 11. Theme System

The design system standardizes layout variables across all presentation elements:

```
┌────────────────────────────────────────────────────────┐
│                      Theme Palette                     │
├────────────────────────────────────────────────────────┤
│  Primary Blue:   #0B3C5D (Trust, Technology, Identity) │
│  Secondary Green: #328CC1 (Environment, Waste)         │
│  Base Neutral:   #F9F9F9 (White / Soft Gray Surfaces)  │
│  Alert Red:      #D9534F (Error, Rejection, Warnings)  │
│  Alert Amber:    #F0AD4E (Pending, Audits, Verification)│
└────────────────────────────────────────────────────────┘
```
*   **Typography:** Enforces the `Inter` font family, using bold headings ($600\text{–}700$ weights) and clean body text ($400\text{–}500$ weights).
*   **Spacing:** Follows a standard $4\text{px}$ scale layout matrix (`p-2`, `p-4`, `p-6`, `p-8`) to maintain consistent gaps.
*   **Cards:** Uses flat white containers with $1\text{px}$ gray borders and small corner radii (`rounded-lg`).
*   **Tables:** Uses high-contrast headers, clear borders (`border-b`), and alternating row backgrounds to maintain readability.
*   **Forms:** Features $1\text{px}$ input borders that highlight in blue on focus, using red border warnings if validations fail.
*   **Buttons:** Standardizes sizes and colors: Primary (Deep Blue), Secondary (Green), Danger (Red), and Disabled (Gray).
*   **Modals:** Features modal components centered on screen overlays, locking body scroll controls during display.
*   **Alerts:** Styled as banner notifications: Error (Red), Warning (Amber), Info (Blue), and Success (Green).
*   **Badges & Indicators:** Used to show clear status states, matching text colors to active backgrounds.

---

## 12. Reusable Component Library

*   **Buttons:** Custom components rendering in four states: Primary, Secondary, Danger, and Loading.
*   **Inputs:** Handles text, email, password, and file types, displaying error messages.
*   **Selects:** Dropdown component populated by database arrays.
*   **Checkboxes & Radios:** High-contrast inputs supporting click-wrap and forms selections.
*   **Tables:** Renders collections grids with custom header layouts.
*   **Pagination:** Simple navigation footer (`First | Previous | Active Page | Next | Last`).
*   **Search Bar:** Text field featuring clear action buttons.
*   **Filters:** Dropdown filter sets supporting search queries.
*   **Cards:** Container components organizing dashboard metrics.
*   **Modals:** Centered dialog popups.
*   **Drawers:** Sliding containers used for mobile sidebars.
*   **Tabs:** Horizontal panel selectors with active state indicators.
*   **Breadcrumbs:** Clean navigation paths mapping nested directories.
*   **Tooltips:** Expands hover metadata.
*   **Notifications Bell:** Header icon displaying unread counts.
*   **Loading Indicators:** Renders inline spinners and dashboard skeletons.
*   **Empty States:** Renders illustrated panels when searches return zero records.
*   **Error Fallbacks:** Displays user-friendly error banners when rendering failures occur.

---

## 13. Form Standards

*   **Validation Validation:** Validates form inputs before submission, checking length and character properties.
*   **Error Messaging:** Validation errors display inline below the affected input field in red text.
*   **Field Indicators:** Enforces clear visual tags to distinguish required input fields from optional variables.
*   **Submission Behavior:** Clicking submit disables the button and displays a loading spinner, preventing secondary submit actions during processing.
*   **Success Handling:** Successful submissions close dialogs, trigger success toasts, and refresh active dashboard queries.
*   **Failure Handling:** Backend failures display inline warning banners, keeping form inputs intact.

---

## 14. Table Standards

*   **Pagination Controls:** Displays the active page index, remaining items, and navigation options.
*   **Sorting Options:** Clicking table headers toggles sorting directions (`asc` / `desc`), updating queries instantly.
*   **Filter Panels:** Exposes status, district, and date selectors, reloading lists on changes.
*   **Search Fields:** Enables text queries, debouncing inputs to prevent spammed queries.
*   **Responsive Viewports:** Renders full tables on desktop, transitioning columns to mobile-friendly list cards on mobile viewports.
*   **Loading Skeletons:** Displays grey skeleton rows during API data fetches.

---

## 15. Search Standards

*   **Global Search:** Accessible on admin dashboards, returning matching user or team profiles.
*   **Module Search:** Accessible on rosters, filtering entries locally.
*   **Input Debouncing:** Debounces text searches ($300\text{ms}$ delay) before executing API calls to prevent spammed database queries.
*   **Results Display:** Lists matches in a dropdown, showing empty states if zero matches are found.

---

## 16. Dashboard Standards

*   **Overview Cards:** Grid of high-priority summary cards showcasing key metrics (e.g., active members, waste approved).
*   **Metrics Grid:** Displays progress meters and milestone summaries.
*   **Charts Panel:** Dynamic charts mapping growth trends and waste collections.
*   ** Roster Feeds:** Renders latest records, showing status logs and activity trails.
*   **Quick Actions Panel:** Provides one-click access to critical tasks (e.g., generating referral code, logging waste deposit).

---

## 17. Public Website Pages

### 17.1 Home Page
*   *Sections:* Navigation menu, Hero banner, Mission, Vision, Initiative highlights, Statistics summary, and central Footer.
*   *Components:* Action buttons, stats sliders, and informational cards.
*   *Actions:* Redirects visitors to leader applications or login screens.

### 17.2 About Page
*   *Sections:* Organization profile, platform objectives, and core principles.
*   *Components:* Clear information text grids.

### 17.3 Initiatives Page
*   *Sections:* Feature cards for Digital India (active), Skill India (disabled), and Clean India (disabled).
*   *Components:* Progress locks and informational cards.

### 17.4 Waste Management Page
*   *Sections:* Material guidelines (plastic bottles, covers) and process flow charts.
*   *Components:* Visual maps and checkmark checklists.

### 17.5 Become Team Leader Page
*   *Sections:* Registration form fields and submission alerts.
*   *Components:* Structured inputs for biographical data, address dropdowns, and file upload fields.
*   *Actions:* Submits leader applications and handles success alerts.

### 17.6 Contact Page
*   *Sections:* Support contact cards and interactive inquiry form.
*   *Components:* Phone, email, address records, and support inquiry inputs.

---

## 18. Authentication Pages

*   **Login Screen:** Form container featuring *Username* and *Password* fields with inline warning banners.
*   **Register Screen:** Closed-loop registration portal requiring a valid referral code, contact details, and OTP verification.
*   **Forgot Password Screen:** Enter mobile number to trigger an OTP verification code.
*   **Reset Password Screen:** Enter the received OTP and new password.
*   **OTP Verification Screen:** Displays a $6$-digit code entry grid with a $5\text{-minute}$ countdown timer.
*   **Profile Completion Screen:** Multi-step wizard containing biographical, Aadhaar, bank routing, and nominee inputs.
*   **Rules Acceptance Screen:** Full-screen click-wrap window showing the platform's terms of use and terms checkbox.

---

## 19. Leader Dashboard Pages

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

## 20. Member Dashboard Pages

*   **Overview:** Individual dashboard status, personal progress levels (7-11), and notifications.
*   **Team Details:** Renders team details, showing leader contacts.
*   **Level Tree:** Personal progression tree for Levels 7–11.
*   **Waste Management:** Upload tool and collection receipt queue.
*   **Payment Transactions:** Payout status list and bank receipts.
*   **Collection Centers:** Map routing to regional centers.
*   **Settings:** Security updates.

---

## 21. Admin Dashboard Pages

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

## 22. Developer Dashboard Pages

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

## 23. Notification UI

*   **Toast Notifications:** Real-time action alerts that fade after $4\text{ seconds}$ (Green for success, Red for errors).
*   **Notification Center:** Sliding header drawer displaying a history list of notifications.
*   **Read/Unread Indication:** Bold borders mark unread items, transitioning to normal views when marked read.
*   **Priority Indicators:** Banners map colors to priority levels: High (Red), Medium (Amber), and Low (Blue).
*   **Dismissal Actions:** Clear options to dismiss alerts or mark all items as read.

---

## 24. Status Visualization Standards

Status states are rendered using high-contrast, color-coded badges to ensure readability:

```
┌────────────────────────────────────────────────────────┐
│                   Status Badge Theme                   │
├────────────────────────────────────────────────────────┤
│  ACTIVE / APPROVED / PAID:        Green Base           │
│  PENDING / WAITING / PROCESSING:  Amber Base           │
│  REJECTED / SUSPENDED / FAILED:   Red Base             │
│  UNPAID / INACTIVE:               Gray Base            │
└────────────────────────────────────────────────────────┘
```

---

## 25. Progress Visualization

*   **Profile Completion:** Circular percentage meter scaling from $0\%$ to $100\%$ as sections are completed.
*   **Team Progress:** Horizontal progress bar detailing active members against next level targets (e.g., `45 / 90 Members`).
*   **Level Progress:** Unified level map detailing completed, active, and locked nodes.
*   **Waste Progress:** Radial gauge detailing approved weights collected (e.g., `4.5 KG / 10.0 KG`).
*   **Claim Progress:** Flow chart showing the claim status lifecycle.

---

## 26. Charts and Analytics

*   **Dashboard Charts:** Renders system-wide user growth trends and waste collection volumes.
*   **Growth Charts:** Displays team recruitment rates and active registrations using clean line charts.
*   **Waste Charts:** Bar graphs comparing monthly collections across districts.
*   **Payment Charts:** Area charts displaying monthly payout disbursements.

---

## 27. Error Handling Interface Specs

*   **404 Not Found Page:** Displays a clear government-style layout with the message *"The page you are looking for does not exist."* Includes a primary return button redirecting users to the home dashboard.
*   **403 Forbidden Page:** Displays a shield icon and the message *"You do not have administrative clearance to access this portal."* Access attempts are logged in the audit trail.
*   **500 Internal Error Page:** Shows the message *"An unexpected database error has occurred. Our development team has been alerted."* Includes a primary retry button.
*   **Session Timeout Alert Modal:** A dismissible overlay popup warning that appears $2\text{ minutes}$ before token expiry, providing a button to renew the session.

---

## 28. Dynamic Loading States

*   **Skeleton Screens:** Gray skeleton placeholders display structure shapes during API fetches, reducing perceived load times.
*   **Button Load Indicators:** Clicking actions transitions buttons to disabled loading states, preventing secondary clicks during processing.
*   **Page Loading Overlay:** Displays a centered progress spinner during full-screen page transitions.

---

## 29. Empty States

*   **No Records Panel:** Shows a clear container card with the message *"No matching records found. Refine your query or check back later."*
*   **No Notifications:** Shows a bell icon with the message *"All caught up! You have no unread notifications."*
*   **No Waste Records:** Displays a scale icon with the message *"No waste collections logged yet. Deposit waste at your nearest center to get started."*
*   **No Claims / Payments:** Displays a card with the message *"No payout claims generated yet. Reach your next level milestone to unlock rewards."*

---

## 30. Responsive Layout Specifications

*   **Desktop Viewport Layout ($1440\text{px}$):** Left-docked navigation sidebar ($260\text{px}$ width) with the main content panel rendering in a fluid grid ($1180\text{px}$).
*   **Tablet Viewport Layout ($768\text{px}$):** Sidebar collapses into an icon-only dock ($80\text{px}$ width). Table views transition to multi-line list cards to preserve readability.
*   **Mobile Viewport Layout ($360\text{px}$):** Sidebar navigation collapses into a slide-out hamburger menu drawer. Data tables transition into single-column cards with responsive spacing.

---

## 31. Accessibility Standards

*   **Keyboard Navigation Support:** Users can navigate forms, navigation menus, and dialog buttons using standard `Tab` and `Enter` inputs.
*   **Screen Reader Labels:** Interactive elements must declare explicit `aria-label` tags describing targets (e.g., `<button aria-label="Copy Referral Code">`).
*   **Contrast Standards:** Text elements must maintain a minimum contrast ratio of $4.5:1$ against backgrounds, using deep blues on off-white surfaces.
*   **Focus States:** Active inputs must show a distinct blue focus outline to help users navigate.

---

## 32. Frontend Security Standards

*   **Token Storage Standards:** Access tokens are stored in memory, and refresh tokens are stored in secure HTTP-only cookies, preventing token theft.
*   **Route Protection Guards:** Protected route guards check active roles and user statuses before rendering dashboards.
*   **XSS Protections:** React's default output engine escapes string fields, preventing XSS injection threats.
*   **Upload Validations:** Uploads are restricted to secure file types (JPEG, PNG, PDF), verifying that files do not exceed the $5\text{MB}$ limit.

---

## 33. Performance Standards

*   **Dynamic Code Splitting:** Implements lazy loading (`React.lazy`) to load feature modules dynamically, reducing initial bundle sizes.
*   **Server State Caching:** React Query caches API responses locally, reducing redundant backend queries.
*   **Resource Optimizations:** Compiles assets into highly optimized bundles, optimizing images to ensure fast mobile page loads.

---

## 34. Frontend Logging Strategy

*   **Client Errors:** Catches unexpected rendering failures, logging event details in Sentry to alert developers.
*   **Network Failures:** Interceptors log network timeouts and connection losses.

---

## 35. Frontend Testing Strategy

*   **Component Testing:** Written using **Vitest** and **React Testing Library** to verify standard UI rendering, checking that buttons, inputs, and elements display correctly.
*   **Form Validations:** Tests verify input bounds (e.g., checking that email forms reject invalid syntax).
*   **Route Guards Tests:** Confirms that route protection wrappers intercept access requests, redirecting unauthorized sessions.

---

## 36. Frontend Documentation Standards

*   **Component Documentation:** Reusable components must include comments detailing props, states, and event handlers.
*   **Usage Examples:** The `/docs` directory must contain code snippets showing how to implement components (e.g., rendering forms with standard input components).

---

## 37. Skill India Frontend Expansion (Phase 2)

*   **Future Navigation Links:** Simply add **Skills** links to sidebar configurations under trainer permissions.
*   **Decoupled Pages:** Mounts future course registries and assignment panels under `/dashboard/skills/*`, avoiding schema conflicts with Phase 1 dashboards.

---

## 38. Clean India Frontend Expansion (Phase 3)

*   **Roster Additions:** Existing collection center registries are easily extended to support logistics dashboards.
*   **Role Adaptability:** Adds new navigation links and geocoded maps, routing options dynamically based on municipal boundaries.

---

## 39. Production Readiness Checklist

Before deploying the frontend application, verify all items on this checklist are completed:

*   [ ] **Performance Audit:** Verify initial bundle sizes are optimized and lazy-loading routes load successfully.
*   [ ] **Security Audit:** Confirm access tokens are stored in memory and route protection guards intercept unauthorized traffic.
*   [ ] **Accessibility Audit:** Confirm contrast ratios meet WCAG 2.1 AA requirements and inputs have explicit `aria-label` tags.
*   [ ] **Responsiveness Audit:** Verify layouts adjust cleanly across desktop, tablet, and mobile breakpoints.
*   [ ] **Testing Audit:** Confirm frontend component, form validation, and route tests pass successfully.

---

## 40. Conclusion

This Frontend Specification Document (`08_FRONTEND_SPECIFICATION.md`) establishes the absolute screen layouts, responsive grids, state cache rules, component libraries, accessibility metrics, and testing criteria for the Athiyaman Platform – Digital India Phase 1. By detailing structures for user dashboards, admin queues, and developer consoles, it serves as a complete technical guide for frontend engineering teams, enabling independent development cycles.
