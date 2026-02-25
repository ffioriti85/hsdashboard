"""
Data Processing Module for Health & Safety Dashboard

This module handles reading, parsing, and cleaning Excel data from H&S dashboard files.
It provides functions to extract safety metrics, normalize data, and prepare it for visualization.

Author: Senior Full-Stack Python Developer
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import streamlit as st


def read_excel_file(uploaded_file) -> Dict[str, pd.DataFrame]:
    """
    Read Excel file and return a dictionary of DataFrames for each sheet.
    
    Args:
        uploaded_file: Streamlit uploaded file object (.xlsm file)
    
    Returns:
        Dict[str, pd.DataFrame]: Dictionary mapping sheet names to DataFrames
    
    Side Effects:
        None (read-only operation)
    """
    try:
        # Read all sheets from the Excel file
        excel_data = pd.read_excel(
            uploaded_file,
            sheet_name=None,  # Read all sheets
            engine='openpyxl'
        )
        return excel_data
    except Exception as e:
        st.error(f"Error reading Excel file: {str(e)}")
        return {}


def detect_data_structure(df: pd.DataFrame) -> Dict[str, any]:
    """
    Analyze DataFrame structure to identify key columns and data patterns.
    
    Args:
        df: Input DataFrame to analyze
    
    Returns:
        Dict containing detected column mappings and data types
    
    Side Effects:
        None (read-only analysis)
    """
    structure = {
        'date_columns': [],
        'contractor_columns': [],
        'metric_columns': [],
        'has_headers': False
    }
    
    # Common column name patterns to look for
    date_patterns = ['date', 'time', 'period', 'month', 'year']
    contractor_patterns = ['contractor', 'company', 'vendor', 'supplier', 'entity']
    metric_patterns = ['incident', 'accident', 'hazard', 'lti', 'man-hour', 'manhour', 'trifr', 'ltifr', 'near miss']
    
    # Convert column names to lowercase for pattern matching
    columns_lower = [str(col).lower() for col in df.columns]
    
    for idx, col in enumerate(columns_lower):
        # Check for date columns
        if any(pattern in col for pattern in date_patterns):
            structure['date_columns'].append(df.columns[idx])
        
        # Check for contractor columns
        if any(pattern in col for pattern in contractor_patterns):
            structure['contractor_columns'].append(df.columns[idx])
        
        # Check for metric columns
        if any(pattern in col for pattern in metric_patterns):
            structure['metric_columns'].append(df.columns[idx])
    
    return structure


def extract_incidents_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Extract and normalize incident data from a DataFrame.
    
    Args:
        df: Raw DataFrame containing incident data
    
    Returns:
        pd.DataFrame: Cleaned DataFrame with standardized column names
    
    Side Effects:
        None (data transformation only)
    """
    df_clean = df.copy()
    
    # Remove completely empty rows
    df_clean = df_clean.dropna(how='all')
    
    # Try to identify and standardize date columns
    date_cols = [col for col in df_clean.columns if 'date' in str(col).lower()]
    if date_cols:
        for col in date_cols:
            try:
                df_clean[col] = pd.to_datetime(df_clean[col], errors='coerce')
            except:
                pass
    
    return df_clean


def calculate_kpis(df: pd.DataFrame, 
                   date_col: Optional[str] = None,
                   contractor_col: Optional[str] = None) -> Dict[str, float]:
    """
    Calculate key performance indicators from the dataset.
    
    Args:
        df: DataFrame containing safety data
        date_col: Name of the date column (optional)
        contractor_col: Name of the contractor column (optional)
    
    Returns:
        Dict[str, float]: Dictionary of KPI names and values
    
    Side Effects:
        None (calculation only)
    
    KPIs Calculated:
        - Total Man-hours
        - Total Incidents
        - Total LTIs (Lost Time Injuries)
        - TRIFR (Total Recordable Injury Frequency Rate)
        - LTIFR (Lost Time Injury Frequency Rate)
        - Near Misses
    """
    kpis = {
        'total_man_hours': 0.0,
        'total_hours': 0.0,  # Alias for total hours
        'total_incidents': 0.0,
        'total_accidents': 0.0,
        'total_hazards': 0.0,
        'total_ltis': 0.0,
        'trifr': 0.0,
        'ltifr': 0.0,
        'near_misses': 0.0
    }
    
    if df.empty:
        return kpis
    
    # Try to find metric columns by common names
    columns_lower = {str(col).lower(): col for col in df.columns}
    
    # Extract man-hours / total hours
    man_hour_cols = [col for key, col in columns_lower.items() 
                     if 'man-hour' in key or 'manhour' in key or 'hours' in key or 'total hour' in key]
    if man_hour_cols:
        for col in man_hour_cols:
            try:
                value = df[col].fillna(0).astype(float).sum()
                kpis['total_man_hours'] += value
                kpis['total_hours'] += value
            except:
                pass
    
    # Extract incidents
    incident_cols = [col for key, col in columns_lower.items() 
                     if 'incident' in key and 'near' not in key and 'accident' not in key]
    if incident_cols:
        for col in incident_cols:
            try:
                kpis['total_incidents'] += df[col].fillna(0).astype(float).sum()
            except:
                pass
    
    # Extract accidents
    accident_cols = [col for key, col in columns_lower.items() 
                     if 'accident' in key]
    if accident_cols:
        for col in accident_cols:
            try:
                kpis['total_accidents'] += df[col].fillna(0).astype(float).sum()
            except:
                pass
    
    # Extract hazards
    hazard_cols = [col for key, col in columns_lower.items() 
                   if 'hazard' in key]
    if hazard_cols:
        for col in hazard_cols:
            try:
                kpis['total_hazards'] += df[col].fillna(0).astype(float).sum()
            except:
                pass
    
    # Extract LTIs
    lti_cols = [col for key, col in columns_lower.items() 
                if 'lti' in key or 'lost time' in key]
    if lti_cols:
        for col in lti_cols:
            try:
                kpis['total_ltis'] += df[col].fillna(0).astype(float).sum()
            except:
                pass
    
    # Extract Near Misses
    near_miss_cols = [col for key, col in columns_lower.items() 
                      if 'near miss' in key or 'near-miss' in key]
    if near_miss_cols:
        for col in near_miss_cols:
            try:
                kpis['near_misses'] += df[col].fillna(0).astype(float).sum()
            except:
                pass
    
    # Calculate TRIFR: (Total Recordable Injuries × 1,000,000) / Total Man-hours
    if kpis['total_man_hours'] > 0:
        kpis['trifr'] = (kpis['total_incidents'] * 1_000_000) / kpis['total_man_hours']
    
    # Calculate LTIFR: (Lost Time Injuries × 1,000,000) / Total Man-hours
    if kpis['total_man_hours'] > 0:
        kpis['ltifr'] = (kpis['total_ltis'] * 1_000_000) / kpis['total_man_hours']
    
    return kpis


def filter_by_contractor(df: pd.DataFrame, 
                         contractor_col: str, 
                         selected_contractors: List[str]) -> pd.DataFrame:
    """
    Filter DataFrame by selected contractors.
    
    Args:
        df: Input DataFrame
        contractor_col: Name of the contractor column
        selected_contractors: List of contractor names to filter by
    
    Returns:
        pd.DataFrame: Filtered DataFrame
    
    Side Effects:
        None (data filtering only)
    """
    if not selected_contractors or contractor_col not in df.columns:
        return df
    
    return df[df[contractor_col].isin(selected_contractors)]


def filter_by_date_range(df: pd.DataFrame, 
                         date_col: str, 
                         start_date: datetime, 
                         end_date: datetime) -> pd.DataFrame:
    """
    Filter DataFrame by date range.
    
    Args:
        df: Input DataFrame
        date_col: Name of the date column
        start_date: Start date for filtering
        end_date: End date for filtering
    
    Returns:
        pd.DataFrame: Filtered DataFrame
    
    Side Effects:
        None (data filtering only)
    """
    if date_col not in df.columns:
        return df
    
    # Ensure date column is datetime type
    df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
    
    # Convert start_date and end_date to pandas Timestamp for proper comparison
    # Streamlit date_input returns date objects, which need to be converted to Timestamp
    start_timestamp = pd.Timestamp(start_date)
    # For end_date, include the entire day by setting to end of day (23:59:59.999999)
    end_timestamp = pd.Timestamp(end_date) + pd.Timedelta(days=1) - pd.Timedelta(microseconds=1)
    
    # Filter by date range
    mask = (df[date_col] >= start_timestamp) & (df[date_col] <= end_timestamp)
    return df[mask]


def combine_year_with_date(df: pd.DataFrame, date_col: Optional[str] = None) -> pd.DataFrame:
    """
    Combine Year column with date column to create proper datetime values.
    
    Args:
        df: Input DataFrame
        date_col: Name of the date column (optional, will auto-detect if not provided)
    
    Returns:
        pd.DataFrame: DataFrame with properly formatted dates
    
    Side Effects:
        Modifies the date column in the DataFrame
    """
    df_work = df.copy()
    
    # Find Year column
    year_col = None
    for col in df_work.columns:
        if str(col).lower() in ['year', 'yr', 'reporting year']:
            year_col = col
            break
    
    if not year_col or year_col not in df_work.columns:
        return df_work
    
    # Find date column if not provided
    if not date_col:
        columns_lower = {str(col).lower(): col for col in df_work.columns}
        date_patterns = ['date', 'time', 'period', 'month']
        for pattern in date_patterns:
            for key, col in columns_lower.items():
                if pattern in key and 'year' not in key:
                    date_col = col
                    break
            if date_col:
                break
    
    if not date_col or date_col not in df_work.columns:
        return df_work
    
    # Convert Year to numeric
    df_work['_Year'] = pd.to_numeric(df_work[year_col], errors='coerce')
    
    # Convert date column to datetime
    df_work[date_col] = pd.to_datetime(df_work[date_col], errors='coerce')
    
    # Identify rows where date year is invalid (defaulting to 1970 or before 2000)
    mask_invalid_year = (df_work[date_col].dt.year < 2000) | (df_work[date_col].isna())
    
    if mask_invalid_year.any():
        # For rows with invalid year, combine Year column with date
        valid_year_mask = df_work['_Year'].notna() & (df_work['_Year'] >= 2000)
        combined_mask = mask_invalid_year & valid_year_mask
        
        if combined_mask.any():
            # Create new datetime using Year column + month/day from date column
            try:
                # Try full date (year-month-day)
                df_work.loc[combined_mask, date_col] = pd.to_datetime(
                    df_work.loc[combined_mask, '_Year'].astype(int).astype(str) + '-' + 
                    df_work.loc[combined_mask, date_col].dt.month.fillna(1).astype(int).astype(str) + '-' + 
                    df_work.loc[combined_mask, date_col].dt.day.fillna(1).astype(int).astype(str),
                    errors='coerce'
                )
            except:
                # Fallback: try year-month only
                try:
                    df_work.loc[combined_mask, date_col] = pd.to_datetime(
                        df_work.loc[combined_mask, '_Year'].astype(int).astype(str) + '-' + 
                        df_work.loc[combined_mask, date_col].dt.month.fillna(1).astype(int).astype(str) + '-01',
                        errors='coerce'
                    )
                except:
                    pass
    
    # Clean up temporary column
    if '_Year' in df_work.columns:
        df_work = df_work.drop(columns=['_Year'])
    
    return df_work


def normalize_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize and clean the dataset for visualization.
    
    Args:
        df: Raw DataFrame
    
    Returns:
        pd.DataFrame: Normalized DataFrame with consistent data types
    
    Side Effects:
        None (data transformation only)
    """
    df_normalized = df.copy()
    
    # Remove rows with all NaN values
    df_normalized = df_normalized.dropna(how='all')
    
    # Convert numeric columns
    for col in df_normalized.columns:
        # Try to convert to numeric, keeping non-numeric values as strings
        try:
            df_normalized[col] = pd.to_numeric(df_normalized[col], errors='ignore')
        except:
            pass
    
    return df_normalized


def get_contractor_list(df: pd.DataFrame, contractor_col: Optional[str] = None) -> List[str]:
    """
    Extract unique list of contractors from the dataset.
    
    Args:
        df: Input DataFrame
        contractor_col: Name of the contractor column (optional, will auto-detect if not provided)
    
    Returns:
        List[str]: Sorted list of unique contractor names
    
    Side Effects:
        None (read-only operation)
    """
    if contractor_col and contractor_col in df.columns:
        contractors = df[contractor_col].dropna().unique().tolist()
        return sorted([str(c) for c in contractors if str(c).strip()])
    
    # Auto-detect contractor column
    columns_lower = {str(col).lower(): col for col in df.columns}
    contractor_patterns = ['contractor', 'company', 'vendor', 'supplier', 'entity']
    
    for pattern in contractor_patterns:
        for key, col in columns_lower.items():
            if pattern in key:
                contractors = df[col].dropna().unique().tolist()
                return sorted([str(c) for c in contractors if str(c).strip()])
    
    return []


def get_entity_list(df: pd.DataFrame, entity_col: Optional[str] = None) -> List[str]:
    """
    Extract unique list of entities from the dataset.
    
    Args:
        df: Input DataFrame
        entity_col: Name of the entity column (optional, will auto-detect if not provided)
    
    Returns:
        List[str]: Sorted list of unique entity names
    
    Side Effects:
        None (read-only operation)
    """
    if entity_col and entity_col in df.columns:
        entities = df[entity_col].dropna().unique().tolist()
        return sorted([str(e) for e in entities if str(e).strip()])
    
    # Auto-detect entity column (prefer 'entity', then contractor patterns)
    columns_lower = {str(col).lower(): col for col in df.columns}
    
    # First try 'entity' specifically
    for key, col in columns_lower.items():
        if 'entity' in key:
            entities = df[col].dropna().unique().tolist()
            return sorted([str(e) for e in entities if str(e).strip()])
    
    # Fall back to contractor patterns
    contractor_patterns = ['contractor', 'company', 'vendor', 'supplier']
    for pattern in contractor_patterns:
        for key, col in columns_lower.items():
            if pattern in key:
                entities = df[col].dropna().unique().tolist()
                return sorted([str(e) for e in entities if str(e).strip()])
    
    return []


def get_metric_column(df: pd.DataFrame, metric_name: str) -> Optional[str]:
    """
    Get the column name for a specific metric.
    
    Args:
        df: Input DataFrame
        metric_name: Name of the metric to find ('accidents', 'incidents', 'hazards', 'near_misses')
    
    Returns:
        Optional[str]: Column name if found, None otherwise
    
    Side Effects:
        None (read-only operation)
    """
    columns_lower = {str(col).lower(): col for col in df.columns}
    metric_lower = metric_name.lower()
    
    # Direct match
    for key, col in columns_lower.items():
        if metric_lower in key:
            return col
    
    # Pattern matching
    patterns = {
        'accidents': ['accident'],
        'incidents': ['incident'],
        'hazards': ['hazard'],
        'near_misses': ['near miss', 'near-miss']
    }
    
    if metric_lower in patterns:
        for pattern in patterns[metric_lower]:
            for key, col in columns_lower.items():
                if pattern in key:
                    return col
    
    return None


def get_date_range(df: pd.DataFrame, date_col: Optional[str] = None) -> Tuple[Optional[datetime], Optional[datetime]]:
    """
    Get the minimum and maximum dates from the dataset.
    
    Args:
        df: Input DataFrame
        date_col: Name of the date column (optional, will auto-detect if not provided)
    
    Returns:
        Tuple[Optional[datetime], Optional[datetime]]: (min_date, max_date)
    
    Side Effects:
        None (read-only operation)
    """
    if date_col and date_col in df.columns:
        try:
            dates = pd.to_datetime(df[date_col], errors='coerce').dropna()
            if not dates.empty:
                return dates.min().to_pydatetime(), dates.max().to_pydatetime()
        except:
            pass
    
    # Auto-detect date column
    columns_lower = {str(col).lower(): col for col in df.columns}
    date_patterns = ['date', 'time', 'period']
    
    for pattern in date_patterns:
        for key, col in columns_lower.items():
            if pattern in key:
                try:
                    dates = pd.to_datetime(df[col], errors='coerce').dropna()
                    if not dates.empty:
                        return dates.min().to_pydatetime(), dates.max().to_pydatetime()
                except:
                    pass
    
    return None, None
