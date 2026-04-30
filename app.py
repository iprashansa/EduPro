import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from data_processing import load_and_merge_data, calculate_kpis, generate_teacher_stats, train_course_rating_model
import numpy as np

# 1. Performance Optimization: Setup page config first
st.set_page_config(page_title="EduPro Analytics Dashboard", page_icon="🎓", layout="wide", initial_sidebar_state="expanded")

# 2. Performance Optimization: Advanced Caching
@st.cache_data(show_spinner=False)
def fetch_processed_data():
    df_merged, df_teachers, df_courses, df_transactions = load_and_merge_data("EduPro_Data.xlsx")
    teacher_stats = generate_teacher_stats(df_merged, df_teachers)
    return df_merged, df_teachers, df_courses, df_transactions, teacher_stats

@st.cache_resource(show_spinner=False)
def fetch_ml_model(df_merged):
    # Caching the ML model prevents retraining on every button click or filter change!
    return train_course_rating_model(df_merged)

try:
    with st.spinner("Loading Platform Data..."):
        df_merged, df_teachers, df_courses, df_transactions, teacher_stats = fetch_processed_data()
        ml_model, le_cat, le_level = fetch_ml_model(df_merged)
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# 3. Premium UI & Custom Styling (Aesthetics)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    /* Elegant KPI Cards */
    .kpi-container {
        display: flex;
        justify-content: space-between;
        gap: 15px;
        margin-bottom: 30px;
    }
    .kpi-card {
        flex: 1;
        background: linear-gradient(135deg, #ffffff 0%, #f8faff 100%);
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 20px 15px;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .kpi-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        border-color: #cbd5e1;
    }
    
    /* Dark Mode Support for KPI Cards */
    @media (prefers-color-scheme: dark) {
        .kpi-card {
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
            border: 1px solid #334155;
        }
        .kpi-title { color: #94a3b8 !important; }
        .kpi-value { color: #f8fafc !important; }
    }

    .kpi-title {
        font-size: 0.9rem;
        color: #64748b;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 8px;
    }
    .kpi-value {
        font-size: 2.2rem;
        font-weight: 800;
        color: #0f172a;
        margin: 0;
        line-height: 1.2;
    }
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 20px;
        border-radius: 8px 8px 0 0;
        font-weight: 600;
    }
    
    /* Headers */
    h1 {
        font-weight: 800 !important;
        background: -webkit-linear-gradient(45deg, #2563eb, #4f46e5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2em !important;
    }
    
    /* Hide Deploy Button and Streamlit Top Bar */
    .stAppDeployButton {display:none !important;}
    [data-testid="stAppDeployButton"] {display:none !important;}
    .stDeployButton {display:none !important;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Application Header
st.title("🎓 EduPro Intelligence Hub")
st.markdown("### EduPro Instructor & Course Quality Analytics")
st.markdown("---")

# ----------------- SIDEBAR -----------------
with st.sidebar:
    st.markdown("## Control Panel")
    
    expertise_filter = st.multiselect(
        "Instructor Expertise", 
        options=df_teachers["Expertise"].unique(),
        default=df_teachers["Expertise"].unique()
    )

    course_cat_filter = st.multiselect(
        "Course Category", 
        options=df_courses["CourseCategory"].unique(),
        default=df_courses["CourseCategory"].unique()
    )

    course_level_filter = st.multiselect(
        "Course Level", 
        options=df_courses["CourseLevel"].unique(),
        default=df_courses["CourseLevel"].unique()
    )

    min_rating, max_rating = st.slider(
        "Teacher Rating Range",
        min_value=float(df_teachers["TeacherRating"].min()),
        max_value=float(df_teachers["TeacherRating"].max()),
        value=(float(df_teachers["TeacherRating"].min()), float(df_teachers["TeacherRating"].max()))
    )

# 4. Data Filtering based on user selections
filtered_teachers = teacher_stats[
    (teacher_stats["Expertise"].isin(expertise_filter)) &
    (teacher_stats["TeacherRating"] >= min_rating) &
    (teacher_stats["TeacherRating"] <= max_rating)
]

filtered_merged = df_merged[
    (df_merged["TeacherID"].isin(filtered_teachers["TeacherID"])) &
    (df_merged["CourseCategory"].isin(course_cat_filter)) &
    (df_merged["CourseLevel"].isin(course_level_filter))
]

# ----------------- KPIs -----------------
# Optimized KPI calculation strictly on filtered data
kpis = calculate_kpis(filtered_merged, filtered_teachers, df_courses[df_courses["CourseCategory"].isin(course_cat_filter) & df_courses["CourseLevel"].isin(course_level_filter)])

st.markdown(f"""
<div class="kpi-container">
    <div class="kpi-card">
        <div class="kpi-title">Avg Teacher Rating</div>
        <div class="kpi-value">{kpis["Average Teacher Rating"]}</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-title">Avg Course Rating</div>
        <div class="kpi-value">{kpis["Average Course Rating"]}</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-title">Consistency (Std Dev)</div>
        <div class="kpi-value">{kpis["Rating Std Dev (Consistency)"]}</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-title">Experience Impact</div>
        <div class="kpi-value">{kpis["Experience Impact (Corr)"]}</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-title">Avg Enrollments</div>
        <div class="kpi-value">{kpis["Avg Enrollments per Teacher"]}</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ----------------- DASHBOARD LAYOUT -----------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🏆 Excellence Leaderboard", 
    "📈 Experience Mapping", 
    "🔥 Quality Heatmaps",
    "🧠 Domain Analysis",
    "🤖 ML Outcome Predictor"
])

# Default Plotly Template for cleaner aesthetic
plotly_template = "plotly_white"

# TAB 1: Leaderboard
with tab1:
    st.markdown("#### 🥇 Instructor Performance Leaderboard")
    
    leaderboard = filtered_teachers[["TeacherName", "Expertise", "YearsOfExperience", "TeacherRating", "Total_Enrollments", "Avg_Course_Rating"]]
    leaderboard = leaderboard.sort_values(by="TeacherRating", ascending=False).reset_index(drop=True)
    
    st.dataframe(
        leaderboard.style.background_gradient(subset=['TeacherRating', 'Avg_Course_Rating'], cmap='Purples'),
        use_container_width=True,
        height=300
    )
    
    st.markdown("#### 🚀 Enrollment Influence by Instructor Tier")
    def rating_tier(rating):
        if rating >= 4.5: return "Elite (4.5+)"
        elif rating >= 3.5: return "Standard (3.5-4.4)"
        else: return "Needs Review (<3.5)"
        
    tier_stats = teacher_stats.copy()
    tier_stats['Tier'] = tier_stats['TeacherRating'].apply(rating_tier)
    enrollments_by_tier = tier_stats.groupby('Tier')['Total_Enrollments'].mean().reset_index()
    
    fig_tier = px.bar(
        enrollments_by_tier,
        x='Tier',
        y='Total_Enrollments',
        color='Tier',
        color_discrete_sequence=['#4f46e5', '#38bdf8', '#94a3b8'],
        category_orders={"Tier": ["Elite (4.5+)", "Standard (3.5-4.4)", "Needs Review (<3.5)"]}
    )
    fig_tier.update_layout(template=plotly_template, margin=dict(t=20, b=0, l=0, r=0))
    st.plotly_chart(fig_tier, use_container_width=True)

# TAB 2: Experience vs Rating
with tab2:
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown("#### Teacher Experience vs Rating")
        fig1 = px.scatter(
            filtered_teachers, 
            x="YearsOfExperience", 
            y="TeacherRating", 
            color="Expertise",
            size="Total_Enrollments",
            hover_name="TeacherName",
            trendline="ols"
        )
        fig1.update_layout(template=plotly_template, margin=dict(t=20))
        st.plotly_chart(fig1, use_container_width=True)
        
    with col_b:
        st.markdown("#### Teacher Experience vs Course Outcomes")
        fig2 = px.scatter(
            filtered_merged, 
            x="YearsOfExperience", 
            y="CourseRating", 
            color="CourseCategory",
            hover_name="CourseName",
            opacity=0.7,
            trendline="ols"
        )
        fig2.update_layout(template=plotly_template, margin=dict(t=20))
        st.plotly_chart(fig2, use_container_width=True)

# TAB 3: Course Quality Heatmaps
with tab3:
    st.markdown("#### Course Quality Matrix (Category & Difficulty)")
    
    if not filtered_merged.empty:
        heatmap_data = filtered_merged.pivot_table(
            values='CourseRating', 
            index='CourseCategory', 
            columns='CourseLevel', 
            aggfunc='mean'
        )
        
        fig3 = px.imshow(
            heatmap_data, 
            text_auto=".2f", 
            aspect="auto", 
            color_continuous_scale="PuBuGn",
            labels=dict(color="Avg Rating")
        )
        fig3.update_layout(template=plotly_template, margin=dict(t=20))
        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.warning("Not enough data with the current filters to generate heatmap.")

# TAB 4: Domain Analysis
with tab4:
    col_c, col_d = st.columns(2)
    
    with col_c:
        st.markdown("#### Peak Performance by Domain")
        expertise_agg = filtered_teachers.groupby("Expertise")["TeacherRating"].mean().reset_index()
        fig4 = px.bar(
            expertise_agg.sort_values(by="TeacherRating", ascending=False),
            x="Expertise",
            y="TeacherRating",
            color="TeacherRating",
            color_continuous_scale="Purples"
        )
        fig4.update_layout(yaxis=dict(range=[2, 5]), template=plotly_template, margin=dict(t=20))
        st.plotly_chart(fig4, use_container_width=True)
        
    with col_d:
        st.markdown("#### Instructor Rating Distributions")
        fig5 = px.histogram(
            filtered_teachers, 
            x="TeacherRating", 
            nbins=20,
            color="Expertise", 
            marginal="box"
        )
        fig5.update_layout(template=plotly_template, margin=dict(t=20))
        st.plotly_chart(fig5, use_container_width=True)

# TAB 5: ML Course Rating Predictor
with tab5:
    st.markdown("#### 🤖 Proactive Quality Assurance: ML Estimator")
    st.markdown("Utilize our **Random Forest Predictive Algorithm** to forecast course success prior to assignment. The model analyzes historical non-linear data to project outcomes.")
    
    st.markdown("---")
    
    col_e, col_f, col_g = st.columns([1, 1, 1.5])
    
    with col_e:
        pred_category = st.selectbox("📚 Course Category", df_courses["CourseCategory"].unique())
        pred_level = st.selectbox("📊 Difficulty Level", df_courses["CourseLevel"].unique())
        
    with col_f:
        pred_teacher_rating = st.slider("⭐ Instructor Baseline Rating", 1.0, 5.0, 4.0, 0.1)
        pred_experience = st.slider("⏳ Years of Experience", 1, 40, 10)
        
    with col_g:
        st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)
        if st.button("🚀 Execute Prediction Framework", type="primary", use_container_width=True):
            try:
                # Process prediction input using cached le_cat, le_level, and ml_model
                cat_val = le_cat.transform([pred_category])[0]
                level_val = le_level.transform([pred_level])[0]
                
                input_features = np.array([[cat_val, level_val, pred_teacher_rating, pred_experience]])
                prediction = ml_model.predict(input_features)[0]
                
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #10b981 0%, #059669 100%); padding: 20px; border-radius: 10px; color: white; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-top: 10px;'>
                    <h4 style='color: rgba(255,255,255,0.9); margin-bottom: 5px; font-weight: 600;'>Projected Course Rating</h4>
                    <h1 style='color: white; margin: 0; font-size: 3rem; font-weight: 800;'>{prediction:.2f} <span style='font-size: 1.5rem'>/ 5.00</span></h1>
                </div>
                """, unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Prediction could not be completed: {e}")
