#!/usr/bin/env python
"""
Test runner script for the PDF extraction project.
Run this script to execute all tests with proper Django setup.
"""

import os
import sys
import django
from django.conf import settings
from django.test.utils import get_runner

if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dealmover_case.settings')
    django.setup()
    
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    
    # Run tests with verbose output
    failures = test_runner.run_tests([
        "tests.unit.test_pdf_parser",
        "tests.integration.test_api"
    ], verbosity=2)
    
    if failures:
        sys.exit(1)
    else:
        print("\n✅ All tests passed!")
        sys.exit(0)
