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
- **Trade-off**: Custom CSS vs. adopting a component framework (e.g., MUI, Chakra)
- **Rationale**: Favor lightweight, dependency-free styling while still achieving a professional look

## Technical Decisions

### Backend Framework
- **Choice**: Django
- **Rationale**: Robust framework with built-in admin, ORM, and security features

### Frontend Framework
- **Choice**: React with TypeScript and Vite
- **Rationale**: Modern, type-safe development with fast build tooling and excellent developer experience

### Component Architecture
- **Choice**: Functional components with hooks over class components
- **Rationale**: Simpler, more modern approach with better TypeScript integration

### State Management
- **Choice**: Local React state over external state management (Redux/Zustand)
- **Rationale**: Simple application with minimal state; local state is sufficient and easier to maintain

### API Integration
- **Choice**: Native fetch API over axios
- **Rationale**: No additional dependencies, built-in browser support, sufficient for this use case

### UI/UX Design
- **Choice**: Custom CSS with modern patterns (gradient background, glassmorphism card, micro-animations) over component libraries
- **Rationale**: Full control over styling, smaller bundle size, and faster iteration without additional dependencies; UI polish achieved through handcrafted CSS

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
- **Choice**: Hybrid approach - manual testing with real 10-K PDF + automated pytest tests
- **Rationale**: PDF parsing is complex and benefits from real-world validation; automated tests ensure regression protection and code reliability

### Test Framework Selection
- **Choice**: pytest with pytest-django over Django's built-in test framework
- **Rationale**: More powerful assertion syntax, better fixture support, cleaner test organization, and superior debugging capabilities

### Test Organization
- **Choice**: Separate unit and integration test directories with comprehensive coverage
- **Rationale**: Clear separation of concerns; unit tests focus on individual functions, integration tests validate API behavior and error handling

### Stretch Goals Implementation
- **Choice**: Operating Income extraction as additional financial field
- **Rationale**: Common financial metric that provides more comprehensive financial analysis; follows same pattern as existing fields

### Comprehensive Testing Strategy
- **Choice**: End-to-end validation suite for all stretch goals
- **Rationale**: Ensures all implemented features work correctly together; validates API functionality, test suite execution, and UI enhancements

### UI Enhancement Approach
- **Choice**: Prominent header row with gradient styling and formatted statement period
- **Rationale**: Improves user experience by clearly displaying financial statement context; professional appearance matches financial industry standards

### UI Polish Decisions (This session)
- **Background & Layout**: Purple-blue gradient with subtle radial overlays; glassmorphism on main container.
- **Interactive States**: Hover/focus states, shimmer effects, and loading spinner to improve perceived performance.
- **Typography & Hierarchy**: Increased header weights; added non-functional icons to improve scannability.
- **Tables**: Larger spacing, soft borders, row hover highlights, and decorative gradient underline on table headers.
- **Responsiveness**: Media queries for ≤768px and ≤480px adjusting paddings, font sizes, and layout spacing.
- **Accessibility**: Stronger focus outlines on inputs; high-contrast text on colored backgrounds.

### API Response Format
- **Choice**: Simple JSON structure with nested results object
- **Rationale**: Easy to parse by frontend, clear separation of metadata (period_end_date) and data (results)

## Future Considerations

- Automated test suite for different PDF formats
- Support for additional financial fields (EBITDA, Net Income, etc.)
- Improved error handling for malformed PDFs
- Frontend unit testing with React Testing Library
- Further responsive refinements (compact table layout at very narrow widths)
- File drag-and-drop functionality for PDF selection
- Optional light/dark theme toggle using CSS variables
