# DealMover Intern Case Study

A simplified DealMover workflow that extracts key financial values from a 10-K PDF and displays them in a grid.

## Project Structure

```
dealmover-intern-case/
├── backend/           # Django backend
├── frontend/          # React frontend
├── tests/            # Test files
├── README.md         # This file
├── AI_USAGE.md       # AI tools usage disclosure
└── DECISIONS.md      # Assumptions and trade-offs
```

## Setup Instructions

### Backend (Django)
```bash
cd backend
pip install -r requirements.txt
python manage.py runserver
```

### Frontend (React)
```bash
cd frontend
npm install
npm run dev
```

## Features

- **Backend**: `/api/extract/` endpoint that accepts PDF uploads and extracts Revenue and Cost of Sales
- **Frontend**: React component for PDF upload and results display in a spreadsheet-like grid

## API Endpoint

**POST** `/api/extract/`
- Accepts: PDF file upload and optional period_end_date (YYYY-MM-DD format)
- Returns: JSON with extracted financial data

Example response:
```json
{
  "period_end_date": "2024-12-31",
  "results": {
    "revenue": "350018",
    "cos": "146306"
  }
}
```
