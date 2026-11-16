"""
Employee Attrition Predictor Page
Real-Time AI Flight Risk Evaluation with XGBoost Pipeline
"""

from pathlib import Path
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import joblib

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
    page_title=" Attrition Predictor",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply Styling
apply_custom_css()
render_sidebar_info()

# Paths resolution
base_dir = Path(__file__).resolve().parent.parent
if not (base_dir / "Cleaned_df.csv").exists():
    base_dir = Path(".")

# Load Data and Model Assets
@st.cache_resource
def load_ml_assets():
    model_path = base_dir / "XGBoost Pipeline.joblib"
    inputs_path = base_dir / "Inputs.pkl"
    model = joblib.load(model_path)
    inputs = joblib.load(inputs_path)
    return model, inputs

df = load_data()
model, inputs = load_ml_assets()

# Precompute City to City_development_index mapping
city_cdi_map = df.groupby('City')['City_development_index'].first().to_dict()
all_cities = sorted(city_cdi_map.keys(), key=str)

# Hero Banner
render_hero(
    badge_text="Predictive Machine Learning Engine",
    title="Employee Flight Risk & Attrition Predictor",
    subtitle="Evaluate individual employee turnover risk in real-time using our trained XGBoost Machine Learning pipeline.",
    icon_class="fa-solid fa-wand-magic-sparkles"
)

st.markdown("""
<div class="mb-4">
    <p class="text-sm text-slate-300">
        Enter candidate professional background, company environment, and demographic parameters below to simulate flight risk and generate tailored retention recommendations.
    </p>
</div>
""", unsafe_allow_html=True)

# Smart Input Form Structured into 3 Thematic Glass Cards
with st.form("prediction_form", clear_on_submit=False):
    col_card1, col_card2, col_card3 = st.columns(3)

    # ---------------------------------------------
    # CARD 1: CANDIDATE PROFILE & EDUCATION
    # ---------------------------------------------
    with col_card1:
        st.markdown("""
        <div class="modern-card p-4 rounded-xl border border-slate-800 bg-slate-900/60 mb-3">
            <div class="flex items-center gap-2 mb-3 text-indigo-400 font-bold text-sm">
                <i class="fa-solid fa-user-tie"></i>
                <span>Candidate Profile & Academics</span>
            </div>
        """, unsafe_allow_html=True)

        gender_options = ['Male', 'Female', 'Other']
        gender = st.selectbox("Gender", options=gender_options, index=0)

        education_hierarchy = ['Primary School', 'High School', 'Graduate', 'Masters', 'Phd']
        education_level = st.selectbox("Education Level", options=education_hierarchy, index=2)

        discipline_options = ['STEM', 'Humanities', 'Business Degree', 'Arts', 'No Major', 'Other']
        major_discipline = st.selectbox("Major Field of Study", options=discipline_options, index=0)

        enrollment_options = ['no_enrollment', 'Full time course', 'Part time course']
        enrolled_university = st.selectbox("University Enrollment Status", options=enrollment_options, index=0)

        st.markdown("</div>", unsafe_allow_html=True)

    # ---------------------------------------------
    # CARD 2: EXPERIENCE & CAREER TRAJECTORY
    # ---------------------------------------------
    with col_card2:
        st.markdown("""
        <div class="modern-card p-4 rounded-xl border border-slate-800 bg-slate-900/60 mb-3">
            <div class="flex items-center gap-2 mb-3 text-emerald-400 font-bold text-sm">
                <i class="fa-solid fa-briefcase"></i>
                <span>Experience & Seniority</span>
            </div>
        """, unsafe_allow_html=True)

        career_stages = ['Fresher', 'Junior', 'Mid-Level', 'Senior', 'Expert']
        career_stage = st.selectbox("Career Seniority Stage", options=career_stages, index=3)

        # Default experience based on stage
        stage_default_exp = {
            'Fresher': 1, 'Junior': 3, 'Mid-Level': 7, 'Senior': 12, 'Expert': 20
        }
        experience_val = st.slider(
            "Total Work Experience (Years)",
            min_value=0,
            max_value=21,
            value=stage_default_exp.get(career_stage, 10),
            help="Note: 21 represents >20 years of industry experience"
        )

        relevant_exp_options = ['Has relevent experience', 'No relevent experience']
        relevent_experience = st.radio("Relevant Domain Experience", options=relevant_exp_options, index=0)

        last_job_options = ['never', '1', '2', '3', '4', '>4']
        last_new_job = st.selectbox("Years Since Last Job Switch", options=last_job_options, index=1)

        st.markdown("</div>", unsafe_allow_html=True)

    # ---------------------------------------------
    # CARD 3: EMPLOYER & GEOGRAPHY
    # ---------------------------------------------
    with col_card3:
        st.markdown("""
        <div class="modern-card p-4 rounded-xl border border-slate-800 bg-slate-900/60 mb-3">
            <div class="flex items-center gap-2 mb-3 text-cyan-400 font-bold text-sm">
                <i class="fa-solid fa-building-user"></i>
                <span>Organization & Location</span>
            </div>
        """, unsafe_allow_html=True)

        # City Dropdown
        default_city_idx = all_cities.index('city_103') if 'city_103' in all_cities else 0
        city = st.selectbox("Resident City", options=all_cities, index=default_city_idx)

        # Auto-prefill CDI with ability to fine-tune
        preset_cdi = float(city_cdi_map.get(city, 0.920))
        city_dev_index = st.slider(
            "City Development Index (CDI)",
            min_value=0.40,
            max_value=0.95,
            value=preset_cdi,
            step=0.01,
            help="Economic development index for the selected city"
        )

        company_size_order = ['<10', '10-49', '50-99', '100-500', '500-999', '1000-4999', '5000-9999', '10000+']
        company_size = st.selectbox("Company Headcount Scale", options=company_size_order, index=2)

        company_types = ['Pvt Ltd', 'Funded Startup', 'Public Sector', 'Early Stage Startup', 'NGO', 'Other']
        company_type = st.selectbox("Company Operating Structure", options=company_types, index=0)

        training_hours = st.slider(
            "Completed Training Hours",
            min_value=1,
            max_value=336,
            value=45,
            step=1
        )

        st.markdown("</div>", unsafe_allow_html=True)

    # Submit Button
    submit_btn = st.form_submit_button(
        label="🚀 Evaluate Flight Risk & Predict Retention",
        use_container_width=True
    )

# Prepare Test Dataframe
test_row = pd.DataFrame(
    data=[[
        city,
        city_dev_index,
        gender,
        relevent_experience,
        enrolled_university,
        education_level,
        major_discipline,
        experience_val,
        company_size,
        company_type,
        last_new_job,
        training_hours,
        career_stage
    ]],
    columns=inputs
)

# EXECUTE PREDICTION
if submit_btn or 'has_predicted' in st.session_state:
    st.session_state['has_predicted'] = True

    # Run XGBoost inference
    prediction = int(model.predict(test_row)[0])
    probabilities = model.predict_proba(test_row)[0]
    p_stay = float(probabilities[0])
    p_leave = float(probabilities[1])

    st.markdown("<div class='my-6'></div>", unsafe_allow_html=True)
    st.markdown("<h3 class='text-2xl font-bold text-white mb-4 flex items-center gap-2'><i class='fa-solid fa-chart-line text-indigo-400'></i> Assessment Outcome</h3>", unsafe_allow_html=True)

    # 1. High-Impact Verdict Banner
    if prediction == 1 or p_leave >= 0.50:
        verdict_html = f"""
        <div class="modern-card border-rose-500/50 bg-rose-950/30 p-6 rounded-2xl relative overflow-hidden mb-6">
            <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div class="flex items-center gap-4">
                    <div class="w-14 h-14 rounded-2xl bg-rose-500/20 border border-rose-500/40 flex items-center justify-center text-rose-400 text-2xl shrink-0">
                        <i class="fa-solid fa-triangle-exclamation"></i>
                    </div>
                    <div>
                        <div class="flex items-center gap-2 mb-1">
                            <span class="badge-pill badge-rose text-xs">High Attrition Risk</span>
                            <span class="text-xs text-rose-300 font-medium">Turnover Probability: {p_leave:.1%}</span>
                        </div>
                        <h2 class="text-2xl font-black text-white">Employee Is Likely Looking for a New Job</h2>
                        <p class="text-slate-300 text-sm mt-1 max-w-2xl">
                            The machine learning model detected significant flight risk factors. Immediate proactive HR retention engagement is recommended.
                        </p>
                    </div>
                </div>
                <div class="text-right shrink-0">
                    <div class="text-3xl font-extrabold text-rose-400">{p_leave:.1%}</div>
                    <div class="text-xs text-slate-400 uppercase tracking-wider">Flight Probability</div>
                </div>
            </div>
        </div>
        """
    else:
        verdict_html = f"""
        <div class="modern-card border-emerald-500/50 bg-emerald-950/30 p-6 rounded-2xl relative overflow-hidden mb-6">
            <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div class="flex items-center gap-4">
                    <div class="w-14 h-14 rounded-2xl bg-emerald-500/20 border border-emerald-500/40 flex items-center justify-center text-emerald-400 text-2xl shrink-0">
                        <i class="fa-solid fa-shield-heart"></i>
                    </div>
                    <div>
                        <div class="flex items-center gap-2 mb-1">
                            <span class="badge-pill badge-emerald text-xs">Retention Stable</span>
                            <span class="text-xs text-emerald-300 font-medium">Retention Probability: {p_stay:.1%}</span>
                        </div>
                        <h2 class="text-2xl font-black text-white">Employee Is Likely to Stay with Current Company</h2>
                        <p class="text-slate-300 text-sm mt-1 max-w-2xl">
                            The profile aligns with high retention characteristics. Maintain engagement and regular growth pathways.
                        </p>
                    </div>
                </div>
                <div class="text-right shrink-0">
                    <div class="text-3xl font-extrabold text-emerald-400">{p_stay:.1%}</div>
                    <div class="text-xs text-slate-400 uppercase tracking-wider">Retention Probability</div>
                </div>
            </div>
        </div>
        """
    st.markdown(verdict_html, unsafe_allow_html=True)

    # 2. Probability Metrics & Visual Donut Chart
    res_col1, res_col2 = st.columns([1, 1])

    with res_col1:
        # Dynamic Metric Cards
        sub_c1, sub_c2 = st.columns(2)
        with sub_c1:
            render_metric_card(
                title="Probability of Staying",
                value=f"{p_stay:.1%}",
                subtitle="Baseline retention strength",
                icon_class="fa-solid fa-lock",
                color="emerald"
            )
        with sub_c2:
            render_metric_card(
                title="Probability of Leaving",
                value=f"{p_leave:.1%}",
                subtitle="Flight intent score",
                icon_class="fa-solid fa-door-open",
                color="rose" if p_leave > 0.4 else "amber"
            )

        # Dynamic Factor Contribution Summary
        st.markdown("<div class='mt-4'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div class="modern-card p-4 rounded-xl border border-slate-800 bg-slate-900/40">
            <h4 class="text-sm font-bold text-white mb-2 flex items-center gap-2">
                <i class="fa-solid fa-magnifying-glass-chart text-indigo-400"></i>
                <span>Key Predictive Profile Signals</span>
            </h4>
            <ul class="text-xs text-slate-300 space-y-2">
        """, unsafe_allow_html=True)

        # Dynamic profile insights
        signals = []
        if career_stage in ['Fresher', 'Junior']:
            signals.append("<li class='flex items-center gap-2 text-rose-300'><i class='fa-solid fa-circle-exclamation text-rose-400 text-[10px]'></i> Early Career Stage elevates turnover probability (+15-20% baseline risk).</li>")
        else:
            signals.append("<li class='flex items-center gap-2 text-emerald-300'><i class='fa-solid fa-circle-check text-emerald-400 text-[10px]'></i> Senior/Expert seniority confers strong retention stability.</li>")

        if enrolled_university == 'Full time course':
            signals.append("<li class='flex items-center gap-2 text-rose-300'><i class='fa-solid fa-circle-exclamation text-rose-400 text-[10px]'></i> Active full-time university study is a strong precursor to post-graduation job transition.</li>")
        
        if city_dev_index < 0.70:
            signals.append("<li class='flex items-center gap-2 text-amber-300'><i class='fa-solid fa-triangle-exclamation text-amber-400 text-[10px]'></i> Lower city development index creates incentive for metropolitan migration.</li>")
        else:
            signals.append("<li class='flex items-center gap-2 text-emerald-300'><i class='fa-solid fa-circle-check text-emerald-400 text-[10px]'></i> High city development index provides competitive local labor market satisfaction.</li>")

        if relevent_experience == 'No relevent experience':
            signals.append("<li class='flex items-center gap-2 text-amber-300'><i class='fa-solid fa-triangle-exclamation text-amber-400 text-[10px]'></i> Lack of prior relevant experience increases early transition friction.</li>")

        for s in signals:
            st.markdown(s, unsafe_allow_html=True)

        st.markdown("</ul></div>", unsafe_allow_html=True)

    with res_col2:
        # Donut Chart of Probability
        prob_df = pd.DataFrame({
            'Outcome': ['Likely to Stay', 'Looking for New Job'],
            'Probability': [p_stay, p_leave]
        })
        fig_prob = px.pie(
            prob_df,
            names='Outcome',
            values='Probability',
            color='Outcome',
            color_discrete_map={
                'Likely to Stay': '#10B981',
                'Looking for New Job': '#F43F5E'
            },
            hole=0.6
        )
        fig_prob.update_traces(
            textinfo='label+percent',
            textposition='outside',
            marker=dict(line=dict(color='#0B0F19', width=2))
        )
        configure_plotly_layout(fig_prob, title="XGBoost Prediction Probability Gauge", height=320)
        st.plotly_chart(fig_prob, use_container_width=True)

    # 3. Actionable Retention Plan Tailored to Candidate
    st.markdown("<div class='my-4'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div class="modern-card">
        <h4 class="text-base font-bold text-white mb-2 flex items-center gap-2">
            <i class="fa-solid fa-clipboard-check text-emerald-400"></i>
            <span>Recommended HR Retention Action Plan</span>
        </h4>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs text-slate-300 mt-3">
            <div class="p-3 rounded-lg bg-slate-900/60 border border-slate-800">
                <strong class="text-indigo-300 block mb-1">1. Compensation & Milestones</strong>
                Schedule a 6-month compensation alignment review to offset competitive market headhunting.
            </div>
            <div class="p-3 rounded-lg bg-slate-900/60 border border-slate-800">
                <strong class="text-emerald-300 block mb-1">2. Growth & Mentorship</strong>
                Pair candidate with a designated technical lead to formulate a personalized 12-month promotion ladder.
            </div>
            <div class="p-3 rounded-lg bg-slate-900/60 border border-slate-800">
                <strong class="text-cyan-300 block mb-1">3. Flexible Work & Study</strong>
                Support continued learning or flexible hours if pursuing academic degrees to prevent external attrition.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

