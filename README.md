# Health and Safety Dashboard

A modern, web-based Health & Safety Dashboard built with Streamlit and Plotly. This application allows users to upload Excel files (.xlsm), process safety data, and visualize key performance indicators (KPIs) with interactive charts and a comprehensive performance matrix.

## Features

- 📊 **Interactive Dashboard**: Real-time visualization of safety metrics
- 📈 **Performance Matrix**: Monthly tracking with year-over-year comparisons
- 📉 **Interactive Charts**: Timeline charts and event classification visualizations
- 🔍 **Dynamic Filtering**: Filter by contract type, contractor, and reporting year
- 📄 **PDF Export**: Generate comprehensive PDF reports
- 🎨 **Modern UI**: QLDC-inspired design with professional styling

## Key Performance Indicators

- **Accidents**: Total accident count
- **Incidents**: Total incident count
- **Hazards Identified**: Proactive hazard identification
- **Total Hours**: Total hours worked
- **Near Misses**: Near miss incidents

## Safety Performance Matrix

The dashboard includes a comprehensive matrix showing:
- Monthly data (January - December)
- Accumulated Fiscal Year (ACCU FY) totals
- Previous Year (ACCU LY) comparisons
- Variance percentages (VAR %)
- Trend indicators (↑ ↓ →)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/health-and-safety-dashboard.git
cd health-and-safety-dashboard
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the Streamlit application:
```bash
streamlit run app.py
```

2. Upload your Excel file (.xlsm) using the sidebar

3. Select the appropriate sheet and apply filters

4. View KPIs, performance matrix, and interactive charts

5. Export data as CSV or generate a PDF report

## Project Structure

```
health-and-safety-dashboard/
├── app.py                 # Main Streamlit application
├── data_processor.py     # Data processing and cleaning functions
├── visuals.py            # Plotly chart generation functions
├── pdf_export.py         # PDF report generation module
├── requirements.txt       # Python dependencies
└── README.md             # Project documentation
```

## Dependencies

- streamlit>=1.28.0
- pandas>=2.1.0
- plotly>=5.17.0
- openpyxl>=3.1.2
- numpy>=1.24.0
- reportlab>=4.0.0
- kaleido>=0.2.1
- Pillow>=10.0.0

## Technical Details

- **Framework**: Streamlit
- **Visualization**: Plotly
- **Data Processing**: Pandas
- **PDF Generation**: ReportLab
- **Python Version**: 3.10+

## Features in Detail

### Data Processing
- Automatic column detection (dates, contractors, metrics)
- Data normalization and cleaning
- KPI calculations (TRIFR, LTIFR, etc.)
- Dynamic filtering capabilities

### Visualizations
- Month-by-month timeline charts
- Stacked bar charts with trendlines
- Event classification donut charts
- Entity performance comparisons

### Export Options
- CSV export for performance matrix
- PDF export with full dashboard report

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Author

Senior Full-Stack Python Developer & Data Scientist
