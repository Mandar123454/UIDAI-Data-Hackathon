import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
import calendar
pio.templates.default = "plotly_dark"

def _style_fig(fig):
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#e5e7eb'
    )
    return fig


def load_and_prepare(csv_path: str, state_filter: str = 'Maharashtra'):
    df = pd.read_csv(csv_path)
    # Basic cleanup
    df.columns = [c.strip().lower() for c in df.columns]
    # Parse dates (assumed monthly granularity)
    # Handle mixed date formats with day-first common in Indian datasets
    df['date'] = pd.to_datetime(df['date'], dayfirst=True, format='mixed', errors='coerce')
    # Filter to state
    df = df[df['state'].str.strip().str.lower() == state_filter.lower()].copy()

    # Ensure numeric types
    for col in ['age_0_5', 'age_5_17', 'age_18_greater']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df['total_enrolments'] = df[['age_0_5', 'age_5_17', 'age_18_greater']].sum(axis=1)

    # Drop rows with missing key fields (including unparsable dates)
    df = df.dropna(subset=['date', 'district', 'pincode'])
    df['district'] = df['district'].astype(str).str.strip()
    df['pincode'] = df['pincode'].astype(str).str.strip()

    # Monthly aggregations for state level
    monthly = df.groupby('date').agg(
        age_0_5=('age_0_5', 'sum'),
        age_5_17=('age_5_17', 'sum'),
        age_18_greater=('age_18_greater', 'sum'),
        total=('total_enrolments', 'sum')
    ).sort_index()

    # District and pincode monthly aggregates
    district_monthly = df.groupby(['district', 'date']).agg(total=('total_enrolments', 'sum')).reset_index()
    pincode_monthly = df.groupby(['pincode', 'date']).agg(total=('total_enrolments', 'sum')).reset_index()

    # Month-of-year for seasonality
    monthly = monthly.copy()
    monthly['month'] = monthly.index.month

    return {
        'df': df,
        'monthly': monthly,
        'district_monthly': district_monthly,
        'pincode_monthly': pincode_monthly,
    }


def _seasonality_index(monthly: pd.DataFrame) -> pd.DataFrame:
    overall_avg = monthly['total'].mean() if len(monthly) else 0
    seasonal = monthly.groupby('month')['total'].mean() / overall_avg if overall_avg else monthly.groupby('month')['total'].mean()
    seasonal = seasonal.reset_index().rename(columns={'total': 'seasonal_index'})
    return seasonal


def _district_saturation_flags(district_monthly: pd.DataFrame) -> pd.DataFrame:
    # Compute last 3-month avg vs rolling 12-month max per district as saturation proxy
    dm = district_monthly.copy()
    dm = dm.sort_values(['district', 'date'])
    dm['rolling12_max'] = dm.groupby('district')['total'].transform(lambda s: s.rolling(12, min_periods=3).max())
    dm['rolling3_avg'] = dm.groupby('district')['total'].transform(lambda s: s.rolling(3, min_periods=3).mean())
    dm['saturation_index'] = dm['rolling3_avg'] / dm['rolling12_max']

    # Momentum vs volatility
    dm['rolling12_avg'] = dm.groupby('district')['total'].transform(lambda s: s.rolling(12, min_periods=6).mean())
    dm['std12'] = dm.groupby('district')['total'].transform(lambda s: s.rolling(12, min_periods=6).std())

    # Last snapshot per district
    last = dm.groupby('district').tail(1).copy()
    # Define flags
    last['low_momentum'] = (last['rolling3_avg'] < 0.5 * last['rolling12_avg']).fillna(False)
    # Volatility compared to state median of std12
    state_vol_threshold = dm['std12'].median()
    last['volatile'] = (last['std12'] > 1.5 * state_vol_threshold).fillna(False)
    last['saturation_risk'] = (last['saturation_index'] < 0.6).fillna(False)

    flags = last[['district', 'saturation_index', 'low_momentum', 'volatile', 'saturation_risk']]
    return flags.sort_values('saturation_index')


def _child_momentum(monthly: pd.DataFrame) -> pd.DataFrame:
    m = monthly.copy()
    m['child_total'] = m['age_0_5'] + m['age_5_17']
    m['child_share'] = (m['child_total'] / m['total']).replace([np.inf, -np.inf], np.nan)
    return m[['child_total', 'child_share']]


def build_figures(data: dict) -> dict:
    monthly = data['monthly']
    district_monthly = data['district_monthly']
    pincode_monthly = data['pincode_monthly']

    figs = {}

    # 1) State monthly total trend
    figs['total_trend'] = _style_fig(px.line(
        monthly.reset_index(), x='date', y='total',
        title='Monthly Aadhaar Enrolments - Maharashtra',
        markers=True
    ))

    # 2) Stacked area by age groups
    age_df = monthly.reset_index()[['date', 'age_0_5', 'age_5_17', 'age_18_greater']]
    figs['age_stacked'] = _style_fig(px.area(
        age_df, x='date', y=['age_0_5', 'age_5_17', 'age_18_greater'],
        title='Age Group Composition Over Time',
    ))

    # 3) District top/bottom by last 12-month total
    last_12_cutoff = monthly.index.max() - pd.DateOffset(months=11) if len(monthly) else None
    if last_12_cutoff is not None:
        recent = district_monthly[district_monthly['date'] >= last_12_cutoff]
    else:
        recent = district_monthly
    dist_totals = recent.groupby('district')['total'].sum().sort_values(ascending=False)
    top15 = dist_totals.head(15).reset_index()
    bottom15 = dist_totals.tail(15).reset_index()

    fig_db = make_subplots(rows=1, cols=2, subplot_titles=('Top Districts (12m)', 'Bottom Districts (12m)'))
    fig_db.add_trace(go.Bar(x=top15['district'], y=top15['total'], name='Top'), row=1, col=1)
    fig_db.add_trace(go.Bar(x=bottom15['district'], y=bottom15['total'], name='Bottom', marker_color='indianred'), row=1, col=2)
    fig_db.update_layout(title_text='District Enrolment Disparities (Last 12 Months)', showlegend=False)
    fig_db.update_xaxes(tickangle=45)
    figs['district_disparity'] = _style_fig(fig_db)

    # 4) Pincode monthly distribution (boxplot)
    figs['pincode_box'] = _style_fig(px.box(
        pincode_monthly, x='date', y='total', points='suspectedoutliers',
        title='Pincode Monthly Enrolment Distribution'
    ))

    # 5) Seasonality index by month-of-year
    seasonal = _seasonality_index(monthly)
    figs['seasonality_index'] = _style_fig(px.bar(
        seasonal, x='month', y='seasonal_index',
        title='Seasonality Index (Month-of-Year)',
    ))

    # 6) District risk flags summary
    flags = _district_saturation_flags(district_monthly)
    summary = {
        'Saturation Risk': int(flags['saturation_risk'].sum()),
        'Low Momentum': int(flags['low_momentum'].sum()),
        'Volatile': int(flags['volatile'].sum()),
    }
    figs['risk_summary'] = _style_fig(px.bar(
        x=list(summary.keys()), y=list(summary.values()),
        title='District Risk Flags Summary'
    ))

    # 7) Child enrolment momentum
    child = _child_momentum(monthly)
    child_fig = go.Figure()
    child_fig.add_trace(go.Scatter(x=monthly.index, y=child['child_share'], mode='lines+markers', name='Child Share'))
    child_fig.update_layout(title='Child Enrolment Share Over Time', yaxis_title='Share of Total')
    figs['child_momentum'] = _style_fig(child_fig)

    return figs


def generate_insights(data: dict) -> dict:
    monthly = data['monthly']
    district_monthly = data['district_monthly']
    pincode_monthly = data['pincode_monthly']

    insights = {}

    # Insights for total trend
    if len(monthly):
        total_change = (monthly['total'].iloc[-1] - monthly['total'].iloc[0]) / max(monthly['total'].iloc[0], 1)
        recent_growth = monthly['total'].pct_change().tail(3).mean()
        insights['total_trend'] = {
            'what': 'Monthly state-level Aadhaar enrolments over time',
            'findings': f'Overall change: {total_change:.1%}; recent avg MoM growth: {recent_growth:.1%}.',
            'why': 'Tracks momentum and helps plan outreach or capacity scaling.'
        }
    else:
        insights['total_trend'] = {
            'what': 'Monthly state-level Aadhaar enrolments over time',
            'findings': 'Insufficient data to compute trends.',
            'why': 'Trend monitoring guides operational planning.'
        }

    # Age dynamics
    age_shares = monthly[['age_0_5', 'age_5_17', 'age_18_greater']].sum()
    total_sum = monthly['total'].sum() if len(monthly) else 0
    if total_sum:
        shares_pct = (age_shares / total_sum).fillna(0)
        insights['age_stacked'] = {
            'what': 'Stacked area of age-group enrolments',
            'findings': f"Shares — 0–5: {shares_pct['age_0_5']:.1%}, 5–17: {shares_pct['age_5_17']:.1%}, 18+: {shares_pct['age_18_greater']:.1%}.",
            'why': 'Helps target initiatives for children, students, and adults.'
        }
    else:
        insights['age_stacked'] = {
            'what': 'Stacked area of age-group enrolments',
            'findings': 'No totals available to compute shares.',
            'why': 'Age mix guides segment-specific policy actions.'
        }

    # District disparities
    dist_totals = district_monthly.groupby('district')['total'].sum().sort_values(ascending=False)
    top_d = dist_totals.head(3)
    bottom_d = dist_totals.tail(3)
    insights['district_disparity'] = {
        'what': 'Top and bottom district enrolments (12 months)',
        'findings': f'Top: {", ".join([f"{i} ({int(v)})" for i, v in top_d.items()])}; Bottom: {", ".join([f"{i} ({int(v)})" for i, v in bottom_d.items()])}.',
        'why': 'Highlights areas for targeted support and resource allocation.'
    }

    # Pincode dispersion
    if len(pincode_monthly):
        dispersion = pincode_monthly.groupby('date')['total'].median().mean()
        insights['pincode_box'] = {
            'what': 'Monthly distribution of pincode-level enrolments',
            'findings': f'Central tendency (median across months): ~{int(dispersion)} enrolments per pincode.',
            'why': 'Assesses local capacity needs and variability.'
        }
    else:
        insights['pincode_box'] = {
            'what': 'Monthly distribution of pincode-level enrolments',
            'findings': 'No pincode-level observations available.',
            'why': 'Local variability informs micro-targeting.'
        }

    # Seasonality
    seasonal = _seasonality_index(monthly)
    if len(seasonal):
        top_months = seasonal.sort_values('seasonal_index', ascending=False).head(2)['month'].tolist()
        insights['seasonality_index'] = {
            'what': 'Month-of-year seasonal index of enrolments',
            'findings': f'Peak months: {", ".join(map(str, top_months))}; plan staffing and campaigns accordingly.',
            'why': 'Seasonal planning improves throughput and user experience.'
        }
    else:
        insights['seasonality_index'] = {
            'what': 'Month-of-year seasonal index of enrolments',
            'findings': 'Insufficient months to estimate seasonality.',
            'why': 'Seasonality informs timing for campaigns.'
        }

    # Risk flags summary
    flags = _district_saturation_flags(district_monthly)
    insights['risk_summary'] = {
        'what': 'Count of districts flagged for saturation, low momentum, and volatility',
        'findings': f"Saturation risk: {int(flags['saturation_risk'].sum())}; Low momentum: {int(flags['low_momentum'].sum())}; Volatile: {int(flags['volatile'].sum())}.",
        'why': 'Directs attention to underperforming or unstable areas.'
    }

    # Child momentum
    child = _child_momentum(monthly)
    if len(child):
        last_share = child['child_share'].tail(1).values[0]
        insights['child_momentum'] = {
            'what': 'Share of child enrolments in total over time',
            'findings': f'Latest child share: {last_share:.1%}. Monitor changes post school cycles.',
            'why': 'Guides child-focused outreach and school partnerships.'
        }
    else:
        insights['child_momentum'] = {
            'what': 'Share of child enrolments in total over time',
            'findings': 'Insufficient data for child share.',
            'why': 'Child enrolment is a UIDAI priority segment.'
        }

    return insights


def generate_recommendations(data: dict) -> list:
    monthly = data['monthly']
    district_monthly = data['district_monthly']
    flags = _district_saturation_flags(district_monthly)

    recs = []

    # 1) Child focus based on latest share
    child = _child_momentum(monthly)
    if len(child):
        last_share = child['child_share'].tail(1).values[0]
        recs.append(f"Prioritize biometric update infrastructure for children ({last_share:.1%} share).")
    else:
        recs.append("Prioritize child enrolment infrastructure; monitor child share trends.")

    # 2) Mobile units in low-performing districts (bottom 3 by recent 12-month total)
    last_12_cutoff = monthly.index.max() - pd.DateOffset(months=11) if len(monthly) else None
    recent = district_monthly if last_12_cutoff is None else district_monthly[district_monthly['date'] >= last_12_cutoff]
    dist_totals = recent.groupby('district')['total'].sum().sort_values(ascending=False)
    bottom3 = dist_totals.tail(3).index.tolist()
    if bottom3:
        recs.append("Deploy mobile enrolment units in low-performing districts (" + ", ".join(bottom3) + ").")
    else:
        recs.append("Deploy mobile units to low-performing areas identified by recent trends.")

    # 3) Align campaigns with seasonal peaks
    seasonal = _seasonality_index(monthly)
    if len(seasonal):
        top_months = seasonal.sort_values('seasonal_index', ascending=False).head(2)['month'].tolist()
        month_names = [calendar.month_name[m] for m in top_months]
        recs.append("Align outreach campaigns with seasonal peaks (" + " & ".join(month_names) + ").")
    else:
        recs.append("Align campaigns with observed seasonal peaks once sufficient data accrues.")

    # 4) Monitor volatile districts
    volatile_names = flags.loc[flags['volatile'] == True, 'district'].astype(str).head(3).tolist()
    if len(volatile_names):
        recs.append("Monitor volatile districts for operational instability (e.g., " + ", ".join(volatile_names) + ").")
    else:
        recs.append("Monitor districts exhibiting high variability for operational stability.")

    # 5) Focus on service quality in saturation-risk districts
    sat_count = int(flags['saturation_risk'].sum()) if 'saturation_risk' in flags.columns else 0
    recs.append(f"Shift focus from enrolment to service quality in saturated districts (approx. {sat_count} flagged).")

    return recs
