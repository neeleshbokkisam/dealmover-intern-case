import pytest
from unittest.mock import patch, mock_open
from core.views import (
    extract_text_from_pdf,
    extract_financial_values,
    extract_value_with_patterns,
    clean_financial_value
)


class TestPDFTextExtraction:
    """Test PDF text extraction functionality"""
    
    @patch('core.views.pdfplumber.open')
    def test_extract_text_from_pdf_success(self, mock_pdfplumber_open):
        """Test successful PDF text extraction"""
        # Mock PDF pages
        mock_page1 = type('MockPage', (), {'extract_text': lambda self: 'Page 1 content'})()
        mock_page2 = type('MockPage', (), {'extract_text': lambda self: 'Page 2 content'})()
        mock_pdf = type('MockPDF', (), {'pages': [mock_page1, mock_page2]})()
        mock_pdfplumber_open.return_value.__enter__.return_value = mock_pdf
        
        result = extract_text_from_pdf('test.pdf')
        
        assert result == 'Page 1 content\nPage 2 content\n'
        mock_pdfplumber_open.assert_called_once_with('test.pdf')
    
    @patch('core.views.pdfplumber.open')
    def test_extract_text_from_pdf_error(self, mock_pdfplumber_open):
        """Test PDF text extraction with error"""
        mock_pdfplumber_open.side_effect = Exception('PDF error')
        
        with pytest.raises(Exception, match='PDF error'):
            extract_text_from_pdf('invalid.pdf')


class TestFinancialValueCleaning:
    """Test financial value cleaning functionality"""
    
    def test_clean_financial_value_positive(self):
        """Test cleaning positive financial values"""
        assert clean_financial_value('$1,234,567') == '1234567'
        assert clean_financial_value('1,234,567') == '1234567'
        assert clean_financial_value('1234567') == '1234567'
        assert clean_financial_value('$ 1,234,567') == '1234567'
    
    def test_clean_financial_value_negative(self):
        """Test cleaning negative financial values"""
        assert clean_financial_value('$(1,234,567)') == '-1234567'
        assert clean_financial_value('(1,234,567)') == '-1234567'
        assert clean_financial_value('-$1,234,567') == '-1234567'
    
    def test_clean_financial_value_edge_cases(self):
        """Test cleaning edge cases"""
        assert clean_financial_value('') == ''
        assert clean_financial_value('N/A') == ''
        assert clean_financial_value('$0') == '0'
        assert clean_financial_value('$(0)') == '-0'


class TestValueExtractionWithPatterns:
    """Test value extraction using regex patterns"""
    
    def test_extract_value_with_patterns_success(self):
        """Test successful value extraction"""
        text = "Total revenues $1,234,567 and other income"
        patterns = [r'total\s+revenues?\s+\$\s*([0-9,]+)']
        
        result = extract_value_with_patterns(text, patterns, "revenue")
        
        assert result == '1234567'
    
    def test_extract_value_with_patterns_multiple_patterns(self):
        """Test value extraction with multiple patterns"""
        text = "Revenue: $1,234,567"
        patterns = [
            r'total\s+revenues?\s+\$\s*([0-9,]+)',
            r'revenue[:\s]*\$?([0-9,]+)'
        ]
        
        result = extract_value_with_patterns(text, patterns, "revenue")
        
        assert result == '1234567'
    
    def test_extract_value_with_patterns_no_match(self):
        """Test value extraction when no patterns match"""
        text = "No financial data here"
        patterns = [r'revenue[:\s]*\$?([0-9,]+)']
        
        result = extract_value_with_patterns(text, patterns, "revenue")
        
        assert result == ""
    
    def test_extract_value_with_patterns_negative_value(self):
        """Test extraction of negative values"""
        text = "Operating loss $(123,456)"
        patterns = [r'operating\s+loss[:\s]*\$?\(([0-9,]+)\)']
        
        result = extract_value_with_patterns(text, patterns, "operating loss")
        
        assert result == '123456'  # The function extracts the number, cleaning handles the negative


class TestFinancialValuesExtraction:
    """Test complete financial values extraction"""
    
    def test_extract_financial_values_complete(self):
        """Test extraction of all financial values"""
        text = """
        CONSOLIDATED STATEMENTS OF OPERATIONS
        Total revenues $1,234,567
        Cost of revenues $800,000
        Income from operations $434,567
        """
        
        result = extract_financial_values(text)
        
        assert result['revenue'] == '1234567'
        assert result['cos'] == '800000'
        assert result['operating_income'] == '434567'
    
    def test_extract_financial_values_partial(self):
        """Test extraction when only some values are found"""
        text = """
        CONSOLIDATED STATEMENTS OF OPERATIONS
        Total revenues $1,234,567
        Cost of revenues $800,000
        """
        
        result = extract_financial_values(text)
        
        assert result['revenue'] == '1234567'
        assert result['cos'] == '800000'
        assert result['operating_income'] == ""
    
    def test_extract_financial_values_alternative_patterns(self):
        """Test extraction using alternative pattern variations"""
        text = """
        INCOME STATEMENT
        Net sales $2,000,000
        Cost of goods sold $1,200,000
        Operating income $800,000
        """
        
        result = extract_financial_values(text)
        
        assert result['revenue'] == '2000000'
        assert result['cos'] == '1200000'
        assert result['operating_income'] == '800000'
    
    def test_extract_financial_values_negative_values(self):
        """Test extraction of negative financial values"""
        text = """
        CONSOLIDATED STATEMENTS OF OPERATIONS
        Total revenues $1,000,000
        Cost of revenues $1,200,000
        Income from operations $(200,000)
        """
        
        result = extract_financial_values(text)
        
        assert result['revenue'] == '1000000'
        assert result['cos'] == '1200000'
        assert result['operating_income'] == ""
    
    def test_extract_financial_values_no_data(self):
        """Test extraction when no financial data is present"""
        text = "This is just regular text with no financial information."
        
        result = extract_financial_values(text)
        
        assert result['revenue'] == ""
        assert result['cos'] == ""
        assert result['operating_income'] == ""


class TestRealWorldPatterns:
    """Test patterns based on real 10-K document structures"""
    
    def test_google_10k_revenue_pattern(self):
        """Test revenue extraction with Google 10-K style formatting"""
        text = """
        CONSOLIDATED STATEMENTS OF OPERATIONS
        (In millions, except per share amounts)
        
        Revenues:
        Google Services revenues $282,836
        Google Cloud revenues $33,062
        Other Bets revenues $226
        Total revenues $316,124
        """
        
        result = extract_financial_values(text)
        
        assert result['revenue'] == '316124'
    
    def test_google_10k_cos_pattern(self):
        """Test cost of sales extraction with Google 10-K style formatting"""
        text = """
        Costs and expenses:
        Cost of revenues $126,203
        Research and development $39,500
        Sales and marketing $22,912
        General and administrative $7,731
        """
        
        result = extract_financial_values(text)
        
        assert result['cos'] == '126203'
    
    def test_google_10k_operating_income_pattern(self):
        """Test operating income extraction with Google 10-K style formatting"""
        text = """
        Income from operations $119,716
        Other income (expense), net $1,376
        Income before income taxes $121,092
        """
        
        result = extract_financial_values(text)
        
        assert result['operating_income'] == '119716'
