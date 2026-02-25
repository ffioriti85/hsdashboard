"""
Visualization Module for Health & Safety Dashboard

This module contains functions to generate interactive Plotly charts and visualizations
for the H&S dashboard, following a modern Gemini Canvas aesthetic.

Author: Senior Full-Stack Python Developer
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import Optional, List, Dict
from datetime import datetime


# Color palette - Gemini Canvas inspired (blues, teals, soft grays)
COLOR_PALETTE = {
    'primary': '#4285F4',      # Google Blue
    'secondary': '#34A853',     # Google Green
    'accent': '#00BCD4',        # Cyan/Teal
    'warning': '#FBBC04',       # Google Yellow
    'danger': '#EA4335',        # Google Red
    'neutral': '#5F6368',       # Gray
    'light_bg': '#F8F9FA',      # Light gray background
    'card_bg': '#FFFFFF',       # White card background
    'text_primary': '#202124',  # Dark text
    'text_secondary': '#5F6368' # Gray text
}


def create_kpi_card_style(value: float, label: str, trend: Optional[float] = None) -> Dict:
    """
    Generate styling information for KPI cards.
    
    Args:
        value: The KPI value to display
        label: The label/title for the KPI
        trend: Optional trend value (positive/negative percentage)
    
    Returns:
        Dict: Styling information for the KPI card
    
    Side Effects:
        None (returns styling data only)
    """
    return {
        'value': value,
        'label': label,
        'trend': trend,
        'color': COLOR_PALETTE['primary']
    }


def create_incident_trend_chart(df: pd.DataFrame, 
                                 date_col: str,
                                 metric_col: str,
                                 title: str = "Incident Trends Over Time") -> go.Figure:
    """
    Create a line chart showing incident trends over time.
    
    Args:
        df: DataFrame with date and metric columns
        date_col: Name of the date column
        metric_col: Name of the metric column to plot
        title: Chart title
    
    Returns:
        go.Figure: Plotly figure object
    
    Side Effects:
        None (chart generation only)
    """
    # Ensure date column is datetime
    df_plot = df.copy()
    df_plot[date_col] = pd.to_datetime(df_plot[date_col], errors='coerce')
    df_plot = df_plot.sort_values(by=date_col)
    
    # Aggregate by date if needed
    if metric_col in df_plot.columns:
        df_grouped = df_plot.groupby(date_col)[metric_col].sum().reset_index()
    else:
        df_grouped = df_plot[[date_col]].copy()
        df_grouped[metric_col] = 0
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df_grouped[date_col],
        y=df_grouped[metric_col],
        mode='lines+markers',
        name=metric_col,
        line=dict(
            color=COLOR_PALETTE['primary'],
            width=3
        ),
        marker=dict(
            size=8,
            color=COLOR_PALETTE['primary']
        ),
        fill='tonexty',
        fillcolor=f"rgba(66, 133, 244, 0.1)"
    ))
    
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=20, color=COLOR_PALETTE['text_primary']),
            x=0.5
        ),
        xaxis=dict(
            title="Date",
            gridcolor='rgba(0,0,0,0.1)',
            showgrid=True
        ),
        yaxis=dict(
            title="Count",
            gridcolor='rgba(0,0,0,0.1)',
            showgrid=True
        ),
        plot_bgcolor=COLOR_PALETTE['card_bg'],
        paper_bgcolor=COLOR_PALETTE['light_bg'],
        hovermode='x unified',
        font=dict(family="Arial, sans-serif"),
        margin=dict(l=20, r=20, t=60, b=20)
    )
    
    return fig


def create_contractor_performance_chart(df: pd.DataFrame,
                                        contractor_col: str,
                                        metric_col: str,
                                        title: str = "Performance by Contractor") -> go.Figure:
    """
    Create a horizontal bar chart showing performance metrics by contractor.
    
    Args:
        df: DataFrame with contractor and metric columns
        contractor_col: Name of the contractor column
        metric_col: Name of the metric column to plot
        title: Chart title
    
    Returns:
        go.Figure: Plotly figure object
    
    Side Effects:
        None (chart generation only)
    """
    if contractor_col not in df.columns or metric_col not in df.columns:
        # Return empty chart if columns don't exist
        fig = go.Figure()
        fig.add_annotation(
            text="Data not available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
        return fig
    
    # Aggregate by contractor
    df_grouped = df.groupby(contractor_col)[metric_col].sum().reset_index()
    df_grouped = df_grouped.sort_values(by=metric_col, ascending=True)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=df_grouped[contractor_col],
        x=df_grouped[metric_col],
        orientation='h',
        marker=dict(
            color=COLOR_PALETTE['accent'],
            line=dict(color=COLOR_PALETTE['primary'], width=1)
        ),
        text=df_grouped[metric_col],
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>Value: %{x}<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=20, color=COLOR_PALETTE['text_primary']),
            x=0.5
        ),
        xaxis=dict(
            title="Count",
            gridcolor='rgba(0,0,0,0.1)',
            showgrid=True
        ),
        yaxis=dict(
            title="Contractor",
            gridcolor='rgba(0,0,0,0.1)',
            showgrid=False
        ),
        plot_bgcolor=COLOR_PALETTE['card_bg'],
        paper_bgcolor=COLOR_PALETTE['light_bg'],
        font=dict(family="Arial, sans-serif"),
        margin=dict(l=20, r=20, t=60, b=20),
        height=400
    )
    
    return fig


def create_incident_category_chart(df: pd.DataFrame,
                                    category_col: str,
                                    metric_col: str,
                                    title: str = "Incidents by Category") -> go.Figure:
    """
    Create a pie or bar chart showing incidents by category.
    
    Args:
        df: DataFrame with category and metric columns
        category_col: Name of the category column
        metric_col: Name of the metric column
        title: Chart title
    
    Returns:
        go.Figure: Plotly figure object
    
    Side Effects:
        None (chart generation only)
    """
    if category_col not in df.columns or metric_col not in df.columns:
        # Return empty chart if columns don't exist
        fig = go.Figure()
        fig.add_annotation(
            text="Data not available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
        return fig
    
    # Aggregate by category
    df_grouped = df.groupby(category_col)[metric_col].sum().reset_index()
    df_grouped = df_grouped.sort_values(by=metric_col, ascending=False)
    
    # Use a color scale
    colors = [COLOR_PALETTE['primary'], COLOR_PALETTE['accent'], 
              COLOR_PALETTE['secondary'], COLOR_PALETTE['warning'], 
              COLOR_PALETTE['danger']]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=df_grouped[category_col],
        y=df_grouped[metric_col],
        marker=dict(
            color=df_grouped[metric_col],
            colorscale='Blues',
            showscale=True,
            colorbar=dict(title="Count")
        ),
        text=df_grouped[metric_col],
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>Count: %{y}<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=20, color=COLOR_PALETTE['text_primary']),
            x=0.5
        ),
        xaxis=dict(
            title="Category",
            gridcolor='rgba(0,0,0,0.1)',
            showgrid=False
        ),
        yaxis=dict(
            title="Count",
            gridcolor='rgba(0,0,0,0.1)',
            showgrid=True
        ),
        plot_bgcolor=COLOR_PALETTE['card_bg'],
        paper_bgcolor=COLOR_PALETTE['light_bg'],
        font=dict(family="Arial, sans-serif"),
        margin=dict(l=20, r=20, t=60, b=20)
    )
    
    return fig


def create_metric_comparison_chart(df: pd.DataFrame,
                                   date_col: str,
                                   metrics: List[str],
                                   title: str = "Metrics Comparison") -> go.Figure:
    """
    Create a multi-line chart comparing multiple metrics over time.
    
    Args:
        df: DataFrame with date and multiple metric columns
        date_col: Name of the date column
        metrics: List of metric column names to compare
        title: Chart title
    
    Returns:
        go.Figure: Plotly figure object
    
    Side Effects:
        None (chart generation only)
    """
    df_plot = df.copy()
    df_plot[date_col] = pd.to_datetime(df_plot[date_col], errors='coerce')
    df_plot = df_plot.sort_values(by=date_col)
    
    # Aggregate by date
    df_grouped = df_plot.groupby(date_col)[metrics].sum().reset_index()
    
    fig = go.Figure()
    
    colors = [COLOR_PALETTE['primary'], COLOR_PALETTE['accent'], 
              COLOR_PALETTE['secondary'], COLOR_PALETTE['warning'], 
              COLOR_PALETTE['danger']]
    
    for idx, metric in enumerate(metrics):
        if metric in df_grouped.columns:
            fig.add_trace(go.Scatter(
                x=df_grouped[date_col],
                y=df_grouped[metric],
                mode='lines+markers',
                name=metric.replace('_', ' ').title(),
                line=dict(
                    color=colors[idx % len(colors)],
                    width=2.5
                ),
                marker=dict(size=6)
            ))
    
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=20, color=COLOR_PALETTE['text_primary']),
            x=0.5
        ),
        xaxis=dict(
            title="Date",
            gridcolor='rgba(0,0,0,0.1)',
            showgrid=True
        ),
        yaxis=dict(
            title="Count",
            gridcolor='rgba(0,0,0,0.1)',
            showgrid=True
        ),
        plot_bgcolor=COLOR_PALETTE['card_bg'],
        paper_bgcolor=COLOR_PALETTE['light_bg'],
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        font=dict(family="Arial, sans-serif"),
        margin=dict(l=20, r=20, t=60, b=20)
    )
    
    return fig


def create_trifr_ltifr_chart(df: pd.DataFrame,
                             date_col: str,
                             trifr_col: Optional[str] = None,
                             ltifr_col: Optional[str] = None,
                             title: str = "TRIFR & LTIFR Trends") -> go.Figure:
    """
    Create a dual-axis chart showing TRIFR and LTIFR trends.
    
    Args:
        df: DataFrame with date and rate columns
        date_col: Name of the date column
        trifr_col: Name of the TRIFR column (optional)
        ltifr_col: Name of the LTIFR column (optional)
        title: Chart title
    
    Returns:
        go.Figure: Plotly figure object
    
    Side Effects:
        None (chart generation only)
    """
    df_plot = df.copy()
    df_plot[date_col] = pd.to_datetime(df_plot[date_col], errors='coerce')
    df_plot = df_plot.sort_values(by=date_col)
    
    fig = make_subplots(specs=[[{"secondary_y": False}]])
    
    if trifr_col and trifr_col in df_plot.columns:
        df_grouped = df_plot.groupby(date_col)[trifr_col].mean().reset_index()
        fig.add_trace(
            go.Scatter(
                x=df_grouped[date_col],
                y=df_grouped[trifr_col],
                name="TRIFR",
                line=dict(color=COLOR_PALETTE['primary'], width=3),
                mode='lines+markers'
            ),
            secondary_y=False
        )
    
    if ltifr_col and ltifr_col in df_plot.columns:
        df_grouped = df_plot.groupby(date_col)[ltifr_col].mean().reset_index()
        fig.add_trace(
            go.Scatter(
                x=df_grouped[date_col],
                y=df_grouped[ltifr_col],
                name="LTIFR",
                line=dict(color=COLOR_PALETTE['danger'], width=3),
                mode='lines+markers'
            ),
            secondary_y=False
        )
    
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=20, color=COLOR_PALETTE['text_primary']),
            x=0.5
        ),
        plot_bgcolor=COLOR_PALETTE['card_bg'],
        paper_bgcolor=COLOR_PALETTE['light_bg'],
        hovermode='x unified',
        font=dict(family="Arial, sans-serif"),
        margin=dict(l=20, r=20, t=60, b=20),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    fig.update_xaxes(
        title_text="Date",
        gridcolor='rgba(0,0,0,0.1)',
        showgrid=True
    )
    
    fig.update_yaxes(
        title_text="Rate",
        gridcolor='rgba(0,0,0,0.1)',
        showgrid=True,
        secondary_y=False
    )
    
    return fig


def create_timeline_chart(df: pd.DataFrame,
                         date_col: str,
                         hazards_col: Optional[str] = None,
                         incidents_col: Optional[str] = None,
                         accidents_col: Optional[str] = None,
                         title: str = "Month-by-Month Reporting Timeline") -> go.Figure:
    """
    Create a timeline chart showing month-by-month trends for Hazards, Incidents, and Accidents.
    
    Args:
        df: DataFrame with date and metric columns
        date_col: Name of the date column
        hazards_col: Name of the hazards column (optional)
        incidents_col: Name of the incidents column (optional)
        accidents_col: Name of the accidents column (optional)
        title: Chart title
    
    Returns:
        go.Figure: Plotly figure object
    
    Side Effects:
        None (chart generation only)
    """
    df_plot = df.copy()
    df_plot[date_col] = pd.to_datetime(df_plot[date_col], errors='coerce')
    df_plot = df_plot.sort_values(by=date_col)
    
    # Group by month
    df_plot['YearMonth'] = df_plot[date_col].dt.to_period('M').astype(str)
    
    # Build aggregation dictionary dynamically
    agg_dict = {}
    if hazards_col and hazards_col in df_plot.columns:
        agg_dict[hazards_col] = 'sum'
    if incidents_col and incidents_col in df_plot.columns:
        agg_dict[incidents_col] = 'sum'
    if accidents_col and accidents_col in df_plot.columns:
        agg_dict[accidents_col] = 'sum'
    
    if agg_dict:
        df_grouped = df_plot.groupby('YearMonth').agg(agg_dict).reset_index()
    else:
        df_grouped = df_plot.groupby('YearMonth').size().reset_index(name='count')
    
    fig = go.Figure()
    
    # Add Hazards line
    if hazards_col and hazards_col in df_plot.columns:
        fig.add_trace(go.Scatter(
            x=df_grouped['YearMonth'],
            y=df_grouped[hazards_col],
            mode='lines+markers',
            name='Hazards',
            line=dict(color=COLOR_PALETTE['warning'], width=3),
            marker=dict(size=8),
            fill='tonexty' if len([c for c in [hazards_col, incidents_col, accidents_col] if c]) == 1 else None,
            fillcolor=f"rgba(251, 188, 4, 0.1)"
        ))
    
    # Add Incidents line
    if incidents_col and incidents_col in df_plot.columns:
        fig.add_trace(go.Scatter(
            x=df_grouped['YearMonth'],
            y=df_grouped[incidents_col],
            mode='lines+markers',
            name='Incidents',
            line=dict(color=COLOR_PALETTE['primary'], width=3),
            marker=dict(size=8)
        ))
    
    # Add Accidents line
    if accidents_col and accidents_col in df_plot.columns:
        fig.add_trace(go.Scatter(
            x=df_grouped['YearMonth'],
            y=df_grouped[accidents_col],
            mode='lines+markers',
            name='Accidents',
            line=dict(color=COLOR_PALETTE['danger'], width=3),
            marker=dict(size=8)
        ))
    
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=20, color=COLOR_PALETTE['text_primary']),
            x=0.5
        ),
        xaxis=dict(
            title="Month",
            gridcolor='rgba(0,0,0,0.1)',
            showgrid=True
        ),
        yaxis=dict(
            title="Count",
            gridcolor='rgba(0,0,0,0.1)',
            showgrid=True
        ),
        plot_bgcolor=COLOR_PALETTE['card_bg'],
        paper_bgcolor=COLOR_PALETTE['light_bg'],
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        font=dict(family="Arial, sans-serif"),
        margin=dict(l=20, r=20, t=60, b=20)
    )
    
    return fig


def create_contractor_timeline_chart(df: pd.DataFrame,
                                     date_col: str,
                                     hazards_col: Optional[str] = None,
                                     incidents_col: Optional[str] = None,
                                     accidents_col: Optional[str] = None,
                                     title: str = "Contractor Distribution Timeline") -> go.Figure:
    """
    Create a stacked bar chart with trendline showing monthly trends for Incidents, Hazards, and Accidents.
    
    Args:
        df: DataFrame with date and metric columns
        date_col: Name of the date column
        hazards_col: Name of the hazards column (optional)
        incidents_col: Name of the incidents column (optional)
        accidents_col: Name of the accidents column (optional)
        title: Chart title
    
    Returns:
        go.Figure: Plotly figure object
    
    Side Effects:
        None (chart generation only)
    """
    df_plot = df.copy()
    df_plot[date_col] = pd.to_datetime(df_plot[date_col], errors='coerce')
    df_plot = df_plot.sort_values(by=date_col)
    
    # Group by month
    df_plot['YearMonth'] = df_plot[date_col].dt.to_period('M').astype(str)
    
    # Build aggregation dictionary dynamically
    agg_dict = {}
    if hazards_col and hazards_col in df_plot.columns:
        agg_dict[hazards_col] = 'sum'
    if incidents_col and incidents_col in df_plot.columns:
        agg_dict[incidents_col] = 'sum'
    if accidents_col and accidents_col in df_plot.columns:
        agg_dict[accidents_col] = 'sum'
    
    if not agg_dict:
        fig = go.Figure()
        fig.add_annotation(
            text="No data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
        return fig
    
    df_grouped = df_plot.groupby('YearMonth').agg(agg_dict).reset_index()
    
    fig = go.Figure()
    
    # Add stacked bars
    if incidents_col and incidents_col in df_plot.columns:
        fig.add_trace(go.Bar(
            x=df_grouped['YearMonth'],
            y=df_grouped[incidents_col],
            name='INCIDENTS',
            marker_color='#EA4335',  # Red
            hovertemplate='<b>%{x}</b><br>INCIDENTS: %{y}<extra></extra>'
        ))
    
    if hazards_col and hazards_col in df_plot.columns:
        fig.add_trace(go.Bar(
            x=df_grouped['YearMonth'],
            y=df_grouped[hazards_col],
            name='HAZARDS',
            marker_color='#00BCD4',  # Teal
            hovertemplate='<b>%{x}</b><br>HAZARDS: %{y}<extra></extra>'
        ))
    
    if accidents_col and accidents_col in df_plot.columns:
        fig.add_trace(go.Bar(
            x=df_grouped['YearMonth'],
            y=df_grouped[accidents_col],
            name='ACCIDENTS',
            marker_color='#001f3f',  # Navy Blue
            hovertemplate='<b>%{x}</b><br>ACCIDENTS: %{y}<extra></extra>'
        ))
    
    # Add trendline for incidents (dashed red line)
    if incidents_col and incidents_col in df_plot.columns:
        # Calculate trendline (simple moving average or linear trend)
        x_numeric = range(len(df_grouped))
        y_values = df_grouped[incidents_col].values
        
        # Simple linear trend
        z = np.polyfit(x_numeric, y_values, 1)
        trendline = np.poly1d(z)(x_numeric)
        
        fig.add_trace(go.Scatter(
            x=df_grouped['YearMonth'],
            y=trendline,
            mode='lines',
            name='Trend',
            line=dict(color='#EA4335', width=2, dash='dash'),
            hovertemplate='<b>%{x}</b><br>Trend: %{y:.1f}<extra></extra>',
            showlegend=False
        ))
    
    fig.update_layout(
        barmode='stack',
        title=dict(
            text=title,
            font=dict(size=16, color='#001f3f'),
            x=0.5
        ),
        xaxis=dict(
            title="",
            gridcolor='rgba(0,0,0,0.1)',
            showgrid=True
        ),
        yaxis=dict(
            title="",
            gridcolor='rgba(0,0,0,0.1)',
            showgrid=True
        ),
        plot_bgcolor='#FFFFFF',
        paper_bgcolor='#F5F5F5',
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        font=dict(family="Arial, sans-serif", size=12),
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    return fig


def create_total_events_pie_chart(df: pd.DataFrame,
                                 accidents_col: Optional[str] = None,
                                 incidents_col: Optional[str] = None,
                                 hazards_col: Optional[str] = None,
                                 near_misses_col: Optional[str] = None,
                                 title: str = "Total Events Distribution",
                                 total_events: Optional[float] = None) -> go.Figure:
    """
    Create a pie chart showing the distribution of total events.
    
    Args:
        df: DataFrame with metric columns
        accidents_col: Name of the accidents column (optional)
        incidents_col: Name of the incidents column (optional)
        hazards_col: Name of the hazards column (optional)
        near_misses_col: Name of the near misses column (optional)
        title: Chart title
    
    Returns:
        go.Figure: Plotly figure object
    
    Side Effects:
        None (chart generation only)
    """
    # Calculate totals for each metric
    data = {}
    labels = []
    values = []
    colors_list = []
    
    if accidents_col and accidents_col in df.columns:
        total = df[accidents_col].fillna(0).sum()
        if total > 0:
            data['Accidents'] = total
            labels.append('Accidents')
            values.append(total)
            colors_list.append(COLOR_PALETTE['danger'])
    
    if incidents_col and incidents_col in df.columns:
        total = df[incidents_col].fillna(0).sum()
        if total > 0:
            data['Incidents'] = total
            labels.append('Incidents')
            values.append(total)
            colors_list.append(COLOR_PALETTE['primary'])
    
    if hazards_col and hazards_col in df.columns:
        total = df[hazards_col].fillna(0).sum()
        if total > 0:
            data['Hazards'] = total
            labels.append('Hazards')
            values.append(total)
            colors_list.append(COLOR_PALETTE['warning'])
    
    if near_misses_col and near_misses_col in df.columns:
        total = df[near_misses_col].fillna(0).sum()
        if total > 0:
            data['Near Misses'] = total
            labels.append('Near Misses')
            values.append(total)
            colors_list.append(COLOR_PALETTE['accent'])
    
    if not labels:
        # Return empty chart if no data
        fig = go.Figure()
        fig.add_annotation(
            text="No data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
        return fig
    
    # Calculate total if not provided
    if total_events is None:
        total_events = sum(values)
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.6,  # Creates a donut chart with larger hole for center text
        marker=dict(colors=colors_list),
        textinfo='none',  # Hide default text
        hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
    )])
    
    # Add center annotation with total events
    fig.add_annotation(
        text=f"<b>TOTAL EVENTS</b><br><span style='font-size:24px;'>{int(total_events)}</span>",
        xref="paper", yref="paper",
        x=0.5, y=0.5,
        showarrow=False,
        font=dict(size=14, color='#001f3f'),
        align="center"
    )
    
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=16, color='#001f3f'),
            x=0.5
        ),
        plot_bgcolor='#FFFFFF',
        paper_bgcolor='#F5F5F5',
        font=dict(family="Arial, sans-serif", size=12),
        margin=dict(l=20, r=20, t=40, b=20),
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.05,
            font=dict(size=11)
        )
    )
    
    return fig


def create_entity_performance_chart(df: pd.DataFrame,
                                    entity_col: str,
                                    metric_col: str,
                                    title: str = "Entity Performance") -> go.Figure:
    """
    Create a bar chart showing entity performance with an average line overlay.
    
    Args:
        df: DataFrame with entity and metric columns
        entity_col: Name of the entity column
        metric_col: Name of the metric column to plot
        title: Chart title
    
    Returns:
        go.Figure: Plotly figure object
    
    Side Effects:
        None (chart generation only)
    """
    if entity_col not in df.columns or metric_col not in df.columns:
        # Return empty chart if columns don't exist
        fig = go.Figure()
        fig.add_annotation(
            text="Data not available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
        return fig
    
    # Aggregate by entity
    df_grouped = df.groupby(entity_col)[metric_col].sum().reset_index()
    df_grouped = df_grouped.sort_values(by=metric_col, ascending=False)
    
    # Calculate average across all entities
    average_value = df_grouped[metric_col].mean()
    
    fig = go.Figure()
    
    # Add bar chart
    fig.add_trace(go.Bar(
        x=df_grouped[entity_col],
        y=df_grouped[metric_col],
        marker=dict(
            color=COLOR_PALETTE['accent'],
            line=dict(color=COLOR_PALETTE['primary'], width=1)
        ),
        text=df_grouped[metric_col],
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>Value: %{y}<br>Average: ' + f'{average_value:.2f}' + '<extra></extra>',
        name=metric_col.replace('_', ' ').title()
    ))
    
    # Add horizontal dashed line for average
    fig.add_hline(
        y=average_value,
        line_dash="dash",
        line_color=COLOR_PALETTE['danger'],
        line_width=2,
        annotation_text=f"Average: {average_value:.2f}",
        annotation_position="right",
        annotation_font_size=12,
        annotation_font_color=COLOR_PALETTE['danger']
    )
    
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=20, color=COLOR_PALETTE['text_primary']),
            x=0.5
        ),
        xaxis=dict(
            title="Entity",
            gridcolor='rgba(0,0,0,0.1)',
            showgrid=False
        ),
        yaxis=dict(
            title="Count",
            gridcolor='rgba(0,0,0,0.1)',
            showgrid=True
        ),
        plot_bgcolor=COLOR_PALETTE['card_bg'],
        paper_bgcolor=COLOR_PALETTE['light_bg'],
        font=dict(family="Arial, sans-serif"),
        margin=dict(l=20, r=20, t=60, b=20),
        showlegend=False
    )
    
    return fig
