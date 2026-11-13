"""
Home Page: Dataset Overview & Schema Documentation
HR Analytics & Employee Mobility Intelligence
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from pathlib import Path

from ui_utils import (
    apply_custom_css,
    render_hero,
    render_metric_card,
    render_sidebar_info,
    configure_plotly_layout,
    load_data
)

# Page Configuration
st.set_page_config(
    page_title="TalentPulse AI | Dataset & Overview",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply Modern Dark & Tailwind Styling
apply_custom_css()
render_sidebar_info()

# Load Data
df = load_data()

# Hero Banner
render_hero(
    badge_text="Data Intelligence & Schema Explorer",
    title="Employee Attrition & Mobility Intelligence",
    subtitle="A comprehensive HR analytics platform designed to analyze employee mobility patterns, uncover flight-risk drivers, and predict talent turnover using machine learning.",
    icon_class="fa-solid fa-database"
)

# Executive KPI Cards
col1, col2, col3, col4, col5 = st.columns(5)

total_records = len(df)
looking_count = (df['Target'] == 1).sum()
looking_rate = (looking_count / total_records) * 100
staying_count = (df['Target'] == 0).sum()
staying_rate = 100.0 - looking_rate
avg_exp = df['Experience'].mean()
unique_cities = df['City'].nunique()

with col1:
    render_metric_card(
        title="Total Records",
        value=f"{total_records:,}",
        subtitle="Cleaned candidate profiles",
        icon_class="fa-solid fa-users",
        color="indigo"
    )

with col2:
    render_metric_card(
        title="Flight Risk (Target=1)",
        value=f"{looking_rate:.1f}%",
        subtitle=f"{looking_count:,} seeking new jobs",
        icon_class="fa-solid fa-door-open",
        color="rose"
    )

with col3:
    render_metric_card(
        title="Retention (Target=0)",
        value=f"{staying_rate:.1f}%",
        subtitle=f"{staying_count:,} stable candidates",
        icon_class="fa-solid fa-shield-halved",
        color="emerald"
    )

with col4:
    render_metric_card(
        title="Avg. Experience",
        value=f"{avg_exp:.1f} yrs",
        subtitle="Industry experience",
        icon_class="fa-solid fa-briefcase",
        color="amber"
    )

with col5:
    render_metric_card(
        title="Geographic Footprint",
        value=f"{unique_cities} Cities",
        subtitle="Global candidate coverage",
        icon_class="fa-solid fa-city",
        color="cyan"
    )

st.markdown("<div class='my-4'></div>", unsafe_allow_html=True)

# Main Navigation Tabs
tab_schema, tab_explore, tab_stats, tab_arch = st.tabs([
    "📋 Column Dictionary & Schema",
    "🔍 Interactive Data Explorer",
    "📊 Statistical Summary",
    "⚙️ Pipeline & Data Architecture"
])

# ==========================================
# TAB 1: COLUMN DICTIONARY & SCHEMA
# ==========================================
with tab_schema:
    st.markdown("""
    <div class="mb-4">
        <h3 class="text-xl font-bold text-white mb-1">Dataset Field Descriptions</h3>
        <p class="text-slate-400 text-sm">
            Comprehensive business definitions, data types, scales, and domain values for all 14 features in <code>Cleaned_df.csv</code>.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Column specifications dictionary
    column_metadata = [
        {
            "name": "City",
            "type": "Categorical (Nominal)",
            "role": "Geographic Predictor",
            "description": "Unique code representing the candidate's resident city (e.g. city_103, city_40). Captures regional hiring hubs and labor supply.",
            "range": "123 unique cities (Top: city_103 with 4,355 rows)",
            "example": "city_103, city_21, city_16"
        },
        {
            "name": "City_development_index",
            "type": "Numerical (Continuous)",
            "role": "Economic Covariate",
            "description": "Standardized human development index (CDI) of the candidate's city. Measures urban infrastructure, economic opportunities, and quality of life.",
            "range": "0.448 to 0.949 (Mean: 0.829, Median: 0.903)",
            "example": "0.920 (Tier-1 hub) vs 0.624 (Developing)"
        },
        {
            "name": "Gender",
            "type": "Categorical (Nominal)",
            "role": "Demographic",
            "description": "Self-reported gender identification of the candidate. Cleaned and imputed from raw data.",
            "range": "3 categories",
            "example": "Male (90.2%), Female (8.5%), Other (1.3%)"
        },
        {
            "name": "Relevent_experience",
            "type": "Categorical (Binary)",
            "role": "Domain Expertise",
            "description": "Indicates whether the candidate has directly applicable professional work experience in software engineering and data disciplines.",
            "range": "Binary categories",
            "example": "'Has relevent experience' (72.0%), 'No relevent experience' (28.0%)"
        },
        {
            "name": "Enrolled_university",
            "type": "Categorical (Nominal)",
            "role": "Academic Commitment",
            "description": "Current enrollment status of the candidate in higher education university courses.",
            "range": "3 categories",
            "example": "'no_enrollment' (72.1%), 'Full time course' (19.6%), 'Part time course' (6.3%)"
        },
        {
            "name": "Education_level",
            "type": "Categorical (Ordinal)",
            "role": "Academic Attainment",
            "description": "Highest formal educational qualification completed by the candidate.",
            "range": "5 ordered tiers",
            "example": "Primary School < High School < Graduate (60.5%) < Masters (22.8%) < Phd (2.2%)"
        },
        {
            "name": "Major_discipline",
            "type": "Categorical (Nominal)",
            "role": "Specialization",
            "description": "Candidate's primary collegiate major / study focus area.",
            "range": "6 categories",
            "example": "STEM (87.6%), Humanities (4.1%), Other (2.3%), Business Degree (2.0%), Arts (1.5%), No Major (1.4%)"
        },
        {
            "name": "Experience",
            "type": "Numerical (Discrete)",
            "role": "Seniority",
            "description": "Cumulative total years of professional work experience. Cleaned from raw strings (where '<1' = 0 and '>20' = 21).",
            "range": "0 to 21 years (Mean: 9.9 years)",
            "example": "0, 1, 5, 10, 21"
        },
        {
            "name": "Company_size",
            "type": "Categorical (Ordinal)",
            "role": "Employer Scale",
            "description": "Total headcount scale of the candidate's current or most recent employer.",
            "range": "8 ordered buckets",
            "example": "<10, 10-49, 50-99, 100-500, 500-999, 1000-4999, 5000-9999, 10000+"
        },
        {
            "name": "Company_type",
            "type": "Categorical (Nominal)",
            "role": "Corporate Structure",
            "description": "Legal and operational structure of the candidate's organization.",
            "range": "6 categories",
            "example": "Pvt Ltd (75.4%), Funded Startup (7.7%), Public Sector (7.3%), Early Stage Startup (4.6%), NGO (4.0%), Other (0.9%)"
        },
        {
            "name": "Last_new_job",
            "type": "Categorical (Ordinal)",
            "role": "Job Hopping Behavior",
            "description": "Number of years elapsed since candidate's last corporate job switch or first appointment.",
            "range": "6 categories",
            "example": "'never' (12.8%), '1' (42.0%), '2' (15.2%), '3' (5.4%), '4' (5.4%), '>4' (17.1%)"
        },
        {
            "name": "Training_hours",
            "type": "Numerical (Continuous)",
            "role": "Skill Development",
            "description": "Total completed hours of company or curriculum training modules.",
            "range": "1 to 336 hours (Mean: 65.4 hrs, Median: 47 hrs)",
            "example": "36, 47, 100, 336"
        },
        {
            "name": "Career_Stage",
            "type": "Categorical (Ordinal)",
            "role": "Engineered Seniority Band",
            "description": "Binned seniority level computed during feature engineering: Fresher (0-1 yr), Junior (2-4 yrs), Mid-Level (5-9 yrs), Senior (10-15 yrs), Expert (16+ yrs).",
            "range": "5 ordered stages",
            "example": "Fresher (2.7%), Junior (8.8%), Mid-Level (22.0%), Senior (26.3%), Expert (40.2%)"
        },
        {
            "name": "Target",
            "type": "Binary (Target Variable)",
            "role": "Prediction Objective",
            "description": "Primary ground-truth flag indicating whether the candidate is actively seeking a new job or open to leaving current role.",
            "range": "0 or 1",
            "example": "0 = Likely to Stay / Retained (75.1%), 1 = Looking for Job Change (24.9%)"
        }
    ]

    # Filter controls
    col_search, col_filter_type = st.columns([3, 1])
    with col_search:
        search_query = st.text_input("🔍 Search column by name or description...", placeholder="e.g. Experience, Target, City...")
    with col_filter_type:
        filter_type = st.selectbox("Filter by Category", ["All", "Numerical", "Categorical", "Target Variable"])

    filtered_cols = column_metadata
    if search_query:
        filtered_cols = [
            c for c in filtered_cols 
            if search_query.lower() in c['name'].lower() or search_query.lower() in c['description'].lower()
        ]
    if filter_type == "Numerical":
        filtered_cols = [c for c in filtered_cols if "Numerical" in c['type']]
    elif filter_type == "Categorical":
        filtered_cols = [c for c in filtered_cols if "Categorical" in c['type']]
    elif filter_type == "Target Variable":
        filtered_cols = [c for c in filtered_cols if "Target" in c['type']]

    # Display Columns Cards
    for item in filtered_cols:
        is_target = "Target" in item['name']
        border_class = "border-rose-500/40 bg-rose-950/20" if is_target else "border-slate-800 bg-slate-900/50"
        badge_style = "badge-rose" if is_target else ("badge-cyan" if "Numerical" in item['type'] else "badge-indigo")

        card_html = f"""
        <div class="modern-card p-4 rounded-xl border {border_class} mb-3">
            <div class="flex flex-col md:flex-row md:items-center justify-between gap-2 mb-2">
                <div class="flex items-center gap-2.5">
                    <span class="font-mono text-base font-bold text-white">{item['name']}</span>
                    <span class="badge-pill {badge_style} text-[10px]">{item['type']}</span>
                    <span class="text-xs text-slate-400 font-medium">({item['role']})</span>
                </div>
                <div class="text-xs font-mono text-slate-400">
                    <span class="text-slate-400">Values:</span> <span class="text-indigo-300">{item['example']}</span>
                </div>
            </div>
            <p class="text-slate-300 text-sm mb-2 leading-relaxed">
                {item['description']}
            </p>
            <div class="text-xs text-slate-400 flex items-center gap-1.5">
                <i class="fa-solid fa-arrows-left-right text-[11px] text-slate-400"></i>
                <span><strong>Range / Domain:</strong> {item['range']}</span>
            </div>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)


# ==========================================
# TAB 2: INTERACTIVE DATA EXPLORER
# ==========================================
with tab_explore:
    st.markdown("""
    <div class="mb-4">
        <h3 class="text-xl font-bold text-white mb-1">Live Dataset Sample & Explorer</h3>
        <p class="text-slate-400 text-sm">
            Inspect raw rows, apply instant slice limits, or select specific feature subsets from <code>Cleaned_df.csv</code>.
        </p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 2, 1])
    with c1:
        row_limit = st.slider("Rows to Preview", min_value=5, max_value=100, value=15, step=5)
    with c2:
        selected_cols = st.multiselect("Select Feature Columns", options=df.columns.tolist(), default=df.columns.tolist())
    with c3:
        target_filter = st.selectbox("Filter by Target Status", ["All Candidates", "Looking for Job (1)", "Retained (0)"])

    preview_df = df[selected_cols]
    if target_filter == "Looking for Job (1)" and "Target" in preview_df.columns:
        preview_df = preview_df[preview_df["Target"] == 1]
    elif target_filter == "Retained (0)" and "Target" in preview_df.columns:
        preview_df = preview_df[preview_df["Target"] == 0]

    st.dataframe(preview_df.head(row_limit), use_container_width=True, height=450)

    # Dataset metadata pills
    st.markdown(f"""
    <div class="flex flex-wrap items-center gap-4 text-xs font-mono text-slate-400 pt-2">
        <span class="badge-pill badge-indigo">Shape: {df.shape[0]:,} Rows × {df.shape[1]} Columns</span>
        <span class="badge-pill badge-emerald">Missing Values: 0 (100% Imputed & Clean)</span>
        <span class="badge-pill badge-cyan">Memory Footprint: ~{df.memory_usage(deep=True).sum() / (1024**2):.2f} MB</span>
    </div>
    """, unsafe_allow_html=True)


# ==========================================
# TAB 3: STATISTICAL SUMMARY
# ==========================================
with tab_stats:
    st.markdown("""
    <div class="mb-4">
        <h3 class="text-xl font-bold text-white mb-1">Statistical Distributions & Profiles</h3>
        <p class="text-slate-400 text-sm">
            Parametric summaries for numerical variables and cardinalities for categorical factors.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<h4 class='text-sm font-semibold uppercase tracking-wider text-indigo-400 mb-2'>Numerical Features Summary</h4>", unsafe_allow_html=True)
    num_summary = df.describe().round(3).T
    num_summary = num_summary.rename(columns={
        "count": "Count", "mean": "Mean", "std": "Std Dev",
        "min": "Min", "25%": "Q1 (25%)", "50%": "Median (50%)",
        "75%": "Q3 (75%)", "max": "Max"
    })
    st.dataframe(num_summary, use_container_width=True)

    st.markdown("<h4 class='text-sm font-semibold uppercase tracking-wider text-indigo-400 mt-6 mb-2'>Categorical Features Cardinality & Top Modes</h4>", unsafe_allow_html=True)
    cat_cols = df.select_dtypes(include=['object']).columns.tolist()
    cat_summary = []
    for col in cat_cols:
        val_counts = df[col].value_counts()
        top_val = val_counts.index[0]
        top_pct = (val_counts.iloc[0] / len(df)) * 100
        cat_summary.append({
            "Feature Name": col,
            "Unique Categories": df[col].nunique(),
            "Dominant Category (Mode)": str(top_val),
            "Mode Frequency": f"{val_counts.iloc[0]:,} rows",
            "Mode Share": f"{top_pct:.1f}%"
        })
    cat_summary_df = pd.DataFrame(cat_summary)
    st.dataframe(cat_summary_df, use_container_width=True)


# ==========================================
# TAB 4: PIPELINE & DATA ARCHITECTURE
# ==========================================
with tab_arch:
    st.markdown("""
    <div class="modern-card">
        <h3 class="text-xl font-bold text-white mb-2">End-to-End Data Pipeline Architecture</h3>
        <p class="text-slate-300 text-sm mb-4 leading-relaxed">
            The dataset originated from HR employee records and underwent rigorous data cleaning, handling of missing values, ordinal encoding, and feature engineering to support production machine learning.
        </p>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mt-4">
            <div class="p-4 rounded-xl bg-slate-800/50 border border-slate-700/60">
                <div class="flex items-center gap-2 text-indigo-400 font-semibold mb-2">
                    <i class="fa-solid fa-broom"></i>
                    <span>1. Data Cleaning</span>
                </div>
                <ul class="text-xs text-slate-300 space-y-1.5 list-disc pl-4">
                    <li>Removed unique ID (<code>Enrollee_id</code>) to prevent data leakage.</li>
                    <li>Mapped strings like <code>&lt;1</code> to 0 and <code>&gt;20</code> to 21 in <code>Experience</code>.</li>
                    <li>Handled missing values in <code>Gender</code>, <code>Company_size</code>, and <code>Company_type</code> using mode imputation.</li>
                </ul>
            </div>

            <div class="p-4 rounded-xl bg-slate-800/50 border border-slate-700/60">
                <div class="flex items-center gap-2 text-emerald-400 font-semibold mb-2">
                    <i class="fa-solid fa-wand-magic-sparkles"></i>
                    <span>2. Feature Engineering</span>
                </div>
                <ul class="text-xs text-slate-300 space-y-1.5 list-disc pl-4">
                    <li>Derived <code>Career_Stage</code> categorizing years of experience into Fresher, Junior, Mid-Level, Senior, Expert.</li>
                    <li>Preserved natural ordering for <code>Education_level</code>, <code>Company_size</code>, and <code>Last_new_job</code>.</li>
                    <li>Maintained exact mapping of <code>City</code> to <code>City_development_index</code>.</li>
                </ul>
            </div>

            <div class="p-4 rounded-xl bg-slate-800/50 border border-slate-700/60">
                <div class="flex items-center gap-2 text-rose-400 font-semibold mb-2">
                    <i class="fa-solid fa-network-wired"></i>
                    <span>3. XGBoost Pipeline</span>
                </div>
                <ul class="text-xs text-slate-300 space-y-1.5 list-disc pl-4">
                    <li>StandardScaler & RobustScaler on continuous variables (CDI, Training Hours, Experience).</li>
                    <li>OrdinalEncoder on ordered categories; OneHotEncoder on nominal features.</li>
                    <li>XGBClassifier calibrated to predict probability of employee job searching.</li>
                </ul>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div class='my-6'></div>", unsafe_allow_html=True)

# Quick Action Cards (Footer Navigation)
st.markdown("""
<div class="grid grid-cols-1 md:grid-cols-2 gap-4">
    <div class="modern-card flex flex-col justify-between">
        <div>
            <div class="flex items-center gap-2 mb-2">
                <span class="badge-pill badge-indigo">
                    <i class="fa-solid fa-chart-pie text-xs"></i>
                    <span>Page 1</span>
                </span>
            </div>
            <h4 class="text-lg font-bold text-white mb-1">Exploratory Insights & Target Analysis</h4>
            <p class="text-slate-300 text-sm leading-relaxed mb-4">
                Explore non-technical visual charts dissecting how career stage, education, company size, and city economic tiers impact employee flight risk.
            </p>
        </div>
        <div class="text-xs text-indigo-400 font-semibold">
            👉 Navigate via Sidebar to: <strong>Analysis</strong>
        </div>
    </div>

    <div class="modern-card flex flex-col justify-between">
        <div>
            <div class="flex items-center gap-2 mb-2">
                <span class="badge-pill badge-emerald">
                    <i class="fa-solid fa-bullseye text-xs"></i>
                    <span>Page 2</span>
                </span>
            </div>
            <h4 class="text-lg font-bold text-white mb-1">Employee Attrition Prediction Model</h4>
            <p class="text-slate-300 text-sm leading-relaxed mb-4">
                Input any candidate profile to receive an immediate XGBoost probability score, flight risk tier, and tailored retention recommendations.
            </p>
        </div>
        <div class="text-xs text-emerald-400 font-semibold">
            👉 Navigate via Sidebar to: <strong>Employee attrition</strong>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
