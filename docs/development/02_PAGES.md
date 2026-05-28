# Athiyaman Platform - Pages & User Interface Specification
## Phase 1 – Digital India Screen-by-Screen & UX Specification

---

## 1. UI Philosophy

The Athiyaman Platform’s User Interface is designed to look clean, professional, and accessible. It uses custom design system rules tailored for civic trust, accessibility, and high performance on budget devices.

*   **Simple Design:** Flat layouts with clean borders, clear text spacing, and high readability. It avoids heavy drop-shadows, complex gradients, or distracting background animations.
*   **Government-Style Interface:** A color scheme that builds trust. It utilizes deep blues for authority, rich greens for environmental focus, and sharp neutrals for structure.
*   **Accessibility First:** Designed to meet WCAG 2.1 AA standards. It enforces high contrast ratios ($4.5:1$ minimum), screen-reader-friendly labels, and full keyboard navigability.
*   **Responsiveness:** A single responsive layout that resizes smoothly from desktop viewports ($1440\text{px}$) to tablets ($768\text{px}$) and mobile screens ($360\text{px}$).
*   **Performance Optimization:** Extremely light bundle footprint. No heavy 3D widgets, parallax libraries, or large canvas components are allowed. The UI is designed to load in under $1.5\text{ seconds}$ on standard mobile connections.
*   **Security Awareness:** The interface handles data masking natively. Aadhaar numbers are masked by default (e.g., `XXXX-XXXX-1234`), bank account details are hidden, and session alerts show clear logout warnings.
*   **Consistency:** Standardized layouts for tables, forms, headers, sidebars, and overlays to keep the user experience consistent across different portals.

### 1.1 Custom Design System Tokens

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

---

## 2. Global Navigation Structure

Menu configurations are determined dynamically based on the user's authenticated role.

### 2.1 Public Website Menu (Visitor)
```
[Logo] -> Home | About | Initiatives | Waste Info | Become Leader | Contact ──> [Login Button]
```

### 2.2 Leader Dashboard Navigation (Left Sidebar + Responsive Drawer)
*   **Overview:** Real-time personal and team dashboard metrics.
*   **My Profile:** Profile completion checklist, bank verification, nominee details.
*   **Team Details:** Team details page showing area boundaries.
*   **Team Members:** Member roster view.
*   **Referral Management:** Active member invitation generator.
*   **Team Progress:** Milestone bar for Levels 1–6.
*   **My Progress:** Personal waste progress tracker for Levels 7–11.
*   **Level Tree:** Visual diagram of progress milestones.
*   **Waste Management:** Upload tool and history list.
*   **Payment Transactions:** Claim states and transaction receipts.
*   **Collection Centers:** Nearest center finder and map routes.
*   **Settings:** Password changes and alert choices.

### 2.3 Member Dashboard Navigation (Left Sidebar + Responsive Drawer)
*   **Overview:** Individual dashboard status and level progress.
*   **Team Details:** Roster listing showing leader contacts.
*   **Level Tree:** Personal progression tree for Levels 7–11.
*   **Waste Management:** Upload tool and collection receipt queue.
*   **Payment Transactions:** Payout status list and bank receipts.
*   **Collection Centers:** Map routing to regional centers.
*   **Settings:** Security updates.

### 2.4 Admin Dashboard Navigation (Double Tier Sidebar)
*   **Overview:** Global analytics summary charts.
*   **Leader Applications:** Queue for vetting and approving applicants.
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

### 2.5 Developer Dashboard Navigation (System Control Console)
*   **Overview:** Real-time health metrics.
*   **System Monitoring:** CPU, Memory, and active database pool monitors.
*   **Security Center:** System logs for failed logins and access blocks.
*   **System Logs:** Real-time runtime outputs.
*   **Audit Explorer:** Advanced SQL logs inspector.
*   **Backup Center:** Database dump and restore triggers.
*   **Data Management:** Data cleanups and maintenance tools.
*   **Feature Controls:** Toggle flags for modular features.
*   **Announcements:** Technical notification creator.
*   **Settings:** System configurations.

---

## 3. Public Website Pages

### 3.1 Common Page Layout Elements
*   **Navigation Bar:** Sticky top navigation panel. Desktop shows inline links; mobile shows a hamburger menu that opens a sliding overlay drawer.
*   **Footer Content:** Site index, official contact details, security credentials, copyright notices, and links to the Privacy Policy and Terms of Service.

---

## 4. Home Page

*   **Hero Section:** High-contrast background banner featuring the headline *"Athiyaman Platform – Digital India Initiative"* with the subtitle *"Join Community Growth, Build Local Teams, Recycle Waste, and Earn Verifiable Rewards."* Includes two action buttons: `Become Team Leader` (Blue) and `Login` (Green outline).
*   **Mission Block:** A clean section detailing our goals: empowering citizens, digitizing field operations, and supporting local communities.
*   **Vision Block:** Highlights regional development plans and upcoming Phase 2 (Skill India) and Phase 3 (Clean India) modules.
*   **Initiative Highlights Carousel:** Displays three interactive cards:
    1.  *Digital India (Phase 1):* Waste collection and digital reward milestones.
    2.  *Skill India (Phase 2):* Future training courses and certifications.
    3.  *Clean India (Phase 3):* Future logistics routing and municipal center expansion.
*   **Statistics Banner:** A dynamic component displaying real-time metrics (Admin configurable):
    *   *Total Teams:* $1,240$
    *   *Total Registered Members:* $45,890$
    *   *Approved Waste Recycled:* $120,450\text{ KG}$
*   **Behavioral Rules:** All statistics display with standard loading skeletons. Call-to-action buttons redirect visitors immediately to the application form or authentication gateway.

---

## 5. About Page

*   **Organization Overview:** High-contrast text detailing the founding agency, administrative partners, and program goals.
*   **Platform Overview:** Explains the technology stack, the role of local collection centers, and the audit trail security structure.
*   **Core Principles Grid:** Dynamic grid showcasing four core pillars: *Transparency*, *Traceability*, *Accountability*, and *Citizen Incentivization*.

---

## 6. Initiatives Page

*   **Interactive Cards Layout:** Three full-width layout segments highlighting the project's phases.
*   **Digital India Segment:** Currently active. Explains the signup system, team setups, level milestones, waste verification rules, and payout processes.
*   **Skill India Segment:** Disabled template block showing a *"Phase 2 - Coming Soon"* label, with illustrative details on future courses and certificates.
*   **Clean India Segment:** Disabled template block showing a *"Phase 3 - Coming Soon"* label, detailing future waste transit logistics and coordinator networks.

---

## 7. Waste Management Information Page

*   **Educational Guidelines Block:** A clear reference list of allowed and prohibited materials, using visual indicators:
    *   *Allowed (Green checkmarks):* Clean plastic bottles, dry food containers, packaging sleeves.
    *   *Prohibited (Red X marks):* Hazardous chemicals, biological items, organic food garbage.
*   **Process Visualizer Map:** A clean flow chart highlighting the submission steps:
    $$\text{Physical Deposit at Center} \rightarrow \text{Upload weight and photo} \rightarrow \text{Admin Audits photo} \rightarrow \text{Level balance updates}$$

---

## 8. Become Team Leader Page

```
┌────────────────────────────────────────────────────────┐
│             Become a Team Leader - Application         │
├────────────────────────────────────────────────────────┤
│  [ Full Name ]             [ Email Address ]           │
│  [ Phone Number ]          [ Aadhaar Number ]          │
│  [ District Selector ]     [ Pincode Input ]           │
│  [ Full Physical Home Address Textarea ]               │
│  [ Tell us why you want to become a Leader ]           │
│                                                        │
│                      [ Submit Application ]            │
└────────────────────────────────────────────────────────┘
```
*   **Form Validation Protocols:**
    *   *Full Name:* Required; accepts only letters and spaces ($5$ to $100$ characters).
    *   *Phone Number:* Required; validates as a $10$-digit numeric sequence.
    *   *Email:* Required; validates correct formatting standards.
    *   *Aadhaar Number:* Required; validates as a $12$-digit numeric sequence.
    *   *Pincode:* Required; validates as a $6$-digit numeric sequence.
    *   *District:* Required; select dropdown populated by district databases.
*   **Submission Behavior:** Clicking submit displays a loading spinner overlay. Successful submission redirects to the Success Screen.
*   **Success Screen:** Displays a green checkmark icon with the message *"Application Submitted Successfully! Our administration will review your credentials and location capacity. Approved leaders will receive their Leader Referral signup link via email/SMS."*
*   **Failure Screen:** Shows a red error icon with the message *"Submission Failed. Please check your network connection and ensure all fields are valid."*

---

## 9. Contact Page

*   **Information Panel:** Displays our official support email, central telephone number, physical office address, and operational hours ($9:00\text{ AM} - 6:00\text{ PM}$).
*   **Contact Form:** Simple form with fields for *Name*, *Phone*, *Subject*, and *Message*. Submitting the form shows a success toast message.

---

## 10. Login Page

*   **Fields Layout:** Clean, centered container box containing *Username* and *Password* inputs.
*   **Client Validation:**
    *   *Username:* Required; alphanumeric ($5$ to $30$ characters).
    *   *Password:* Required; minimum $8$ characters.
*   **Error Messaging & Lockout:** Displays clean inline warnings:
    *   *"Incorrect Username or Password. Please try again."*
    *   *"Account is suspended. Please contact platform support."*
    *   **Account Lockout:** Accounts are temporarily locked after **5 failed login attempts** within an hour, returning a lockout message in the UI.
*   **Role Redirect Actions:** The backend checks user roles upon login, redirecting users to their corresponding dashboards:
    *   `LEADER` $\rightarrow$ `/dashboard/leader/overview`
    *   `MEMBER` $\rightarrow$ `/dashboard/member/overview`
    *   `ADMIN` $\rightarrow$ `/dashboard/admin/overview`
    *   `DEVELOPER` $\rightarrow$ `/dashboard/developer/overview`

---

## 11. Registration Page

```
┌────────────────────────────────────────────────────────┐
│                 Citizen Registration Portal            │
├────────────────────────────────────────────────────────┤
│  [ Referral Code ] (Admin Issued / Leader Shared)      │
│  [ Desired Username ]                                  │
│  [ Password ]              [ Confirm Password ]        │
│  [ Mobile Number ]         [ SMS OTP Code ]            │
│                                                        │
│  [ ] I accept the Privacy Policy and Terms of Use.     │
│                                                        │
│                            [ Register Account ]        │
└────────────────────────────────────────────────────────┘
```
*   **Strict Input Validations:**
    *   *Referral Code:* Checks length and characters; shows a green checkmark once verified by API.
    *   *Passwords:* Verifies complexity and matches.
    *   *OTP code:* Requires a $6$-digit numeric sequence. Shows a countdown timer ($5\text{ minutes}$) with a *"Resend OTP"* option when expired.
*   **Success Flow:** Displays a verification message, redirects to the login screen, and populates the username automatically.

---

## 12. First Login Experience

*   **Profile Completion Overlay Modal:** A non-dismissible popup modal that locks the dashboard upon first login. It displays the message *"Complete Your Profile to Unlock Your Dashboard."*
*   **Progress Indicator:** Features a progress bar that scales from $0\%$ to $100\%$ as sections are completed:
    $$\text{Personal (20\%)} \rightarrow \text{Contact (10\%)} \rightarrow \text{Address (10\%)} \rightarrow \text{Aadhaar (20\%)} \rightarrow \text{Bank (30\%)} \rightarrow \text{Nominee (10\%)}$$
*   **Rules Acceptance Screen:** A follow-up step presenting the platform's terms of use, privacy policy, and program rules. Users must click an active `I Agree` button to unlock the dashboard.

---

## 13. Leader Dashboard Structure

Features a sidebar navigation panel with links to all 12 operational views.

---

## 14. Leader Dashboard Overview Page

*   **Profile Completion Card:** Displays a warning badge if the profile is incomplete, showing the progress score and directing the user to the profile setup screen.
*   **Team Level Progress Widget:** Displays a progress card for the team's level (Levels 1–6):
    *   Displays current active members and required thresholds (e.g., Level 2: `45 / 90 Members`).
*   **Personal Level Progress Widget:** Displays a progress card for individual level progress (Levels 7–11):
    *   Displays approved waste weights collected (e.g., Level 7: `6.5 / 10.0 KG`).
*   **Active Referrals Card:** Shows the active team referral code with a `Copy Code` button, sharing instructions, and current usage count.
*   **Notifications Panel:** Displays the latest three in-app notifications with read/unread indicators.
*   **Recent Activities Table:** Shows the latest five logs (e.g., member registration, waste verification approval).

---

## 15. Team Details Page

*   **Team Profile Block:** Displays the team's name, unique team code, district, neighborhood area, pincode registry, and team creation date.
*   **Team Statistics Grid:** Displays analytical summary widgets:
    *   *Active Members:* $210$
    *   *Levels Cleared:* $2\text{ of } 6$
    *   *Total Combined Waste Recycled:* $1,420\text{ KG}$
*   **Operational Status Badge:** Shows the team's status: `ACTIVE` (Green) or `SUSPENDED` (Red).

---

## 16. Team Members Page

*   ** Roster Table Layout:**
    | Member Name | Username | Joining Date | Active Level | Profile Status | Actions |
    | :--- | :--- | :--- | :--- | :--- | :--- |
    | Ramesh Kumar | `ramesh99` | 2026-05-10 | Level 7 | Complete (100%) | `View Profile` |
*   **Search Component:** Real-time text filter matching Member Names or Usernames.
*   **Filter Options:** Dropdowns to filter by *Level* or *Profile Completeness*.
*   **Pagination Bar:** Simple navigation footer (`First | Previous | 1 | 2 | 3 | Next | Last`).

---

## 17. Referral Management Page

*   **Active Referral Generator Panel:** Displays the current active code. Reaching the usage limit enables a `Generate Next Referral Code` button.
*   **Referral Capacity Chart:** Shows a progress indicator matching team growth metrics.
*   **Referral Logs Table:**
    | Referral Code | Linked Level | Generated Date | Usage Counts | Status |
    | :--- | :--- | :--- | :--- | :--- |
    | `MAD-LEADER-98` | Level 2 | 2026-05-01 | `45 / 90 Used` | `ACTIVE` |

---

## 18. Team Progress Page

*   **Progression Map:** A linear progress visualization showing Levels 1 to 6.
*   **Threshold Metrics Panel:** Details member targets for the current level (e.g., Level 3 requires $720$ members, $420$ remaining).
*   **Claim Reward Action:** Reaching a level milestone unlocks the `Claim Reward` button. No second claim can be created while one is in `PENDING` state, preventing duplicate claims. Level progress is locked during claim review; new progress accumulated is separate and stored in future level buckets.

---

## 19. My Progress Page

*   **Personal Progress Widget:** Tracks individual progress through Levels 7 to 11.
*   **Waste Milestone Tracker:** Shows approved waste weight balances (e.g., `4.5 KG / 10.0 KG`).
*   **Progress Visualization:** Displays a radial gauge highlighting progress toward the next personal level.

---

## 20. Level Tree Page

```
                                  [ LEVEL 6 ] (Reward: ₹5000)
                                       ▲
                                  [ LEVEL 5 ] (Reward: ₹4000)
                                       ▲
     [ TEAM PROGRESS ] ───────────►[ LEVEL 4 ] (Reward: ₹3000) ◄─── [ CURRENT TEAM LEVEL ]
                                       ▲
                                  [ LEVEL 3 ] (Reward: ₹2000)
                                       ▲
                                  [ LEVEL 2 ] (Reward: ₹1000)
                                       ▲
                                  [ LEVEL 1 ] (Reward: ₹100)
     
     ───────────────────────────────────────────────────────────────────────────────────────
     
                                  [ LEVEL 11 ] (Reward: ₹50000)
                                       ▲
                                  [ LEVEL 10 ] (Reward: ₹40000)
                                       ▲
     [ PERSONAL PROGRESS ] ───────►[ LEVEL 9 ] (Reward: ₹30000)  ◄─── [ CURRENT PERSONAL LEVEL ]
                                       ▲
                                  [ LEVEL 8 ] (Reward: ₹20000)
                                       ▲
                                  [ LEVEL 7 ] (Reward: ₹10000)
```
*   **Visual Interface Controls:**
    *   *Completed Nodes:* Marked with a solid green background and a checkmark icon.
    *   *Active Node:* Highlighted with an amber border and pulse animation.
    *   *Locked Nodes:* Displayed with gray backgrounds and lock icons.
    *   Hovering over any node displays a popup detailing level requirements and reward amounts.

---

## 21. Waste Management Page

*   **Submission Form Dialog:**
    *   *Collection Center:* Dropdown menu of geocoded locations.
    *   *Weight (KG):* Numeric input (validated from $0.1$ to $50.0\text{ KG}$).
    *   *Photo Upload:* File field accepting JPEG, PNG, or PDF files showing waste on a scale. Upload service validates actual file structure (magic bytes), dynamically strips metadata/EXIF headers, renames files using UUIDv7, stores files outside public web directories, and NGINX blocks execution on storage folders.
*   **Waste Log History Table:**
    | Photo Preview | Center Location | Weight (KG) | Submit Date | Verification Status | Payment Status |
    | :--- | :--- | :--- | :--- | :--- | :--- |
    | `Image Thumbnail` | Madurai Center A | $12.5\text{ KG}$ | 2026-05-15 | `PENDING` (Amber) | `UNPAID` (Gray) |
*   **Log Filters:** Filter by *Verification Status* (`Pending`, `Approved`, `Rejected`) or *Date Range*.

---

## 22. Payment Transactions Page

*   **Reward Accounts Balance Grid:** Displays summary widgets:
    *   *Total Earned:* ₹11,100
    *   *Paid Out:* ₹1,100
    *   *Processing:* ₹10,000
*   **Transactions Table:**
    | Claim ID | Reward Type | Level Milestone | Claim Date | Disbursed Date | Bank Tx Reference | Status |
    | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
    | `CLM-8291` | Team Level 2 | Level 2 | 2026-05-01 | 2026-05-03 | `TXN-90218201` | `PAID` (Green) |

---

## 23. Collection Centers Page

*   **Interactive Locator Grid:** Displays regional collection centers, searchable by pincode or district.
*   **Geomap Panel:** A Google Maps dashboard plotting active regional collection centers.
*   **Navigation Cards:** Selecting a center displays details including the center's name, address, phone number, and a `Get Directions` button that opens Google Maps navigation.

---

## 24. Settings Page

*   **Profile Settings Form:** Enables updates to profile photo, phone number, and email. Locked details (Aadhaar, bank routing) show a warning badge redirecting users to support channels.
*   **Security Settings Form:** Contains *Current Password*, *New Password*, and *Confirm Password* inputs.
*   **Notification Settings Form:** Toggle switches to manage email and system alert preferences.

---

## 25. Member Dashboard Structure

Features a sidebar navigation panel with links to all 7 member-specific dashboard views.

---

## 26. Member Overview Page

*   **Personal Progression Widget:** Shows individual level progress (Levels 7–11), approved waste weights, and active claim states.
*   **Notification Alert Panel:** Displays real-time updates for waste approvals and payout changes.
*   **Recent Activity Log:** Roster of recent submissions and level achievements.

---

## 27. Member Team Details Page

*   **Roster Listing Panel:** Shows details for the user's active team: team name, unique code, district, and owner identity.
*   **Leader Contact Card:** Provides direct email and support details for the Team Leader to coordinate local collections.

---

## 28. Member Level Tree Page

*   **Personal progression tree:** Identical tree view to the Leader's tree, displaying only the individual progression roadmap (Levels 7–11).

---

## 29. Member Waste Management Page

*   **Waste Log Form:** Enables direct logging of waste weights, center selections, and photo uploads.
*   **Personal Logs Table:** Displays a history list of the member's waste submissions, showing weight measurements, approval states, and review dates.

---

## 30. Member Payment Page

*   **Disbursement Registry:** Dashboard displaying the member's completed milestones, claim dates, approval timelines, and bank transaction reference numbers.

---

## 31. Admin Dashboard Structure

Features a sidebar navigation panel with links to all 14 administrative control portals.

---

## 32. Admin Dashboard Overview

*   **Platform Statistics Grid:** Displays high-level system metrics:
    *   *Active Citizens:* $50,210$
    *   *Active Teams:* $1,210$
    *   *Pending Waste Approvals:* $142$
    *   *Pending Reward Claims:* $32$
    *   *Total Rewards Disbursed:* ₹1,240,000
*   **Analytics Visualization Panel:** Displays platform growth trends, waste collection volumes, and financial payout charts.

---

## 33. Leader Applications Page

*   **Applications Roster Table:**
    | Applicant Name | Mobile | Email | District | Pincode | Apply Date | Status | Actions |
    | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
    | K. Arumugam | `9842101234` | `aru@email.com` | Madurai | 625001 | 2026-05-20 | `PENDING` | `Review Application` |
*   **Review Action Overlay Panel:**
    *   Displays full application details (Aadhaar, address, and applicant notes).
    *   *Approve:* Triggers a confirmation modal, registers the user, and sends a signup code.
    *   *Reject:* Requires an admin comment detailing the reason for rejection before processing.

---

## 34. User Management Page

*   **User Registry Table:** Details all platform users, their roles, and status flags.
*   **Administrative Actions:** Includes one-click buttons to `View Profile`, `Suspend Account`, `Activate Account`, or `Reset Password`.
*   **Filter Panel:** Dropdowns to filter user lists by *Role*, *District*, or *Account Status*.

---

## 35. Team Management Page

*   **Teams Directory Table:** Details active teams, leader names, member counts, and levels.
*   **Administrative Operations Panel:** Allows admins to suspend teams or view detailed member rosters and level progress logs.

---

## 36. Referral Management Page

*   **Referral Directory Table:** Displays all active codes, code types (`LEADER_REFERRAL` / `TEAM_REFERRAL`), utilization stats, and expirations.
*   **Admin Code Generator:** Panel to generate single-use `LEADER_REFERRAL` codes, with custom expiration settings.

---

## 37. Waste Verification Page

```
┌────────────────────────────────────────────────────────┐
│             Waste Record Audit & Verification          │
├────────────────────────────────────────────────────────┤
│  [ Uploaded Photo Evidence ]                           │
│  User: Suresh Kumar (`suresh88`)                       │
│  Weight Claimed: 18.5 KG                               │
│  Location Center: Madurai Center A                     │
│  Collection Date: 2026-05-22                           │
│                                                        │
│  Admin Comments: [ Write audit notes here...         ] │
│                                                        │
│            [ Approve Weight ]      [ Reject Record ]   │
└────────────────────────────────────────────────────────┘
```
*   **Verification Controls:**
    *   `Approve Weight`: Approves the record, updates the user's level progress, and triggers an in-app alert.
    *   `Reject Record`: Requires an admin comment explaining the rejection before processing.

---

## 38. Reward Claims Page

*   **Claims Queue Table:** Details outstanding claims, user accounts, completed levels, and reward amounts.
*   ** Vetting Actions:** Admins can verify bank credentials, view profile logs, and approve claims to route them to the payment queue.

---

## 39. Payments Page

*   **Outstanding Payments Queue:** Details approved claims ready for disbursement.
*   **Disbursement Form Dialog:**
    *   *Transaction Reference Number:* Required text input from bank portals.
    *   *Disbursement Date:* Calendar date selector.
    *   *Audit Notes:* Text area for tracking notes.
*   **Disbursement Execution:** Clicking `Confirm Payout` records the transaction references, marks the claim as paid, and notifies the user.

---

## 40. Collection Center Management Page

*   **Collection Center Registry Table:** Lists authorized centers, regional districts, and geocodes.
*   **Center Operations Panel:** Form inputs to add centers, edit details, or toggle operational statuses.

---

## 41. Notifications Page

*   **Broadcast Interface Panel:** Form inputs to manage announcements:
    *   *Target:* Dropdown to select targets (`All Users`, `Leaders`, `Members`, `Specific Team`).
    *   *Message:* Text area supporting rich markdown formats.
*   **Transmission Logs:** Displays past announcements, target lists, delivery status rates, and admin IDs.

---

## 42. Analytics Page

*   **Report Generation Panel:** Provides tools to export platform analytics (growth trends, waste totals, and financial metrics) as PDF or CSV files.

---

## 43. Documents Page

*   **Citizen Document Audit Panel:** Interface to review uploaded citizen documents (Aadhaar cards, bank books, nominee records) using side-by-side photo audit tools.

---

## 44. Audit Logs Page

*   **System Event Registry Table:**
    | Timestamp | User Account | Active Role | Action Logged | Targeted Entity | IP Address |
    | :--- | :--- | :--- | :--- | :--- | :--- |
    | 2026-05-23 12:00:00 | `admin_santhosh` | Admin | Approve Claim | `CLM-8291` | `192.168.1.1` |
*   **Advanced Filter Panel:** Search logs by *User Account*, *Event Category*, *IP Address*, or *Date Range*.

---

## 45. Developer Dashboard Structure

Features a sidebar navigation panel with links to all 10 developer maintenance views.

---

## 46. Developer Overview Page

*   **System Health Summary Panel:** Displays indicators for system uptime, active connection pools, API status, and database health.
*   **Diagnostic Widgets:** Tracks online users and API request latency trends.

---

## 55. Responsive Layout Specifications

The platform UI adapts fluidly to different screen sizes:

*   **Desktop Viewport Layout ($1440\text{px}$):** Left-docked navigation sidebar ($260\text{px}$ width) with the main content panel rendering in a fluid grid ($1180\text{px}$).
*   **Tablet Viewport Layout ($768\text{px}$):** Sidebar collapses into an icon-only dock ($80\text{px}$ width). Table views transition to multi-line list cards to preserve readability.
*   **Mobile Viewport Layout ($360\text{px}$):** Sidebar navigation collapses into a slide-out hamburger menu drawer. Data tables transition into single-column cards with responsive spacing.

---

## 56. Accessibility Requirements

*   **Screen Reader Labels:** All interactive elements (buttons, form inputs, geocode panels) must include explicit `aria-label` tags.
*   **Contrast Standards:** Text elements must maintain a minimum contrast ratio of $4.5:1$ against backgrounds, using deep blues on off-white surfaces.
*   **Keyboard Navigation Support:** Users can navigate forms, navigation menus, and dialog buttons using standard `Tab` and `Enter` inputs.

---

## 57. Error Handling Interface Specs

*   **404 Not Found Page:** Displays a clear government-style layout with the message *"The page you are looking for does not exist."* Includes a primary return button redirecting users to the home dashboard.
*   **403 Forbidden Page:** Displays a shield icon and the message *"You do not have administrative clearance to access this portal."* Access attempts are logged in the audit trail.
*   **500 Internal Error Page:** Shows the message *"An unexpected database error has occurred. Our development team has been alerted."* Includes a primary retry button.
*   **Session Timeout Alert Modal:** A dismissible overlay popup warning that appears $2\text{ minutes}$ before token expiry, providing a button to renew the session.

---

## 58. Notification UX

*   **Real-time Alerts Panel:** Notifications appear in the dashboard header as a bell icon badge showing unread counts.
*   **Alert Categorization:**
    *   *High Priority (Red):* Account updates, failed logins, and payout rejections.
    *   *Medium Priority (Amber):* Verification reviews and new team signups.
    *   *Low Priority (Blue):* Welcomes, level milestones, and announcements.
*   **Dismissal Actions:** Users can mark notifications as read individually or clear all items.

---

## 59. Dynamic Loading States

*   **Skeleton Screens:** Used for charts, profiles, and tables during API loads.
*   **Button Load Indicators:** Clicking action buttons transitions them to loading states, disabling secondary clicks during processing.

---

## 60. Conclusion

This Pages & User Interface Specification Document (`02_PAGES.md`) provides the absolute screen-by-screen, layout, widget, component, and interaction blueprints for the Athiyaman Platform – Digital India Phase 1. By detailing layout grids, responsive breakpoints, access configurations, and accessibility rules, it serves as a complete reference for engineering teams. All front-end builds and component systems must adhere strictly to these guidelines, ensuring a highly performant, accessible, and consistent user experience.
