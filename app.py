import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

from modules.calorie_calculator import (
    calculate_bmr, calculate_tdee, calculate_target_calories, calculate_macros,
)
from modules.ml_model import predict_weight_change, predict_diet_recommendation
from modules.genetic_algorithm import run_genetic_algorithm

st.set_page_config(
    page_title="NutriAI",
    page_icon="🥗",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Session state ─────────────────────────────────────────────────────────────
for k, v in {
    "step": 0,
    "gender": "male",
    "age": 25,
    "height": 175,
    "weight": 75,
    "activity_level": "moderate",
    "goal": "lose_weight",
    "preferred_cuisine": "Any",
    "allergies": [],
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

TOTAL_STEPS = 6

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

*, html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    box-sizing: border-box;
}

/* Hide Streamlit chrome */
#MainMenu, footer { visibility: hidden; }
[data-testid="stHeader"] { display: none; }
[data-testid="stSidebar"] { display: none; }
[data-testid="collapsedControl"] { display: none; }
.stDeployButton { display: none; }

/* ── Background ── */
.stApp {
    background: linear-gradient(160deg, #FFF0F7 0%, #F0EEFF 50%, #E8F4FF 100%);
    min-height: 100vh;
}
.block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

/* ── Top bar ── */
.top-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1.1rem 1.5rem;
    border-bottom: 1px solid #E4D9F5;
}
.logo-text {
    font-size: 1.15rem;
    font-weight: 800;
    background: linear-gradient(90deg, #B48FD8, #8FBCE0);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -0.01em;
}
.step-label {
    font-size: 0.75rem;
    font-weight: 600;
    color: #A896C8;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

/* ── Progress dots ── */
.progress-bar-wrap {
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 1rem 1.5rem 0;
}
.p-dot {
    height: 4px;
    border-radius: 4px;
    flex: 1;
    background: #DDD6F0;
    transition: background 0.3s;
}
.p-dot.done { background: #B48FD8; }

/* ── Page wrapper ── */
.page-wrap {
    max-width: 480px;
    margin: 0 auto;
    padding: 3rem 1.5rem 6rem;
}

/* ── Question heading ── */
.q-title {
    font-size: 1.65rem;
    font-weight: 800;
    color: #3D2B6B;
    text-align: center;
    margin-bottom: 0.6rem;
    line-height: 1.2;
}
.q-sub {
    font-size: 0.82rem;
    font-weight: 500;
    color: #9B8ABF;
    text-align: center;
    margin-bottom: 2.5rem;
    letter-spacing: 0.04em;
}

/* ── Welcome ── */
.hero-badge {
    display: inline-block;
    background: rgba(180,143,216,0.15);
    border: 1px solid rgba(180,143,216,0.45);
    color: #9B6BC8;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 0.3rem 0.9rem;
    border-radius: 50px;
    margin-bottom: 1.5rem;
}
.hero-title {
    font-size: 2.4rem;
    font-weight: 900;
    color: #3D2B6B;
    line-height: 1.1;
    margin-bottom: 0.75rem;
    letter-spacing: -0.02em;
}
.hero-title span {
    background: linear-gradient(90deg, #B48FD8, #8FBCE0);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero-desc {
    font-size: 0.9rem;
    color: #9B8ABF;
    margin-bottom: 2.5rem;
    line-height: 1.6;
}
.hero-features {
    display: flex;
    gap: 1rem;
    margin-bottom: 2.5rem;
}
.hero-feat {
    flex: 1;
    background: rgba(255,255,255,0.7);
    border: 1px solid #E4D9F5;
    border-radius: 12px;
    padding: 0.9rem 0.75rem;
    text-align: center;
}
.hero-feat-icon { font-size: 1.4rem; margin-bottom: 0.3rem; }
.hero-feat-label {
    font-size: 0.72rem;
    font-weight: 600;
    color: #9B8ABF;
    letter-spacing: 0.04em;
}

/* ── PRIMARY button ── */
button[data-testid="baseButton-primary"] {
    background: linear-gradient(135deg, #C4A0E8 0%, #9BC4E8 100%) !important;
    color: #3D2B6B !important;
    border: none !important;
    border-radius: 14px !important;
    font-weight: 800 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.02em !important;
    padding: 0.8rem 2rem !important;
    transition: opacity 0.2s !important;
    box-shadow: 0 4px 20px rgba(180,143,216,0.35) !important;
}
button[data-testid="baseButton-primary"]:hover {
    opacity: 0.88 !important;
}

/* ── SECONDARY button = selectable card ── */
button[data-testid="baseButton-secondary"] {
    background: rgba(255,255,255,0.75) !important;
    border: 1.5px solid #DDD6F0 !important;
    border-radius: 14px !important;
    color: #3D2B6B !important;
    font-weight: 500 !important;
    font-size: 0.95rem !important;
    padding: 1.1rem 1.3rem !important;
    text-align: left !important;
    justify-content: flex-start !important;
    height: auto !important;
    min-height: 70px !important;
    transition: all 0.15s !important;
    white-space: normal !important;
    line-height: 1.4 !important;
    margin-bottom: 0.3rem !important;
}
button[data-testid="baseButton-secondary"]:hover {
    background: rgba(180,143,216,0.12) !important;
    border-color: #B48FD8 !important;
    color: #3D2B6B !important;
    box-shadow: 0 0 0 1px rgba(180,143,216,0.3) !important;
}

/* Gender cards */
.gender-col button[data-testid="baseButton-secondary"] {
    min-height: 160px !important;
    justify-content: center !important;
    text-align: center !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
    flex-direction: column !important;
    margin-bottom: 0 !important;
}

/* Back button */
.back-wrap button[data-testid="baseButton-secondary"] {
    min-height: unset !important;
    padding: 0.4rem 0.9rem !important;
    font-size: 0.82rem !important;
    border-radius: 8px !important;
    color: #9B8ABF !important;
    border-color: #DDD6F0 !important;
    font-weight: 600 !important;
    background: transparent !important;
}
.back-wrap button[data-testid="baseButton-secondary"]:hover {
    color: #3D2B6B !important;
    border-color: #B48FD8 !important;
    background: rgba(180,143,216,0.08) !important;
    box-shadow: none !important;
}

/* ── Number input ── */
.stNumberInput > div > div > input {
    background: rgba(255,255,255,0.8) !important;
    border: 1.5px solid #DDD6F0 !important;
    border-radius: 14px !important;
    color: #3D2B6B !important;
    font-size: 2rem !important;
    font-weight: 800 !important;
    text-align: center !important;
    padding: 1rem !important;
}
.stNumberInput > div > div > input:focus {
    border-color: #B48FD8 !important;
    box-shadow: 0 0 0 2px rgba(180,143,216,0.2) !important;
}
.stNumberInput label {
    color: #9B8ABF !important;
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.07em !important;
}
.stNumberInput button {
    background: rgba(255,255,255,0.7) !important;
    border: 1px solid #DDD6F0 !important;
    color: #3D2B6B !important;
    border-radius: 8px !important;
}

/* ── Select / Multiselect ── */
.stSelectbox > div > div,
.stMultiSelect > div > div {
    background: rgba(255,255,255,0.8) !important;
    border: 1.5px solid #DDD6F0 !important;
    border-radius: 14px !important;
    color: #3D2B6B !important;
}
.stSelectbox label, .stMultiSelect label {
    color: #9B8ABF !important;
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.07em !important;
}
[data-baseweb="select"] * { color: #3D2B6B !important; }
[data-baseweb="menu"] {
    background: #FAF6FF !important;
    border: 1px solid #DDD6F0 !important;
    border-radius: 12px !important;
}

/* ── Metric cards ── */
div[data-testid="metric-container"] {
    background: rgba(255,255,255,0.75);
    border: 1px solid #DDD6F0;
    border-radius: 16px;
    padding: 1.2rem 1.4rem;
}
div[data-testid="metric-container"] [data-testid="stMetricLabel"] {
    color: #9B8ABF;
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.07em;
}
div[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #3D2B6B;
    font-size: 1.5rem;
    font-weight: 800;
}
div[data-testid="metric-container"] [data-testid="stMetricDelta"] {
    color: #B48FD8;
    font-size: 0.78rem;
    font-weight: 600;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: transparent;
    border-bottom: 1px solid #DDD6F0;
    gap: 0;
}
.stTabs [data-baseweb="tab"] {
    background: transparent;
    border: none;
    color: #9B8ABF;
    font-weight: 600;
    font-size: 0.82rem;
    padding: 0.75rem 1.2rem;
}
.stTabs [aria-selected="true"] {
    color: #7B4FBF !important;
    border-bottom: 2px solid #B48FD8 !important;
    background: transparent !important;
}
.stTabs [data-baseweb="tab-panel"] {
    background: transparent;
    padding-top: 1.5rem;
}

/* ── Alerts ── */
.stAlert {
    background: rgba(255,255,255,0.7) !important;
    border: 1px solid #DDD6F0 !important;
    border-radius: 14px !important;
    color: #5A4080 !important;
}

/* ── Dataframe ── */
.stDataFrame {
    border-radius: 14px;
    border: 1px solid #DDD6F0;
    overflow: hidden;
}

/* ── Badges ── */
.bmi-badge {
    display: inline-block;
    padding: 0.2rem 0.7rem;
    border-radius: 50px;
    font-weight: 700;
    font-size: 0.78rem;
}
.diet-tag {
    background: rgba(180,143,216,0.15);
    border: 1px solid rgba(180,143,216,0.45);
    color: #7B4FBF;
    display: inline-block;
    padding: 0.2rem 0.8rem;
    border-radius: 50px;
    font-weight: 700;
    font-size: 0.85rem;
}

h2, h3 { color: #3D2B6B !important; font-weight: 700; }
hr { border: none; border-top: 1px solid #DDD6F0; margin: 1rem 0; }

p, label, .stMarkdown { color: #5A4080; }
</style>
""", unsafe_allow_html=True)


# ── Helpers ───────────────────────────────────────────────────────────────────
def bmi_category(bmi):
    if bmi < 18.5: return "Underweight", "#FF9800"
    if bmi < 25:   return "Normal",      "#00BFA5"
    if bmi < 30:   return "Overweight",  "#FF9800"
    return "Obese", "#F44336"


def top_bar(show_back=False, step_txt=""):
    c1, c2, c3 = st.columns([1, 4, 1])
    with c1:
        if show_back:
            st.markdown('<div class="back-wrap">', unsafe_allow_html=True)
            if st.button("← Back", key="back_btn", type="secondary"):
                st.session_state.step -= 1
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown(
            f'<div style="text-align:center;padding-top:0.25rem;">'
            f'<span class="logo-text">NutriAI</span>'
            f'{"<br><span class=step-label>" + step_txt + "</span>" if step_txt else ""}'
            f'</div>',
            unsafe_allow_html=True,
        )
    with c3:
        pass


def progress(current, total=TOTAL_STEPS):
    dots = "".join(
        f'<div class="p-dot {"done" if i < current else ""}"></div>'
        for i in range(total)
    )
    st.markdown(f'<div class="progress-bar-wrap">{dots}</div>', unsafe_allow_html=True)


def qtitle(title, sub=""):
    st.markdown(
        f'<div class="q-title">{title}</div>'
        + (f'<div class="q-sub">{sub}</div>' if sub else '<div style="margin-bottom:2rem;"></div>'),
        unsafe_allow_html=True,
    )


def pw():
    """Open page wrapper div."""
    st.markdown('<div style="max-width:480px;margin:0 auto;padding:3rem 1.5rem 6rem;">', unsafe_allow_html=True)


def pw_close():
    st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# STEP 0 — Welcome
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.step == 0:
    top_bar(show_back=False)
    pw()
    st.markdown("""
    <div style="text-align:center;padding-top:3rem;">
        <div class="hero-badge">✦ AI-Powered Nutrition</div>
        <div class="hero-title">Your <span>perfect diet</span><br>starts here.</div>
        <div class="hero-desc">
            Answer a few quick questions and get a fully personalised<br>
            meal plan optimised by machine learning & genetic algorithms.
        </div>
    </div>
    <div class="hero-features">
        <div class="hero-feat">
            <div class="hero-feat-icon">🧮</div>
            <div class="hero-feat-label">Calorie Calc</div>
        </div>
        <div class="hero-feat">
            <div class="hero-feat-icon">🤖</div>
            <div class="hero-feat-label">ML Model</div>
        </div>
        <div class="hero-feat">
            <div class="hero-feat-icon">🧬</div>
            <div class="hero-feat-label">Genetic AI</div>
        </div>
        <div class="hero-feat">
            <div class="hero-feat-icon">🍽️</div>
            <div class="hero-feat-label">Meal Plan</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Get Started →", width="stretch", type="primary"):
        st.session_state.step = 1
        st.rerun()
    pw_close()


# ══════════════════════════════════════════════════════════════════════════════
# STEP 1 — Gender
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.step == 1:
    top_bar(show_back=True, step_txt="Step 1 of 6")
    progress(1)
    pw()
    qtitle("Who are you?", "This helps us calibrate your calorie needs")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="gender-col">', unsafe_allow_html=True)
        if st.button("👨\n\nMale", key="g_male", width="stretch", type="secondary"):
            st.session_state.gender = "male"
            st.session_state.step = 2
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="gender-col">', unsafe_allow_html=True)
        if st.button("👩\n\nFemale", key="g_female", width="stretch", type="secondary"):
            st.session_state.gender = "female"
            st.session_state.step = 2
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    pw_close()


# ══════════════════════════════════════════════════════════════════════════════
# STEP 2 — Age
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.step == 2:
    top_bar(show_back=True, step_txt="Step 2 of 6")
    progress(2)
    pw()
    qtitle("How old are you?")
    age_val = st.number_input(
        "Age", min_value=10, max_value=100,
        value=st.session_state.age, step=1, label_visibility="collapsed",
    )
    st.markdown(
        '<div style="text-align:center;font-size:0.8rem;color:#9B8ABF;'
        'letter-spacing:0.08em;text-transform:uppercase;margin:0.5rem 0 2rem;">years old</div>',
        unsafe_allow_html=True,
    )
    if st.button("Continue →", width="stretch", type="primary", key="age_next"):
        st.session_state.age = int(age_val)
        st.session_state.step = 3
        st.rerun()
    pw_close()


# ══════════════════════════════════════════════════════════════════════════════
# STEP 3 — Height & Weight
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.step == 3:
    top_bar(show_back=True, step_txt="Step 3 of 6")
    progress(3)
    pw()
    qtitle("Your measurements", "Height and current body weight")
    c1, c2 = st.columns(2)
    with c1:
        h_val = st.number_input("Height (cm)", min_value=100, max_value=230,
                                 value=st.session_state.height, step=1)
    with c2:
        w_val = st.number_input("Weight (kg)", min_value=30, max_value=200,
                                 value=st.session_state.weight, step=1)
    st.markdown('<div style="margin-top:1.5rem;">', unsafe_allow_html=True)
    if st.button("Continue →", width="stretch", type="primary", key="hw_next"):
        st.session_state.height = int(h_val)
        st.session_state.weight = int(w_val)
        st.session_state.step = 4
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    pw_close()


# ══════════════════════════════════════════════════════════════════════════════
# STEP 4 — Activity Level
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.step == 4:
    top_bar(show_back=True, step_txt="Step 4 of 6")
    progress(4)
    pw()
    qtitle("How active are you?", "On a typical week")

    for key, label in [
        ("sedentary",   "🪑   Sedentary  ·  Little or no exercise"),
        ("light",       "🚶   Light  ·  1–3 days per week"),
        ("moderate",    "🏃   Moderate  ·  3–5 days per week"),
        ("active",      "🏋️   Active  ·  6–7 days per week"),
        ("very_active", "⚡   Very Active  ·  Intense daily training"),
    ]:
        if st.button(label, key=f"act_{key}", width="stretch", type="secondary"):
            st.session_state.activity_level = key
            st.session_state.step = 5
            st.rerun()
    pw_close()


# ══════════════════════════════════════════════════════════════════════════════
# STEP 5 — Goal
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.step == 5:
    top_bar(show_back=True, step_txt="Step 5 of 6")
    progress(5)
    pw()
    qtitle("What's your main goal?", "We'll optimise your plan around this")

    for key, label in [
        ("lose_weight",     "🔻   Lose Weight  ·  Burn fat, feel lighter"),
        ("maintain_weight", "⚖️   Maintain Weight  ·  Stay balanced"),
        ("gain_weight",     "🔺   Gain Weight  ·  Build strength & mass"),
    ]:
        if st.button(label, key=f"goal_{key}", width="stretch", type="secondary"):
            st.session_state.goal = key
            st.session_state.step = 6
            st.rerun()
    pw_close()


# ══════════════════════════════════════════════════════════════════════════════
# STEP 6 — Preferences
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.step == 6:
    top_bar(show_back=True, step_txt="Step 6 of 6")
    progress(6)
    pw()
    qtitle("Food preferences", "Almost done — just a couple more things")

    cuisine = st.selectbox(
        "Preferred Cuisine",
        ["Any", "Turkish", "Mediterranean", "Asian", "Western"],
        index=["Any", "Turkish", "Mediterranean", "Asian", "Western"].index(
            st.session_state.preferred_cuisine
        ),
        format_func=lambda x: {
            "Any": "🌍  Any cuisine",
            "Turkish": "🇹🇷  Turkish",
            "Mediterranean": "🫒  Mediterranean",
            "Asian": "🍜  Asian",
            "Western": "🍔  Western",
        }[x],
    )
    allergies = st.multiselect(
        "Allergies / Intolerances",
        ["Milk", "Gluten", "Egg", "Nuts", "Fish", "Soy"],
        default=st.session_state.allergies,
        placeholder="Select any that apply…",
    )
    st.markdown('<div style="margin-top:2rem;">', unsafe_allow_html=True)
    if st.button("Generate My Plan →", width="stretch", type="primary", key="gen"):
        st.session_state.preferred_cuisine = cuisine
        st.session_state.allergies = allergies
        st.session_state.step = 7
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    pw_close()


# ══════════════════════════════════════════════════════════════════════════════
# STEP 7 — Results
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.step == 7:
    top_bar(show_back=True)

    st.markdown('<div style="max-width:680px;margin:0 auto;padding:2rem 1.5rem 4rem;">', unsafe_allow_html=True)

    with st.spinner("Generating your personalised plan…"):
        age, gender = st.session_state.age, st.session_state.gender
        height, weight = st.session_state.height, st.session_state.weight
        activity_level = st.session_state.activity_level
        goal = st.session_state.goal
        preferred_cuisine = st.session_state.preferred_cuisine
        allergies = st.session_state.allergies

        bmr        = calculate_bmr(gender, weight, height, age)
        tdee       = calculate_tdee(bmr, activity_level)
        target_cal = calculate_target_calories(tdee, goal)
        macros     = calculate_macros(target_cal, weight)
        bmi        = weight / ((height / 100) ** 2)
        bmi_cat, bmi_color = bmi_category(bmi)

        user_data = {
            "age": age, "gender": gender, "height": height,
            "current_weight": weight, "bmi": bmi, "bmr": bmr, "tdee": tdee,
            "daily_calories": target_cal, "activity_level": activity_level,
            "protein": macros["protein"], "carbs": macros["carbs"],
            "fat": macros["fat"], "goal": goal,
        }
        weight_change = predict_weight_change(user_data)
        diet_rec      = predict_diet_recommendation(user_data)
        meal_plan, ga_result = run_genetic_algorithm(
            targets={"calories": target_cal, "protein": macros["protein"],
                     "carbs": macros["carbs"], "fat": macros["fat"]},
            diet_recommendation=diet_rec,
            allergies=allergies,
            preferred_cuisine=preferred_cuisine,
        )

    # Results hero
    st.markdown(f"""
    <div style="text-align:center;padding:1.5rem 0 2rem;">
        <div style="font-size:0.75rem;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;
                    color:#B48FD8;margin-bottom:0.5rem;">✦ Your plan is ready</div>
        <div style="font-size:1.9rem;font-weight:900;color:#3D2B6B;letter-spacing:-0.02em;">
            {target_cal:.0f} kcal / day
        </div>
        <div style="font-size:0.85rem;color:#9B8ABF;margin-top:0.3rem;">
            BMI {bmi:.1f} &nbsp;·&nbsp; {bmi_cat} &nbsp;·&nbsp; {diet_rec}
        </div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["📊 Summary", "🍽️ Meal Plan", "📈 Charts", "🧬 AI Details"])

    # ── Summary ──────────────────────────────────────────────────────────────
    with tab1:
        st.subheader("Energy")
        c1, c2, c3 = st.columns(3)
        c1.metric("🔥 BMR",            f"{bmr:.0f} kcal")
        c2.metric("⚡ TDEE",           f"{tdee:.0f} kcal")
        c3.metric("🎯 Target",         f"{target_cal:.0f} kcal",
                  delta=f"{target_cal - tdee:+.0f} vs TDEE")
        st.divider()
        st.subheader("Macros")
        c4, c5, c6 = st.columns(3)
        c4.metric("🥩 Protein", f"{macros['protein']} g")
        c5.metric("🍞 Carbs",   f"{macros['carbs']} g")
        c6.metric("🫒 Fat",     f"{macros['fat']} g")
        st.divider()
        st.subheader("Health")
        h1, h2, h3 = st.columns(3)
        with h1:
            st.markdown(
                f"**BMI:** {bmi:.1f} "
                f'<span class="bmi-badge" style="background:{bmi_color};color:#0D1B2A">{bmi_cat}</span>',
                unsafe_allow_html=True,
            )
        with h2:
            icon = "🔻" if weight_change < 0 else ("🔺" if weight_change > 0 else "⚖️")
            st.markdown(f"**Weekly change:** {icon} {weight_change:+.2f} kg")
        with h3:
            st.markdown(f"**Diet:** <span class='diet-tag'>{diet_rec}</span>", unsafe_allow_html=True)

    # ── Meal Plan ─────────────────────────────────────────────────────────────
    with tab2:
        if meal_plan.empty:
            st.error("No meals found — try removing some allergy filters.")
        else:
            plan_cal  = meal_plan["Calories"].sum()
            plan_prot = meal_plan["Protein"].sum()
            plan_carb = meal_plan["Carbs"].sum()
            plan_fat  = meal_plan["Fat"].sum()
            st.subheader("Today's Meal Plan")
            st.dataframe(meal_plan, width="stretch", hide_index=True)
            st.divider()
            st.subheader("Totals vs Targets")
            t1, t2, t3, t4 = st.columns(4)
            t1.metric("Calories", f"{plan_cal:.0f}",  delta=f"{plan_cal - target_cal:+.0f}")
            t2.metric("Protein",  f"{plan_prot:.1f} g", delta=f"{plan_prot - macros['protein']:+.1f}")
            t3.metric("Carbs",    f"{plan_carb:.1f} g", delta=f"{plan_carb - macros['carbs']:+.1f}")
            t4.metric("Fat",      f"{plan_fat:.1f} g",  delta=f"{plan_fat - macros['fat']:+.1f}")

    # ── Charts ────────────────────────────────────────────────────────────────
    with tab3:
        if meal_plan.empty:
            st.warning("No meal plan to chart.")
        else:
            plan_cal  = meal_plan["Calories"].sum()
            plan_prot = meal_plan["Protein"].sum()
            plan_carb = meal_plan["Carbs"].sum()
            plan_fat  = meal_plan["Fat"].sum()

            ch1, ch2 = st.columns(2)
            _layout = dict(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#5A4080"),
                legend=dict(orientation="h", font=dict(color="#9B8ABF")),
            )
            with ch1:
                pie = go.Figure(go.Pie(
                    labels=["Protein", "Carbs", "Fat"],
                    values=[macros["protein"], macros["carbs"], macros["fat"]],
                    hole=0.45,
                    marker_colors=["#C4A0E8", "#8FBCE0", "#F7C5D8"],
                ))
                pie.update_layout(title="Macro Distribution", **_layout)
                st.plotly_chart(pie, width="stretch")
            with ch2:
                bar = go.Figure()
                cats = ["Calories", "Protein", "Carbs", "Fat"]
                bar.add_trace(go.Bar(name="Target",
                                     x=cats, y=[target_cal, macros["protein"], macros["carbs"], macros["fat"]],
                                     marker_color="#C4A0E8"))
                bar.add_trace(go.Bar(name="Plan",
                                     x=cats, y=[plan_cal, plan_prot, plan_carb, plan_fat],
                                     marker_color="#8FBCE0"))
                bar.update_layout(title="Target vs Plan", barmode="group", **_layout)
                st.plotly_chart(bar, width="stretch")

            st.subheader("Calories per Meal")
            meal_bar = px.bar(
                meal_plan,
                x="Meal Type" if "Meal Type" in meal_plan.columns else meal_plan.columns[0],
                y="Calories", color="Calories",
                color_continuous_scale=[[0,"#E8D5F5"],[0.5,"#C4A0E8"],[1,"#8FBCE0"]],
                text_auto=".0f",
            )
            meal_bar.update_layout(showlegend=False, **_layout)
            st.plotly_chart(meal_bar, width="stretch")

    # ── AI Details ────────────────────────────────────────────────────────────
    with tab4:
        st.subheader("🤖 Machine Learning")
        ml1, ml2, ml3 = st.columns(3)
        ml1.metric("Weekly Change",     f"{weight_change:+.2f} kg")
        ml2.metric("Recommended Diet",  diet_rec)
        ml3.metric("BMI",               f"{bmi:.1f} – {bmi_cat}")
        st.info("Calorie-balance model for weight prediction + BMI/goal-based diet classification.")
        st.divider()
        st.subheader("🧬 Genetic Algorithm")
        ga1, ga2, ga3, ga4 = st.columns(4)
        ga1.metric("Best Fitness",    ga_result["best_fitness"])
        ga2.metric("Best Error",      ga_result["best_error"])
        ga3.metric("Mutation Rate",   ga_result["mutation_rate"])
        ga4.metric("Population Size", ga_result["population_size"])
        st.info("GA optimises meal combos against calorie/macro targets (protein ×5, fat ×3, calories ×2, carbs ×2).")

    st.divider()
    if st.button("← Start Over", width="stretch", type="primary", key="restart"):
        for k in ["step","gender","age","height","weight",
                  "activity_level","goal","preferred_cuisine","allergies"]:
            if k in st.session_state:
                del st.session_state[k]
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
