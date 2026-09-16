import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# =========================================================
# PAGE SETUP
# =========================================================
st.set_page_config(
    page_title="OBE Chain Reaction",
    page_icon="🔗",
    layout="centered"
)

# =========================================================
# DATABASE
# =========================================================
conn = sqlite3.connect(
    "obe_chain_responses.db",
    check_same_thread=False
)
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

# Shared control table
cur.execute("""
CREATE TABLE IF NOT EXISTS app_control (
    id INTEGER PRIMARY KEY,
    reveal_answers INTEGER DEFAULT 0
)
""")

cur.execute("""
INSERT OR IGNORE INTO app_control (id, reveal_answers)
VALUES (1, 0)
""")

conn.commit()


# =========================================================
# FUNCTIONS
# =========================================================
def answers_revealed():
    cur.execute(
        "SELECT reveal_answers FROM app_control WHERE id = 1"
    )
    row = cur.fetchone()
    return bool(row[0]) if row else False


def set_reveal(value):
    cur.execute(
        "UPDATE app_control SET reveal_answers = ? WHERE id = 1",
        (1 if value else 0,)
    )
    conn.commit()


# =========================================================
# VISUAL STYLE
# =========================================================
st.markdown("""
<style>

/* Main title */
.main-title {
    text-align:center;
    font-size:42px;
    font-weight:900;
    color:#26386f;
    margin-bottom:0px;
}

.subtitle {
    text-align:center;
    font-size:19px;
    font-weight:700;
    color:#168b78;
    margin-bottom:18px;
}

/* Challenge banner */
.challenge-banner {
    text-align:center;
    background:#eef3ff;
    border-radius:15px;
    padding:14px;
    margin:10px 0 20px 0;
    font-size:19px;
    font-weight:800;
    color:#26386f;
}

/* Discipline badge */
.discipline {
    text-align:center;
    font-size:25px;
    font-weight:900;
    color:#26386f;
    margin-bottom:15px;
}

/* Chain heading */
.chain-heading {
    text-align:center;
    font-size:21px;
    font-weight:800;
    margin-top:10px;
    margin-bottom:12px;
}

/* Cards */
.obe-card {
    height:200px;
    border-radius:17px;
    padding:15px 12px;
    text-align:center;
    box-shadow:0px 3px 10px rgba(0,0,0,0.08);
    border:2px solid #e8e8e8;
}

.card-clo {
    background:#fff3e6;
}

.card-activity {
    background:#eef8f3;
}

.card-assessment {
    background:#eef4ff;
}

.card-rubric {
    background:#f8efff;
}

.card-icon {
    font-size:31px;
}

.card-title {
    font-size:17px;
    font-weight:900;
    margin:5px 0 10px 0;
    color:#26386f;
}

.card-text {
    font-size:14px;
    line-height:1.35;
    color:#303541;
}

.arrow {
    text-align:center;
    font-size:27px;
    font-weight:900;
    color:#26386f;
    margin:5px 0;
}

.spot-box {
    background:#fff8dc;
    border-radius:15px;
    padding:12px;
    text-align:center;
    font-size:19px;
    font-weight:900;
    margin-top:18px;
    margin-bottom:8px;
}

.fix-box {
    background:#eaf8f5;
    border-radius:15px;
    padding:12px;
    text-align:center;
    font-size:19px;
    font-weight:900;
    margin-top:18px;
    margin-bottom:8px;
}

.wait-box {
    background:#eef3ff;
    border:2px solid #d6e1ff;
    border-radius:16px;
    padding:18px;
    text-align:center;
    margin-top:18px;
    font-size:18px;
    font-weight:700;
}

.answer-box {
    background:#eaf8ef;
    border:2px solid #9fd5ae;
    border-radius:16px;
    padding:18px;
    margin-top:18px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# SIX EQUAL-DIFFICULTY CASES
# =========================================================
cases = {

    "Group 1": {
        "discipline": "📚 English",
        "name": "English Case",

        "clo": "<b>ANALYZE</b><br>persuasive language in an advertisement.",

        "activity": "<b>ANALYZE</b><br>persuasive techniques in sample advertisements.",

        "assessment": "<b>ANALYZE</b><br>the persuasive language in one advertisement.",

        "rubric": "<b>Presentation — 70%</b><br>Analysis — 30%",

        "correct_break": "📋 Rubric",

        "fixes": [
            "Analysis — 70% | Evidence — 30%",
            "Presentation — 100%",
            "Grammar — 70% | Formatting — 30%"
        ],

        "correct_fix":
            "Analysis — 70% | Evidence — 30%",

        "why":
            "The CLO asks students to analyze. "
            "The activity and assessment also require analysis, "
            "but the rubric mainly rewards presentation."
    },


    "Group 2": {
        "discipline": "🇵🇰 Pakistan Studies",
        "name": "Pakistan Studies Case",

        "clo": "<b>EXPLAIN</b><br>two causes of the Pakistan Movement.",

        "activity": "<b>COPY</b><br>definitions and dates from the slides.",

        "assessment": "<b>EXPLAIN</b><br>two causes of the Pakistan Movement.",

        "rubric": "<b>Explanation — 70%</b><br>Evidence — 30%",

        "correct_break": "🎨 Learning Activity",

        "fixes": [
            "Discuss causes and explain their importance.",
            "Copy more definitions from the slides.",
            "Memorize ten important dates."
        ],

        "correct_fix":
            "Discuss causes and explain their importance.",

        "why":
            "Students are expected to explain causes, "
            "but copying definitions does not give them practice in explaining."
    },


    "Group 3": {
        "discipline": "🕌 Islamic Studies",
        "name": "Islamic Studies Case",

        "clo": "<b>APPLY</b><br>ethical principles to everyday situations.",

        "activity": "<b>APPLY</b><br>ethical principles to short situations.",

        "assessment": "<b>DEFINE</b><br>five ethical principles.",

        "rubric": "<b>Accuracy — 100%</b>",

        "correct_break": "📝 Assessment",

        "fixes": [
            "Apply ethical principles to two everyday situations.",
            "Define ten ethical principles.",
            "List five ethical principles."
        ],

        "correct_fix":
            "Apply ethical principles to two everyday situations.",

        "why":
            "The CLO requires application, "
            "but the assessment only asks students to define concepts."
    },


    "Group 4": {
        "discipline": "🧠 Psychology",
        "name": "Psychology Case",

        "clo": "<b>COMPARE</b><br>classical and operant conditioning.",

        "activity": "<b>COMPARE</b><br>examples of both forms of conditioning.",

        "assessment": "<b>COMPARE</b><br>classical and operant conditioning.",

        "rubric": "<b>Comparison — 60%</b><br>Examples — 40%",

        "correct_break":
            "✅ Nothing — the chain is aligned",

        "fixes": [
            "Keep the chain as it is.",
            "Replace the assessment with definitions.",
            "Assess only spelling and presentation."
        ],

        "correct_fix":
            "Keep the chain as it is.",

        "why":
            "The CLO, activity, assessment and rubric "
            "all focus on comparison."
    },


    "Group 5": {
        "discipline": "✍️ English Writing",
        "name": "Writing Case",

        "clo": "<b>WRITE</b><br>a clear persuasive paragraph.",

        "activity": "<b>WRITE</b><br>a persuasive paragraph in class.",

        "assessment": "<b>WRITE</b><br>a 150-word persuasive paragraph.",

        "rubric": "<b>Grammar — 100%</b>",

        "correct_break": "📋 Rubric",

        "fixes": [
            "Ideas — 40% | Organization — 30% | Language — 30%",
            "Grammar — 100%",
            "Formatting — 70% | Spelling — 30%"
        ],

        "correct_fix":
            "Ideas — 40% | Organization — 30% | Language — 30%",

        "why":
            "The task requires effective persuasive writing, "
            "but the rubric measures only grammar."
    },


    "Group 6": {
        "discipline": "🌱 Pakistan Studies",
        "name": "Environment Case",

        "clo": "<b>LIST</b><br>environmental problems in Pakistan.",

        "activity": "<b>ANALYZE</b><br>a problem and discuss possible solutions.",

        "assessment": "<b>ANALYZE</b><br>one problem and recommend a solution.",

        "rubric": "<b>Analysis — 60%</b><br>Solution — 40%",

        "correct_break": "🎯 CLO",

        "fixes": [
            "Analyze an environmental problem and recommend a solution.",
            "List five environmental problems.",
            "Name environmental problems in Pakistan."
        ],

        "correct_fix":
            "Analyze an environmental problem and recommend a solution.",

        "why":
            "The activity and assessment expect analysis and recommendation, "
            "but the CLO only requires students to list information."
    }
}


# =========================================================
# HEADER
# =========================================================
st.markdown(
    '<div class="main-title">🔗 OBE CHAIN REACTION</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">SPOT IT → FIX IT → SUBMIT IT</div>',
    unsafe_allow_html=True
)


# =========================================================
# KEEP ORIGINAL SCREEN CHOICE
# =========================================================
role = st.radio(
    "Choose your screen:",
    ["👥 Group Challenge", "👩‍⚖️ Facilitator Dashboard"],
    horizontal=True
)

st.markdown("---")


# =========================================================
# PARTICIPANT / GROUP SCREEN
# =========================================================
if role == "👥 Group Challenge":

    st.markdown("""
    <div class="challenge-banner">
    ⚡ 5-MINUTE CHALLENGE<br>
    Look at the four cards. Spot what does not fit. Then fix it.
    </div>
    """, unsafe_allow_html=True)

    # KEEP ORIGINAL GROUP SELECTION
    group = st.selectbox(
        "Select your group:",
        list(cases.keys()),
        index=None,
        placeholder="Choose Group 1–6"
    )

    if group:

        c = cases[group]

        st.markdown(
            f'<div class="discipline">{c["discipline"]} — {group}</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="chain-heading">'
            '🎯 CLO &nbsp;→&nbsp; 🎨 ACTIVITY &nbsp;→&nbsp; '
            '📝 ASSESSMENT &nbsp;→&nbsp; 📋 RUBRIC'
            '</div>',
            unsafe_allow_html=True
        )

        # -------------------------------------------------
        # VISUAL FOUR-CARD CHAIN
        # -------------------------------------------------
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(f"""
            <div class="obe-card card-clo">
                <div class="card-icon">🎯</div>
                <div class="card-title">CLO</div>
                <div class="card-text">{c["clo"]}</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="obe-card card-activity">
                <div class="card-icon">🎨</div>
                <div class="card-title">ACTIVITY</div>
                <div class="card-text">{c["activity"]}</div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div class="obe-card card-assessment">
                <div class="card-icon">📝</div>
                <div class="card-title">ASSESSMENT</div>
                <div class="card-text">{c["assessment"]}</div>
            </div>
            """, unsafe_allow_html=True)

        with col4:
            st.markdown(f"""
            <div class="obe-card card-rubric">
                <div class="card-icon">📋</div>
                <div class="card-title">RUBRIC</div>
                <div class="card-text">{c["rubric"]}</div>
            </div>
            """, unsafe_allow_html=True)

        # -------------------------------------------------
        # SPOT IT
        # -------------------------------------------------
        st.markdown("""
        <div class="spot-box">
        🔍 SPOT IT — Which card doesn't fit?
        </div>
        """, unsafe_allow_html=True)

        broken = st.radio(
            "Select one:",
            [
                "🎯 CLO",
                "🎨 Learning Activity",
                "📝 Assessment",
                "📋 Rubric",
                "✅ Nothing — the chain is aligned"
            ],
            index=None,
            key=f"broken_{group}",
            label_visibility="collapsed"
        )

        # -------------------------------------------------
        # FIX IT
        # -------------------------------------------------
        st.markdown("""
        <div class="fix-box">
        🔧 FIX IT — Choose the simplest repair.
        </div>
        """, unsafe_allow_html=True)

        repair = st.radio(
            "Choose repair:",
            c["fixes"],
            index=None,
            key=f"repair_{group}",
            label_visibility="collapsed"
        )

        # -------------------------------------------------
        # SUBMIT
        # -------------------------------------------------
        if st.button(
            "🚀 SUBMIT GROUP RESPONSE",
            use_container_width=True
        ):

            if broken is None or repair is None:
                st.warning("⚠️ Please answer both questions.")

            else:
                cur.execute("""
                    INSERT OR REPLACE INTO responses
                    (
                        group_name,
                        case_name,
                        broken_link,
                        repair,
                        submitted_at
                    )
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    group,
                    c["name"],
                    broken,
                    repair,
                    datetime.now().strftime("%H:%M:%S")
                ))

                conn.commit()

                st.success("✅ Response submitted!")

        # -------------------------------------------------
        # CHECK IF THIS GROUP HAS SUBMITTED
        # -------------------------------------------------
        cur.execute(
            """
            SELECT broken_link, repair
            FROM responses
            WHERE group_name = ?
            """,
            (group,)
        )

        submitted = cur.fetchone()

        if submitted:

            # ANSWERS STILL LOCKED
            if not answers_revealed():

                st.markdown("""
                <div class="wait-box">
                    🔒 <b>ANSWERS LOCKED</b><br><br>
                    Your response has been sent to the facilitator.<br>
                    Wait for the class discussion.
                </div>
                """, unsafe_allow_html=True)

            # FACILITATOR HAS REVEALED
            else:

                participant_break = submitted[0]
                participant_fix = submitted[1]

                break_ok = (
                    participant_break == c["correct_break"]
                )

                fix_ok = (
                    participant_fix == c["correct_fix"]
                )

                if break_ok and fix_ok:
                    result_message = "🎉 Your group got the chain right!"
                elif break_ok:
                    result_message = (
                        "🟡 You spotted the correct link. "
                        "Review the repair."
                    )
                else:
                    result_message = (
                        "🔍 Compare your answer with the solution below."
                    )

                st.markdown(f"""
                <div class="answer-box">

                <h3>🔓 ANSWERS REVEALED</h3>

                <b>{result_message}</b>

                <br><br>

                <b>💥 Correct link:</b><br>
                {c["correct_break"]}

                <br><br>

                <b>🔧 Best repair:</b><br>
                {c["correct_fix"]}

                <br><br>

                <b>💡 Why?</b><br>
                {c["why"]}

                </div>
                """, unsafe_allow_html=True)


# =========================================================
# FACILITATOR DASHBOARD
# =========================================================
else:

    st.markdown("## 👩‍⚖️ Facilitator Dashboard")

    st.caption(
        "Group responses appear here. "
        "Participants cannot see answers until you reveal them."
    )

    # -----------------------------------------------------
    # REFRESH
    # -----------------------------------------------------
    if st.button(
        "🔄 REFRESH RESPONSES",
        use_container_width=True
    ):
        st.rerun()

    # -----------------------------------------------------
    # READ RESPONSES
    # -----------------------------------------------------
    df = pd.read_sql_query("""
        SELECT
            group_name,
            case_name,
            broken_link,
            repair,
            submitted_at
        FROM responses
        ORDER BY group_name
    """, conn)

    if df.empty:

        st.warning("⏳ Waiting for group responses...")
        st.metric("Groups Submitted", "0 / 6")

    else:

        # -------------------------------------------------
        # NEUTRAL TABLE — NO CORRECTNESS
        # -------------------------------------------------
        neutral_rows = []

        for _, r in df.iterrows():

            neutral_rows.append({
                "Group": r["group_name"],
                "Case": r["case_name"],
                "Card Selected": r["broken_link"],
                "Repair Selected": r["repair"],
                "Time": r["submitted_at"]
            })

        neutral_results = pd.DataFrame(neutral_rows)

        st.dataframe(
            neutral_results,
            use_container_width=True,
            hide_index=True
        )

        st.metric(
            "Groups Submitted",
            f"{len(neutral_results)} / 6"
        )

        st.info(
            "💬 Discuss the responses first. "
            "No correctness is shown above."
        )

    # =====================================================
    # FACILITATOR CONTROL
    # =====================================================
    st.markdown("---")
    st.markdown("## 🔐 Participant Answer Control")

    if not answers_revealed():

        st.warning(
            "🔒 Participant answers are currently LOCKED."
        )

        if st.button(
            "🔓 REVEAL ANSWERS TO PARTICIPANTS",
            use_container_width=True
        ):
            set_reveal(True)
            st.success(
                "Answers are now visible to participants."
            )
            st.rerun()

    else:

        st.success(
            "🔓 Participants can now see the answers."
        )

        if st.button(
            "🔒 HIDE ANSWERS FROM PARTICIPANTS",
            use_container_width=True
        ):
            set_reveal(False)
            st.rerun()

    # =====================================================
    # FACILITATOR'S OWN EVALUATION
    # =====================================================
    if not df.empty:

        st.markdown("---")
        st.markdown("## 📊 Facilitator Evaluation")

        evaluated_rows = []

        for _, r in df.iterrows():

            c = cases[r["group_name"]]

            break_ok = (
                r["broken_link"] == c["correct_break"]
            )

            fix_ok = (
                r["repair"] == c["correct_fix"]
            )

            if break_ok and fix_ok:
                result = "✅ Correct"

            elif break_ok:
                result = "🟡 Link correct; repair needs review"

            else:
                result = "❌ Review"

            evaluated_rows.append({
                "Group": r["group_name"],
                "Card Selected": r["broken_link"],
                "Repair Selected": r["repair"],
                "Result": result
            })

        evaluated_results = pd.DataFrame(
            evaluated_rows
        )

        st.dataframe(
            evaluated_results,
            use_container_width=True,
            hide_index=True
        )

        correct = (
            evaluated_results["Result"] == "✅ Correct"
        ).sum()

        st.metric(
            "Fully Correct",
            f"{correct} / {len(evaluated_results)}"
        )

    # =====================================================
    # FACILITATOR ANSWER KEY
    # =====================================================
    st.markdown("---")
    st.markdown("## 🗝️ Facilitator Answer Key")

    st.caption(
        "This section is visible only on the Facilitator Dashboard."
    )

    for group_name, c in cases.items():

        with st.expander(
            f"{group_name} — {c['discipline']}"
        ):

            if (
                c["correct_break"]
                == "✅ Nothing — the chain is aligned"
            ):
                st.success(
                    "✅ THE CHAIN IS ALIGNED"
                )

            else:
                st.error(
                    f"💥 BROKEN LINK: {c['correct_break']}"
                )

            st.markdown(
                f"""
                **🔧 Best repair:**  
                {c["correct_fix"]}

                **💡 Why:**  
                {c["why"]}
                """
            )

    # =====================================================
    # ALIGNMENT REMINDER
    # =====================================================
    st.markdown("---")

    st.markdown("## 🔗 The Alignment Check")

    st.success("""
**🎯 CLO → 🎨 Activity → 📝 Assessment → 📋 Rubric**

Ask one simple question:

**Are students practising, demonstrating and being rewarded
for the same intended learning?**
""")

    # =====================================================
    # RESET
    # =====================================================
    st.markdown("---")
    st.markdown("## 🧹 Reset for a New Session")

    if st.button(
        "🗑️ CLEAR ALL RESPONSES & LOCK ANSWERS",
        use_container_width=True
    ):

        cur.execute("DELETE FROM responses")

        cur.execute("""
            UPDATE app_control
            SET reveal_answers = 0
            WHERE id = 1
        """)

        conn.commit()

        st.success(
            "Responses cleared and participant answers locked."
        )

        st.rerun()
