"""
Health & Safety Dashboard - Main Application

A high-fidelity Health & Safety Dashboard matching QLDC design specifications.
Parses .xlsm files and displays interactive KPIs, performance matrix, and charts.

Author: Senior Frontend Engineer & Python Developer
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import data_processor as dp
import visuals as vis
import pdf_export as pdf_gen

# Page configuration
st.set_page_config(
    page_title="Health & Safety Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for QLDC/QLDC-inspired design
st.markdown("""
    <style>
    /* Main background */
    .stApp {
        background-color: #F5F5F5;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Header styling */
    .dashboard-header {
        background-color: #FFFFFF;
        padding: 1.5rem 2rem;
        margin: -1rem -1rem 2rem -1rem;
        border-bottom: 2px solid #E0E0E0;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .header-left {
        display: flex;
        align-items: center;
        gap: 1.5rem;
    }
    
    .logo-box {
        width: 60px;
        height: 60px;
        background-color: #001f3f;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 4px;
    }
    
    .logo-text {
        color: #FFFFFF;
        font-weight: bold;
        font-size: 1.2rem;
    }
    
    .header-title {
        display: flex;
        flex-direction: column;
    }
    
    .header-title h1 {
        color: #001f3f;
        font-size: 1.8rem;
        font-weight: 700;
        margin: 0;
        line-height: 1.2;
    }
    
    .header-title p {
        color: #666;
        font-size: 0.9rem;
        margin: 0.2rem 0 0 0;
    }
    
    .header-filters {
        display: flex;
        gap: 1rem;
        align-items: center;
    }
    
    .filter-group {
        display: flex;
        flex-direction: column;
        gap: 0.3rem;
    }
    
    .filter-label {
        font-size: 0.75rem;
        color: #666;
        text-transform: uppercase;
        font-weight: 600;
        letter-spacing: 0.5px;
    }
    
    /* KPI Card Styling */
    .kpi-card {
        background-color: #FFFFFF;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        margin-bottom: 1rem;
        position: relative;
        border-top: 4px solid;
        height: 140px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    
    .kpi-card.attention {
        border-top-color: #EA4335;
    }
    
    .kpi-card.review {
        border-top-color: #FBBC04;
    }
    
    .kpi-card.proactive {
        border-top-color: #00BCD4;
    }
    
    .kpi-card.utilization {
        border-top-color: #5F6368;
    }
    
    .kpi-status-badge {
        position: absolute;
        top: 1rem;
        right: 1rem;
        background-color: rgba(0,0,0,0.05);
        padding: 0.3rem 0.8rem;
        border-radius: 12px;
        font-size: 0.7rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .kpi-card.attention .kpi-status-badge {
        background-color: rgba(234, 67, 53, 0.1);
        color: #EA4335;
    }
    
    .kpi-card.review .kpi-status-badge {
        background-color: rgba(251, 188, 4, 0.1);
        color: #FBBC04;
    }
    
    .kpi-card.proactive .kpi-status-badge {
        background-color: rgba(0, 188, 212, 0.1);
        color: #00BCD4;
    }
    
    .kpi-card.utilization .kpi-status-badge {
        background-color: rgba(95, 99, 104, 0.1);
        color: #5F6368;
    }
    
    .kpi-content {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-top: 0.5rem;
    }
    
    .kpi-icon {
        font-size: 2.5rem;
        opacity: 0.7;
    }
    
    .kpi-value {
        font-size: 2.8rem;
        font-weight: 700;
        color: #001f3f;
        line-height: 1;
    }
    
    .kpi-label {
        font-size: 0.85rem;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-top: 0.5rem;
    }
    
    /* Matrix Table Styling */
    .matrix-container {
        background-color: #FFFFFF;
        padding: 2rem;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        margin: 2rem 0;
    }
    
    .matrix-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1.5rem;
    }
    
    .matrix-title {
        color: #001f3f;
        font-size: 1.5rem;
        font-weight: 700;
        margin: 0;
    }
    
    .matrix-subtitle {
        color: #666;
        font-size: 0.9rem;
        margin: 0.3rem 0 0 0;
    }
    
    .matrix-legend {
        display: flex;
        gap: 1.5rem;
        align-items: center;
    }
    
    .legend-item {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 0.85rem;
    }
    
    .legend-dot {
        width: 12px;
        height: 12px;
        border-radius: 50%;
    }
    
    .legend-dot.actual {
        background-color: #4285F4;
    }
    
    .legend-dot.previous {
        background-color: #34A853;
    }
    
    .export-btn {
        background-color: #001f3f;
        color: #FFFFFF;
        border: none;
        padding: 0.6rem 1.2rem;
        border-radius: 4px;
        font-size: 0.85rem;
        font-weight: 600;
        cursor: pointer;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .export-btn:hover {
        background-color: #003366;
    }
    
    /* Table styling */
    .dataframe {
        width: 100%;
        border-collapse: collapse;
    }
    
    .dataframe th {
        background-color: #F5F5F5;
        color: #001f3f;
        font-weight: 600;
        padding: 0.8rem;
        text-align: left;
        border-bottom: 2px solid #E0E0E0;
        font-size: 0.85rem;
    }
    
    .dataframe td {
        padding: 0.8rem;
        border-bottom: 1px solid #F0F0F0;
        font-size: 0.85rem;
    }
    
    .dataframe tr:hover {
        background-color: #F9F9F9;
    }
    
    /* Trend arrows */
    .trend-up {
        color: #EA4335;
    }
    
    .trend-down {
        color: #34A853;
    }
    
    .trend-stable {
        color: #5F6368;
    }
    </style>
""", unsafe_allow_html=True)


def render_kpi_card(value: float, label: str, status: str, icon: str, format_type: str = "number"):
    """
    Render a KPI card with status badge, icon, value, and label.
    
    Args:
        value: The KPI value to display
        label: The label/title for the KPI
        status: Status type ("attention", "review", "proactive", "utilization")
        icon: Icon emoji or symbol
        format_type: Format type ("number", "currency", "percentage")
    
    Side Effects:
        Renders HTML in Streamlit
    """
    if format_type == "number":
        if value >= 1000:
            formatted_value = f"{value:,.2f}" if value % 1 != 0 else f"{value:,.0f}"
        else:
            formatted_value = f"{value:.0f}" if value % 1 == 0 else f"{value:.2f}"
    elif format_type == "percentage":
        formatted_value = f"{value:.2f}%"
    else:
        formatted_value = f"{value:,.2f}"
    
    status_upper = status.upper()
    
    st.markdown(f"""
        <div class="kpi-card {status}">
            <div class="kpi-status-badge">{status_upper}</div>
            <div class="kpi-content">
                <div class="kpi-icon">{icon}</div>
                <div class="kpi-value">{formatted_value}</div>
            </div>
            <div class="kpi-label">{label}</div>
        </div>
    """, unsafe_allow_html=True)


def create_performance_matrix(df: pd.DataFrame, 
                             date_col: str,
                             metrics_config: dict,
                             current_year: int,
                             previous_year: int) -> pd.DataFrame:
    """
    Create the Safety Performance Matrix with monthly data and calculations.
    
    Args:
        df: Input DataFrame
        date_col: Name of the date column
        metrics_config: Dict mapping metric names to column names
        current_year: Current fiscal year
        previous_year: Previous fiscal year
    
    Returns:
        pd.DataFrame: Matrix DataFrame with all calculations
    
    Side Effects:
        None (data transformation only)
    """
    df_work = df.copy()
    
    # Ensure date column is datetime (should already be processed by combine_year_with_date)
    if date_col and date_col in df_work.columns:
        df_work[date_col] = pd.to_datetime(df_work[date_col], errors='coerce')
    
    # Filter by fiscal years
    df_current = df_work[df_work[date_col].dt.year == current_year].copy()
    df_previous = df_work[df_work[date_col].dt.year == previous_year].copy()
    
    # Initialize matrix
    matrix_data = []
    
    for metric_name, metric_col in metrics_config.items():
        if metric_col not in df.columns:
            continue
        
        row_data = {'KPI INDICATOR': metric_name}
        
        # Monthly data for current year
        for month in range(1, 13):
            month_data = df_current[df_current[date_col].dt.month == month]
            if not month_data.empty and metric_col in month_data.columns:
                value = month_data[metric_col].fillna(0).sum()
                row_data[datetime(2024, month, 1).strftime('%b').upper()] = value if value > 0 else '-'
            else:
                row_data[datetime(2024, month, 1).strftime('%b').upper()] = '-'
        
        # ACCU FY (Current Year Total)
        accu_fy = df_current[metric_col].fillna(0).sum() if metric_col in df_current.columns else 0
        row_data['ACCU FY'] = accu_fy
        
        # ACCU LY (Previous Year Total)
        accu_ly = df_previous[metric_col].fillna(0).sum() if metric_col in df_previous.columns else 0
        row_data['ACCU LY'] = accu_ly
        
        # VAR % (Variance Percentage)
        if accu_ly > 0:
            var_pct = ((accu_fy - accu_ly) / accu_ly) * 100
            row_data['VAR %'] = f"{var_pct:.1f}%"
        else:
            row_data['VAR %'] = "0.0%" if accu_fy == 0 else "N/A"
        
        # TREND (Up/Down arrow based on variance)
        if accu_ly > 0:
            var_pct = ((accu_fy - accu_ly) / accu_ly) * 100
            if var_pct > 0:
                row_data['TREND'] = "↑"
            elif var_pct < 0:
                row_data['TREND'] = "↓"
            else:
                row_data['TREND'] = "→"
        else:
            row_data['TREND'] = "→"
        
        matrix_data.append(row_data)
    
    # Create DataFrame
    months = [datetime(2024, m, 1).strftime('%b').upper() for m in range(1, 13)]
    columns = ['KPI INDICATOR'] + months + ['ACCU FY', 'ACCU LY', 'VAR %', 'TREND']
    
    matrix_df = pd.DataFrame(matrix_data)
    
    # Ensure all columns exist
    for col in columns:
        if col not in matrix_df.columns:
            matrix_df[col] = 0 if col in ['ACCU FY', 'ACCU LY'] else '-'
    
    # Reorder columns
    matrix_df = matrix_df[columns]
    
    return matrix_df


def main():
    """
    Main application function.
    
    Side Effects:
        Renders the complete Streamlit dashboard interface
    """
    # Sidebar - File Upload
    with st.sidebar:
        st.markdown("## 📁 Data Upload")
        st.markdown("---")
        uploaded_file = st.file_uploader(
            "Upload H&S Dashboard Excel File",
            type=['xlsm', 'xlsx'],
            help="Upload your Health & Safety Dashboard Excel file (.xlsm)"
        )
        
        if uploaded_file is None:
            st.info("👆 Please upload an Excel file to begin")
            st.markdown("---")
            st.markdown("### 📖 Instructions")
            st.markdown("""
            1. Click **Browse files** above
            2. Select your **H&S DASHBOARD (1).xlsm** file
            3. The dashboard will automatically load and display your data
            """)
    
    # Initialize session state
    if 'processed_data' not in st.session_state:
        st.session_state.processed_data = None
    if 'sheets_data' not in st.session_state:
        st.session_state.sheets_data = {}
    if 'selected_sheet' not in st.session_state:
        st.session_state.selected_sheet = None
    
    # Process uploaded file
    if uploaded_file is not None:
        try:
            # Read Excel file
            with st.spinner("Reading Excel file..."):
                sheets_data = dp.read_excel_file(uploaded_file)
                st.session_state.sheets_data = sheets_data
            
            if sheets_data:
                # Sheet selection
                sheet_names = list(sheets_data.keys())
                selected_sheet = st.sidebar.selectbox(
                    "Select Sheet",
                    sheet_names,
                    index=0 if sheet_names else None
                )
                st.session_state.selected_sheet = selected_sheet
                
                if selected_sheet:
                    df = sheets_data[selected_sheet]
                    st.session_state.processed_data = df
                    
                    # Auto-detect columns
                    structure = dp.detect_data_structure(df)
                    
                    # Get metric columns
                    columns_lower = {str(col).lower(): col for col in df.columns}
                    accidents_col = dp.get_metric_column(df, 'accidents')
                    incidents_col = dp.get_metric_column(df, 'incidents')
                    hazards_col = dp.get_metric_column(df, 'hazards')
                    near_misses_col = dp.get_metric_column(df, 'near_misses')
                    
                    # Get contractor and date columns
                    contractor_col = structure['contractor_columns'][0] if structure['contractor_columns'] else None
                    date_col = structure['date_columns'][0] if structure['date_columns'] else None
                    
                    # Combine Year column with date column if Year exists
                    df = dp.combine_year_with_date(df, date_col)
                    
                    # Normalize data
                    df = dp.normalize_data(df)
                    
                    # ========== HEADER SECTION ==========
                    header_col1, header_col2 = st.columns([2, 1])
                    
                    with header_col1:
                        st.markdown("""
                            <div style="display: flex; align-items: center; gap: 1.5rem;">
                                <div class="logo-box">
                                    <div class="logo-text">QLDC</div>
                                </div>
                                <div class="header-title">
                                    <h1>HEALTH & SAFETY DASHBOARD</h1>
                                    <p>CONTRACTOR PERFORMANCE MATRIX</p>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                    
                    with header_col2:
                        # Global Filters
                        st.markdown('<div class="filter-label">CONTRACT TYPE</div>', unsafe_allow_html=True)
                        contract_types = ['All'] + (df['Contract Type'].unique().tolist() if 'Contract Type' in df.columns else [])
                        selected_contract_type = st.selectbox(
                            "",
                            options=contract_types,
                            index=0,
                            label_visibility="collapsed",
                            key="contract_type"
                        )
                        
                        st.markdown('<div class="filter-label">CONTRACTOR</div>', unsafe_allow_html=True)
                        contractors = ['All'] + (dp.get_contractor_list(df, contractor_col) if contractor_col else [])
                        selected_contractor = st.selectbox(
                            "",
                            options=contractors,
                            index=0,
                            label_visibility="collapsed",
                            key="contractor"
                        )
                        
                        st.markdown('<div class="filter-label">REPORTING YEAR</div>', unsafe_allow_html=True)
                        if date_col:
                            # Convert date column to datetime first
                            df_date_converted = df.copy()
                            df_date_converted[date_col] = pd.to_datetime(df_date_converted[date_col], errors='coerce')
                            # Filter out null dates and extract unique years
                            valid_dates = df_date_converted[df_date_converted[date_col].notna()]
                            if not valid_dates.empty:
                                years = sorted(valid_dates[date_col].dt.year.unique(), reverse=True)
                                reporting_years = [f"FY {y}" for y in years] if len(years) > 0 else ["FY 2025"]
                            else:
                                reporting_years = ["FY 2025"]
                        else:
                            reporting_years = ["FY 2025"]
                        selected_year = st.selectbox(
                            "",
                            options=reporting_years,
                            index=0,
                            label_visibility="collapsed",
                            key="reporting_year"
                        )
                    
                    # Apply filters
                    df_filtered = df.copy()
                    
                    if selected_contractor != 'All' and contractor_col:
                        df_filtered = df_filtered[df_filtered[contractor_col] == selected_contractor]
                    
                    if selected_contract_type != 'All' and 'Contract Type' in df_filtered.columns:
                        df_filtered = df_filtered[df_filtered['Contract Type'] == selected_contract_type]
                    
                    # Extract year from selection
                    current_year = int(selected_year.split()[-1]) if selected_year else 2025
                    previous_year = current_year - 1
                    
                    # Calculate KPIs on filtered data
                    kpis = dp.calculate_kpis(df_filtered, date_col, contractor_col)
                    
                    # ========== KPI CARDS ROW ==========
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        render_kpi_card(
                            kpis.get('total_accidents', 0),
                            "ACCIDENTS",
                            "attention",
                            "🛡️",
                            "number"
                        )
                    
                    with col2:
                        render_kpi_card(
                            kpis.get('total_incidents', 0),
                            "INCIDENTS",
                            "review",
                            "⚠️",
                            "number"
                        )
                    
                    with col3:
                        render_kpi_card(
                            kpis.get('total_hazards', 0),
                            "HAZARDS IDENTIFIED",
                            "proactive",
                            "📊",
                            "number"
                        )
                    
                    with col4:
                        total_hours = kpis.get('total_hours', kpis.get('total_man_hours', 0))
                        render_kpi_card(
                            total_hours,
                            "TOTAL HOURS",
                            "utilization",
                            "⏱️",
                            "number"
                        )
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    # ========== SAFETY PERFORMANCE MATRIX ==========
                    st.markdown("""
                        <div class="matrix-container">
                            <div class="matrix-header">
                                <div>
                                    <h2 class="matrix-title">SAFETY PERFORMANCE MATRIX</h2>
                                    <p class="matrix-subtitle">COMPREHENSIVE KPI TRACKING ACROSS {}</p>
                                </div>
                                <div style="display: flex; gap: 1.5rem; align-items: center;">
                                    <div class="matrix-legend">
                                        <div class="legend-item">
                                            <div class="legend-dot actual"></div>
                                            <span>ACTUAL (FY)</span>
                                        </div>
                                        <div class="legend-item">
                                            <div class="legend-dot previous"></div>
                                            <span>PREVIOUS (LY)</span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    """.format(selected_year), unsafe_allow_html=True)
                    
                    # Build metrics config
                    metrics_config = {}
                    if accidents_col:
                        metrics_config['Accident'] = accidents_col
                    if incidents_col:
                        metrics_config['Incident'] = incidents_col
                    if hazards_col:
                        metrics_config['Hazard Before Sh*t Happens'] = hazards_col
                    if near_misses_col:
                        metrics_config['Near-Miss That was Lucky'] = near_misses_col
                    
                    # Add additional metrics if columns exist
                    for col in df_filtered.columns:
                        col_lower = str(col).lower()
                        if 'lti' in col_lower or 'lost time' in col_lower:
                            metrics_config['Lost Time Injury (LTI)'] = col
                        if 'take 5' in col_lower or 'take5' in col_lower:
                            metrics_config['Take 5'] = col
                        if 'toolbox' in col_lower:
                            metrics_config['ToolBoxes'] = col
                        if 'audit' in col_lower:
                            metrics_config['Audits'] = col
                        if 'hour' in col_lower and 'total' in col_lower:
                            metrics_config['Total hours worked'] = col
                    
                    if date_col and metrics_config:
                        matrix_df = create_performance_matrix(
                            df_filtered,
                            date_col,
                            metrics_config,
                            current_year,
                            previous_year
                        )
                        
                        # Display matrix table
                        st.dataframe(
                            matrix_df,
                            use_container_width=True,
                            hide_index=True
                        )
                        
                        # Export buttons
                        export_col1, export_col2 = st.columns(2)
                        
                        with export_col1:
                            csv = matrix_df.to_csv(index=False).encode('utf-8')
                            st.download_button(
                                label="📥 EXPORT TABLE (CSV)",
                                data=csv,
                                file_name=f"safety_performance_matrix_{current_year}.csv",
                                mime="text/csv"
                            )
                        
                        with export_col2:
                            # Store chart figures for PDF export (will be set after charts are created)
                            st.session_state['matrix_df'] = matrix_df
                            st.session_state['kpis'] = kpis
                            st.session_state['pdf_reporting_year'] = selected_year
                    else:
                        st.info("Date column and metrics required to generate performance matrix")
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    # ========== BOTTOM CHARTS ROW ==========
                    chart_col1, chart_col2 = st.columns([2, 1])
                    
                    # Initialize chart variables
                    fig_timeline = None
                    fig_pie = None
                    
                    with chart_col1:
                        st.markdown("#### CONTRACTOR DISTRIBUTION TIMELINE")
                        if date_col:
                            try:
                                # Create stacked bar chart with trendline
                                fig_timeline = vis.create_contractor_timeline_chart(
                                    df_filtered,
                                    date_col,
                                    hazards_col=hazards_col,
                                    incidents_col=incidents_col,
                                    accidents_col=accidents_col,
                                    title=""
                                )
                                st.plotly_chart(fig_timeline, use_container_width=True)
                                # Store for PDF export
                                st.session_state['fig_timeline'] = fig_timeline
                            except Exception as e:
                                st.warning(f"Could not create timeline chart: {str(e)}")
                        else:
                            st.info("Date column required for timeline chart")
                    
                    with chart_col2:
                        st.markdown("#### EVENT CLASSIFICATION")
                        try:
                            # Calculate total events
                            total_events = (
                                kpis.get('total_accidents', 0) +
                                kpis.get('total_incidents', 0) +
                                kpis.get('total_hazards', 0) +
                                kpis.get('near_misses', 0)
                            )
                            
                            fig_pie = vis.create_total_events_pie_chart(
                                df_filtered,
                                accidents_col=accidents_col,
                                incidents_col=incidents_col,
                                hazards_col=hazards_col,
                                near_misses_col=near_misses_col,
                                title="",
                                total_events=total_events
                            )
                            st.plotly_chart(fig_pie, use_container_width=True)
                            # Store for PDF export
                            st.session_state['fig_pie'] = fig_pie
                        except Exception as e:
                            st.warning(f"Could not create pie chart: {str(e)}")
                    
                    # PDF Export Button (after charts are created)
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown("---")
                    
                    if 'matrix_df' in st.session_state and 'kpis' in st.session_state:
                        try:
                            # Get stored data
                            matrix_df_pdf = st.session_state.get('matrix_df')
                            kpis_pdf = st.session_state.get('kpis')
                            reporting_year_pdf = st.session_state.get('pdf_reporting_year', selected_year)
                            fig_timeline_pdf = st.session_state.get('fig_timeline')
                            fig_pie_pdf = st.session_state.get('fig_pie')
                            
                            # Generate PDF
                            with st.spinner("Generating PDF report..."):
                                pdf_bytes = pdf_gen.generate_pdf_download(
                                    kpis=kpis_pdf,
                                    matrix_df=matrix_df_pdf,
                                    timeline_chart=fig_timeline_pdf,
                                    pie_chart=fig_pie_pdf,
                                    reporting_year=reporting_year_pdf
                                )
                            
                            st.download_button(
                                label="📄 EXPORT DASHBOARD TO PDF",
                                data=pdf_bytes,
                                file_name=f"health_safety_dashboard_{current_year}_{datetime.now().strftime('%Y%m%d')}.pdf",
                                mime="application/pdf",
                                help="Download a complete PDF report with KPIs, performance matrix, and charts"
                            )
                        except Exception as e:
                            st.warning(f"PDF export error: {str(e)}. Make sure kaleido is installed: pip install kaleido")
        
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")
            st.exception(e)
    
    else:
        # Welcome screen
        st.info("👈 Please upload an Excel file (.xlsm) to begin using the sidebar")
        
        # Instructions
        st.markdown("""
        ### 📖 Instructions
        
        1. **Upload File**: Use the sidebar to upload your H&S Dashboard Excel file
        2. **Select Sheet**: Choose the sheet containing your safety data
        3. **Apply Filters**: Use the filters in the header to filter data
        4. **View Dashboard**: Explore KPIs, matrix, and interactive charts
        
        ### 📊 Supported Metrics
        
        - **Accidents**: Total accidents
        - **Incidents**: Total recordable incidents
        - **Hazards**: Hazards identified
        - **Near Misses**: Near miss incidents
        - **Total Hours**: Total hours worked
        """)


if __name__ == "__main__":
    main()
