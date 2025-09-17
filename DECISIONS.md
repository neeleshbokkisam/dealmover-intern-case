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
- **Choice**: PyPDF2 or pdfplumber
- **Rationale**: Lightweight libraries suitable for text extraction

## Future Considerations

- Error handling for malformed PDFs
- Support for additional financial fields
- Improved UI/UX design
- Comprehensive test coverage
