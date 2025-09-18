from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
import pdfplumber
import re
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

@api_view(['POST'])
def extract_financial_data(request):
    """
    Extract Revenue and Cost of Sales from uploaded PDF
    """
    try:
        # Check if PDF file is provided
        if 'pdf_file' not in request.FILES:
            return Response(
                {'error': 'No PDF file provided'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        pdf_file = request.FILES['pdf_file']
        period_end_date = request.data.get('period_end_date', '')
        
        # Validate file type
        if not pdf_file.name.lower().endswith('.pdf'):
            return Response(
                {'error': 'File must be a PDF'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Extract text from PDF
        text = extract_text_from_pdf(pdf_file)
        
        # Extract financial data
        financial_data = extract_financial_values(text)
        
        # Validate period_end_date format if provided
        if period_end_date:
            try:
                datetime.strptime(period_end_date, '%Y-%m-%d')
            except ValueError:
                return Response(
                    {'error': 'period_end_date must be in YYYY-MM-DD format'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        response_data = {
            'period_end_date': period_end_date or '2024-12-31',  # Default if not provided
            'results': financial_data
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Error processing PDF: {str(e)}")
        return Response(
            {'error': f'Error processing PDF: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

def extract_text_from_pdf(pdf_file):
    """Extract text from PDF file"""
    text = ""
    try:
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        logger.error(f"Error extracting text from PDF: {str(e)}")
        raise e
    
    return text

def extract_financial_values(text):
    """
    Extract Revenue and Cost of Sales from text using regex patterns
    """
    # Normalize text for better pattern matching
    text = text.replace('\n', ' ').replace('\r', ' ')
    
    # Define patterns for Revenue and Cost of Sales
    revenue_patterns = [
        # Look for "Total revenues $ XXX,XXX" pattern
        r'total\s+revenues?\s+\$\s*([0-9,]+(?:\([0-9,]+\))?)',
        # Look for "Revenues $ XXX,XXX" pattern
        r'revenues?\s+\$\s*([0-9,]+(?:\([0-9,]+\))?)',
        # Look for "Consolidated revenues $ XXX,XXX" pattern
        r'consolidated\s+revenues?\s+\$\s*([0-9,]+(?:\([0-9,]+\))?)',
        # General revenue patterns
        r'revenue[:\s]*\$?([0-9,]+(?:\([0-9,]+\))?)',
        r'total\s+revenue[:\s]*\$?([0-9,]+(?:\([0-9,]+\))?)',
        r'net\s+revenue[:\s]*\$?([0-9,]+(?:\([0-9,]+\))?)',
        r'net\s+sales[:\s]*\$?([0-9,]+(?:\([0-9,]+\))?)',
    ]
    
    cos_patterns = [
        # Look for "Cost of revenues XXX,XXX" pattern (main cost line, no $ symbol)
        r'^cost\s+of\s+revenues?\s+([0-9,]+(?:\([0-9,]+\))?)',
        # Look for "Cost of revenues XXX,XXX" pattern in table context
        r'costs?\s+and\s+expenses:\s*cost\s+of\s+revenues?\s+([0-9,]+(?:\([0-9,]+\))?)',
        # Look for "Cost of revenues $ XXX,XXX" pattern
        r'cost\s+of\s+revenues?\s+\$\s*([0-9,]+(?:\([0-9,]+\))?)',
        # General cost patterns
        r'cost\s+of\s+sales[:\s]*\$?([0-9,]+(?:\([0-9,]+\))?)',
        r'cost\s+of\s+revenue[:\s]*\$?([0-9,]+(?:\([0-9,]+\))?)',
        r'cost\s+of\s+goods\s+sold[:\s]*\$?([0-9,]+(?:\([0-9,]+\))?)',
        r'cost\s+of\s+services[:\s]*\$?([0-9,]+(?:\([0-9,]+\))?)',
    ]
    
    # Extract Revenue
    revenue = extract_value_with_patterns(text, revenue_patterns, "revenue")
    
    # Extract Cost of Sales
    cos = extract_value_with_patterns(text, cos_patterns, "cost of sales")
    
    return {
        'revenue': revenue,
        'cos': cos
    }

def extract_value_with_patterns(text, patterns, field_name):
    """
    Try multiple patterns to extract a financial value
    """
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            # Handle both single group and multiple group patterns
            if isinstance(matches[0], tuple):
                # Multiple groups - take the last one (usually the number)
                value = matches[0][-1]
            else:
                # Single group - take the first match
                value = matches[0]
            
            cleaned_value = clean_financial_value(value)
            if cleaned_value:
                logger.info(f"Found {field_name}: {cleaned_value}")
                return cleaned_value
    
    logger.warning(f"Could not find {field_name} in PDF")
    return ""

def clean_financial_value(value):
    """
    Clean and normalize financial values
    - Remove $ symbols and spaces
    - Convert (X) to -X format for negative values
    - Remove commas
    """
    if not value:
        return ""
    
    # Remove $ and spaces
    cleaned = value.replace('$', '').replace(' ', '')
    
    # Handle negative values in parentheses format
    if cleaned.startswith('(') and cleaned.endswith(')'):
        cleaned = '-' + cleaned[1:-1]
    
    # Remove commas
    cleaned = cleaned.replace(',', '')
    
    # Validate it's a number
    try:
        float(cleaned)
        return cleaned
    except ValueError:
        return ""