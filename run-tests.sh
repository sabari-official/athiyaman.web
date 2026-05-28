#!/bin/bash
# Test runner script for the entire project

set -e

echo "======================================"
echo "Athiyaman Platform - Test Suite"
echo "======================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Backend Tests
echo -e "\n${YELLOW}Running Backend Tests...${NC}"
cd backend
python -m pytest tests/ -v --tb=short --cov=. --cov-report=html:../coverage/backend --cov-report=term

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Backend tests passed${NC}"
else
    echo -e "${RED}✗ Backend tests failed${NC}"
    exit 1
fi

# Go back to root
cd ..

# Frontend Tests
echo -e "\n${YELLOW}Running Frontend Tests...${NC}"
cd frontend
npm run test:coverage

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Frontend tests passed${NC}"
else
    echo -e "${RED}✗ Frontend tests failed${NC}"
    exit 1
fi

# Go back to root
cd ..

# Lint Backend
echo -e "\n${YELLOW}Linting Backend Code...${NC}"
flake8 backend --count --statistics || true
black --check backend || true

# Lint Frontend
echo -e "\n${YELLOW}Linting Frontend Code...${NC}"
cd frontend
npm run lint || true
cd ..

echo -e "\n${GREEN}======================================"
echo "Test Suite Completed Successfully!"
echo "=====================================${NC}"
echo -e "\nCoverage Reports:"
echo "- Backend: coverage/backend/index.html"
echo "- Frontend: frontend/coverage/index.html"
