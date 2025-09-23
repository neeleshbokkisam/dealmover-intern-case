# Test Suite for PDF Financial Data Extraction

This directory contains comprehensive tests for the PDF financial data extraction system.

## Test Structure

```
tests/
├── unit/                    # Unit tests for individual functions
│   └── test_pdf_parser.py   # PDF parsing and financial extraction tests
├── integration/             # Integration tests for API endpoints
│   └── test_api.py          # API endpoint and error handling tests
├── __init__.py
└── README.md               # This file
```

## Running Tests

### All Tests
```bash
cd backend
source venv/bin/activate
python -m pytest tests/ -v
```

### Unit Tests Only
```bash
python -m pytest tests/unit/ -v
```

### Integration Tests Only
```bash
python -m pytest tests/integration/ -v
```

### Specific Test File
```bash
python -m pytest tests/unit/test_pdf_parser.py -v
```

## Test Coverage

### Unit Tests (17 tests)
- **PDF Text Extraction**: Success and error scenarios
- **Financial Value Cleaning**: Positive, negative, and edge cases
- **Pattern Matching**: Success, failure, and multiple pattern scenarios
- **Financial Values Extraction**: Complete, partial, and no-data scenarios
- **Real-World Patterns**: Google 10-K style document patterns

### Integration Tests (10 tests)
- **API Endpoint**: GET/POST method handling
- **File Upload**: Valid PDF, invalid file types, empty files
- **Error Handling**: Malformed requests, extraction failures
- **Data Processing**: Successful extraction, partial data, large files

## Test Features

- **Mocking**: Uses `unittest.mock` for PDF processing and external dependencies
- **Django Integration**: Proper Django test client and database setup
- **Error Scenarios**: Comprehensive error handling validation
- **Real Data Patterns**: Tests based on actual 10-K document structures
- **Edge Cases**: Empty values, malformed data, missing fields

## Test Configuration

- **pytest.ini**: Django settings and test discovery configuration
- **conftest.py**: Django setup for pytest integration
- **run_tests.py**: Custom test runner script

## Dependencies

- `pytest==8.4.2`
- `pytest-django==4.11.1`
- `Django==4.2.24`
- `djangorestframework==3.16.1`

## Test Results

All 27 tests pass successfully, providing comprehensive coverage of:
- PDF text extraction functionality
- Financial data parsing and cleaning
- API endpoint behavior
- Error handling and edge cases
- Real-world document patterns
