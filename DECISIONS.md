# Design Decisions and Assumptions

This document outlines key assumptions and trade-offs made during development.

## Assumptions

### PDF Parsing
- **Assumption**: 10-K PDFs contain financial data in a consistent format
- **Trade-off**: Using regex patterns for extraction vs. more sophisticated NLP
- **Rationale**: Simpler implementation for case study scope

### Data Normalization
- **Assumption**: Financial values may contain $ symbols, spaces, and parentheses for negative values
- **Implementation**: Remove $ and spaces, convert (X) to -X format

### Frontend Design
- **Assumption**: Simple grid display is sufficient for case study
- **Trade-off**: Basic styling vs. comprehensive UI framework
- **Rationale**: Focus on functionality over aesthetics

## Technical Decisions

### Backend Framework
- **Choice**: Django
- **Rationale**: Robust framework with built-in admin, ORM, and security features

### Frontend Framework
- **Choice**: React with TypeScript
- **Rationale**: Modern, type-safe development with good tooling

### PDF Processing
- **Choice**: pdfplumber (primary) with PyPDF2 as backup
- **Rationale**: pdfplumber provides better text extraction accuracy and handles complex PDF layouts better than PyPDF2

### API Design
- **Choice**: Django REST Framework with function-based views
- **Rationale**: Simple, straightforward approach for single endpoint; easier to debug and maintain

### Financial Data Extraction
- **Choice**: Regex pattern matching over NLP/ML approaches
- **Rationale**: Faster, more predictable, and sufficient for structured financial documents like 10-K forms

### Value Normalization Strategy
- **Choice**: Remove $ symbols, spaces, convert (X) to -X, remove commas
- **Rationale**: Standardizes financial values for consistent processing and storage

### Testing Strategy
- **Choice**: Manual testing with real 10-K PDF over automated unit tests
- **Rationale**: PDF parsing is complex and benefits from real-world validation; manual testing ensures accuracy with actual financial documents

### API Response Format
- **Choice**: Simple JSON structure with nested results object
- **Rationale**: Easy to parse by frontend, clear separation of metadata (period_end_date) and data (results)

## Future Considerations

- Automated test suite for different PDF formats
- Support for additional financial fields (EBITDA, Net Income, etc.)
- Improved error handling for malformed PDFs
- Frontend integration and UI/UX design
