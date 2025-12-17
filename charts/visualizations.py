"""
Visualization functions cho các biểu đồ Plotly.
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from config.settings import GRADE_ORDER, STATUS_COLORS


def create_grade_distribution_chart(df: pd.DataFrame) -> go.Figure:
    """Tạo biểu đồ phân bố theo Grade."""
    if 'grade' not in df.columns:
        return go.Figure()
    
    grade_data = df.groupby('grade').agg({
        'loan_amount': ['sum', 'mean', 'count'],
        'int_rate': 'mean'
    }).round(2)
    
    grade_data.columns = ['Total_Volume', 'Avg_Loan', 'Count', 'Avg_Interest']
    grade_data = grade_data.reset_index()
    
    grade_data['grade'] = pd.Categorical(grade_data['grade'], categories=GRADE_ORDER, ordered=True)
    grade_data = grade_data.sort_values('grade')
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig.add_trace(
        go.Bar(
            x=grade_data['grade'],
            y=grade_data['Count'],
            name="Number of Loans",
            marker_color='rgba(102, 126, 234, 0.8)',
            text=grade_data['Count'],
            textposition='outside',
            hovertemplate='<b>Grade %{x}</b><br>Count: %{y:,}<br>Total: $%{customdata[0]:,.0f}<br><extra></extra>',
            customdata=grade_data[['Total_Volume']].values
        ),
        secondary_y=False
    )
    
    fig.add_trace(
        go.Scatter(
            x=grade_data['grade'],
            y=grade_data['Avg_Interest'] * 100,
            name="Avg Interest Rate (%)",
            mode='lines+markers',
            line=dict(color='#f5576c', width=3),
            marker=dict(size=10, symbol='diamond'),
            hovertemplate='<b>Grade %{x}</b><br>Avg Interest: %{y:.2f}%<br><extra></extra>'
        ),
        secondary_y=True
    )
    
    fig.update_layout(
        title=dict(text="Loan Distribution by Grade", font=dict(size=20, color='#333'), x=0.5),
        xaxis_title="Credit Grade",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        template="plotly_white",
        height=450,
        hovermode='x unified'
    )
    
    fig.update_yaxes(title_text="Number of Loans", secondary_y=False)
    fig.update_yaxes(title_text="Interest Rate (%)", secondary_y=True)
    
    return fig


def create_purpose_chart(df: pd.DataFrame) -> go.Figure:
    """Tạo biểu đồ phân bố theo Purpose."""
    purpose_cols = [col for col in df.columns if col.startswith('purpose_')]
    
    if not purpose_cols:
        return go.Figure()
    
    purpose_data = []
    for col in purpose_cols:
        purpose_name = col.replace('purpose_', '').replace('_', ' ').title()
        count = df[col].sum()
        if count > 0:
            avg_amount = df[df[col] == 1]['loan_amount'].mean() if 'loan_amount' in df.columns else 0
            purpose_data.append({'Purpose': purpose_name, 'Count': count, 'Avg_Amount': avg_amount})
    
    if not purpose_data:
        return go.Figure()
    
    purpose_df = pd.DataFrame(purpose_data).sort_values('Count', ascending=True)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=purpose_df['Purpose'],
        x=purpose_df['Count'],
        orientation='h',
        marker=dict(color=purpose_df['Count'], colorscale='Viridis', showscale=True, colorbar=dict(title="Count")),
        text=purpose_df['Count'],
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>Count: %{x:,}<br>Avg Amount: $%{customdata:,.0f}<br><extra></extra>',
        customdata=purpose_df['Avg_Amount']
    ))
    
    fig.update_layout(
        title=dict(text="Loan Purpose Distribution", font=dict(size=20, color='#333'), x=0.5),
        xaxis_title="Number of Loans",
        yaxis_title="Loan Purpose",
        template="plotly_white",
        height=500,
        showlegend=False
    )
    
    return fig


def create_status_pie_chart(df: pd.DataFrame) -> go.Figure:
    """Tạo biểu đồ tròn cho Loan Status."""
    if 'loan_status' not in df.columns:
        return go.Figure()
    
    status_counts = df['loan_status'].value_counts()
    
    fig = go.Figure(data=[go.Pie(
        labels=status_counts.index,
        values=status_counts.values,
        hole=0.4,
        marker=dict(colors=[STATUS_COLORS.get(status, '#95a5a6') for status in status_counts.index]),
        textinfo='label+percent',
        textposition='outside',
        hovertemplate='<b>%{label}</b><br>Count: %{value:,}<br>Percentage: %{percent}<br><extra></extra>'
    )])
    
    fig.update_layout(
        title=dict(text="Loan Status Distribution", font=dict(size=20, color='#333'), x=0.5),
        template="plotly_white",
        height=400,
        annotations=[dict(text=f'{len(df):,}<br>Total', x=0.5, y=0.5, font_size=16, showarrow=False)]
    )
    
    return fig


def create_interest_rate_histogram(df: pd.DataFrame) -> go.Figure:
    """Tạo histogram cho Interest Rate theo Grade."""
    if 'int_rate' not in df.columns or 'grade' not in df.columns:
        return go.Figure()
    
    fig = px.histogram(
        df, x='int_rate', color='grade', nbins=50,
        title="Interest Rate Distribution by Grade",
        labels={'int_rate': 'Interest Rate', 'grade': 'Grade'},
        color_discrete_sequence=px.colors.qualitative.Set2,
        opacity=0.7
    )
    
    fig.update_layout(
        template="plotly_white", height=400,
        xaxis_title="Interest Rate", yaxis_title="Count",
        legend_title="Grade", barmode='overlay'
    )
    fig.update_xaxes(tickformat='.1%')
    
    return fig


def create_region_map(df: pd.DataFrame) -> go.Figure:
    """Tạo biểu đồ phân bố theo Region."""
    if 'region' not in df.columns:
        return go.Figure()
    
    region_data = df.groupby('region').agg({
        'loan_amount': ['sum', 'count'],
        'int_rate': 'mean'
    }).round(4)
    
    region_data.columns = ['Total_Volume', 'Count', 'Avg_Interest']
    region_data = region_data.reset_index()
    
    region_data['Avg_Interest_Pct'] = region_data['Avg_Interest'] * 100
    
    fig = px.treemap(
        region_data, path=['region'], values='Count', 
        color='Avg_Interest_Pct',
        color_continuous_scale='RdYlGn_r', 
        range_color=[5, 25],  
        title="Loan Distribution by Region",
        labels={'Avg_Interest_Pct': 'Avg Interest (%)'}
    )
    
    # Custom hover template
    fig.update_traces(
        hovertemplate='<b>%{label}</b><br>Count: %{value:,}<br>Avg Interest: %{color:.2f}%<extra></extra>'
    )
    
    fig.update_layout(template="plotly_white", height=400)
    return fig


def create_scatter_plot(df: pd.DataFrame) -> go.Figure:
    """Tạo scatter plot Income vs Loan Amount."""
    if 'annual_income' not in df.columns or 'loan_amount' not in df.columns:
        return go.Figure()
    
    sample_df = df.sample(n=min(1000, len(df)), random_state=42)
    
    fig = px.scatter(
        sample_df, x='annual_income', y='loan_amount',
        color='grade' if 'grade' in sample_df.columns else None,
        size='int_rate' if 'int_rate' in sample_df.columns else None,
        title="Annual Income vs Loan Amount",
        labels={'annual_income': 'Annual Income ($)', 'loan_amount': 'Loan Amount ($)', 'grade': 'Grade', 'int_rate': 'Interest Rate'},
        color_discrete_sequence=px.colors.qualitative.Set2,
        opacity=0.6
    )
    
    fig.update_layout(
        template="plotly_white", height=450,
        xaxis=dict(tickformat='$,.0f'),
        yaxis=dict(tickformat='$,.0f')
    )
    
    return fig


def create_rate_gauge(rate: float, color: str) -> go.Figure:
    """Tạo gauge chart cho Interest Rate prediction."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=rate,
        number={'suffix': '%', 'font': {'size': 40}},
        title={'text': "Predicted Interest Rate", 'font': {'size': 20}},
        gauge={
            'axis': {'range': [0, 30], 'tickwidth': 1, 'tickcolor': "darkgray"},
            'bar': {'color': color},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 8], 'color': 'rgba(56, 239, 125, 0.3)'},
                {'range': [8, 12], 'color': 'rgba(102, 126, 234, 0.3)'},
                {'range': [12, 16], 'color': 'rgba(254, 202, 87, 0.3)'},
                {'range': [16, 20], 'color': 'rgba(255, 159, 67, 0.3)'},
                {'range': [20, 30], 'color': 'rgba(245, 87, 108, 0.3)'}
            ],
            'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': rate}
        }
    ))
    
    fig.update_layout(height=300, margin=dict(l=20, r=20, t=50, b=20))
    return fig


def create_rate_comparison_chart(predicted_rate: float, grade: str) -> go.Figure:
    """Tạo biểu đồ so sánh lãi suất."""
    from config.settings import AVG_RATES_BY_GRADE
    
    grades = list(AVG_RATES_BY_GRADE.keys())
    avg_rates = list(AVG_RATES_BY_GRADE.values())
    
    colors_list = ['#38ef7d' if g == grade else '#667eea' for g in grades]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=grades, y=avg_rates, name='Average Rate by Grade',
        marker_color=colors_list,
        text=[f'{r:.1f}%' for r in avg_rates],
        textposition='outside'
    ))
    
    fig.add_hline(
        y=predicted_rate, line_dash="dash", line_color="#f5576c",
        annotation_text=f"Your Predicted Rate: {predicted_rate:.2f}%",
        annotation_position="top right"
    )
    
    fig.update_layout(
        title="Interest Rate Comparison by Credit Grade",
        xaxis_title="Credit Grade",
        yaxis_title="Interest Rate (%)",
        template="plotly_white",
        height=400,
        showlegend=False
    )
    
    return fig