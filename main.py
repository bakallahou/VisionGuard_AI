import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import sqlite3  # 📌 IMPORT POUR LA BASE DE DONNÉES
from database.database import init_db
from app.auth import login  # ✅ AJOUTÉ (ÉTAPE 4)

# =========================================
# CONFIG PAGE
# =========================================

st.set_page_config(
    page_title="VisionGuard AI",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)
init_db()

# ✅ AJOUTÉ (ÉTAPE 5)
if "authenticated" not in st.session_state:

    st.session_state["authenticated"] = False

# =========================================
# CSS PREMIUM CYBERPUNK GLASSMORPHISM
# =========================================

st.markdown("""
<style>

/* =====================================
BACKGROUND
===================================== */

.stApp {
    background: linear-gradient(
        135deg,
        #0f172a,
        #111827,
        #1e293b
    );
    color: white;
}

/* =====================================
SIDEBAR
===================================== */

[data-testid="stSidebar"] {

    background: linear-gradient(
        180deg,
        rgba(15,23,42,0.95),
        rgba(30,41,59,0.95)
    );

    backdrop-filter: blur(25px);

    border-right: 1px solid rgba(0,255,255,0.2);

    box-shadow:
        0 0 30px rgba(0,255,255,0.2);

    transition: 0.3s;
}

/* =====================================
HEADERS
===================================== */

h1, h2, h3, h4 {
    color: #00FFFF;
    text-shadow: 0px 0px 15px #00FFFF;
}

/* =====================================
GLASS KPI CARDS
===================================== */

.metric-card {

    background: rgba(255,255,255,0.08);

    border: 1px solid rgba(255,255,255,0.1);

    backdrop-filter: blur(20px);

    padding: 25px;

    border-radius: 25px;

    text-align: center;

    box-shadow:
        0 0 20px rgba(0,255,255,0.3),
        0 0 40px rgba(0,255,255,0.1);

    transition: 0.3s;
}

/* =====================================
HOVER EFFECT
===================================== */

.metric-card:hover {

    transform: translateY(-5px);

    box-shadow:
        0 0 25px rgba(0,255,255,0.6),
        0 0 50px rgba(0,255,255,0.2);
}

/* =====================================
BIG FONT
===================================== */

.big-font {

    font-size: 42px !important;

    font-weight: bold;

    color: #00FFFF;

    text-shadow: 0px 0px 15px #00FFFF;
}

/* =====================================
SMALL FONT
===================================== */

.small-font {

    color: #cbd5e1;

    font-size: 15px;
}

/* =====================================
BUTTONS
===================================== */

.stButton>button {

    background: linear-gradient(
        135deg,
        #06b6d4,
        #3b82f6
    );

    color: white;

    border: none;

    border-radius: 15px;

    padding: 10px 25px;

    font-weight: bold;

    box-shadow:
        0 0 20px rgba(59,130,246,0.5);

    transition: 0.3s;
}

.stButton>button:hover {

    transform: scale(1.05);

    box-shadow:
        0 0 30px rgba(59,130,246,0.8);
}

/* =====================================
DATAFRAME
===================================== */

[data-testid="stDataFrame"] {

    background: rgba(255,255,255,0.05);

    border-radius: 20px;

    padding: 10px;
}

/* =====================================
SUCCESS BOX
===================================== */

.stAlert {

    border-radius: 15px;
}

/* =====================================
SIDEBAR TEXT
===================================== */

section[data-testid="stSidebar"] * {

    color: white !important;

    font-weight: 500;
}

/* =====================================
RADIO BUTTONS
===================================== */

.stRadio > div {

    background: rgba(255,255,255,0.05);

    padding: 10px;

    border-radius: 15px;
}

/* =====================================
TITLE GLOW
===================================== */

.sidebar-title {

    font-size: 28px;

    font-weight: bold;

    color: #00FFFF;

    text-shadow:
        0 0 10px #00FFFF,
        0 0 20px #00FFFF;
}

</style>
""", unsafe_allow_html=True)

# =========================================
# LOGIN CHECK (✅ AJOUTÉ ÉTAPE 6)
# =========================================

if not st.session_state["authenticated"]:

    login()

    st.stop()

# =========================================
# SIDEBAR
# =========================================

st.sidebar.markdown(
    """
    <div class="sidebar-title">
        🚀 VisionGuard AI
    </div>
    """,
    unsafe_allow_html=True
)

# =====================================
# LOGOUT BUTTON
# =====================================

if st.sidebar.button("Logout"):

    st.session_state["authenticated"] = False

    st.rerun()

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Real-Time Monitoring",
        "Analytics",
        "Reports",
        "Settings"
    ]
)

# =========================================
# DASHBOARD
# =========================================

if page == "Dashboard":

    st.title("🧠 AI Smart Attendance Dashboard")

    # =========================================
    # DATABASE CONNECTION
    # =========================================
    conn = sqlite3.connect("database/attendance.db")
    query = "SELECT * FROM attendance"
    df = pd.read_sql(query, conn)
    conn.close()

    # =========================================
    # REAL STUDENT LIST
    # =========================================

    student_list = [
        "AATIQ_ABDERRAHIM",
        "ALILOU_FATIMA_ZAHRAE",
        "ATMANI_SAAD",
        "AZOUGAGH_HAYAT",
        "BAKALLA_HOUSSAM",
        "BEN_JELLOUN_ISMAIL",
        "BENSALEM_BADR",
        "BENTANI_AYA",
        "CHAAIRI_MARIA",
        "EL_HAZATI_LAMYAE",
        "ELAAMRI_NAIMA",
        "ETTAHALY_AMINE",
        "GOURINI_HIND",
        "GROUZ_YASSMINE",
        "HAFIDI_FAICAL",
        "KAMSAOUI_YASSIR",
        "KHABBA_JAWAD",
        "KORSAGA_KISWENDSIDA_LANDRY",
        "LAABADI_MOHAMMED",
        "LASFAR_YASIR",
        "LEMNOUNI_HIBA",
        "LHAOU_MOHAMED",
        "MALHOUNI_MARWANE",
        "MRANI_ALAOUI_SALMA",
        "OUHDDOU_HAMZA",
        "OUHNA_FARAH",
        "OUMHA_INSAF",
        "SOSSEY_SARA",
        "SOUINIA_SAFAA",
        "STITOU_KHADIJA"
    ]

    # =========================================
    # REAL CALCULATIONS
    # =========================================

    total_students = len(student_list)

    # Récupération des étudiants uniques présents aujourd'hui (depuis la colonne 'name')
    if not df.empty and "name" in df.columns:
        present_students = df["name"].unique()
        present_today = len(present_students)
    else:
        present_today = 0

    absent_today = total_students - present_today

    attendance_rate = round(
        (present_today / total_students) * 100,
        2
    ) if total_students > 0 else 0.0

    # =========================================
    # KPI CARDS
    # =========================================
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="big-font">{total_students}</div>
            <div class="small-font">Total Students</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="big-font">{present_today}</div>
            <div class="small-font">Present Today</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="big-font">{attendance_rate}%</div>
            <div class="small-font">Attendance Rate</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="big-font">{absent_today}</div>
            <div class="small-font">Absent Students</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # =====================================
    # AI SYSTEM STATUS PANEL
    # =====================================

    st.subheader("🛡️ AI System Status")

    status_col1, status_col2, status_col3, status_col4 = st.columns(4)

    with status_col1:

        st.markdown("""
        <div class="metric-card">
            <div class="big-font">ONLINE</div>
            <div class="small-font">
                Camera Status
            </div>
        </div>
        """, unsafe_allow_html=True)

    with status_col2:

        st.markdown("""
        <div class="metric-card">
            <div class="big-font">ACTIVE</div>
            <div class="small-font">
                AI Engine
            </div>
        </div>
        """, unsafe_allow_html=True)

    with status_col3:

        st.markdown("""
        <div class="metric-card">
            <div class="big-font">SECURED</div>
            <div class="small-font">
                Anti-Spoofing
            </div>
        </div>
        """, unsafe_allow_html=True)

    with status_col4:

        st.markdown("""
        <div class="metric-card">
            <div class="big-font">CONNECTED</div>
            <div class="small-font">
                Database
            </div>
        </div>
        """, unsafe_allow_html=True)

    # =====================================
    # REAL ANALYTICS FROM DATABASE
    # =====================================

    analytics_query = """
    SELECT date, COUNT(*) as total
    FROM attendance
    GROUP BY date
    ORDER BY date
    """

    conn = sqlite3.connect("database/attendance.db")
    analytics_df = pd.read_sql(analytics_query, conn)
    conn.close()

    if not analytics_df.empty:
        fig = px.line(
            analytics_df,
            x="date",
            y="total",
            markers=True,
            title="Real Attendance Analytics"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No analytics data available yet.")

    # =====================================
    # LIVE ACTIVITY FEED
    # =====================================

    st.subheader("⚡ Live Activity Feed")

    if not df.empty:
        # Trie par heure décroissante pour afficher les détections les plus récentes d'abord
        latest_activity = df.sort_values(
            by="time",
            ascending=False
        ).head(5)

        for _, row in latest_activity.iterrows():
            st.success(
                f"🟢 {row['name']} detected at {row['time']}"
            )
    else:
        st.warning("No activity detected yet.")

    # =====================================
    # TABLE
    # =====================================

    st.subheader("📋 Today's Attendance")

    if not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No attendance records found in the database yet.")

# =========================================
# REAL TIME PAGE
# =========================================

elif page == "Real-Time Monitoring":

    from ai_engine.recognition import run_face_recognition

    run_face_recognition()

# =========================================
# ANALYTICS
# =========================================

elif page == "Analytics":

    st.title("📊 Advanced AI Analytics")

    # =====================================
    # DATABASE CONNECTION
    # =====================================

    conn = sqlite3.connect(
        "database/attendance.db"
    )

    # =====================================
    # DAILY ATTENDANCE ANALYTICS
    # =====================================

    daily_query = """
    SELECT date, COUNT(*) as total
    FROM attendance
    GROUP BY date
    ORDER BY date
    """

    daily_df = pd.read_sql(
        daily_query,
        conn
    )

    # =====================================
    # STUDENT ATTENDANCE ANALYTICS
    # =====================================

    student_query = """
    SELECT name, COUNT(*) as total
    FROM attendance
    GROUP BY name
    ORDER BY total DESC
    """

    student_df = pd.read_sql(
        student_query,
        conn
    )

    conn.close()

    # =====================================
    # DAILY GRAPH
    # =====================================

    st.subheader("📈 Daily Attendance")

    if not daily_df.empty:

        fig1 = px.line(
            daily_df,
            x="date",
            y="total",
            markers=True,
            title="Daily Attendance Analytics"
        )

        st.plotly_chart(
            fig1,
            use_container_width=True
        )

    else:

        st.warning(
            "No attendance analytics available."
        )

    # =====================================
    # STUDENT GRAPH
    # =====================================

    st.subheader("👨‍🎓 Student Attendance Ranking")

    if not student_df.empty:

        fig2 = px.bar(
            student_df,
            x="name",
            y="total",
            title="Top Attendance Students"
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

        st.dataframe(
            student_df,
            use_container_width=True
        )

    else:

        st.warning(
            "No student analytics available."
        )

# =========================================
# REPORTS
# =========================================

elif page == "Reports":

    from app.reports import (
        generate_pdf_report,
        generate_excel_report,
        send_email_report
    )

    st.title("📄 AI Reports")

    st.write("Generate professional attendance reports.")

    if st.button("Generate PDF Report"):

        report_file = generate_pdf_report()

        st.success(f"Report generated : {report_file}")

    # =====================================
    # SEND EMAIL REPORT (✅ AJOUTÉ ICI)
    # =====================================

    if st.button("Send PDF By Email"):

        report_file = generate_pdf_report()

        send_email_report(report_file)

        st.success(
            "Email sent successfully."
        )

    if st.button("Generate Excel Report"):

        excel_file = generate_excel_report()

        st.success(
            f"Excel report generated : {excel_file}"
        )

# =========================================
# SETTINGS
# =========================================

elif page == "Settings":

    st.title("⚙️ System Settings")

    st.write("Configure AI system parameters.")