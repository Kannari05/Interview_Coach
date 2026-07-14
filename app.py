import streamlit as st
import pandas as pd
import numpy as np
import random
import time
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import speech_recognition as sr

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="AI Interview Coach",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

:root {
    --bg: #0a0e1a;
    --surface: #111827;
    --surface2: #1a2235;
    --accent: #00e5ff;
    --accent2: #7c3aed;
    --accent3: #f59e0b;
    --green: #10b981;
    --red: #ef4444;
    --text: #e2e8f0;
    --muted: #64748b;
    --border: rgba(0,229,255,0.15);
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

h1, h2, h3, h4 {
    font-family: 'Syne', sans-serif !important;
    letter-spacing: -0.02em;
}

/* Main background */
.stApp { background: linear-gradient(135deg, #0a0e1a 0%, #0d1526 50%, #0a0e1a 100%); }

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1526 0%, #111827 100%) !important;
    border-right: 1px solid var(--border);
}
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stSlider label,
[data-testid="stSidebar"] p {
    color: var(--text) !important;
}

/* Metric cards */
.metric-card {
    background: linear-gradient(135deg, #111827, #1a2235);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 20px 24px;
    text-align: center;
    position: relative;
    overflow: hidden;
    box-shadow: 0 4px 24px rgba(0,0,0,0.3);
    transition: transform 0.2s ease;
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--accent), var(--accent2));
}
.metric-card .val {
    font-family: 'Syne', sans-serif;
    font-size: 2.4rem;
    font-weight: 800;
    color: var(--accent);
    line-height: 1;
}
.metric-card .label {
    font-size: 0.78rem;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-top: 6px;
}

/* Feedback box */
.feedback-box {
    background: linear-gradient(135deg, #1a2235, #111827);
    border: 1px solid var(--border);
    border-left: 4px solid var(--accent);
    border-radius: 12px;
    padding: 20px;
    margin: 12px 0;
    font-size: 0.95rem;
    line-height: 1.7;
}

/* Answer area */
.stTextArea textarea {
    background: #111827 !important;
    color: var(--text) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.95rem !important;
}
.stTextArea textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px rgba(0,229,255,0.15) !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #00c4d9, #7c3aed) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.05em !important;
    padding: 10px 28px !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 15px rgba(0,229,255,0.2) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(0,229,255,0.35) !important;
}

/* Selectbox & slider */
.stSelectbox > div > div {
    background: #111827 !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
}
.stSlider > div > div { color: var(--accent) !important; }

/* Progress bar */
.stProgress > div > div { background: linear-gradient(90deg, var(--accent), var(--accent2)) !important; }

/* Section header */
.section-header {
    font-family: 'Syne', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--accent);
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin: 24px 0 12px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.section-header::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
    margin-left: 8px;
}

/* Score badge */
.score-badge {
    display: inline-block;
    padding: 4px 14px;
    border-radius: 20px;
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 0.85rem;
}
.badge-excellent { background: rgba(16,185,129,0.2); color: #10b981; border: 1px solid rgba(16,185,129,0.4); }
.badge-good      { background: rgba(0,229,255,0.2);  color: #00e5ff; border: 1px solid rgba(0,229,255,0.4);  }
.badge-average   { background: rgba(245,158,11,0.2); color: #f59e0b; border: 1px solid rgba(245,158,11,0.4); }
.badge-poor      { background: rgba(239,68,68,0.2);  color: #ef4444; border: 1px solid rgba(239,68,68,0.4);  }

/* Alert boxes */
.alert-success {
    background: rgba(16,185,129,0.1);
    border: 1px solid rgba(16,185,129,0.3);
    border-radius: 10px;
    padding: 14px 18px;
    color: #10b981;
    margin: 8px 0;
}
.alert-warning {
    background: rgba(245,158,11,0.1);
    border: 1px solid rgba(245,158,11,0.3);
    border-radius: 10px;
    padding: 14px 18px;
    color: #f59e0b;
    margin: 8px 0;
}
div[data-testid="stMarkdownContainer"] p { color: var(--text) !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SAMPLE DATA
# ─────────────────────────────────────────────
from questions import QUESTIONS_DB
from languages import LANGUAGE_DB

SAMPLE_HISTORY = pd.DataFrame({
    "Session": [f"Session {i}" for i in range(1, 9)],
    "Date": pd.date_range("2024-11-01", periods=8, freq="5D"),
    "Role": ["Software Engineer"]*4 + ["Data Scientist"]*4,
    "Avg Score": [52, 61, 68, 74, 45, 58, 67, 76],
    "Questions": [5, 5, 6, 6, 5, 5, 6, 6],
    "Confidence": [55, 63, 70, 78, 48, 60, 68, 79],
    "Clarity":    [50, 60, 67, 72, 44, 57, 66, 74],
    "Relevance":  [51, 60, 67, 72, 43, 57, 66, 75],
})

# ─────────────────────────────────────────────
# ML ENGINE
# ─────────────────────────────────────────────
@st.cache_resource
def build_ml_model():
    """Train a simple ML classifier for answer quality prediction."""
    np.random.seed(42)
    texts, labels = [], []
    for role_data in QUESTIONS_DB.values():
        for cat_questions in role_data.values():
            for item in cat_questions:
                ideal = item["ideal"]
                texts.append(ideal); labels.append("Excellent")
                # Partial answers
                words = ideal.split()
                texts.append(" ".join(words[:len(words)//2])); labels.append("Good")
                texts.append(" ".join(words[:len(words)//4])); labels.append("Average")
                texts.append("I am not sure about this topic"); labels.append("Poor")
                texts.append("Maybe yes or no depends"); labels.append("Poor")
    vectorizer = TfidfVectorizer(max_features=300, ngram_range=(1,2))
    X = vectorizer.fit_transform(texts)
    le = LabelEncoder()
    y = le.fit_transform(labels)
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X, y)
    return vectorizer, clf, le

def score_answer_ml(user_answer, ideal_answer, keywords, vectorizer, clf, le):
    """Score answer using ML + keyword matching + semantic similarity."""
    if not user_answer.strip():
        return 0, 0, 0, 0, "No answer provided."

    # 1. ML prediction
    X_user = vectorizer.transform([user_answer])
    proba = clf.predict_proba(X_user)[0]
    classes = le.classes_
    class_scores = {"Excellent": 95, "Good": 75, "Average": 55, "Poor": 30}
    ml_score = sum(proba[i] * class_scores.get(c, 50) for i, c in enumerate(classes))

    # 2. Keyword hit rate
    kw_hits = sum(1 for kw in keywords if kw.lower() in user_answer.lower())
    kw_score = min(100, (kw_hits / max(len(keywords), 1)) * 120)

    # 3. Cosine similarity
    tfidf = TfidfVectorizer().fit([ideal_answer, user_answer])
    vecs  = tfidf.transform([ideal_answer, user_answer])
    sim   = cosine_similarity(vecs[0], vecs[1])[0][0]
    sim_score = sim * 100

    # 4. Length / fluency proxy
    word_count = len(user_answer.split())
    fluency = min(100, word_count * 4)

    # Weighted composite
    composite = 0.35*ml_score + 0.30*kw_score + 0.25*sim_score + 0.10*fluency

    found_kws = [kw for kw in keywords if kw.lower() in user_answer.lower()]
    missing   = [kw for kw in keywords if kw.lower() not in user_answer.lower()]
    feedback  = f"✅ Good keywords: **{', '.join(found_kws[:4]) if found_kws else 'None found'}**\n\n"
    feedback += f"💡 Missing keywords: **{', '.join(missing[:4]) if missing else 'None — great coverage!'}**\n\n"
    if word_count < 20:
        feedback += "⚠️ Answer is too brief. Try to elaborate with examples and structure.\n"
    elif word_count > 200:
        feedback += "ℹ️ Good detail! Make sure to stay concise in real interviews.\n"
    else:
        feedback += "✅ Answer length is appropriate.\n"

    return round(composite), round(kw_score), round(sim_score), round(fluency), feedback

# ─────────────────────────────────────────────
# CHART HELPERS
# ─────────────────────────────────────────────
PLOT_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans", color="#e2e8f0", size=12),
    margin=dict(l=10, r=10, t=30, b=10),
)

def gauge_chart(value, title, color="#00e5ff"):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={"text": title, "font": {"family":"Syne","size":14,"color":"#94a3b8"}},
        number={"font": {"family":"Syne","size":28,"color":color}, "suffix":"%"},
        gauge={
            "axis": {"range":[0,100], "tickcolor":"#334155", "tickfont":{"size":9,"color":"#64748b"}},
            "bar": {"color": color, "thickness":0.25},
            "bgcolor": "#1a2235",
            "bordercolor": "rgba(0,229,255,0.1)",
            "steps": [
                {"range":[0,40],  "color":"rgba(239,68,68,0.15)"},
                {"range":[40,65], "color":"rgba(245,158,11,0.15)"},
                {"range":[65,80], "color":"rgba(0,229,255,0.15)"},
                {"range":[80,100],"color":"rgba(16,185,129,0.15)"},
            ],
            "threshold": {"line":{"color":"white","width":2},"thickness":0.75,"value":value},
        }
    ))
    fig.update_layout(**PLOT_LAYOUT, height=200)
    return fig

def radar_chart(scores_dict):
    cats = list(scores_dict.keys())
    vals = list(scores_dict.values())
    fig = go.Figure(go.Scatterpolar(
        r=vals + [vals[0]],
        theta=cats + [cats[0]],
        fill="toself",
        fillcolor="rgba(0,229,255,0.15)",
        line=dict(color="#00e5ff", width=2),
        marker=dict(color="#00e5ff", size=6),
    ))
    fig.update_layout(
        **PLOT_LAYOUT,
        polar=dict(
            bgcolor="rgba(17,24,39,0.8)",
            radialaxis=dict(visible=True, range=[0,100], tickfont=dict(size=9, color="#64748b"), gridcolor="rgba(255,255,255,0.05)"),
            angularaxis=dict(tickfont=dict(size=11, color="#94a3b8"), gridcolor="rgba(255,255,255,0.05)"),
        ),
        showlegend=False,
        height=320,
    )
    return fig

def progress_line_chart(history_df):
    fig = go.Figure()
    colors = {"Avg Score":"#00e5ff", "Confidence":"#7c3aed", "Clarity":"#f59e0b", "Relevance":"#10b981"}
    for col, clr in colors.items():
        fig.add_trace(go.Scatter(
            x=history_df["Session"], y=history_df[col],
            mode="lines+markers", name=col,
            line=dict(color=clr, width=2.5, shape="spline"),
            marker=dict(size=7, color=clr, line=dict(color="white", width=1.5)),
            fill="tozeroy", fillcolor=f"rgba({int(clr[1:3],16)},{int(clr[3:5],16)},{int(clr[5:7],16)},0.05)",
        ))
    fig.update_layout(
        **PLOT_LAYOUT, height=300,
        xaxis=dict(gridcolor="rgba(255,255,255,0.04)", tickfont=dict(size=10)),
        yaxis=dict(gridcolor="rgba(255,255,255,0.04)", range=[0,110], tickfont=dict(size=10)),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, font=dict(size=11)),
    )
    return fig

def bar_breakdown_chart(scores):
    labels = list(scores.keys())
    vals   = list(scores.values())
    colors = ["#00e5ff","#7c3aed","#10b981","#f59e0b"]
    fig = go.Figure(go.Bar(
        x=labels, y=vals, marker_color=colors,
        marker_line_color="rgba(255,255,255,0.1)", marker_line_width=1,
        text=[f"{v}%" for v in vals], textposition="outside",
        textfont=dict(family="Syne", size=13, color="white"),
    ))
    fig.update_layout(
        **PLOT_LAYOUT, height=260,
        yaxis=dict(range=[0,115], gridcolor="rgba(255,255,255,0.04)", tickfont=dict(size=10)),
        xaxis=dict(tickfont=dict(size=11)),
        bargap=0.35,
    )
    return fig

def keyword_heatmap(sessions_scores):
    cats = ["ML Score", "Keyword Match", "Semantic Sim", "Fluency"]
    df = pd.DataFrame(sessions_scores, columns=cats)
    fig = px.imshow(
        df.T, color_continuous_scale=["#0a0e1a","#1a2235","#00e5ff","#7c3aed"],
        aspect="auto", zmin=0, zmax=100,
    )
    fig.update_layout(**PLOT_LAYOUT, height=200, coloraxis_showscale=False,
        xaxis=dict(tickvals=list(range(len(sessions_scores))), ticktext=[f"Q{i+1}" for i in range(len(sessions_scores))], tickfont=dict(size=10)),
        yaxis=dict(tickfont=dict(size=10)),
    )
    return fig

def grade_badge(score):
    if score >= 80: return f'<span class="score-badge badge-excellent">Excellent</span>'
    elif score >= 65: return f'<span class="score-badge badge-good">Good</span>'
    elif score >= 45: return f'<span class="score-badge badge-average">Average</span>'
    else: return f'<span class="score-badge badge-poor">Needs Work</span>'

# ─────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────
def init_state():
    defaults = {
        "page": "home",
        "role": "Software Engineer",
        "category": "Technical",
        "q_index": 0,
        "answers": [],
        "scores": [],
        "detail_scores": [],
        "feedbacks": [],
        "session_done": False,
        "num_questions": 5,
        "current_questions": [],
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()
vectorizer, clf, le = build_ml_model()

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 20px 0 12px;'>
        <div style='font-size:2.5rem;'>🎯</div>
        <div style='font-family:Syne; font-size:1.3rem; font-weight:800; color:#00e5ff; letter-spacing:-0.02em;'>Interview Coach</div>
        <div style='font-size:0.75rem; color:#64748b; letter-spacing:0.1em; text-transform:uppercase;'>AI-Powered · ML-Driven</div>
    </div>
    """, unsafe_allow_html=True)
    st.divider()

    nav_opts = ["🏠 Home", "🎤 Practice Session", "📊 Analytics", "📚 Question Bank"]
    page_to_index = {"home": 0, "session": 1, "analytics": 2, "bank": 3}
    lbl_to_page = {"🏠 Home":"home", "🎤 Practice Session":"session", "📊 Analytics":"analytics", "📚 Question Bank":"bank"}
    
    current_index = page_to_index.get(st.session_state.page, 0)
    selected_val = st.radio("Navigation", nav_opts, index=current_index, label_visibility="collapsed")
    new_page = lbl_to_page[selected_val]
    
    if new_page != st.session_state.page:
        st.session_state.page = new_page
        st.rerun()

    st.divider()
    st.markdown("<div style='font-size:0.8rem; color:#64748b; text-transform:uppercase; letter-spacing:0.1em; margin-bottom:10px;'>Session Config</div>", unsafe_allow_html=True)
    role = st.selectbox("Target Role", list(QUESTIONS_DB.keys()))
    cats = list(QUESTIONS_DB[role].keys())
    cat  = st.selectbox("Category", ["All Categories"] + cats)
    
    lang_opts = ["None"] + list(LANGUAGE_DB.keys())
    coding_lang = st.selectbox("Coding Language", lang_opts)
    
    n_q  = st.slider("Questions", 2, 6, 4)

    if st.button("▶ Start New Session", use_container_width=True):
        st.session_state.role = role
        st.session_state.category = cat
        st.session_state.coding_lang = coding_lang
        st.session_state.num_questions = n_q
        st.session_state.q_index = 0
        st.session_state.answers = []
        st.session_state.scores = []
        st.session_state.detail_scores = []
        st.session_state.feedbacks = []
        st.session_state.session_done = False
        st.session_state.page = "session"
        
        if cat == "All Categories":
            pool = []
            for c in QUESTIONS_DB.get(role, {}).values():
                pool.extend(c)
        else:
            pool = list(QUESTIONS_DB.get(role, {}).get(cat, []))
            
        if coding_lang != "None":
            pool.extend(LANGUAGE_DB.get(coding_lang, []))
            
        if pool:
            import random
            shuffled_pool = random.sample(pool, len(pool))
            questions = (shuffled_pool * ((n_q // len(shuffled_pool)) + 1))[:n_q]
            random.shuffle(questions)
            st.session_state.current_questions = questions
        else:
            st.session_state.current_questions = []
            
        st.rerun()

# ─────────────────────────────────────────────
# HOME PAGE
# ─────────────────────────────────────────────
if st.session_state.page == "home":
    st.markdown("""
    <div style='padding: 40px 0 20px;'>
        <div style='font-family:Syne; font-size:3rem; font-weight:800; line-height:1.1; letter-spacing:-0.03em;'>
            Ace Your Next<br><span style='color:#00e5ff;'>Interview</span> with AI
        </div>
        <div style='color:#94a3b8; font-size:1.1rem; margin-top:14px; max-width:560px; line-height:1.7;'>
            Practice with real questions. Get instant ML-powered feedback. Track your growth across sessions.
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    metrics = [("3", "Roles Available"), ("20+", "Questions"), ("4", "Scoring Dimensions"), ("ML", "Powered Engine")]
    for col, (val, lbl) in zip([col1,col2,col3,col4], metrics):
        col.markdown(f'<div class="metric-card"><div class="val">{val}</div><div class="label">{lbl}</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns([1, 1])
    with c1:
        st.markdown('<div class="section-header">🔬 How It Works</div>', unsafe_allow_html=True)
        steps = [("1", "Choose Role & Category", "Select your target job and question type in the sidebar."),
                 ("2", "Answer Questions", "Type your answers naturally — no time pressure."),
                 ("3", "Get ML Feedback", "Instant scoring across 4 dimensions using ML + NLP."),
                 ("4", "Track Progress", "View trends and improve session over session.")]
        for num, title, desc in steps:
            st.markdown(f"""
            <div style='display:flex; gap:14px; align-items:flex-start; margin-bottom:16px;'>
                <div style='background:linear-gradient(135deg,#00e5ff,#7c3aed); border-radius:50%; width:32px; height:32px; display:flex; align-items:center; justify-content:center; font-family:Syne; font-weight:800; font-size:0.9rem; flex-shrink:0;'>{num}</div>
                <div><div style='font-family:Syne; font-weight:600; color:#e2e8f0;'>{title}</div><div style='color:#64748b; font-size:0.88rem; margin-top:3px;'>{desc}</div></div>
            </div>
            """, unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="section-header">📈 Sample Progress</div>', unsafe_allow_html=True)
        st.plotly_chart(progress_line_chart(SAMPLE_HISTORY[:8]), use_container_width=True, config={"displayModeBar":False})

    st.markdown('<div class="section-header">🎯 Supported Roles</div>', unsafe_allow_html=True)
    role_cols = st.columns(3)
    role_names = list(QUESTIONS_DB.keys())
    colors = ["#00e5ff", "#7c3aed", "#f59e0b", "#10b981", "#ef4444", "#3b82f6", "#f472b6", "#14b8a6", "#eab308"]
    for i, role_key in enumerate(role_names):
        if i >= 9:
            break
        col = role_cols[i % 3]
        cats_str = " · ".join(QUESTIONS_DB[role_key].keys())
        color = colors[i % len(colors)]
        icon = "💼"
        if "Engineer" in role_key or "Developer" in role_key: icon = "💻"
        elif "Data" in role_key: icon = "📊"
        elif "Manager" in role_key: icon = "🗂"
        elif "Designer" in role_key: icon = "🎨"
        elif "Ops" in role_key: icon = "⚙️"
        
        col.markdown(f"""
        <div style='background:linear-gradient(135deg,#111827,#1a2235); border:1px solid rgba(255,255,255,0.06); border-top:3px solid {color}; border-radius:14px; padding:20px; text-align:center; margin-bottom:15px;'>
            <div style='font-family:Syne; font-size:1.05rem; font-weight:700; color:{color};'>{icon} {role_key}</div>
            <div style='color:#64748b; font-size:0.82rem; margin-top:6px;'>{cats_str}</div>
        </div>
        """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# PRACTICE SESSION PAGE
# ─────────────────────────────────────────────
elif st.session_state.page == "session":
    role = st.session_state.role
    cat  = st.session_state.category
    n_q  = st.session_state.num_questions
    questions = st.session_state.get("current_questions", [])

    if not questions:
        st.warning("No questions found for this session. Please start a new session from the sidebar.")
    else:
        if not st.session_state.session_done:
            idx = st.session_state.q_index
            q   = questions[idx]

            # Header
            st.markdown(f"""
            <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;'>
                <div style='font-family:Syne; font-size:0.8rem; text-transform:uppercase; letter-spacing:0.1em; color:#64748b;'>{role} · {cat}</div>
                <div style='font-family:Syne; font-size:0.85rem; color:#00e5ff;'>Question {idx+1} / {n_q}</div>
            </div>
            """, unsafe_allow_html=True)
            st.progress((idx) / n_q)

            st.markdown(f"""
            <div style='background:linear-gradient(135deg,#111827,#1a2235); border:1px solid rgba(0,229,255,0.15); border-radius:16px; padding:26px 28px; margin:18px 0;'>
                <div style='font-size:0.75rem; text-transform:uppercase; letter-spacing:0.12em; color:#00e5ff; margin-bottom:10px;'>Question</div>
                <div style='font-family:Syne; font-size:1.25rem; font-weight:600; color:#f1f5f9; line-height:1.5;'>{q["q"]}</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<div style='font-size:0.85rem; color:#64748b; margin-bottom:8px;'>🎙️ Or use voice to answer:</div>", unsafe_allow_html=True)
            audio_bytes = st.audio_input("Record Voice Answer", label_visibility="collapsed", key=f"audio_{idx}")

            if audio_bytes is not None:
                if f"prev_audio_{idx}" not in st.session_state or st.session_state[f"prev_audio_{idx}"] != audio_bytes.getvalue():
                    st.session_state[f"prev_audio_{idx}"] = audio_bytes.getvalue()
                    with st.spinner("Transcribing..."):
                        try:
                            r = sr.Recognizer()
                            with sr.AudioFile(audio_bytes) as source:
                                audio_data = r.record(source)
                                text = r.recognize_google(audio_data)
                                
                                current_text = st.session_state.get(f"ans_{idx}", "")
                                if current_text:
                                    st.session_state[f"ans_{idx}"] = current_text + "\n" + text
                                else:
                                    st.session_state[f"ans_{idx}"] = text
                                st.rerun()
                        except sr.UnknownValueError:
                            st.error("Could not understand the audio. Please try speaking clearer or closer to the microphone.")
                        except sr.RequestError as e:
                            st.error(f"Speech recognition service error: {e}")
                        except Exception as e:
                            st.error(f"Error processing audio: {e}")

            answer = st.text_area("Your Answer", height=160, placeholder="Type your answer here or record voice above...", key=f"ans_{idx}", label_visibility="collapsed")
            wc = len(answer.split()) if answer.strip() else 0
            st.markdown(f"<div style='font-size:0.78rem; color:#64748b; text-align:right;'>Word count: {wc}</div>", unsafe_allow_html=True)

            btn_cols = st.columns([1,1,4])
            has_answered = len(st.session_state.answers) > idx
            if not has_answered:
                submit = btn_cols[0].button("✅ Submit")
                skip   = btn_cols[1].button("⏭ Skip")

                if submit or skip:
                    final_answer = answer if submit else ""
                    score, kw_s, sim_s, flu_s, fb = score_answer_ml(
                        final_answer, q["ideal"], q["keywords"], vectorizer, clf, le
                    )
                    st.session_state.answers.append(final_answer)
                    st.session_state.scores.append(score)
                    st.session_state.detail_scores.append([score, kw_s, sim_s, flu_s])
                    st.session_state.feedbacks.append(fb)
                    st.rerun()
            else:
                score = st.session_state.scores[idx]
                kw_s, sim_s, flu_s = st.session_state.detail_scores[idx][1:]
                fb = st.session_state.feedbacks[idx]

                # Instant result
                with st.expander("📋 Instant Feedback", expanded=True):
                    r1, r2, r3, r4 = st.columns(4)
                    r1.plotly_chart(gauge_chart(score,   "Overall"),  use_container_width=True, config={"displayModeBar":False})
                    r2.plotly_chart(gauge_chart(kw_s,  "#Keywords", "#7c3aed"), use_container_width=True, config={"displayModeBar":False})
                    r3.plotly_chart(gauge_chart(sim_s, "Semantic",  "#f59e0b"), use_container_width=True, config={"displayModeBar":False})
                    r4.plotly_chart(gauge_chart(flu_s, "Fluency",   "#10b981"), use_container_width=True, config={"displayModeBar":False})

                    st.markdown(f'<div class="feedback-box">{fb}</div>', unsafe_allow_html=True)
                    st.markdown('<div style="font-size:0.85rem; color:#64748b; font-style:italic; margin-top:8px;">💡 Ideal answer hint:</div>', unsafe_allow_html=True)
                    st.markdown(f'<div style="background:#1a2235; border-radius:10px; padding:14px 18px; color:#94a3b8; font-size:0.88rem; line-height:1.6;">{q["ideal"]}</div>', unsafe_allow_html=True)

                if idx + 1 < n_q:
                    if st.button("Next Question →"):
                        st.session_state.q_index += 1
                        st.rerun()
                else:
                    if st.button("📊 View Results"):
                        st.session_state.session_done = True
                        st.rerun()

        else:
            # SESSION RESULTS
            scores = st.session_state.scores
            detail = st.session_state.detail_scores
            avg = int(np.mean(scores)) if scores else 0

            st.markdown(f"""
            <div style='text-align:center; padding:30px 0 20px;'>
                <div style='font-size:3.5rem;'>{"🏆" if avg>=80 else "✅" if avg>=65 else "📚"}</div>
                <div style='font-family:Syne; font-size:2rem; font-weight:800; color:#00e5ff;'>Session Complete!</div>
                <div style='color:#64748b; margin-top:6px;'>Here's your performance breakdown</div>
            </div>
            """, unsafe_allow_html=True)

            m1, m2, m3, m4 = st.columns(4)
            m1.markdown(f'<div class="metric-card"><div class="val">{avg}%</div><div class="label">Overall Score</div></div>', unsafe_allow_html=True)
            m2.markdown(f'<div class="metric-card"><div class="val">{len(scores)}</div><div class="label">Questions</div></div>', unsafe_allow_html=True)
            best = max(scores) if scores else 0
            m3.markdown(f'<div class="metric-card"><div class="val">{best}%</div><div class="label">Best Answer</div></div>', unsafe_allow_html=True)
            grade_lbl = "Excellent" if avg>=80 else "Good" if avg>=65 else "Average" if avg>=45 else "Keep Practicing"
            m4.markdown(f'<div class="metric-card"><div class="val" style="font-size:1.4rem">{grade_lbl}</div><div class="label">Grade</div></div>', unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            v1, v2 = st.columns([1,1])
            with v1:
                st.markdown('<div class="section-header">📊 Score Breakdown</div>', unsafe_allow_html=True)
                avg_detail = np.mean(detail, axis=0).tolist() if detail else [0,0,0,0]
                dim_scores = {"ML Score": int(avg_detail[0]), "Keyword Match": int(avg_detail[1]),
                              "Semantic Sim": int(avg_detail[2]), "Fluency": int(avg_detail[3])}
                st.plotly_chart(bar_breakdown_chart(dim_scores), use_container_width=True, config={"displayModeBar":False})

            with v2:
                st.markdown('<div class="section-header">🕸 Skill Radar</div>', unsafe_allow_html=True)
                radar_scores = {"Content": int(avg_detail[1]), "Relevance": int(avg_detail[2]),
                                "Fluency": int(avg_detail[3]), "Accuracy": int(avg_detail[0]),
                                "Structure": min(100, int(avg_detail[3]*0.9 + avg_detail[2]*0.1))}
                st.plotly_chart(radar_chart(radar_scores), use_container_width=True, config={"displayModeBar":False})

            if len(detail) > 1:
                st.markdown('<div class="section-header">🔥 Per-Question Heatmap</div>', unsafe_allow_html=True)
                st.plotly_chart(keyword_heatmap(detail), use_container_width=True, config={"displayModeBar":False})

            st.markdown('<div class="section-header">📋 Answer Review</div>', unsafe_allow_html=True)
            qs = st.session_state.get("current_questions", [])
            for i, (q, ans, sc, fb) in enumerate(zip(qs, st.session_state.answers, scores, st.session_state.feedbacks)):
                with st.expander(f"Q{i+1}: {q['q'][:60]}...  {grade_badge(sc)}", expanded=False):
                    st.markdown(f"**Your answer:** {ans if ans else '_Skipped_'}")
                    st.markdown(f'<div class="feedback-box">{fb}</div>', unsafe_allow_html=True)
                    st.markdown(f"**Ideal:** _{q['ideal']}_")

# ─────────────────────────────────────────────
# ANALYTICS PAGE
# ─────────────────────────────────────────────
elif st.session_state.page == "analytics":
    st.markdown('<h2 style="font-family:Syne; color:#00e5ff; letter-spacing:-0.02em;">📊 Progress Analytics</h2>', unsafe_allow_html=True)
    st.markdown('<p style="color:#64748b;">Based on sample training data — your real sessions will populate this over time.</p>', unsafe_allow_html=True)

    a1, a2, a3 = st.columns(3)
    a1.markdown('<div class="metric-card"><div class="val">76%</div><div class="label">Latest Score</div></div>', unsafe_allow_html=True)
    a2.markdown('<div class="metric-card"><div class="val">+24pts</div><div class="label">Improvement</div></div>', unsafe_allow_html=True)
    a3.markdown('<div class="metric-card"><div class="val">8</div><div class="label">Sessions Done</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">📈 Score Trends Over Sessions</div>', unsafe_allow_html=True)
    st.plotly_chart(progress_line_chart(SAMPLE_HISTORY), use_container_width=True, config={"displayModeBar":False})

    p1, p2 = st.columns(2)
    with p1:
        st.markdown('<div class="section-header">🧪 Role Comparison</div>', unsafe_allow_html=True)
        role_avg = SAMPLE_HISTORY.groupby("Role")["Avg Score"].mean().reset_index()
        fig_bar = px.bar(role_avg, x="Role", y="Avg Score",
            color="Avg Score", color_continuous_scale=["#0a0e1a","#00e5ff","#7c3aed"],
            text_auto=True)
        fig_bar.update_layout(**PLOT_LAYOUT, height=260, showlegend=False,
            yaxis=dict(range=[0,100], gridcolor="rgba(255,255,255,0.04)"),
            coloraxis_showscale=False)
        st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar":False})

    with p2:
        st.markdown('<div class="section-header">🎯 Dimension Distribution</div>', unsafe_allow_html=True)
        avg_dims = {
            "Confidence": SAMPLE_HISTORY["Confidence"].mean(),
            "Clarity":    SAMPLE_HISTORY["Clarity"].mean(),
            "Relevance":  SAMPLE_HISTORY["Relevance"].mean(),
        }
        fig_pie = go.Figure(go.Pie(
            labels=list(avg_dims.keys()), values=list(avg_dims.values()),
            hole=0.55, marker=dict(colors=["#00e5ff","#7c3aed","#f59e0b"]),
            textfont=dict(family="Syne", size=12),
        ))
        fig_pie.update_layout(**PLOT_LAYOUT, height=260, showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.15))
        st.plotly_chart(fig_pie, use_container_width=True, config={"displayModeBar":False})

    st.markdown('<div class="section-header">📋 Session History</div>', unsafe_allow_html=True)
    display_df = SAMPLE_HISTORY[["Session","Date","Role","Avg Score","Questions"]].copy()
    display_df["Date"] = display_df["Date"].dt.strftime("%b %d, %Y")
    display_df["Grade"] = display_df["Avg Score"].apply(
        lambda s: "🏆 Excellent" if s>=80 else "✅ Good" if s>=65 else "📊 Average" if s>=45 else "📚 Needs Work")
    st.dataframe(display_df, use_container_width=True, hide_index=True)

# ─────────────────────────────────────────────
# QUESTION BANK PAGE
# ─────────────────────────────────────────────
elif st.session_state.page == "bank":
    st.markdown('<h2 style="font-family:Syne; color:#00e5ff; letter-spacing:-0.02em;">📚 Question Bank</h2>', unsafe_allow_html=True)

    f1, f2 = st.columns(2)
    with f1: role_f = st.selectbox("Filter by Role", list(QUESTIONS_DB.keys()), key="bank_role")
    with f2: cat_f  = st.selectbox("Filter by Category", ["All Categories"] + list(QUESTIONS_DB[role_f].keys()), key="bank_cat")

    if cat_f == "All Categories":
        questions = []
        for c in QUESTIONS_DB[role_f].values():
            questions.extend(c)
    else:
        questions = QUESTIONS_DB[role_f][cat_f]
    st.markdown(f"<div style='color:#64748b; font-size:0.85rem; margin:8px 0 20px;'>Showing {len(questions)} questions for <b style='color:#00e5ff;'>{role_f} · {cat_f}</b></div>", unsafe_allow_html=True)

    for i, item in enumerate(questions):
        with st.expander(f"Q{i+1}. {item['q']}", expanded=False):
            st.markdown(f"**💡 Ideal Answer:**")
            st.markdown(f'<div class="feedback-box">{item["ideal"]}</div>', unsafe_allow_html=True)
            kw_html = "".join([f'<span style="background:rgba(0,229,255,0.1); color:#00e5ff; border:1px solid rgba(0,229,255,0.3); border-radius:6px; padding:3px 10px; font-size:0.8rem; margin:3px; display:inline-block;">{kw}</span>' for kw in item["keywords"]])
            st.markdown(f"**🔑 Key Terms:**<br>{kw_html}", unsafe_allow_html=True)

    st.markdown(f"<br><div style='color:#64748b; font-size:0.82rem; text-align:center;'>Total questions in bank: <b style='color:#e2e8f0;'>{sum(len(q) for r in QUESTIONS_DB.values() for q in r.values())}</b></div>", unsafe_allow_html=True)
