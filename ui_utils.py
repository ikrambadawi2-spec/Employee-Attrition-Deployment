"""
HR Analytics & Employee Attrition UI Utility Module
Provides Tailwind CSS injection, dark modern themes, and layout helpers.
"""

from pathlib import Path
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def get_base_path() -> Path:
    """Returns the base project directory."""
    return Path(__file__).resolve().parent

@st.cache_data
def load_data() -> pd.DataFrame:
    """Loads Cleaned_df.csv with caching."""
    data_path = get_base_path() / "Cleaned_df.csv"
    if not data_path.exists():
        data_path = Path("Cleaned_df.csv")
    df = pd.read_csv(data_path)
    return df

def apply_custom_css():
    """Injects modern dark theme, Tailwind CDN, and typography into Streamlit."""
    custom_html = """
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            darkMode: 'class',
            theme: {
                extend: {
                    colors: {
                        brand: {
                            50: '#eef2ff',
                            100: '#e0e7ff',
                            400: '#818cf8',
                            500: '#6366f1',
                            600: '#4f46e5',
                            700: '#4338ca',
                            900: '#312e81',
                        },
                        dark: {
                            base: '#0B0F19',
                            card: '#161F30',
                            cardHover: '#1E293B',
                            border: 'rgba(255, 255, 255, 0.08)',
                        }
                    },
                    fontFamily: {
                        sans: ['Plus Jakarta Sans', 'Inter', 'Segoe UI', 'sans-serif'],
                    }
                }
            }
        }
    </script>

    <!-- Font Awesome Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">

    <style>
        /* Global Typography & Background */
        html, body, [class*="css"] {
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
            color: #F8FAFC;
        }

        /* App Background styling */
        .stApp {
            background: linear-gradient(135deg, #0B0F19 0%, #0F172A 50%, #111827 100%);
            background-attachment: fixed;
        }

        /* Remove stock Streamlit padding at top */
        .block-container {
            padding-top: 1.8rem;
            padding-bottom: 2.5rem;
            max-width: 1300px;
        }

        /* Modern Glassmorphic Cards */
        .modern-card {
            background: rgba(22, 31, 48, 0.75);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 1rem;
            padding: 1.5rem;
            box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
            margin-bottom: 1.25rem;
        }

        .modern-card:hover {
            border-color: rgba(99, 102, 241, 0.3);
            box-shadow: 0 14px 35px -8px rgba(99, 102, 241, 0.15);
            transform: translateY(-2px);
        }

        /* Hero Banner */
        .hero-banner {
            background: radial-gradient(100% 100% at 50% 0%, rgba(99, 102, 241, 0.18) 0%, rgba(15, 23, 42, 0) 100%),
                        rgba(22, 31, 48, 0.85);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(99, 102, 241, 0.25);
            border-radius: 1.25rem;
            padding: 2.25rem 2rem;
            margin-bottom: 2rem;
            box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.6);
            position: relative;
            overflow: hidden;
        }

        .hero-banner::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 2px;
            background: linear-gradient(90deg, transparent, #6366F1, #38BDF8, transparent);
        }

        /* Metric Cards */
        .metric-card {
            background: rgba(30, 41, 59, 0.6);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: 0.875rem;
            padding: 1.25rem 1.5rem;
            transition: all 0.2s ease;
        }
        .metric-card:hover {
            border-color: rgba(99, 102, 241, 0.4);
            transform: translateY(-2px);
            background: rgba(30, 41, 59, 0.85);
        }

        /* Pill Badges */
        .badge-pill {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.35rem 0.85rem;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 600;
            letter-spacing: 0.05em;
            text-transform: uppercase;
        }
        .badge-indigo {
            background: rgba(99, 102, 241, 0.15);
            color: #A5B4FC;
            border: 1px solid rgba(99, 102, 241, 0.3);
        }
        .badge-emerald {
            background: rgba(16, 185, 129, 0.15);
            color: #6EE7B7;
            border: 1px solid rgba(16, 185, 129, 0.3);
        }
        .badge-amber {
            background: rgba(245, 158, 11, 0.15);
            color: #FCD34D;
            border: 1px solid rgba(245, 158, 11, 0.3);
        }
        .badge-rose {
            background: rgba(244, 63, 94, 0.15);
            color: #FDA4AF;
            border: 1px solid rgba(244, 63, 94, 0.3);
        }
        .badge-cyan {
            background: rgba(6, 182, 212, 0.15);
            color: #67E8F9;
            border: 1px solid rgba(6, 182, 212, 0.3);
        }

        /* Custom Streamlit Form Controls Styling */
        div[data-testid="stMetricValue"] {
            font-size: 1.85rem !important;
            font-weight: 700 !important;
            color: #F8FAFC !important;
        }
        div[data-testid="stMetricLabel"] {
            font-size: 0.85rem !important;
            font-weight: 500 !important;
            color: #94A3B8 !important;
        }

        /* Modern Buttons */
        .stButton > button {
            background: linear-gradient(135deg, #4F46E5 0%, #6366F1 50%, #4338CA 100%) !important;
            color: #FFFFFF !important;
            font-weight: 600 !important;
            border-radius: 0.75rem !important;
            border: 1px solid rgba(255, 255, 255, 0.15) !important;
            padding: 0.65rem 1.75rem !important;
            box-shadow: 0 4px 15px rgba(79, 70, 229, 0.4) !important;
            transition: all 0.25s ease !important;
        }
        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 25px rgba(79, 70, 229, 0.6) !important;
            border-color: rgba(255, 255, 255, 0.3) !important;
        }

        /* Sidebar Styling */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #090D16 0%, #0F172A 100%) !important;
            border-right: 1px solid rgba(255, 255, 255, 0.07) !important;
        }
        section[data-testid="stSidebar"] .block-container {
            padding-top: 2rem !important;
        }

        /* Streamlit Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background-color: rgba(15, 23, 42, 0.6);
            padding: 6px;
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.06);
        }
        .stTabs [data-baseweb="tab"] {
            height: 42px;
            border-radius: 8px;
            color: #94A3B8;
            font-weight: 500;
            padding: 0 16px;
            border: none !important;
        }
        .stTabs [aria-selected="true"] {
            background-color: #6366F1 !important;
            color: #FFFFFF !important;
            font-weight: 600;
        }

        /* Streamlit Dataframe custom style */
        div[data-testid="stDataFrame"] {
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 0.75rem !important;
            overflow: hidden !important;
        }

        /* Custom scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        ::-webkit-scrollbar-track {
            background: #0B0F19;
        }
        ::-webkit-scrollbar-thumb {
            background: #334155;
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #475569;
        }
    </style>
    """
    st.markdown(custom_html, unsafe_allow_html=True)

def render_hero(badge_text: str, title: str, subtitle: str, icon_class: str = "fa-solid fa-chart-line"):
    """Renders a sleek Tailwind hero banner."""
    html = f"""
    <div class="hero-banner">
        <div class="flex items-center gap-2 mb-3">
            <span class="badge-pill badge-indigo">
                <i class="{icon_class} text-xs"></i>
                <span>{badge_text}</span>
            </span>
        </div>
        <h1 class="text-3xl md:text-4xl font-extrabold text-white tracking-tight mb-2.5">
            {title}
        </h1>
        <p class="text-slate-300 text-base md:text-lg max-w-3xl leading-relaxed">
            {subtitle}
        </p>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def render_metric_card(title: str, value: str, subtitle: str = "", icon_class: str = "fa-solid fa-users", color: str = "indigo"):
    """Renders an executive statistic card."""
    color_map = {
        "indigo": ("text-indigo-400", "bg-indigo-500/10", "border-indigo-500/20"),
        "emerald": ("text-emerald-400", "bg-emerald-500/10", "border-emerald-500/20"),
        "rose": ("text-rose-400", "bg-rose-500/10", "border-rose-500/20"),
        "amber": ("text-amber-400", "bg-amber-500/10", "border-amber-500/20"),
        "cyan": ("text-cyan-400", "bg-cyan-500/10", "border-cyan-500/20"),
    }
    t_col, bg_col, b_col = color_map.get(color, color_map["indigo"])
    
    html = f"""
    <div class="metric-card flex flex-col justify-between h-full">
        <div class="flex items-center justify-between mb-2">
            <span class="text-xs font-semibold uppercase tracking-wider text-slate-400">{title}</span>
            <div class="w-8 h-8 rounded-lg {bg_col} {b_col} border flex items-center justify-center {t_col}">
                <i class="{icon_class} text-sm"></i>
            </div>
        </div>
        <div>
            <div class="text-2xl md:text-3xl font-extrabold text-white tracking-tight">{value}</div>
            {f'<div class="text-xs text-slate-400 mt-1">{subtitle}</div>' if subtitle else ''}
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def render_sidebar_info():
    """Renders sleek sidebar navigation details and system status."""
    with st.sidebar:
        sidebar_html = """
        <div class="p-3 mb-4 rounded-xl bg-slate-900/60 border border-slate-700/50">
            <div class="flex items-center gap-3">
                <div class="w-10 h-10 rounded-lg bg-indigo-600/20 border border-indigo-500/30 flex items-center justify-center text-indigo-400 text-lg">
                    <i class="fa-solid fa-brain"></i>
                </div>
                <div>
                    <div class="text-sm font-bold text-white leading-tight">TalentPulse AI</div>
                    <div class="text-xs text-indigo-300 font-medium">Workforce Analytics</div>
                </div>
            </div>
            <div class="mt-3 pt-3 border-t border-slate-700/50 flex items-center justify-between text-xs text-slate-400">
                <span class="inline-flex items-center gap-1.5">
                    <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                    <span>System Active</span>
                </span>
                <span class="text-slate-400 font-mono">v2.4.0</span>
            </div>
        </div>
        """
        st.markdown(sidebar_html, unsafe_allow_html=True)

def configure_plotly_layout(fig, title: str = "", height: int = 380):
    """Applies modern dark styling, transparent background, and typography to Plotly figures."""
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0, 0, 0, 0)",
        plot_bgcolor="rgba(0, 0, 0, 0)",
        font=dict(
            family="Plus Jakarta Sans, sans-serif",
            color="#94A3B8",
            size=12
        ),
        title=dict(
            text=f"<b>{title}</b>" if title else None,
            font=dict(color="#F8FAFC", size=15),
            x=0.02,
            y=0.96
        ) if title else None,
        margin=dict(l=20, r=20, t=50 if title else 25, b=25),
        height=height,
        hoverlabel=dict(
            bgcolor="#1E293B",
            font_size=12,
            font_family="Plus Jakarta Sans, sans-serif",
            bordercolor="rgba(255, 255, 255, 0.15)"
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color="#CBD5E1", size=11)
        )
    )
    fig.update_xaxes(
        gridcolor="rgba(255, 255, 255, 0.06)",
        zerolinecolor="rgba(255, 255, 255, 0.08)",
        tickfont=dict(color="#94A3B8")
    )
    fig.update_yaxes(
        gridcolor="rgba(255, 255, 255, 0.06)",
        zerolinecolor="rgba(255, 255, 255, 0.08)",
        tickfont=dict(color="#94A3B8")
    )
    return fig

