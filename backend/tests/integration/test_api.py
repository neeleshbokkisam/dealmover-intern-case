import pytest
from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest.mock import patch, mock_open
import json


class TestPDFExtractionAPI(TestCase):
    """Integration tests for PDF extraction API endpoint"""
    
    def setUp(self):
        """Set up test client"""
        self.client = Client()
        self.api_url = '/api/extract/'
    
    def test_api_endpoint_exists(self):
        """Test that the API endpoint is accessible"""
        response = self.client.get(self.api_url)
        # Should return 405 Method Not Allowed for GET request
        assert response.status_code == 405
    
    def test_api_post_without_file(self):
        """Test API POST request without file"""
        response = self.client.post(self.api_url)
        
        assert response.status_code == 400
        data = response.json()
        assert 'error' in data
        assert 'No PDF file provided' in data['error']
    
    def test_api_post_with_invalid_file_type(self):
        """Test API POST request with invalid file type"""
        # Create a text file instead of PDF
        text_file = SimpleUploadedFile(
            "test.txt",
            b"Some text content",
            content_type="text/plain"
        )
        
        response = self.client.post(self.api_url, {'pdf_file': text_file})
        
        assert response.status_code == 400
        data = response.json()
        assert 'error' in data
        assert 'File must be a PDF' in data['error']
    
    @patch('core.views.extract_text_from_pdf')
    @patch('core.views.extract_financial_values')
    def test_api_post_successful_extraction(self, mock_extract_values, mock_extract_text):
        """Test successful PDF extraction via API"""
        # Mock the PDF text extraction
        mock_extract_text.return_value = """
        CONSOLIDATED STATEMENTS OF OPERATIONS
        Total revenues $1,234,567
        Cost of revenues $800,000
        Income from operations $434,567
        """
        
        # Mock the financial values extraction
        mock_extract_values.return_value = {
            'revenue': '1234567',
            'cos': '800000',
            'operating_income': '434567'
        }
        
        # Create a mock PDF file
        pdf_content = b"Mock PDF content"
        pdf_file = SimpleUploadedFile(
            "test.pdf",
            pdf_content,
            content_type="application/pdf"
        )
        
        response = self.client.post(self.api_url, {
            'pdf_file': pdf_file,
            'period_end_date': '2024-12-31'
        })
        
        assert response.status_code == 200
        data = response.json()
        
        assert 'period_end_date' in data
        assert 'results' in data
        assert data['period_end_date'] == '2024-12-31'
        
        results = data['results']
        assert results['revenue'] == '1234567'
        assert results['cos'] == '800000'
        assert results['operating_income'] == '434567'
    
    @patch('core.views.extract_text_from_pdf')
    def test_api_post_pdf_extraction_error(self, mock_extract_text):
        """Test API response when PDF extraction fails"""
        # Mock PDF extraction failure
        mock_extract_text.return_value = None
        
        pdf_file = SimpleUploadedFile(
            "test.pdf",
            b"Mock PDF content",
            content_type="application/pdf"
        )
        
        response = self.client.post(self.api_url, {'pdf_file': pdf_file})
        
        assert response.status_code == 500  # Internal server error due to NoneType error
        data = response.json()
        assert 'error' in data
    
    @patch('core.views.extract_text_from_pdf')
    @patch('core.views.extract_financial_values')
    def test_api_post_without_period_date(self, mock_extract_values, mock_extract_text):
        """Test API POST without period end date"""
        # Mock successful extraction
        mock_extract_text.return_value = "Some text"
        mock_extract_values.return_value = {
            'revenue': '1000000',
            'cos': '600000',
            'operating_income': '400000'
        }
        
        pdf_file = SimpleUploadedFile(
            "test.pdf",
            b"Mock PDF content",
            content_type="application/pdf"
        )
        
        response = self.client.post(self.api_url, {'pdf_file': pdf_file})
        
        assert response.status_code == 200
        data = response.json()
        
        # Should use current date when no period_end_date provided
        assert 'period_end_date' in data
        assert data['period_end_date'] is not None  # Should be current date
    
    @patch('core.views.extract_text_from_pdf')
    @patch('core.views.extract_financial_values')
    def test_api_post_partial_extraction(self, mock_extract_values, mock_extract_text):
        """Test API response with partial financial data extraction"""
        # Mock partial extraction
        mock_extract_text.return_value = "Some text"
        mock_extract_values.return_value = {
            'revenue': '1000000',
            'cos': "",  # Not found
            'operating_income': '400000'
        }
        
        pdf_file = SimpleUploadedFile(
            "test.pdf",
            b"Mock PDF content",
            content_type="application/pdf"
        )
        
        response = self.client.post(self.api_url, {'pdf_file': pdf_file})
        
        assert response.status_code == 200
        data = response.json()
        
        results = data['results']
        assert results['revenue'] == '1000000'
        assert results['cos'] == ""
        assert results['operating_income'] == '400000'
    
    def test_api_large_file_handling(self):
        """Test API handling of large files"""
        # Create a large mock PDF file (simulate large file)
        large_content = b"Mock PDF content" * 10000  # ~150KB
        pdf_file = SimpleUploadedFile(
            "large_test.pdf",
            large_content,
            content_type="application/pdf"
        )
        
        with patch('core.views.extract_text_from_pdf') as mock_extract_text:
            mock_extract_text.return_value = "Large PDF text content"
            
            with patch('core.views.extract_financial_values') as mock_extract_values:
                mock_extract_values.return_value = {
                    'revenue': '5000000',
                    'cos': '3000000',
                    'operating_income': '2000000'
                }
                
                response = self.client.post(self.api_url, {'pdf_file': pdf_file})
                
                assert response.status_code == 200
                data = response.json()
                assert 'results' in data


class TestAPIErrorHandling(TestCase):
    """Test API error handling scenarios"""
    
    def setUp(self):
        """Set up test client"""
        self.client = Client()
        self.api_url = '/api/extract/'
    
    def test_api_malformed_request(self):
        """Test API with malformed request data"""
        response = self.client.post(
            self.api_url,
            data="invalid json",
            content_type="application/json"
        )
        
        # Should handle gracefully
        assert response.status_code == 500  # Internal server error due to JSON parsing error
    
    def test_api_empty_file(self):
        """Test API with empty file"""
        empty_file = SimpleUploadedFile(
            "empty.pdf",
            b"",
            content_type="application/pdf"
        )
        
        response = self.client.post(self.api_url, {'pdf_file': empty_file})
        
        assert response.status_code == 500  # Internal server error due to PDF parsing error
        data = response.json()
        assert 'error' in data
