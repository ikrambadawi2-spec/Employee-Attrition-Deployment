"""
Analysis Page: Plain-English Workforce Insights & Attrition Drivers
HR Analytics & Employee Mobility Intelligence
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
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
    page_title="TalentPulse AI | Workforce Insights & Analysis",
    page_icon="📊",
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
    badge_text="Executive Analysis & Insights",
    title="Workforce Attrition & Mobility Drivers",
    subtitle="Plain-language visual analytics uncovering why employees look for new opportunities and how organizations can retain top talent.",
    icon_class="fa-solid fa-chart-pie"
)

# Top Summary KPI Cards
c1, c2, c3, c4 = st.columns(4)

total_records = len(df)
looking_rate = (df['Target'] == 1).mean() * 100
fresher_risk = df[df['Career_Stage'] == 'Fresher']['Target'].mean() * 100
expert_risk = df[df['Career_Stage'] == 'Expert']['Target'].mean() * 100
student_risk = df[df['Enrolled_university'] == 'Full time course']['Target'].mean() * 100

with c1:
    render_metric_card(
        title="Baseline Flight Intent",
        value=f"{looking_rate:.1f}%",
        subtitle="~1 in 4 candidates seeking new job",
        icon_class="fa-solid fa-person-walking-dashed-line-arrow-right",
        color="rose"
    )

with c2:
    render_metric_card(
        title="Fresher Risk (0-1 yr)",
        value=f"{fresher_risk:.1f}%",
        subtitle="Highest flight risk career tier",
        icon_class="fa-solid fa-seedling",
        color="amber"
    )

with c3:
    render_metric_card(
        title="Expert Retention (16+ yrs)",
        value=f"{(100 - expert_risk):.1f}%",
        subtitle="Most loyal workforce cohort",
        icon_class="fa-solid fa-award",
        color="emerald"
    )

with c4:
    render_metric_card(
        title="Full-Time Student Churn",
        value=f"{student_risk:.1f}%",
        subtitle="Upskilling candidates seeking transition",
        icon_class="fa-solid fa-graduation-cap",
        color="cyan"
    )

st.markdown("<div class='my-4'></div>", unsafe_allow_html=True)

# Executive Summary Callout Box
st.markdown("""
<div class="modern-card border-indigo-500/30 bg-indigo-950/20 mb-6">
    <div class="flex items-start gap-3">
        <div class="w-9 h-9 rounded-lg bg-indigo-500/20 border border-indigo-500/30 flex items-center justify-center text-indigo-400 shrink-0 mt-0.5">
            <i class="fa-solid fa-lightbulb"></i>
        </div>
        <div>
            <h4 class="text-base font-bold text-white mb-1">Executive Summary for HR Leaders</h4>
            <p class="text-slate-300 text-sm leading-relaxed">
                Analysis of <strong>19,044 candidate profiles</strong> reveals that employee turnover intent is heavily concentrated in 
                <strong>early-career professionals (0-3 years)</strong>, employees pursuing <strong>full-time university degrees</strong>, and candidates residing in 
                <strong>developing economic regions</strong>. Conversely, employees with 15+ years of tenure, individuals working in funded startups, and those in tier-1 tech cities exhibit exceptional stability.
            </p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# SECTION 1: MACRO ATTRITION OVERVIEW & CAREER STAGE
st.markdown("<h3 class='text-xl font-bold text-white mb-3 flex items-center gap-2'><i class='fa-solid fa-chart-simple text-indigo-400 text-lg'></i> 1. Overall Workforce Intent & Career Seniority</h3>", unsafe_allow_html=True)

row1_col1, row1_col2 = st.columns([1, 1])

with row1_col1:
    # Donut Chart for Target Distribution
    target_counts = df['Target'].value_counts().reset_index()
    target_counts.columns = ['Status', 'Count']
    target_counts['Label'] = target_counts['Status'].map({0: 'Likely to Stay (75.1%)', 1: 'Seeking New Job (24.9%)'})
    
    fig_target = px.pie(
        target_counts,
        names='Label',
        values='Count',
        color='Label',
        color_discrete_map={
            'Likely to Stay (75.1%)': '#10B981',
            'Seeking New Job (24.9%)': '#F43F5E'
        },
        hole=0.55
    )
    fig_target.update_traces(
        textposition='outside',
        textinfo='label+percent',
        marker=dict(line=dict(color='#0B0F19', width=2))
    )
    configure_plotly_layout(fig_target, title="Overall Workforce Mobility Intent", height=340)
    st.plotly_chart(fig_target, use_container_width=True)

with row1_col2:
    # Career Stage Flight Risk Bar Chart
    stage_order = ['Fresher', 'Junior', 'Mid-Level', 'Senior', 'Expert']
    stage_stats = df.groupby('Career_Stage')['Target'].agg(['count', 'mean']).reindex(stage_order).reset_index()
    stage_stats['Attrition_Pct'] = (stage_stats['mean'] * 100).round(1)
    
    fig_stage = px.bar(
        stage_stats,
        x='Attrition_Pct',
        y='Career_Stage',
        orientation='h',
        text='Attrition_Pct',
        color='Attrition_Pct',
        color_continuous_scale=['#10B981', '#F59E0B', '#F43F5E'],
        labels={'Attrition_Pct': 'Flight Risk (%)', 'Career_Stage': 'Career Stage'}
    )
    fig_stage.update_traces(
        texttemplate='%{text:.1f}%',
        textposition='inside',
        marker_line_color='rgba(255,255,255,0.1)',
        marker_line_width=1
    )
    fig_stage.update_coloraxes(showscale=False)
    configure_plotly_layout(fig_stage, title="Flight Risk by Career Stage (% Seeking Job)", height=340)
    st.plotly_chart(fig_stage, use_container_width=True)

# Non-technical explanation card for Section 1
st.markdown("""
<div class="p-3.5 rounded-xl bg-slate-900/60 border border-slate-800 text-xs text-slate-300 mb-6 flex items-start gap-2.5">
    <i class="fa-solid fa-circle-info text-indigo-400 mt-0.5"></i>
    <div>
        <strong class="text-white">Why Career Stage Matters:</strong>
        Freshers (45.3%) and Juniors (36.1%) switch jobs at more than double the rate of seasoned Experts (16.9%). Early career talent seeks accelerated promotions, salary jumps, and mentorship. Retention programs should prioritize early talent with structured 6-month milestone check-ins.
    </div>
</div>
""", unsafe_allow_html=True)


# SECTION 2: EXPERIENCE CURVE & RELEVANT BACKGROUND
st.markdown("<h3 class='text-xl font-bold text-white mb-3 flex items-center gap-2'><i class='fa-solid fa-user-graduate text-emerald-400 text-lg'></i> 2. Experience Depth & Academic Commitments</h3>", unsafe_allow_html=True)

row2_col1, row2_col2 = st.columns([1, 1])

with row2_col1:
    # Attrition by Years of Experience (Line Chart)
    exp_stats = df.groupby('Experience')['Target'].agg(['count', 'mean']).reset_index()
    exp_stats['Flight_Risk_Pct'] = exp_stats['mean'] * 100
    
    fig_exp = px.line(
        exp_stats,
        x='Experience',
        y='Flight_Risk_Risk' if 'Flight_Risk_Risk' in exp_stats else 'Flight_Risk_Pct',
        markers=True,
        labels={'Experience': 'Total Years of Work Experience', 'Flight_Risk_Pct': 'Flight Risk (%)'},
    )
    fig_exp.update_traces(
        line=dict(color='#818CF8', width=3),
        marker=dict(size=7, color='#6366F1', line=dict(color='#FFFFFF', width=1.5))
    )
    configure_plotly_layout(fig_exp, title="Turnover Probability Across Years of Experience", height=340)
    st.plotly_chart(fig_exp, use_container_width=True)

with row2_col2:
    # Attrition by University Enrollment
    enroll_map = {
        'no_enrollment': 'No Studies (Working Full-Time)',
        'Full time course': 'Enrolled Full-Time',
        'Part time course': 'Enrolled Part-Time'
    }
    df_temp = df.copy()
    df_temp['Enroll_Label'] = df_temp['Enrolled_university'].map(enroll_map)
    enroll_stats = df_temp.groupby('Enroll_Label')['Target'].agg(['count', 'mean']).reset_index()
    enroll_stats['Flight_Risk_Pct'] = (enroll_stats['mean'] * 100).round(1)
    enroll_stats = enroll_stats.sort_values('Flight_Risk_Pct', ascending=True)

    fig_enroll = px.bar(
        enroll_stats,
        x='Flight_Risk_Pct',
        y='Enroll_Label',
        orientation='h',
        text='Flight_Risk_Pct',
        color='Flight_Risk_Pct',
        color_continuous_scale=['#10B981', '#F59E0B', '#F43F5E'],
        labels={'Flight_Risk_Pct': 'Flight Risk (%)', 'Enroll_Label': 'Current University Status'}
    )
    fig_enroll.update_traces(
        texttemplate='%{text:.1f}%',
        textposition='outside',
        marker_line_color='rgba(255,255,255,0.1)'
    )
    fig_enroll.update_coloraxes(showscale=False)
    configure_plotly_layout(fig_enroll, title="Impact of University Enrollment on Mobility", height=340)
    st.plotly_chart(fig_enroll, use_container_width=True)

st.markdown("""
<div class="p-3.5 rounded-xl bg-slate-900/60 border border-slate-800 text-xs text-slate-300 mb-6 flex items-start gap-2.5">
    <i class="fa-solid fa-circle-info text-emerald-400 mt-0.5"></i>
    <div>
        <strong class="text-white">Academic Commitment Insight:</strong>
        Employees actively enrolled in full-time academic programs show a high flight intent (38.0%). They are typically upskilling with the explicit intent of transitioning into higher-paying data/engineering roles upon graduation. Offering clear internal transfer pathways retains this upgraded talent.
    </div>
</div>
""", unsafe_allow_html=True)


# SECTION 3: WORKPLACE ENVIRONMENT & COMPANY TYPE
st.markdown("<h3 class='text-xl font-bold text-white mb-3 flex items-center gap-2'><i class='fa-solid fa-building text-amber-400 text-lg'></i> 3. Company Ecosystem & Employer Scale</h3>", unsafe_allow_html=True)

row3_col1, row3_col2 = st.columns([1, 1])

with row3_col1:
    # Turnover by Company Type
    ctype_stats = df.groupby('Company_type')['Target'].agg(['count', 'mean']).reset_index()
    ctype_stats['Flight_Risk_Pct'] = (ctype_stats['mean'] * 100).round(1)
    ctype_stats = ctype_stats.sort_values('Flight_Risk_Pct', ascending=False)

    fig_ctype = px.bar(
        ctype_stats,
        x='Company_type',
        y='Flight_Risk_Pct',
        text='Flight_Risk_Pct',
        color='Flight_Risk_Pct',
        color_continuous_scale=['#10B981', '#F59E0B', '#F43F5E'],
        labels={'Company_type': 'Company Structure', 'Flight_Risk_Pct': 'Flight Risk (%)'}
    )
    fig_ctype.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    fig_ctype.update_coloraxes(showscale=False)
    configure_plotly_layout(fig_ctype, title="Flight Intent by Company Type", height=340)
    st.plotly_chart(fig_ctype, use_container_width=True)

with row3_col2:
    # Turnover by Time Since Last Job Change (Last_new_job)
    job_order = ['never', '1', '2', '3', '4', '>4']
    lnj_stats = df.groupby('Last_new_job')['Target'].agg(['count', 'mean']).reindex(job_order).reset_index()
    lnj_stats['Flight_Risk_Pct'] = (lnj_stats['mean'] * 100).round(1)

    fig_lnj = px.bar(
        lnj_stats,
        x='Last_new_job',
        y='Flight_Risk_Pct',
        text='Flight_Risk_Pct',
        color='Flight_Risk_Pct',
        color_continuous_scale=['#10B981', '#F59E0B', '#F43F5E'],
        labels={'Last_new_job': 'Years Since Last Job Change', 'Flight_Risk_Pct': 'Flight Risk (%)'}
    )
    fig_lnj.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    fig_lnj.update_coloraxes(showscale=False)
    configure_plotly_layout(fig_lnj, title="Flight Intent vs Years Since Last Job Transition", height=340)
    st.plotly_chart(fig_lnj, use_container_width=True)

st.markdown("""
<div class="p-3.5 rounded-xl bg-slate-900/60 border border-slate-800 text-xs text-slate-300 mb-6 flex items-start gap-2.5">
    <i class="fa-solid fa-circle-info text-amber-400 mt-0.5"></i>
    <div>
        <strong class="text-white">Company Stability Finding:</strong>
        Funded Startups demonstrate the lowest turnover intent (14.0%), benefiting from strong equity incentives and high growth morale. In contrast, candidates in early-stage startups (23.5%) or those who have never changed jobs (30.1%) exhibit heightened mobility intent.
    </div>
</div>
""", unsafe_allow_html=True)


# SECTION 4: CITY ECONOMIC DEVELOPMENT (CDI) & TRAINING
st.markdown("<h3 class='text-xl font-bold text-white mb-3 flex items-center gap-2'><i class='fa-solid fa-map-location-dot text-cyan-400 text-lg'></i> 4. Geographic Economic Prosperity & Training Hours</h3>", unsafe_allow_html=True)

row4_col1, row4_col2 = st.columns([1, 1])

with row4_col1:
    # Binned City Development Index
    df_cdi = df.copy()
    bins = [0.4, 0.65, 0.75, 0.85, 0.95]
    labels = ['Low (<0.65)', 'Developing (0.65-0.75)', 'Developed (0.75-0.85)', 'Metro Tech Hub (>0.85)']
    df_cdi['CDI_Tier'] = pd.cut(df_cdi['City_development_index'], bins=bins, labels=labels)
    cdi_stats = df_cdi.groupby('CDI_Tier', observed=True)['Target'].agg(['count', 'mean']).reset_index()
    cdi_stats['Flight_Risk_Pct'] = (cdi_stats['mean'] * 100).round(1)

    fig_cdi = px.bar(
        cdi_stats,
        x='CDI_Tier',
        y='Flight_Risk_Pct',
        text='Flight_Risk_Pct',
        color='Flight_Risk_Pct',
        color_continuous_scale=['#10B981', '#F59E0B', '#F43F5E'],
        labels={'CDI_Tier': 'City Development Tier', 'Flight_Risk_Pct': 'Flight Risk (%)'}
    )
    fig_cdi.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    fig_cdi.update_coloraxes(showscale=False)
    configure_plotly_layout(fig_cdi, title="Job-Seeking Rate by City Development Tier", height=340)
    st.plotly_chart(fig_cdi, use_container_width=True)

with row4_col2:
    # Training Hours distribution by Target (Box / Violin simplified as grouped mean by bin)
    df_train = df.copy()
    train_bins = [0, 20, 50, 100, 200, 400]
    train_labels = ['<20 hrs', '20-50 hrs', '50-100 hrs', '100-200 hrs', '200+ hrs']
    df_train['Training_Tier'] = pd.cut(df_train['Training_hours'], bins=train_bins, labels=train_labels)
    train_stats = df_train.groupby('Training_Tier', observed=True)['Target'].agg(['count', 'mean']).reset_index()
    train_stats['Flight_Risk_Pct'] = (train_stats['mean'] * 100).round(1)

    fig_train = px.bar(
        train_stats,
        x='Training_Tier',
        y='Flight_Risk_Pct',
        text='Flight_Risk_Pct',
        color='Flight_Risk_Pct',
        color_continuous_scale=['#10B981', '#F59E0B', '#F43F5E'],
        labels={'Training_Tier': 'Completed Training Hours', 'Flight_Risk_Pct': 'Flight Risk (%)'}
    )
    fig_train.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    fig_train.update_coloraxes(showscale=False)
    configure_plotly_layout(fig_train, title="Training Hours vs Flight Risk", height=340)
    st.plotly_chart(fig_train, use_container_width=True)

st.markdown("""
<div class="p-3.5 rounded-xl bg-slate-900/60 border border-slate-800 text-xs text-slate-300 mb-6 flex items-start gap-2.5">
    <i class="fa-solid fa-circle-info text-cyan-400 mt-0.5"></i>
    <div>
        <strong class="text-white">Geographic Migration Insight:</strong>
        Candidates in low-development cities have a 45%+ flight risk, as talent seeks to migrate to major metro hubs (where flight risk drops to 16.5%). Furthermore, completed training hours alone do not cause attrition; rather, career mobility and regional economics dictate talent movement.
    </div>
</div>
""", unsafe_allow_html=True)


# SECTION 5: INTERACTIVE SCENARIO DRILLDOWN
st.markdown("<h3 class='text-xl font-bold text-white mb-3 flex items-center gap-2'><i class='fa-solid fa-sliders text-indigo-400 text-lg'></i> 5. Interactive Cohort Risk Calculator</h3>", unsafe_allow_html=True)

with st.expander("🔍 Click to Explore Custom Workforce Segments", expanded=False):
    st.markdown("<p class='text-xs text-slate-300 mb-3'>Filter candidates by career stage, university enrollment, and company size to inspect specific cohort retention rates.</p>", unsafe_allow_html=True)
    
    fc1, fc2, fc3 = st.columns(3)
    with fc1:
        selected_stage = st.selectbox("Career Stage", ["All Stages"] + stage_order)
    with fc2:
        selected_enroll = st.selectbox("University Enrollment", ["All Statuses"] + df['Enrolled_university'].unique().tolist())
    with fc3:
        selected_csize = st.selectbox("Company Size", ["All Sizes"] + df['Company_size'].dropna().unique().tolist())

    filtered_sub = df.copy()
    if selected_stage != "All Stages":
        filtered_sub = filtered_sub[filtered_sub['Career_Stage'] == selected_stage]
    if selected_enroll != "All Statuses":
        filtered_sub = filtered_sub[filtered_sub['Enrolled_university'] == selected_enroll]
    if selected_csize != "All Sizes":
        filtered_sub = filtered_sub[filtered_sub['Company_size'] == selected_csize]

    sub_count = len(filtered_sub)
    if sub_count > 0:
        sub_risk = (filtered_sub['Target'] == 1).mean() * 100
        sub_stay = 100.0 - sub_risk
        
        m1, m2, m3 = st.columns(3)
        with m1:
            render_metric_card("Filtered Cohort Size", f"{sub_count:,}", "Candidates in segment", "fa-solid fa-filter", "indigo")
        with m2:
            render_metric_card("Cohort Flight Risk", f"{sub_risk:.1f}%", "Seeking new job", "fa-solid fa-door-open", "rose" if sub_risk > 25 else "emerald")
        with m3:
            render_metric_card("Retention Rate", f"{sub_stay:.1f}%", "Expected to stay", "fa-solid fa-shield-halved", "emerald")
    else:
        st.warning("No candidates match this specific combination of filters. Try broadening your selection.")



