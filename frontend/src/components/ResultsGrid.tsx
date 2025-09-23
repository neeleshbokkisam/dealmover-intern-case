import React from 'react';

interface FinancialData {
  revenue: string;
  cos: string;
  operating_income: string;
}

interface ResultsGridProps {
  data: FinancialData | null;
  periodEndDate: string;
}

const ResultsGrid: React.FC<ResultsGridProps> = ({ data, periodEndDate }) => {
  if (!data) {
    return (
      <div className="results-grid">
        <p>No data available. Upload a PDF to extract financial information.</p>
      </div>
    );
  }

  // Calculate financial metrics
  const revenue = parseFloat(data.revenue) || 0;
  const costOfSales = parseFloat(data.cos) || 0;
  const operatingIncome = parseFloat(data.operating_income) || 0;
  const grossProfit = revenue - costOfSales;

  // Format the period end date for display
  const formatPeriodEndDate = (dateString: string) => {
    if (!dateString) return 'Period Not Specified';
    try {
      const date = new Date(dateString);
      return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      });
    } catch {
      return dateString;
    }
  };

  return (
    <div className="results-grid">
      <div className="statement-header">
        <h3>Financial Statement Results</h3>
        <div className="statement-period">
          <span className="period-label">Statement Period:</span>
          <span className="period-date">{formatPeriodEndDate(periodEndDate)}</span>
        </div>
      </div>
      <table className="financial-table">
        <thead>
          <tr>
            <th>Financial Metric</th>
            <th>Value ($)</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Revenue</td>
            <td>{revenue.toLocaleString()}</td>
          </tr>
          <tr>
            <td>Gross Profit</td>
            <td>{grossProfit.toLocaleString()}</td>
          </tr>
          <tr>
            <td>Operating Income</td>
            <td>{operatingIncome.toLocaleString()}</td>
          </tr>
        </tbody>
      </table>
    </div>
  );
};

export default ResultsGrid;
