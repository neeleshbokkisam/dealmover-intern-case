import React from 'react';

interface FinancialData {
  revenue: string;
  cos: string;
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

  // Calculate Gross Profit (Revenue - Cost of Sales)
  const revenue = parseFloat(data.revenue) || 0;
  const costOfSales = parseFloat(data.cos) || 0;
  const grossProfit = revenue - costOfSales;

  return (
    <div className="results-grid">
      <h3>Financial Results - {periodEndDate}</h3>
      <table className="financial-table">
        <thead>
          <tr>
            <th>Metric</th>
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
        </tbody>
      </table>
    </div>
  );
};

export default ResultsGrid;
