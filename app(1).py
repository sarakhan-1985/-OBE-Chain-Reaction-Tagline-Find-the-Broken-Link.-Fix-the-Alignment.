import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="OBE Chain Reaction", page_icon="🔗", layout="centered")

# -------------------- SHARED DATABASE --------------------
conn = sqlite3.connect("obe_chain_responses.db", check_same_thread=False)
cur = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS responses (
    group_name TEXT PRIMARY KEY,
    case_name TEXT,
    broken_link TEXT,
    repair TEXT,
    submitted_at TEXT
)
""")
conn.commit()

# -------------------- STYLE --------------------
st.markdown("""
<style>
.main-title {text-align:center;font-size:44px;font-weight:900;color:#26386f;margin-bottom:0}
.subtitle {text-align:center;font-size:20px;font-weight:600;color:#168b78;margin-bottom:22px}
.case-box {background:#f7f8fc;padding:20px;border-radius:15px;border-left:6px solid #26386f;margin:12px 0}
.chain {text-align:center;font-size:22px;font-weight:700;background:#f4f7ff;padding:15px;border-radius:14px;margin:15px 0}
</style>
""", unsafe_allow_html=True)

# -------------------- SIX DIFFERENT CASES --------------------
cases = {
    "Group 1": {
        "discipline": "🌍 Environmental Studies",
        "name": "The Assessment Break",
        "clo": "Analyze how major causes of climate change interact.",
        "activity": "Compare climate data and discuss relationships among causes.",
        "assessment": "List five causes of climate change.",
        "rubric": "Correct causes — 70% | Accuracy — 30%",
        "correct_break": "📝 Assessment",
        "fixes": [
            "List five causes and define each one.",
            "Analyze how three causes interact, using evidence.",
            "Name three greenhouse gases."
        ],
        "correct_fix": "Analyze how three causes interact, using evidence.",
        "why": "The CLO requires analysis, but the assessment only asks students to list information."
    },
    "Group 2": {
        "discipline": "🧠 Psychology",
        "name": "The Activity Break",
        "clo": "Evaluate two therapies for anxiety and justify the more suitable option.",
        "activity": "Memorize definitions of CBT and psychodynamic therapy.",
        "assessment": "Compare both therapies for a case and justify the more suitable option.",
        "rubric": "Evaluation — 40% | Application — 30% | Justification — 30%",
        "correct_break": "👩‍🏫 Learning Activity",
        "fixes": [
            "Memorize more therapy definitions.",
            "Compare therapies using short clinical cases.",
            "Copy notes on both therapies."
        ],
        "correct_fix": "Compare therapies using short clinical cases.",
        "why": "The assessment requires evaluation, but the learning activity does not prepare students to practise evaluation."
    },
    "Group 3": {
        "discipline": "📚 English",
        "name": "The Rubric Break",
        "clo": "Critically analyze how language constructs gender identity in a literary text.",
        "activity": "Examine lexical choices, dialogue and narrative perspective.",
        "assessment": "Write a critical analysis of gender construction in one literary text.",
        "rubric": "Grammar — 40% | Formatting — 30% | Referencing — 20% | Critical analysis — 10%",
        "correct_break": "📋 Rubric",
        "fixes": [
            "Critical analysis — 50% | Evidence — 30% | Organization/language — 20%",
            "Grammar — 60% | Presentation — 40%",
            "Referencing — 50% | Formatting — 50%"
        ],
        "correct_fix": "Critical analysis — 50% | Evidence — 30% | Organization/language — 20%",
        "why": "The task is aligned, but the rubric gives very little weight to the critical analysis required by the CLO."
    },
    "Group 4": {
        "discipline": "💻 Computer Science",
        "name": "The Intact Chain",
        "clo": "Design and justify an appropriate database structure for a given scenario.",
        "activity": "Examine sample database designs and practise creating schemas.",
        "assessment": "Design a database structure for a scenario and justify key design choices.",
        "rubric": "Design quality — 45% | Justification — 35% | Technical accuracy — 20%",
        "correct_break": "✅ Nothing — the chain is aligned",
        "fixes": [
            "Keep the chain as it is.",
            "Replace the assessment with a definitions quiz.",
            "Give all marks for formatting."
        ],
        "correct_fix": "Keep the chain as it is.",
        "why": "The activity prepares students for the CLO, the assessment demonstrates it, and the rubric rewards the intended performance."
    },
    "Group 5": {
        "discipline": "📈 Business",
        "name": "The CLO Break",
        "clo": "Recommend a marketing strategy for a new product.",
        "activity": "Compare marketing strategies using product scenarios.",
        "assessment": "Recommend a strategy for a new product and justify the choice.",
        "rubric": "Recommendation — 30% | Justification — 40% | Evidence — 30%",
        "correct_break": "🎯 CLO",
        "fixes": [
            "Recommend and justify an appropriate marketing strategy for a new product.",
            "Know marketing strategies.",
            "Understand marketing."
        ],
        "correct_fix": "Recommend and justify an appropriate marketing strategy for a new product.",
        "why": "The assessment and rubric require justification, but the CLO does not explicitly capture that expected performance."
    },
    "Group 6": {
        "discipline": "⚡ Electrical Engineering",
        "name": "Another Rubric Break",
        "clo": "Evaluate two circuit designs and select the more efficient design using performance data.",
        "activity": "Compare circuit performance data and discuss efficiency.",
        "assessment": "Evaluate two circuit designs and select the more efficient one using provided data.",
        "rubric": "Neat presentation — 50% | Correct terminology — 30% | Evaluation — 20%",
        "correct_break": "📋 Rubric",
        "fixes": [
            "Evaluation — 45% | Use of data — 35% | Justification — 20%",
            "Presentation — 70% | Terminology — 30%",
            "Neatness — 100%"
        ],
        "correct_fix": "Evaluation — 45% | Use of data — 35% | Justification — 20%",
        "why": "The task requires evaluation using data, but the rubric mostly rewards presentation and terminology."
    }
}

# -------------------- HEADER --------------------
st.markdown('<div class="main-title">🔗 OBE CHAIN REACTION</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Find the Broken Link. Fix the Alignment.</div>', unsafe_allow_html=True)

role = st.radio(
    "Choose your screen:",
    ["👥 Group Challenge", "👩‍⚖️ Facilitator Dashboard"],
    horizontal=True
)
st.markdown("---")

# =========================================================
# GROUP SCREEN
# =========================================================
if role == "👥 Group Challenge":
    st.info("⏱️ **2-minute challenge:** Select your group, find the broken link, and choose the best repair.")

    group = st.selectbox(
        "Select your group:",
        list(cases.keys()),
        index=None,
        placeholder="Choose Group 1–6"
    )

    if group:
        c = cases[group]
        st.markdown(f"## {c['discipline']} — {group}")

        st.markdown(f"""
<div class="case-box">

### 🎯 CLO
{c["clo"]}

### 👩‍🏫 Learning Activity
{c["activity"]}

### 📝 Assessment
{c["assessment"]}

### 📋 Rubric
{c["rubric"]}

</div>
""", unsafe_allow_html=True)

        st.markdown(
            '<div class="chain">🎯 CLO → 👩‍🏫 Activity → 📝 Assessment → 📋 Rubric</div>',
            unsafe_allow_html=True
        )

        broken = st.radio(
            "### 1️⃣ Where does the OBE chain break?",
            ["🎯 CLO", "👩‍🏫 Learning Activity", "📝 Assessment", "📋 Rubric",
             "✅ Nothing — the chain is aligned"],
            index=None,
            key=f"broken_{group}"
        )

        repair = st.radio(
            "### 2️⃣ What is the best repair?",
            c["fixes"],
            index=None,
            key=f"repair_{group}"
        )

        if st.button("📨 SUBMIT GROUP RESPONSE", use_container_width=True):
            if broken is None or repair is None:
                st.warning("Please answer both questions.")
            else:
                cur.execute("""
                    INSERT OR REPLACE INTO responses
                    (group_name, case_name, broken_link, repair, submitted_at)
                    VALUES (?, ?, ?, ?, ?)
                """, (group, c["name"], broken, repair, datetime.now().strftime("%H:%M:%S")))
                conn.commit()
                st.success(f"✅ {group} response submitted.")
                st.info("🔒 Your answer has been sent to the facilitator. Please wait for the class discussion.")

# =========================================================
# FACILITATOR SCREEN
# =========================================================
else:
    st.markdown("## 👩‍⚖️ Facilitator Dashboard")
    st.caption("This is your screen. Group responses appear here after submission.")

    if st.button("🔄 REFRESH RESPONSES", use_container_width=True):
        st.rerun()

    df = pd.read_sql_query("""
        SELECT group_name, case_name, broken_link, repair, submitted_at
        FROM responses
        ORDER BY group_name
    """, conn)

    if df.empty:
        st.warning("⏳ Waiting for group responses...")
        st.metric("Groups Submitted", "0 / 6")
    else:
        rows = []
        for _, r in df.iterrows():
            c = cases[r["group_name"]]
            break_ok = r["broken_link"] == c["correct_break"]
            fix_ok = r["repair"] == c["correct_fix"]

            if break_ok and fix_ok:
                result = "✅ Correct"
            elif break_ok:
                result = "🟡 Link correct; repair needs review"
            else:
                result = "❌ Review"

            rows.append({
                "Group": r["group_name"],
                "Case": r["case_name"],
                "Broken Link Selected": r["broken_link"],
                "Repair Selected": r["repair"],
                "Evaluator Check": result
            })

        results = pd.DataFrame(rows)
        st.dataframe(results, use_container_width=True, hide_index=True)

        correct = (results["Evaluator Check"] == "✅ Correct").sum()
        col1, col2 = st.columns(2)
        col1.metric("Groups Submitted", f"{len(results)} / 6")
        col2.metric("Fully Correct", f"{correct} / {len(results)}")

    st.markdown("---")
    st.markdown("## 🔐 Facilitator Answer Key")
    st.caption("Keep these closed until you are ready to discuss each group's case.")

    for group, c in cases.items():
        with st.expander(f"{group} — {c['discipline']} {c['name']}"):
            if c["correct_break"] == "✅ Nothing — the chain is aligned":
                st.success("✅ THE CHAIN IS ALIGNED")
            else:
                st.error(f"💥 BROKEN LINK: {c['correct_break']}")

            st.markdown(f"""
**Best repair:**  
{c["correct_fix"]}

**Why:**  
{c["why"]}
""")

    st.markdown("---")
    st.markdown("## 🔗 The Alignment Check")
    st.success("""
**CLO → Learning Activity → Assessment → Rubric**

Each link should prepare for, measure, and reward the **same intended learning**.
""")

    st.markdown("### 🧹 Reset for a New Session")
    if st.button("🗑️ CLEAR ALL RESPONSES"):
        cur.execute("DELETE FROM responses")
        conn.commit()
        st.success("Responses cleared.")
        st.rerun()
