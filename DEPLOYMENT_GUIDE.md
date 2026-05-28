# Athiyaman Platform - Deployment & Setup Guide

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL 12+
- Node.js 18+
- npm or yarn

### Backend Setup

1. **Install Python Dependencies**
   ```bash
   cd d:\Athiyaman
   pip install -r requirements.txt
   ```

2. **Setup Environment Variables**
   Create/update `.env` file:
   ```env
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=athiyaman
   DB_USER=postgres
   DB_PASSWORD=<your-password>
   
   JWT_SECRET=<generate-secure-secret>
   JWT_ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=15
   REFRESH_TOKEN_EXPIRE_DAYS=7
   
   STORAGE_TYPE=LOCAL
   STORAGE_PATH=d:\Athiyaman\uploads
   ```

3. **Database Setup**
   ```bash
   # Create PostgreSQL database
   psql -U postgres
   CREATE DATABASE athiyaman;
   
   # Run migrations
   cd backend
   alembic upgrade head
   
   # Load seed data
   psql -U postgres -d athiyaman -f ../database/seed.sql
   ```

4. **Start Backend Server**
   ```bash
   cd backend
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```
   - Server runs at: http://localhost:8000
   - Swagger docs: http://localhost:8000/docs

### Frontend Setup

1. **Install Frontend Dependencies**
   ```bash
   cd frontend
   npm install
   ```

2. **Start Development Server**
   ```bash
   npm run dev
   ```
   - Frontend runs at: http://localhost:5173

3. **Build for Production**
   ```bash
   npm run build
   npm run preview
   ```

---

## 🌐 Public Website Structure

### Pages
- **/** → Home page with registration CTA
- **/about** → Platform mission & values
- **/how-it-works** → Generic process overview
- **/plans** → Phase roadmap (Digital/Skill/Clean India)
- **/gallery** → Community images (placeholder)
- **/contact** → Contact form & support info

### Key Design Principle
**Public website shows GENERAL information only:**
- No sensitive details about payment structure
- No complete level requirements
- No internal processes
- Links direct users to login for complete information

---

## 🔐 Instructions Page (Protected)

### Access
- **Only available after login**
- Route: `/instructions`
- Requires authentication

### Content (7 Tabs)
1. **Overview** - Quick start guide, platform features
2. **Levels** - Complete 10-level system with rewards (₹500 to ₹100,000)
3. **Payments** - Timeline, bank account setup, FAQs
4. **Waste** - Submission guide, pricing, tips
5. **Teams** - Leadership guide, requirements, management
6. **Claims** - Reward claim process, statuses
7. **Support** - Contact info, FAQs, resources

**Complete payment structures, level requirements, and earnings details are ONLY on this page.**

---

## 📊 Key Differences: Public vs Protected

| Information | Public Site | Instructions Page |
|-----------|-----------|----------|
| Phase overview | ✓ (General) | ✓ (Detailed) |
| How to join | ✓ (Steps) | ✓ (Complete) |
| Level system | ✗ Generic only | ✓ Full details |
| Payment amounts | ✗ | ✓ Complete structure |
| Earnings calculation | ✗ | ✓ Detailed |
| Team requirements | ✗ | ✓ All 5 levels |
| Waste pricing | ✗ | ✓ By type |
| Contact info | ✓ | ✓ |

---

## 🛠️ Critical Issues Fixed

### 1. ✅ Dependencies
- **Issue:** 9 core packages missing
- **Fix:** Updated requirements.txt with 20+ packages
- **Status:** All dependencies installed

### 2. ✅ Directory Typo
- **Issue:** `/backend/utlils/` should be `/backend/utils/`
- **Fix:** 
  - Created correct directory
  - Migrated files
  - Updated 9 import statements
- **Status:** All imports fixed

### 3. ✅ Public Website
- **Issue:** No public landing site
- **Fix:** Created 7-page public website with proper information hierarchy
- **Status:** Complete and integrated

### 4. ✅ Instructions
- **Issue:** No comprehensive guide for logged-in users
- **Fix:** Created 7-tab instructions page with complete information
- **Status:** Complete and protected

---

## 📦 Component Library

### Created Components
```typescript
// UI Components (frontend/src/components/athi/index.tsx)
- Button (4 variants)
- Input (with validation)
- Card
- Modal (3 sizes)
- Alert (4 types)
- Badge (4 variants)
- Loading
- Navbar
- Table
- ProfileGuard
```

### Usage Example
```typescript
import { Button, Modal, Card, Alert } from './components/athi';

<Card>
  <h2>Welcome</h2>
  <Alert type="success" message="Setup complete!" />
  <Button variant="primary" onClick={handleClick}>
    Click Me
  </Button>
</Card>
```

---

## 🔄 Application Flow

```
┌─────────────────────┐
│   User Visits App   │
└──────────┬──────────┘
           ↓
    ┌─────────────────┐
    │ Public Website  │
    │   (General Info)│
    └────────┬────────┘
             ↓
    ┌────────────────────┐
    │ Login/Signup Page  │
    │  (/login, /signup) │
    └────────┬───────────┘
             ↓
    ┌────────────────────┐
    │ Authenticated User │
    │ (JWT Token)        │
    └────────┬───────────┘
             ↓
    ┌────────────────────┐
    │ Instructions Page  │
    │ (Complete Details) │
    └────────┬───────────┘
             ↓
    ┌────────────────────┐
    │ Dashboard/Features │
    │ (Waste, Claims,    │
    │  Teams, etc.)      │
    └────────────────────┘
```

---

## 📋 Testing the Setup

### 1. Test Backend
```bash
curl http://localhost:8000/docs
# Should see Swagger UI with all endpoints
```

### 2. Test Public Website
```bash
# Open http://localhost:5173
# Check pages:
- / (Home)
- /about (About)
- /how-it-works (How It Works)
- /plans (Plans)
- /contact (Contact)
```

### 3. Test Authentication
```bash
# Try to access protected route
http://localhost:5173/instructions
# Should redirect to /login

# After login, should see Instructions page
```

---

## 🐳 Docker Setup (Optional)

### Dockerfile - Backend
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0"]
```

### Dockerfile - Frontend
```dockerfile
FROM node:18 AS builder
WORKDIR /app
COPY . .
RUN npm install && npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
```

### docker-compose.yml
```yaml
version: '3.8'
services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: athiyaman
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    depends_on:
      - postgres

  frontend:
    build: ./frontend
    ports:
      - "3000:80"
```

---

## 📝 Next Steps

### Phase 1: Make App Runnable
- [ ] Create Login page UI
- [ ] Create Signup page UI
- [ ] Deploy database
- [ ] Test API connectivity

### Phase 2: Core Features
- [ ] Dashboard pages
- [ ] Waste submission form
- [ ] Claims workflow
- [ ] Team management

### Phase 3: Production
- [ ] Full test coverage
- [ ] Docker deployment
- [ ] CI/CD pipeline
- [ ] Performance optimization

---

## 🆘 Troubleshooting

### Backend won't start
```bash
# Check Python version
python --version  # Should be 3.11+

# Reinstall dependencies
pip install --force-reinstall -r requirements.txt

# Check database connection
psql -U postgres -d athiyaman
```

### Frontend won't load
```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install

# Check if port 5173 is available
netstat -an | grep 5173
```

### Database connection errors
```bash
# Verify PostgreSQL is running
pg_isready -h localhost -p 5432

# Check .env file has correct credentials
cat .env | grep DB_
```

---

## 📞 Support

For issues or questions:
- Email: support@athiyaman.in
- Phone: +91-XXXX-XXXX-XX
- Documentation: See Instructions page (after login)

---

## 📄 Files & Folders

```
d:\Athiyaman\
├── backend/
│   ├── main.py
│   ├── api/v1/api.py
│   ├── modules/              (14 modules)
│   ├── core/
│   ├── database/
│   ├── utils/                ✅ (FIXED)
│   ├── security/
│   ├── middleware/
│   └── migrations/
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── public/       ✅ (NEW)
│   │   │   ├── Instructions.tsx  ✅ (NEW)
│   │   │   └── ...
│   │   ├── components/
│   │   │   └── athi/         ✅ (NEW)
│   │   ├── lib/
│   │   └── App.tsx           ✅ (UPDATED)
│   └── package.json
├── database/
│   ├── schema.sql
│   ├── seed.sql
│   └── deploy.py
├── docs/
│   ├── development/
│   └── database/
├── requirements.txt          ✅ (FIXED)
└── .env
```

---

## ✅ Completion Checklist

- ✅ Fixed missing dependencies
- ✅ Fixed directory typo (utlils → utils)
- ✅ Created component library
- ✅ Built public website (6 pages)
- ✅ Created instructions page
- ✅ Updated routing
- ✅ Proper security (public vs protected)
- ✅ Documentation complete

**System is ready for next development phase!**
