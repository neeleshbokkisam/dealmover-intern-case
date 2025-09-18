import React, { useState } from 'react';

interface PDFUploadProps {
  onFileSelect: (file: File) => void;
  onDateChange: (date: string) => void;
  onExtract: () => void;
  isLoading: boolean;
  selectedFile: File | null;
  periodEndDate: string;
}

const PDFUpload: React.FC<PDFUploadProps> = ({
  onFileSelect,
  onDateChange,
  onExtract,
  isLoading,
  selectedFile,
  periodEndDate
}) => {
  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file && file.type === 'application/pdf') {
      onFileSelect(file);
    } else {
      alert('Please select a valid PDF file.');
    }
  };

  const handleDateChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    onDateChange(event.target.value);
  };

  return (
    <div className="pdf-upload">
      <h2>DealMover PDF Financial Data Extractor</h2>
      
      <div className="upload-section">
        <label htmlFor="pdf-file" className="file-label">
          Choose PDF File
        </label>
        <input
          id="pdf-file"
          type="file"
          accept=".pdf"
          onChange={handleFileChange}
          className="file-input"
        />
        {selectedFile && (
          <p className="file-info">Selected: {selectedFile.name}</p>
        )}
      </div>

      <div className="date-section">
        <label htmlFor="period-date" className="date-label">
          Period End Date (Optional)
        </label>
        <input
          id="period-date"
          type="date"
          value={periodEndDate}
          onChange={handleDateChange}
          className="date-input"
        />
      </div>

      <button
        onClick={onExtract}
        disabled={!selectedFile || isLoading}
        className="extract-button"
      >
        {isLoading ? 'Extracting...' : 'Extract Financial Data'}
      </button>
    </div>
  );
};

export default PDFUpload;
