import streamlit as st
import time
import sys
import os
from io import StringIO

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResearchMind · Multi-Agent AI",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&family=DM+Sans:wght@300;400;500&display=swap');

/* ── Root Variables ── */
:root {
    --bg:        #0a0b0f;
    --surface:   #12141a;
    --surface2:  #1a1d26;
    --border:    #252836;
    --accent:    #e8ff5a;
    --accent2:   #5af0e8;
    --accent3:   #ff6b6b;
    --text:      #e8eaf0;
    --muted:     #6b7080;
    --success:   #5af0b8;
}

/* ── Global Reset ── */
html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
}

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse 80% 50% at 20% -10%, rgba(232,255,90,0.07) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 85% 90%, rgba(90,240,232,0.06) 0%, transparent 55%),
        var(--bg) !important;
}

[data-testid="stHeader"],
[data-testid="stToolbar"],
.stDeployButton,
footer { display: none !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: var(--surface); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }

/* ── Headings ── */
h1,h2,h3,h4 { font-family: 'Syne', sans-serif !important; }

/* ── Hero Section ── */
.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(232,255,90,0.1);
    border: 1px solid rgba(232,255,90,0.3);
    border-radius: 100px;
    padding: 6px 16px;
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    letter-spacing: 0.12em;
    color: var(--accent);
    text-transform: uppercase;
    margin-bottom: 20px;
}

.hero-badge::before {
    content: '';
    width: 6px; height: 6px;
    border-radius: 50%;
    background: var(--accent);
    animation: pulse-dot 2s ease-in-out infinite;
}

@keyframes pulse-dot {
    0%, 100% { opacity: 1; transform: scale(1); }
    50%       { opacity: 0.4; transform: scale(0.7); }
}

.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2.5rem, 6vw, 4.5rem);
    font-weight: 800;
    line-height: 1.05;
    letter-spacing: -0.03em;
    margin: 0 0 16px 0;
    color: var(--text);
}

.hero-title span {
    color: var(--accent);
    position: relative;
}

.hero-sub {
    font-family: 'DM Sans', sans-serif;
    font-size: 1.05rem;
    color: var(--muted);
    line-height: 1.6;
    max-width: 520px;
    margin-bottom: 40px;
}

/* ── Input Box ── */
.stTextInput > div > div {
    background: var(--surface2) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 12px !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1rem !important;
    padding: 14px 18px !important;
    transition: border-color 0.2s !important;
}

.stTextInput > div > div:focus-within {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(232,255,90,0.12) !important;
}

.stTextInput input { color: var(--text) !important; }
.stTextInput label { color: var(--muted) !important; font-family: 'DM Mono', monospace !important; font-size: 11px !important; letter-spacing: 0.1em !important; text-transform: uppercase !important; }

/* ── Button ── */
.stButton > button {
    background: var(--accent) !important;
    color: #0a0b0f !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.02em !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 14px 32px !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    width: 100% !important;
}

.stButton > button:hover {
    background: #f5ff80 !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(232,255,90,0.25) !important;
}

.stButton > button:active { transform: translateY(0) !important; }

/* ── Pipeline Step Cards ── */
.step-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 20px 24px;
    margin-bottom: 12px;
    position: relative;
    overflow: hidden;
    transition: all 0.3s ease;
}

.step-card::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 3px;
    background: var(--border);
    border-radius: 3px 0 0 3px;
    transition: background 0.3s ease;
}

.step-card.active::before  { background: var(--accent); box-shadow: 0 0 12px rgba(232,255,90,0.5); }
.step-card.done::before    { background: var(--success); }
.step-card.error::before   { background: var(--accent3); }

.step-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 4px;
}

.step-num {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    font-weight: 500;
    color: var(--muted);
    background: var(--surface2);
    border-radius: 6px;
    padding: 3px 8px;
    letter-spacing: 0.08em;
}

.step-name {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 0.95rem;
    color: var(--text);
}

.step-desc {
    font-size: 0.82rem;
    color: var(--muted);
    padding-left: 52px;
    line-height: 1.5;
}

.step-status {
    margin-left: auto;
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    padding: 3px 10px;
    border-radius: 100px;
}

.status-waiting  { color: var(--muted);   background: rgba(107,112,128,0.1); }
.status-running  { color: var(--accent);  background: rgba(232,255,90,0.1); animation: status-blink 1.2s ease-in-out infinite; }
.status-done     { color: var(--success); background: rgba(90,240,184,0.1); }
.status-error    { color: var(--accent3); background: rgba(255,107,107,0.1); }

@keyframes status-blink {
    0%, 100% { opacity: 1; }
    50%       { opacity: 0.5; }
}

/* ── Result Panels ── */
.result-panel {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 24px 28px;
    margin-bottom: 16px;
}

.result-panel-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 16px;
    padding-bottom: 16px;
    border-bottom: 1px solid var(--border);
}

.result-label {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--muted);
}

.result-icon {
    width: 32px; height: 32px;
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 15px;
}

.icon-search  { background: rgba(232,255,90,0.12); }
.icon-reader  { background: rgba(90,240,232,0.12); }
.icon-writer  { background: rgba(90,240,184,0.12); }
.icon-critic  { background: rgba(255,107,107,0.12); }

.result-content {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.88rem;
    line-height: 1.7;
    color: var(--text);
    white-space: pre-wrap;
    word-break: break-word;
}

/* Final report gets special treatment */
.result-panel.report {
    border-color: rgba(90,240,184,0.3);
    background: linear-gradient(135deg, var(--surface) 0%, rgba(90,240,184,0.04) 100%);
}

.result-panel.report .result-content {
    font-size: 0.93rem;
    line-height: 1.8;
}

/* ── Divider ── */
.section-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--border), transparent);
    margin: 32px 0;
}

/* ── Stats Row ── */
.stat-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 100px;
    padding: 6px 14px;
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    color: var(--muted);
    margin-right: 8px;
}

.stat-pill strong { color: var(--text); }

/* ── Streamlit overrides ── */
.stSpinner > div { color: var(--accent) !important; }
[data-testid="stMarkdownContainer"] p { color: var(--text) !important; }
.stAlert { border-radius: 12px !important; border: 1px solid var(--border) !important; }

/* ── Expander ── */
.streamlit-expanderHeader {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 12px !important;
}

.streamlit-expanderContent {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-top: none !important;
    border-radius: 0 0 10px 10px !important;
}

/* ── Error box ── */
.error-box {
    background: rgba(255,107,107,0.08);
    border: 1px solid rgba(255,107,107,0.3);
    border-radius: 12px;
    padding: 16px 20px;
    color: var(--accent3);
    font-family: 'DM Mono', monospace;
    font-size: 0.82rem;
    line-height: 1.6;
}

/* ── Empty state ── */
.empty-state {
    text-align: center;
    padding: 60px 20px;
    color: var(--muted);
}
.empty-state .big-icon { font-size: 48px; margin-bottom: 16px; opacity: 0.4; }
.empty-state p { font-size: 0.9rem; line-height: 1.6; }

/* hide streamlit branding */
#MainMenu, [data-testid="stDecoration"] { display:none !important; }
</style>
""", unsafe_allow_html=True)


# ── Session State Init ────────────────────────────────────────────────────────
for key in ["results", "step_status", "running", "elapsed", "topic_run"]:
    if key not in st.session_state:
        st.session_state[key] = None

if st.session_state.step_status is None:
    st.session_state.step_status = {
        "search": "waiting",
        "reader": "waiting",
        "writer": "waiting",
        "critic": "waiting",
    }


# ── Helper: render a pipeline step card ──────────────────────────────────────
def step_card(num: str, icon: str, name: str, desc: str, status: str):
    card_cls   = {"waiting": "", "running": "active", "done": "done", "error": "error"}[status]
    status_cls = f"status-{status}"
    label      = {"waiting": "Waiting", "running": "Running…", "done": "Done ✓", "error": "Error ✗"}[status]
    st.markdown(f"""
    <div class="step-card {card_cls}">
        <div class="step-header">
            <span class="step-num">STEP {num}</span>
            <span style="font-size:18px">{icon}</span>
            <span class="step-name">{name}</span>
            <span class="step-status {status_cls}">{label}</span>
        </div>
        <div class="step-desc">{desc}</div>
    </div>
    """, unsafe_allow_html=True)


# ── Helper: render a result panel ────────────────────────────────────────────
def result_panel(icon: str, icon_cls: str, label: str, content: str, extra_cls: str = ""):
    # Escape HTML special chars in content
    safe = (content
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;"))
    st.markdown(f"""
    <div class="result-panel {extra_cls}">
        <div class="result-panel-header">
            <div class="result-icon {icon_cls}">{icon}</div>
            <span class="result-label">{label}</span>
        </div>
        <div class="result-content">{safe}</div>
    </div>
    """, unsafe_allow_html=True)


# ── Layout ────────────────────────────────────────────────────────────────────
col_left, col_right = st.columns([1, 1.6], gap="large")

# ════════════════════════════════ LEFT COLUMN ════════════════════════════════
with col_left:
    # Hero
    st.markdown("""
    <div class="hero-badge">Multi-Agent Research System</div>
    <h1 class="hero-title">Deep Research,<br><span>Automated.</span></h1>
    <p class="hero-sub">
        A four-agent pipeline — Search · Read · Write · Critique —
        that turns any topic into a structured, peer-reviewed research report.
    </p>
    """, unsafe_allow_html=True)

    # Input
    topic = st.text_input(
        "Research Topic",
        placeholder="e.g. Quantum computing breakthroughs in 2025",
        label_visibility="visible",
    )

    run_btn = st.button("⚡  Run Research Pipeline", use_container_width=True)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # Pipeline steps (dynamic status)
    ss = st.session_state.step_status
    steps_placeholder = st.empty()

    def render_steps():
        with steps_placeholder.container():
            step_card("01", "🔍", "Search Agent",
                      "Queries the web for recent, reliable sources on the topic.", ss["search"])
            step_card("02", "📖", "Reader Agent",
                      "Picks the best URL from results and scrapes it for deeper content.", ss["reader"])
            step_card("03", "✍️", "Writer Chain",
                      "Synthesises all gathered data into a structured research report.", ss["writer"])
            step_card("04", "🧐", "Critic Chain",
                      "Reviews the report for accuracy, gaps, and quality.", ss["critic"])

    render_steps()

    # Elapsed time (shown after run)
    if st.session_state.elapsed:
        st.markdown(f"""
        <br>
        <span class="stat-pill">⏱ Elapsed <strong>{st.session_state.elapsed:.1f}s</strong></span>
        <span class="stat-pill">📌 Topic <strong>{st.session_state.topic_run or "—"}</strong></span>
        """, unsafe_allow_html=True)


# ═══════════════════════════════ RIGHT COLUMN ════════════════════════════════
with col_right:
    results_container = st.container()

    with results_container:
        if not st.session_state.results and not st.session_state.running:
            st.markdown("""
            <div class="empty-state">
                <div class="big-icon">🔬</div>
                <p>Enter a topic on the left and hit<br>
                <strong style="color:#e8eaf0">Run Research Pipeline</strong><br>
                to see the full multi-agent output here.</p>
            </div>
            """, unsafe_allow_html=True)

        elif st.session_state.results:
            res = st.session_state.results

            if "error" in res:
                st.markdown(f'<div class="error-box">⚠️ {res["error"]}</div>',
                            unsafe_allow_html=True)
            else:
                # Search results
                if res.get("search_results"):
                    result_panel("🔍", "icon-search", "Search Agent · Raw Results",
                                 res["search_results"])

                # Scraped content
                if res.get("scraped_content"):
                    result_panel("📖", "icon-reader", "Reader Agent · Scraped Content",
                                 res["scraped_content"])

                # Final report
                if res.get("report"):
                    report_text = (res["report"].content
                                   if hasattr(res["report"], "content")
                                   else str(res["report"]))
                    result_panel("✍️", "icon-writer", "Writer · Research Report",
                                 report_text, extra_cls="report")

                # Critic feedback
                if res.get("feedback"):
                    feedback_text = (res["feedback"].content
                                     if hasattr(res["feedback"], "content")
                                     else str(res["feedback"]))
                    result_panel("🧐", "icon-critic", "Critic · Review & Feedback",
                                 feedback_text)

                # Download button
                if res.get("report"):
                    report_str = (res["report"].content
                                  if hasattr(res["report"], "content")
                                  else str(res["report"]))
                    st.download_button(
                        label="⬇  Download Report (.txt)",
                        data=report_str,
                        file_name=f"research_{(st.session_state.topic_run or 'report').replace(' ','_')[:40]}.txt",
                        mime="text/plain",
                        use_container_width=True,
                    )


# ── Run Logic ─────────────────────────────────────────────────────────────────
if run_btn:
    if not topic.strip():
        st.warning("Please enter a research topic first.")
    else:
        st.session_state.running = True
        st.session_state.results = None
        st.session_state.elapsed = None
        st.session_state.topic_run = topic.strip()
        st.session_state.step_status = {k: "waiting" for k in ["search", "reader", "writer", "critic"]}

        start_time = time.time()

        try:
            from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain

            state = {}

            # ── Step 1: Search ─────────────────────────────────────────────
            st.session_state.step_status["search"] = "running"
            render_steps()

            search_agent = build_search_agent()
            search_result = search_agent.invoke({
                "messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]
            })
            state["search_results"] = search_result["messages"][-1].content
            st.session_state.step_status["search"] = "done"
            render_steps()

            # ── Step 2: Reader ─────────────────────────────────────────────
            st.session_state.step_status["reader"] = "running"
            render_steps()

            reader_agent = build_reader_agent()
            reader_result = reader_agent.invoke({
                "messages": [("user",
                    f"Based on the following search results about '{topic}', "
                    f"pick the most relevant URL and scrape it for deeper content.\n\n"
                    f"Search Results:\n{state['search_results'][:800]}"
                )]
            })
            state["scraped_content"] = reader_result["messages"][-1].content
            st.session_state.step_status["reader"] = "done"
            render_steps()

            # ── Step 3: Writer ─────────────────────────────────────────────
            st.session_state.step_status["writer"] = "running"
            render_steps()

            research_combined = (
                f"SEARCH RESULTS:\n{state['search_results']}\n\n"
                f"DETAILED SCRAPED CONTENT:\n{state['scraped_content']}"
            )
            state["report"] = writer_chain.invoke({
                "topic": topic,
                "research": research_combined
            })
            st.session_state.step_status["writer"] = "done"
            render_steps()

            # ── Step 4: Critic ─────────────────────────────────────────────
            st.session_state.step_status["critic"] = "running"
            render_steps()

            state["feedback"] = critic_chain.invoke({"report": state["report"]})
            st.session_state.step_status["critic"] = "done"
            render_steps()

            # ── Done ───────────────────────────────────────────────────────
            st.session_state.results = state
            st.session_state.elapsed = time.time() - start_time
            st.session_state.running = False
            st.rerun()

        except Exception as e:
            failed_step = next(
                (k for k, v in st.session_state.step_status.items() if v == "running"),
                None
            )
            if failed_step:
                st.session_state.step_status[failed_step] = "error"
            render_steps()
            st.session_state.results = {"error": str(e)}
            st.session_state.elapsed = time.time() - start_time
            st.session_state.running = False
            st.rerun()