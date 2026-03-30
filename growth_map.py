import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import folium
from folium import Choropleth
from shapely.geometry import shape
import json
from streamlit.components.v1 import html
from datetime import datetime

# --- Page config ---
st.set_page_config(
    page_title="HGF Insights Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items=None
)

# Add this immediately after page_config
st.markdown("""
    <style>
    /* Hide all Streamlit branding and default elements */
    #MainMenu {visibility: hidden !important;}
    header {display: none !important;}
    footer {visibility: hidden !important;}
    .stDeployButton {display: none !important;}
    div.block-container {padding-top: 1rem;}
    [data-testid="stToolbar"] {display: none !important;}
    [data-testid="stDecoration"] {display: none !important;}
    [data-testid="stHeader"] {display: none !important;}
    .stApp header {display: none !important;}
    
    /* Updated color scheme to match the image */
    :root {
        --primary-color: #2F6D6A;  /* Green for headings */
        --accent-color: #2F6D6A;   /* Same green for accents */
        --background-color: #FAF7F2;  /* Beige background */
        --card-background: #FFFFFF;  /* Pure white for cards */
        --text-color: #2F6D6A;     /* Green for text */
    }
    
    .stApp {
        background-color: var(--background-color);
    }
    
    /* Title styling */
    h1 {
        color: var(--text-color) !important;
        font-family: "Georgia", serif !important;
        font-size: 2.5rem !important;
        font-weight: normal !important;
        padding-bottom: 2rem !important;
    }
    
    /* Section headers */
    .section-header {
        color: var(--accent-color);
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        font-size: 1.5rem;
        font-weight: 500;
        margin: 2rem 0 1rem 0;
    }
    
    /* KPI cards */
    .metric-card {
        background-color: var(--card-background);
        border-radius: 8px;
        padding: 1.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    
    .metric-label {
        color: var(--text-color);
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        font-size: 1rem;
        font-weight: 400;
        margin-bottom: 0.5rem;
    }
    
    .metric-value {
        color: var(--accent-color);
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        font-size: 2.5rem;
        font-weight: 500;
    }
    
    .metric-delta {
        color: #666;
        font-size: 0.9rem;
        margin-top: 0.25rem;
    }
    
    /* Filter section styling */
    .filter-section {
        background-color: white;
        border-radius: 8px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
    }
    
    .filter-label {
        color: #2F6D6A;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
    }
    
    /* Update Streamlit native elements */
    .stSelectbox label, .stSlider label {
        display: none !important;
    }

    .stSelectbox > div > div {
        background-color: transparent;
    }

    .stSlider > div > div {
        background-color: transparent;
    }
    
    /* Add this to remove any extra padding */
    .stMultiSelect, .stSlider {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }
    
    /* Style for the multiselect pills */
    .stMultiSelect [data-baseweb="tag"] {
        background-color: #2F6D6A !important;
        border-radius: 20px !important;
        padding: 5px 10px !important;
        color: white !important;
    }
    
    /* Style for the slider */
    .stSlider [data-baseweb="slider"] div {
        background-color: #2F6D6A !important;
    }
    
    .stSlider [data-baseweb="slider"] div[role="slider"] {
        background-color: #2F6D6A !important;
        border-color: #2F6D6A !important;
    }
    
    .stSlider [data-baseweb="slider"] div[role="progressbar"] {
        background-color: #2F6D6A !important;
    }
    
    /* Section headers with hamburger icon */
    .section-header-with-icon {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        color: #2F6D6A;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        font-size: 1.5rem;
        margin-bottom: 1rem;
    }
    
    .section-header-with-icon::before {
        content: "≡";
        color: #2F6D6A;
    }
    
    /* Slider styling updates */
    .stSlider {
        background-color: white;
        padding: 1rem 0;
    }
    
    /* Main track of the slider */
    .stSlider [data-baseweb="slider"] div[role="slider"] {
        background-color: #FF4B4B !important;
        border-color: #FF4B4B !important;
        box-shadow: none !important;
        height: 16px !important;
        width: 16px !important;
        margin-top: -7px !important;
    }
    
    /* Progress bar part */
    .stSlider [data-baseweb="slider"] div[role="progressbar"] {
        background-color: #FF4B4B !important;
        height: 4px !important;
    }
    
    /* Background track */
    .stSlider [data-baseweb="slider"] div {
        background-color: #E5E5E5 !important;
        height: 4px !important;
    }
    
    /* Remove any red focus outlines */
    .stSlider [data-baseweb="slider"] div[role="slider"]:focus {
        outline: none !important;
        box-shadow: none !important;
    }
    
    /* Slider label color */
    .stSlider label {
        color: #2F6D6A !important;
    }

    /* Enhanced slider styling */
    .stSlider [data-baseweb="slider"] {
        margin-top: 2rem;
    }
    
    /* Slider track */
    .stSlider [data-baseweb="slider"] div[role="slider"] {
        background-color: #2F6D6A !important;
        border-color: #2F6D6A !important;
        box-shadow: none !important;
    }
    
    /* Slider progress bar */
    .stSlider [data-baseweb="slider"] div[role="progressbar"] {
        background-color: #2F6D6A !important;
    }
    
    /* Slider background track */
    .stSlider [data-baseweb="slider"] div {
        background-color: #E5E0D8 !important;
    }

    /* Chat container styling */
    .chat-container {
        background-color: white;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
    }
    
    .chat-message {
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 8px;
    }
    
    .assistant-message {
        background-color: #f0f0f0;
    }
    
    .user-message {
        background-color: #2F6D6A;
        color: white;
        text-align: right;
    }

    /* Filter box container */
    .filter-box {
        background-color: white;
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    /* Filter box title */
    .filter-title {
        color: #1B3A4B;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        font-size: 1.5rem;
        font-weight: 400;
        margin-bottom: 1.5rem;
    }
    
    /* Multiselect styling */
    .stMultiSelect > div > div {
        background-color: white;
        border: none !important;
        box-shadow: none !important;
    }
    
    .stMultiSelect [data-baseweb="tag"] {
        background-color: #2F6D6A !important;
        border-radius: 25px !important;
        padding: 8px 16px !important;
        color: white !important;
        font-size: 1rem !important;
        font-weight: 400 !important;
        margin: 4px !important;
    }
    
    /* Slider styling */
    .stSlider > div > div {
        background-color: white;
    }
    
    .stSlider [data-baseweb="slider"] div[role="slider"] {
        background-color: #2F6D6A !important;
        border-color: #2F6D6A !important;
        width: 20px !important;
        height: 20px !important;
        border-radius: 50% !important;
        box-shadow: none !important;
        top: -8px !important;
    }
    
    .stSlider [data-baseweb="slider"] div[role="progressbar"] {
        background-color: #2F6D6A !important;
        height: 4px !important;
        border-radius: 2px !important;
    }
    
    .stSlider [data-baseweb="slider"] div {
        background-color: #E5E0D8 !important;
        height: 4px !important;
        border-radius: 2px !important;
    }
    
    /* Hide default labels */
    .stSlider label, .stMultiSelect label {
        display: none !important;
    }

    /* Value display for slider */
    .slider-value {
        color: #1B3A4B;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        font-size: 2rem;
        font-weight: 500;
        position: absolute;
        right: 2rem;
        top: 50%;
        transform: translateY(-50%);
    }

    /* Remove white boxes below Dashboard Filters */
    [data-testid="stVerticalBlock"] > [style*="flex-direction: column;"] > [data-testid="stVerticalBlock"] {
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }
    
    /* Ensure filter boxes have correct styling */
    .filter-box {
        background-color: white !important;
        border-radius: 16px !important;
        padding: 1.5rem !important;
        margin: 1rem 0 !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05) !important;
    }

    /* Target and remove the white boxes above filters */
    [data-testid="stVerticalBlock"] > div:has([data-baseweb="select"]) {
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding-top: 0 !important;
        margin-top: 0 !important;
    }

    /* Remove any extra padding from the multiselect container */
    .stMultiSelect > div:first-child {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }

    /* Remove extra space above slider */
    .stSlider > div:first-child {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }

    /* pull the Streamlit slider up inside its filter box */
    .filter-box .stSlider {
        margin-top: -0.75rem !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- Title Section ---
st.markdown('<div class="title-container">', unsafe_allow_html=True)
st.title("High-Growth Firm Insights Dashboard")
st.markdown('</div>', unsafe_allow_html=True)

# --- Load data with error handling ---
@st.cache_data
def load_data():
    try:
        with st.spinner('Loading dashboard data...'):
            df = pd.read_excel("romania_hgfs.xlsx")
            df["Topic List"] = df["Topics"].str.split(", ")
            return df
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        st.stop()

df = load_data()

# --- KPI Section ---
st.markdown('<div class="section-header-with-icon">Key Performance Indicators</div>', unsafe_allow_html=True)
total_firms = len(df)
avg_age = round(df['Company Age'].mean(), 1)
unique_topics = df['Topic List'].explode().nunique()

# Create KPI cards in columns
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Total Firms</div>
            <div class="metric-value">{}</div>
            <div class="metric-delta">Active Companies</div>
        </div>
    """.format(f"{total_firms:,}"), unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Average Company Age</div>
            <div class="metric-value">{} years</div>
            <div class="metric-delta">+{} years std dev</div>
        </div>
    """.format(f"{avg_age}", f"{round(df['Company Age'].std(), 1)}"), unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Industry Diversity</div>
            <div class="metric-value">{}</div>
            <div class="metric-delta">Unique Industries</div>
        </div>
    """.format(f"{unique_topics}"), unsafe_allow_html=True)

# --- Interactive Filters ---
st.markdown('<div class="section-header-with-icon">Dashboard Filters</div>', unsafe_allow_html=True)

# Create two columns for the filters
col1, col2 = st.columns(2)

with col1:
    # Region Selection Box (without white box wrapper)
    st.markdown('<div class="filter-title">Select Regions</div>', unsafe_allow_html=True)
    regions = st.multiselect(
        "",
        df["Region in country"].unique(),
        default=["Bucharest-Ilfov", "South-West Oltenia", "South-East"],
        label_visibility="collapsed"
    )

with col2:
    # Age Range Box (without white box wrapper)
    st.markdown('<div class="filter-title">Company Age Range</div>', unsafe_allow_html=True)
    age_range = st.slider(
        "",
        min_value=0,
        max_value=32,
        value=(0, 32),
        step=1,
        label_visibility="collapsed"
    )

# Filter the dataframe based on selections
df_filtered = df[
    (df["Region in country"].isin(regions)) &
    (df["Company Age"].between(age_range[0], age_range[1]))
]

# --- Regional Analysis ---
st.markdown('<div class="section-header">📍 Regional Analysis</div>', unsafe_allow_html=True)
region_counts = df_filtered["Region in country"].value_counts().reset_index()
region_counts.columns = ["Region", "Count"]

fig_region = px.bar(
    region_counts,
    x="Region", y="Count",
    color_discrete_sequence=["#E8ECF1"],  # Light gray bars
    title="Number of Firms by Region"
)

fig_region.update_layout(
    template="plotly_white",
    hoverlabel=dict(bgcolor="white"),
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    xaxis_title="Region",
    yaxis_title="Number of Companies",
    showlegend=False,
    height=500,
    font=dict(
        family="system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial",
        color="#1B3A4B"  # Using the actual color value instead of CSS variable
    )
)

fig_region.update_traces(marker_color="#2F6D6A")  # Change to green

st.plotly_chart(fig_region, use_container_width=True)

# --- Industry Analysis ---
st.markdown('<div class="section-header">🏷️ Industry Distribution</div>', unsafe_allow_html=True)

# Add a container for the filter with a title
st.markdown("""
    <div style='margin-bottom: 1rem;'>
        <div style='color: #2F6D6A; font-size: 1.1rem; font-weight: 500; margin-bottom: 0.5rem;'>
            Number of Top Industries to Display
        </div>
    </div>
""", unsafe_allow_html=True)

# Add number selector for top industries
num_industries = st.select_slider(
    "",  # Empty label since we're using custom HTML label above
    options=[5, 10, 15, 20, 25, "All"],
    value=10,
    key="industry_filter",
    label_visibility="collapsed"
)

topics_exploded = df_filtered.explode("Topic List")
topic_counts = topics_exploded["Topic List"].value_counts().reset_index()
topic_counts.columns = ["Industry", "Count"]

# Filter for top N industries if not "All"
if num_industries != "All":
    topic_counts = topic_counts.head(num_industries)

fig_topics = px.bar(
    topic_counts,
    x="Industry", y="Count",
    color_discrete_sequence=["#2F6D6A"],
    title=f"Top {num_industries} Industries by Number of Firms" if num_industries != "All" else "All Industries by Number of Firms"
)

fig_topics.update_layout(
    template="plotly_white",
    hoverlabel=dict(bgcolor="white"),
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    xaxis=dict(
        title="Industry",
        showgrid=False,
        tickangle=45,
        tickfont=dict(size=10),
        categoryorder='total descending'
    ),
    yaxis=dict(
        title="Number of Companies",
        showgrid=True,
        gridcolor='rgba(0,0,0,0.1)',
        gridwidth=1,
        zeroline=True,
        zerolinecolor='rgba(0,0,0,0.1)',
        zerolinewidth=1,
        dtick=5
    ),
    showlegend=False,
    height=500,
    margin=dict(b=150),
    font=dict(
        family="system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial",
        color="#1B3A4B"
    )
)

# Add y-axis line
fig_topics.update_xaxes(showline=True, linewidth=1, linecolor='rgba(0,0,0,0.1)', mirror=True)
fig_topics.update_yaxes(showline=True, linewidth=1, linecolor='rgba(0,0,0,0.1)', mirror=True)

st.plotly_chart(fig_topics, use_container_width=True)

# --- Growth Analysis ---
st.markdown('<div class="section-header">📊 Growth Analysis</div>', unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    # Growth by Region
    growth_region = df_filtered.groupby("Region in country")["avg_growth_3yr_pct"].mean().reset_index()
    growth_region = growth_region.sort_values(by="avg_growth_3yr_pct", ascending=False)
    
    fig_growth_region = go.Figure()
    
    # Add the horizontal lines
    for idx, row in growth_region.iterrows():
        fig_growth_region.add_trace(go.Scatter(
            x=[0, row["avg_growth_3yr_pct"]],  # Line from 0 to the value
            y=[row["Region in country"], row["Region in country"]],  # Same y for straight line
            mode='lines',
            line=dict(color='#2F6D6A', width=2),
            hoverinfo='skip',
            showlegend=False
        ))
    
    # Add the dots at the end of lines
    fig_growth_region.add_trace(go.Scatter(
        x=growth_region["avg_growth_3yr_pct"],
        y=growth_region["Region in country"],
        mode='markers+text',
        marker=dict(color='#2F6D6A', size=10),
        text=growth_region["avg_growth_3yr_pct"].apply(lambda x: f"{x:.1f}%"),
        textposition='middle right',
        textfont=dict(color='black', size=12),
        hoverinfo='skip',
        showlegend=False
    ))
    
    # Update layout
    fig_growth_region.update_layout(
        title={
            'text': "Average 3-Year Growth % by Region",
            'y':0.95,
            'x':0,
            'xanchor': 'left',
            'yanchor': 'top',
        },
        template="plotly_white",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=300,
        margin=dict(l=10, r=100, t=30, b=50),  # Increased bottom margin
        xaxis=dict(
            title="avg_growth_3yr_pct",
            showgrid=True,
            gridcolor='rgba(0,0,0,0.1)',
            zeroline=True,
            zerolinecolor='rgba(0,0,0,0.1)',
            showline=True,
            linecolor='rgba(0,0,0,0.1)',
            range=[0, max(growth_region["avg_growth_3yr_pct"]) * 1.3],
            showticklabels=True,
            dtick=10  # Show ticks every 10 units
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(0,0,0,0.1)',
            zeroline=True,
            zerolinecolor='rgba(0,0,0,0.1)',
            showline=True,
            linecolor='rgba(0,0,0,0.1)'
        ),
        font=dict(
            family="system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial",
            color="#1B3A4B"
        )
    )
    
    # Add axis lines
    fig_growth_region.update_xaxes(showline=True, linewidth=1, linecolor='rgba(0,0,0,0.1)', mirror=True)
    fig_growth_region.update_yaxes(showline=True, linewidth=1, linecolor='rgba(0,0,0,0.1)', mirror=True)
    
    st.plotly_chart(fig_growth_region, use_container_width=True)

with col2:
    # Age vs Growth Scatter
    fig_scatter = px.scatter(
        df_filtered,
        x="Company Age",
        y="avg_growth_3yr_pct",
        title="Age vs. 3-Year Average Growth %",
        color_discrete_sequence=["#2F6D6A"],
        labels={"Growth Segment": "HGF"}  # Change legend label to HGF
    )
    
    fig_scatter.update_traces(
        marker=dict(size=8, color="#2F6D6A"),
        hovertemplate="<b>Age:</b> %{x}<br>" +
                      "<b>Growth:</b> %{y:.1f}%<br>" +
                      "<extra></extra>"
    )
    
    fig_scatter.update_layout(
        template="plotly_white",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=300,
        margin=dict(l=50, r=50, t=30, b=50),
        showlegend=True,
        legend_title_text="Growth Segment",
        xaxis=dict(
            title="Company Age",
            showgrid=True,
            gridcolor='rgba(0,0,0,0.1)',
            zeroline=False,
            range=[0, 40],
            dtick=10  # Set major grid lines every 10 units
        ),
        yaxis=dict(
            title="3-Year Average Growth %",
            showgrid=True,
            gridcolor='rgba(0,0,0,0.1)',
            zeroline=False,
            range=[0, 100],
            dtick=20  # Set major grid lines every 20 units
        ),
        font=dict(
            family="system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial",
            color="#1B3A4B"
        )
    )
    
    st.plotly_chart(fig_scatter, use_container_width=True)

# --- Revenue & Profit Analysis ---
st.markdown('<div class="section-header">💶 Revenue & Profit Analysis</div>', unsafe_allow_html=True)

df_rev = pd.read_excel("romania_hgfs.xlsx")
df_rev = df_rev.rename(columns={
    'NACE Rev. 2 main section': 'Industry',
    'Region in country clean': 'Region',
    'Revenue (in euro)': 'Revenue',
    'Profit (in euro)': 'Profit'
})
df_rev['Revenue'] = pd.to_numeric(df_rev['Revenue'], errors='coerce')
df_rev['Profit'] = pd.to_numeric(df_rev['Profit'], errors='coerce')
df_rev = df_rev.dropna(subset=['Industry', 'Region', 'Revenue', 'Profit'])

agg = df_rev.groupby(['Region', 'Industry'], as_index=False).agg({
    'Revenue': 'sum',
    'Profit': 'sum'
})
agg['Profit Margin'] = agg['Profit'] / agg['Revenue']

# --- Scatter Plot: Revenue vs. Profit ---
st.subheader("Revenue vs. Profit by Region and Industry")
fig_scatter = px.scatter(
    agg,
    x='Revenue',
    y='Profit',
    color='Region',
    hover_data=['Industry', 'Profit Margin'],
    labels={'Revenue': 'Total Revenue (€)', 'Profit': 'Total Profit (€)'},
    title='Revenue vs. Profit by Region and Industry'
)
fig_scatter.update_layout(
    plot_bgcolor='#FAF7F2',
    paper_bgcolor='#FAF7F2',
    font=dict(color="#1B3A4B"),
)
st.plotly_chart(fig_scatter, use_container_width=True)

# --- Pareto Chart: Cumulative Revenue ---
st.subheader("Pareto Chart of Revenue by Region and Industry")

# Slider for top N industries
top_n_options = [5, 10, 15, 20, 25, "All"]
top_n = st.select_slider(
    "Number of Top Region-Industry Pairs to Display",
    options=top_n_options,
    value=10,
    key="pareto_top_n"
)

pareto = agg.sort_values('Revenue', ascending=False).reset_index(drop=True)
pareto['CumRevenue'] = pareto['Revenue'].cumsum()
pareto['CumPerc'] = 100 * pareto['CumRevenue'] / pareto['Revenue'].sum()
pareto['Label'] = pareto['Region'] + " - " + pareto['Industry']

# Filter for top N if not "All"
if top_n != "All":
    pareto = pareto.head(top_n)

fig_pareto = go.Figure()
fig_pareto.add_trace(go.Bar(
    x=pareto['Label'],
    y=pareto['Revenue'],
    name='Revenue (€)',
    marker_color='#2F6D6A',
    yaxis='y1'
))
fig_pareto.add_trace(go.Scatter(
    x=pareto['Label'],
    y=pareto['CumPerc'],
    name='Cumulative Revenue (%)',
    yaxis='y2',
    mode='lines+markers',
    marker=dict(color='#FF4B4B')
))
fig_pareto.update_layout(
    plot_bgcolor='#FAF7F2',
    paper_bgcolor='#FAF7F2',
    font=dict(color="#1B3A4B"),
    xaxis=dict(
        tickangle=45,
        tickmode='array',
        tickvals=pareto['Label'],
        ticktext=pareto['Label'],
        showgrid=False
    ),
    yaxis=dict(
        title='Revenue (€)',
        showgrid=True,
        gridcolor='rgba(0,0,0,0.1)'
    ),
    yaxis2=dict(
        title='Cumulative Revenue (%)',
        overlaying='y',
        side='right',
        range=[0, 110]
    ),
    legend=dict(x=0.01, y=0.99),
    title='Pareto Chart of Revenue by Region and Industry',
    margin=dict(b=150),
    height=500
)
st.plotly_chart(fig_pareto, use_container_width=True)

# --- Geographic Distribution ---
st.markdown('<div class="section-header">🗺️ Geographic Distribution</div>', unsafe_allow_html=True)

# Create region name mapping
region_name_map = {
    "North-West": "Nord-Vest",
    "Center": "Centru",
    "North-East": "Nord-Est",
    "South-East": "Sud-Est",
    "South-Muntenia": "Sud-Muntenia",
    "Bucharest-Ilfov": "Bucureşti-Ilfov",
    "South-West Oltenia": "Sud-Vest Oltenia",
    "West": "Vest"
}

# Prepare region counts
region_counts = df_filtered["Region in country clean"].value_counts().reset_index()
region_counts.columns = ["Region", "Company Count"]
region_counts["NUTS_Region"] = region_counts["Region"].map(region_name_map)

# Load GeoJSON data
with open("NUTS_RG_20M_2021_4326_LEVL_2.geojson", "r", encoding="utf-8") as f:
    nuts2_geojson = json.load(f)

# Filter for Romanian regions
romania_nuts2 = [
    feature for feature in nuts2_geojson['features']
    if feature['properties'].get('CNTR_CODE') == 'RO'
]

# Create NUTS ID mapping
nuts_id_map = {
    feature['properties']['NAME_LATN']: feature['properties']['NUTS_ID']
    for feature in romania_nuts2
    if 'NAME_LATN' in feature['properties'] and 'NUTS_ID' in feature['properties']
}

region_counts["NUTS_ID"] = region_counts["NUTS_Region"].map(nuts_id_map)

# Create the map
m = folium.Map(
    location=[45.9432, 24.9668],
    zoom_start=6,
    tiles='CartoDB positron'
)

# Add choropleth layer with corrected styling
folium.Choropleth(
    geo_data={"type": "FeatureCollection", "features": romania_nuts2},
    name="Company Distribution",
    data=region_counts,
    columns=["NUTS_ID", "Company Count"],
    key_on="feature.properties.NUTS_ID",
    fill_color='Greens',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name="Number of Companies",
    smooth_factor=0,
    highlight=True,
    nan_fill_color='#FAF7F2',
    nan_fill_opacity=0.4,
    line_color='white',
    line_weight=2,
    overlay=True,
    show=True
).add_to(m)

# Add circle markers
for _, row in region_counts.iterrows():
    region = row["NUTS_Region"]
    count = row["Company Count"]
    nuts_id = row["NUTS_ID"]
    for feature in romania_nuts2:
        if feature['properties']['NUTS_ID'] == nuts_id:
            geom = shape(feature['geometry'])
            centroid = geom.centroid
            folium.CircleMarker(
                location=[centroid.y, centroid.x],
                radius=8,
                popup=f"<b>{region}</b><br>{count} companies",
                color='#2F6D6A',
                fill=True,
                fill_color='#2F6D6A',
                fill_opacity=0.9,
                weight=2
            ).add_to(m)
            break

# Display the map
st.components.v1.html(m._repr_html_(), height=500)

# --- FAQ Section ---
st.markdown('<div class="section-header">💬 FAQs</div>', unsafe_allow_html=True)

# Welcome message
st.markdown("""
    <div class="chat-message assistant-message">
        Hi! I'm here to help you understand the dashboard better. Please select a question below:
    </div>
""", unsafe_allow_html=True)

# Predefined FAQ dictionary
faqs = {
    "What exactly is a 'High-Growth Firm' and how did you decide which companies qualify?": 
        "In this dashboard, a High-Growth Firm (HGF) is defined based only on employment growth. Here's what qualifies a company as 'high-growth' in our dataset:\n\n"
        "• Consistent Employee Growth: The company must have increased its number of employees by more than 20% every year, for three years in a row.\n\n"
        "• Minimum Size: Only firms that had at least 10 employees at the start of that growth period are included. This avoids counting very small or volatile businesses and ensures we're looking at sustainable job creators.",

    "Take me through the dashboard": 
        "Welcome to the High-Growth Firm Insights Dashboard! Let's walk you through it.\n\n"
        "Start with the KPIs (Top Summary Cards):\n"
        "• Total Firms: Shows how many companies meet the high-growth criteria.\n"
        "• Average Company Age: Gives a feel for how mature these firms are.\n"
        "• Industry Diversity: Tells you how many different sectors these high-growth firms span.\n\n"
        "Customise with Filters:\n"
        "• Region Selector: Click on one or more regions to narrow your view.\n"
        "• Company Age Range: Use the slider to explore younger or older high-growth firms.\n\n"
        "Growth Analysis:\n"
        "• Average 3-Year Growth by Region: See how strong the growth is in each selected region.\n"
        "• Scatter Plot (Age vs. Growth %): Each dot is a company, showing if older or younger firms tend to grow faster.\n\n"
        "Explore Industry Distribution and Geographic Map for more insights into sector patterns and regional concentration.",

    "How is the 'Average 3-Year Growth %' calculated?": 
        "This metric shows how fast the companies in a region have been growing in terms of employment over the past three years—on average. Here's how it works:\n\n"
        "• For each firm, we look at the number of employees at the start and end of the 3-year period.\n"
        "• We calculate that firm's annual growth rate using a standard formula.\n"
        "• Once we have the annual growth rates for all qualifying firms, we calculate the average across firms in that region.",

    "What does the 'Industry Diversity' metric actually measure?": 
        "The Industry Diversity metric tells you how many different industries are represented among the high-growth firms in the dashboard. It counts the number of unique industry classifications (typically based on NACE Rev. 2 codes) that appear in the dataset. This gives you a sense of how broadly spread high-growth activity is across the economy—not just concentrated in one or two sectors.",

    "Are private and public companies treated differently in the metrics?": 
        "No—in this dashboard, private and public companies are treated the same when calculating all metrics. This ensures a fair and consistent view of where high-growth employment is happening, regardless of ownership model.",

    "Why do older companies sometimes have lower growth rates in the graph?": 
        "There are several reasons:\n\n"
        "• Law of Large Numbers: Older firms are usually larger, so adding 20% more employees means hiring dozens or hundreds of people.\n"
        "• Stabilization Over Time: Mature companies tend to stabilize as they find their niche and optimize operations.\n"
        "• Growth Constraints: Older firms may face more bureaucracy, market saturation, or structural limitations that make high-percentage growth harder to sustain.",

    "How is 'Industry Diversity' different from 'Industry Distribution'?": 
        "Industry Diversity refers to the number of different industries represented among high-growth firms, showing how broadly spread growth is across the economy. In contrast, Industry Distribution shows how many firms belong to each industry, highlighting which sectors dominate in terms of high-growth activity. While diversity tells us about variety, distribution reveals the concentration of firms within specific sectors.",

    "Why are some industries more represented than others?": 
        "Some industries are more represented among high-growth firms because they naturally offer more room for rapid scaling, have lower entry barriers, or are aligned with economic trends and local advantages. For example, sectors like construction, manufacturing, and IT services often dominate because they respond to high demand, benefit from infrastructure or EU funding, and can add employees quickly as projects scale. Industries like public administration or utilities tend to grow more slowly due to regulation, capital intensity, or limited market flexibility."
}

# Question selector
selected_question = st.selectbox(
    "Choose your question:",
    options=list(faqs.keys()),
    key="faq_selector"
)

# Display answer when question is selected (without the green user-message box)
if selected_question:
    st.markdown(f"""
        <div class="chat-message assistant-message">
            {faqs[selected_question]}
        </div>
    """, unsafe_allow_html=True)

# --- Footer (simplified) ---
st.markdown("""
    <div style='text-align: center; padding: 2rem; color: #666;'>
        <p>Dashboard last updated: {}</p>
    </div>
""".format(pd.Timestamp.now().strftime("%Y-%m-%d")), unsafe_allow_html=True)
