@echo off
REM Test runner script for Windows

echo.
echo ======================================
echo Athiyaman Platform - Test Suite
echo ======================================

REM Backend Tests
echo.
echo Running Backend Tests...
cd backend
python -m pytest tests/ -v --tb=short --cov=. --cov-report=html:..\coverage\backend --cov-report=term
if errorlevel 1 (
    echo Backend tests failed
    exit /b 1
)
cd ..

REM Frontend Tests
echo.
echo Running Frontend Tests...
cd frontend
call npm run test:coverage
if errorlevel 1 (
    echo Frontend tests failed
    exit /b 1
)
cd ..

REM Lint Backend
echo.
echo Linting Backend Code...
flake8 backend --count --statistics

REM Lint Frontend
echo.
echo Linting Frontend Code...
cd frontend
call npm run lint
cd ..

echo.
echo ======================================
echo Test Suite Completed Successfully!
echo ======================================
echo.
echo Coverage Reports:
echo - Backend: coverage\backend\index.html
echo - Frontend: frontend\coverage\index.html
