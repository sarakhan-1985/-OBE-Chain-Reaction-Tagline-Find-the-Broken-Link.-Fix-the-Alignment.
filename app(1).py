import streamlit as st

st.set_page_config(
    page_title="OBE Chain Reaction",
    page_icon="🔗",
    layout="centered"
)

st.markdown("""
<style>
.main-title {
    text-align:center;
    font-size:44px;
    font-weight:900;
    color:#26386f;
    margin-bottom:0;
}
.subtitle {
    text-align:center;
    font-size:20px;
    font-weight:600;
    color:#168b78;
    margin-bottom:20px;
}
.chain {
    text-align:center;
    font-size:24px;
    font-weight:700;
    padding:14px;
    background:#f5f7fb;
    border-radius:14px;
    margin:12px 0 20px 0;
}
.case-box {
    padding:18px;
    background:#f8f9fc;
    border-radius:14px;
    border-left:6px solid #26386f;
    margin-bottom:16px;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# CASES: one different chain for each group
# ---------------------------------------------------------
cases = {
    "Group 1": {
        "discipline": "🌍 Environmental Studies",
        "clo": "Analyze how major causes of climate change interact.",
        "activity": "Students compare climate data and discuss relationships among causes.",
        "assessment": "List five causes of climate change.",
        "rubric": "Correct causes — 70% | Accuracy — 30%",
        "break": "📝 Assessment",
        "fixes": [
            "List five causes and define each one.",
            "Analyze how three causes interact, using evidence.",
            "Write the names of three greenhouse gases."
        ],
        "correct_fix": "Analyze how three causes interact, using evidence.",
        "why": "The CLO requires analysis, but the assessment only asks students to list information."
    },
    "Group 2": {
        "discipline": "🧠 Psychology",
        "clo": "Evaluate two therapies for anxiety and justify the more suitable option.",
        "activity": "Students memorize definitions of CBT and psychodynamic therapy.",
        "assessment": "Compare both therapies for a case and justify the more suitable option.",
        "rubric": "Evaluation — 40% | Application — 30% | Justification — 30%",
        "break": "👩‍🏫 Learning Activity",
        "fixes": [
            "Give students more therapy definitions to memorize.",
            "Ask students to compare therapies using short clinical cases.",
            "Ask students to copy notes on both therapies."
        ],
        "correct_fix": "Ask students to compare therapies using short clinical cases.",
        "why": "The assessment and rubric require evaluation, but the learning activity does not prepare students to practise it."
    },
    "Group 3": {
        "discipline": "📚 English",
        "clo": "Critically analyze how language constructs gender identity in a literary text.",
        "activity": "Students examine lexical choices, dialogue and narrative perspective.",
        "assessment": "Write a critical analysis of gender construction in one literary text.",
        "rubric": "Grammar — 40% | Formatting — 30% | Referencing — 20% | Critical analysis — 10%",
        "break": "📋 Rubric",
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
        "clo": "Design and justify an appropriate database structure for a given scenario.",
        "activity": "Students examine sample database designs and practise creating schemas.",
        "assessment": "Design a database structure for a scenario and justify key design choices.",
        "rubric": "Design quality — 45% | Justification — 35% | Technical accuracy — 20%",
        "break": "✅ Nothing — the chain is aligned",
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
        "clo": "Recommend a marketing strategy for a new product.",
        "activity": "Students compare marketing strategies using product scenarios.",
        "assessment": "Recommend a strategy for a new product and justify the choice.",
        "rubric": "Recommendation — 30% | Justification — 40% | Use of evidence — 30%",
        "break": "🎯 CLO",
        "fixes": [
            "Recommend and justify an appropriate marketing strategy for a new product.",
            "Know marketing strategies.",
            "Understand marketing."
        ],
        "correct_fix": "Recommend and justify an appropriate marketing strategy for a new product.",
        "why": "The assessment and rubric require justification, but the CLO does not explicitly capture that important expected performance."
    },
    "Group 6": {
        "discipline": "⚡ Electrical Engineering",
        "clo": "Evaluate two circuit designs and select the more efficient design using performance data.",
        "activity": "Students compare circuit performance data and discuss efficiency.",
        "assessment": "Evaluate two circuit designs and select the more efficient one using provided data.",
        "rubric": "Neat presentation — 50% | Correct terminology — 30% | Evaluation — 20%",
        "break": "📋 Rubric",
        "fixes": [
            "Evaluation — 45% | Use of data — 35% | Justification — 20%",
            "Presentation — 70% | Terminology — 30%",
            "Neatness — 100%"
        ],
        "correct_fix": "Evaluation — 45% | Use of data — 35% | Justification — 20%",
        "why": "The task asks for evaluation using data, but the rubric mostly rewards presentation and terminology."
    }
}

if "submitted" not in st.session_state:
    st.session_state.submitted = False

st.markdown('<div class="main-title">🔗 OBE CHAIN REACTION</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Find the Broken Link. Fix the Alignment.</div>', unsafe_allow_html=True)

st.info("""
⏱️ **5-Minute Group Challenge**

Your group has one OBE chain:

**🎯 CLO → 👩‍🏫 Learning Activity → 📝 Assessment → 📋 Rubric**

Find the broken link, then choose the best repair.
""")

group = st.selectbox(
    "Select your group:",
    list(cases.keys()),
    index=None,
    placeholder="Choose your group"
)

if group:
    case = cases[group]

    st.markdown(f"## {case['discipline']} — {group}")

    st.markdown(f"""
<div class="case-box">

### 🎯 CLO
{case["clo"]}

### 👩‍🏫 Learning Activity
{case["activity"]}

### 📝 Assessment
{case["assessment"]}

### 📋 Rubric
{case["rubric"]}

</div>
""", unsafe_allow_html=True)

    st.markdown(
        '<div class="chain">🎯 CLO &nbsp;→&nbsp; 👩‍🏫 Activity &nbsp;→&nbsp; 📝 Assessment &nbsp;→&nbsp; 📋 Rubric</div>',
        unsafe_allow_html=True
    )

    st.markdown("### 1️⃣ Where does the OBE chain break?")

    broken_link = st.radio(
        "Choose one:",
        [
            "🎯 CLO",
            "👩‍🏫 Learning Activity",
            "📝 Assessment",
            "📋 Rubric",
            "✅ Nothing — the chain is aligned"
        ],
        index=None,
        key=f"break_{group}"
    )

    st.markdown("### 2️⃣ What is the best repair?")

    repair = st.radio(
        "Choose one:",
        case["fixes"],
        index=None,
        key=f"repair_{group}"
    )

    if not st.session_state.submitted:
        if st.button("🔧 REPAIR THE CHAIN", use_container_width=True):
            if broken_link is None or repair is None:
                st.warning("Please answer both questions.")
            else:
                st.session_state.submitted = True
                st.rerun()

    if st.session_state.submitted:
        correct_break = broken_link == case["break"]
        correct_fix = repair == case["correct_fix"]

        if correct_break and correct_fix:
            st.success("✅ Chain repaired! Your group identified both the broken link and the best fix.")
        elif correct_break:
            st.warning("🟡 You found the broken link. Reconsider the best repair.")
        else:
            st.warning("🔎 Look again at what the CLO requires and what each next link actually does.")

        with st.expander("🔐 Reveal the OBE repair"):
            st.markdown(f"""
### Broken link
**{case["break"]}**

### Best repair
**{case["correct_fix"]}**

### Why?
{case["why"]}

### 🔑 OBE Check
**Does each link prepare for, measure, and reward the same intended learning?**
""")

        if st.button("🔄 TRY ANOTHER GROUP / RESET"):
            st.session_state.clear()
            st.rerun()
