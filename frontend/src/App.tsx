import React, { useState } from 'react';
import PDFUpload from './components/PDFUpload';
import ResultsGrid from './components/ResultsGrid';
import './App.css';

interface FinancialData {
  revenue: string;
  cos: string;
  operating_income: string;
}

function App() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [periodEndDate, setPeriodEndDate] = useState<string>('');
  const [financialData, setFinancialData] = useState<FinancialData | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string>('');

  const handleFileSelect = (file: File) => {
    setSelectedFile(file);
    setError('');
  };

  const handleDateChange = (date: string) => {
    setPeriodEndDate(date);
  };

  const handleExtract = async () => {
    if (!selectedFile) return;

    setIsLoading(true);
    setError('');

    try {
      const formData = new FormData();
      formData.append('pdf_file', selectedFile);
      if (periodEndDate) {
        formData.append('period_end_date', periodEndDate);
      }

      const response = await fetch('http://localhost:8001/api/extract/', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setFinancialData(data.results);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app">
      <PDFUpload
        onFileSelect={handleFileSelect}
        onDateChange={handleDateChange}
        onExtract={handleExtract}
        isLoading={isLoading}
        selectedFile={selectedFile}
        periodEndDate={periodEndDate}
      />
      
      {error && (
        <div className="error-message">
          Error: {error}
        </div>
      )}

      <ResultsGrid
        data={financialData}
        periodEndDate={periodEndDate || '2024-12-31'}
      />
    </div>
  );
}

export default App
