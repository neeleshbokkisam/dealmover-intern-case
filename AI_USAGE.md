# AI Usage Disclosure

This document tracks AI tool usage throughout the project. AI was used strategically for targeted help while a human developer retained ownership of architecture and final code quality.

## Tools Used
- **Claude (Anthropic)**: Targeted assistance on specific development tasks (backend parsing, testing patterns)
- **GPT-based coding assistant (Cursor/GPT-5)**: Pair-programming during UI polish (CSS improvements, minor JSX tweaks) and documentation updates

## Usage Log

### Project Setup Phase
- **Task**: Initial project structure and documentation
- **AI Role**: Suggested basic directory layout and documentation templates
- **Human Role**: Designed overall architecture, wrote all implementation code
- **Status**: ✅ Complete

### Backend Development
- **Task**: Django setup and PDF parsing implementation
- **AI Role**: Suggested Django project structure, provided regex patterns for financial data extraction, helped with error handling patterns
- **Human Role**: Designed overall API architecture, wrote core business logic, implemented PDF parsing strategy, made final decisions on pattern matching approach
- **Status**: ✅ Complete

### Frontend Development
- **Task**: React components and initial UI implementation
- **AI Role**: Suggested component structure, provided TypeScript interfaces, helped with API integration patterns and baseline styling approach
- **Human Role**: Designed overall UI/UX workflow, implemented component logic, made decisions on state management and error handling
- **Status**: ✅ Complete

### UI Polish
- **Task**: Modernize styling, improve visual hierarchy, add responsive design and micro-animations
- **AI Role** (Cursor/GPT-5): Proposed CSS upgrades (gradient background, glassmorphism card, enhanced table styles, focus/hover states, loading spinner), suggested minor JSX label/icon improvements in `PDFUpload.tsx` and `ResultsGrid.tsx`
- **Human Role**: Reviewed suggestions, accepted edits, validated no functional regressions, ensured no new dependencies were introduced
- **Files Updated**:
  - `frontend/src/App.css` (comprehensive styling refresh, responsive rules)
  - `frontend/src/components/PDFUpload.tsx` (labels/icons, loading UI)
  - `frontend/src/components/ResultsGrid.tsx` (header icons, formatted values)
- **Status**: ✅ Complete

### Testing & Documentation
- **Task**: Test implementation and final documentation
- **AI Role**: Suggested test script structure, validation approach, and pytest testing patterns
- **Human Role**: Designed comprehensive test strategy, implemented test script, validated API functionality with real PDF data, created pytest test suite with 27 comprehensive tests, built comprehensive stretch goals validation suite
- **Status**: ✅ Complete

### Stretch Goals Implementation
- **Task**: Operating Income extraction, pytest tests, header row enhancement, comprehensive testing
- **AI Role**: Suggested implementation patterns, provided testing frameworks, helped with UI enhancements
- **Human Role**: Designed Operating Income extraction logic, created comprehensive pytest test suite, implemented prominent header row with statement period, built end-to-end validation system
- **Status**: ✅ Complete

## Usage Guidelines
- AI used for specific technical questions and code suggestions
- All AI outputs reviewed and adapted before implementation
- Human maintains full ownership of architectural decisions and final code quality
- Focus on strategic assistance rather than wholesale code generation
