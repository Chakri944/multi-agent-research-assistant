import streamlit as st
from graph import build_graph
from agents import is_topic_safe

st.set_page_config(page_title="Multi-Agent Research Assistant", page_icon="🔍", layout="wide")

# ── Custom CSS for cards ──────────────────────────────────────
st.markdown("""
<style>
.agent-card {
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 10px;
    border: 2px solid #2d2d2d;
    background-color: #1a1a1a;
    transition: all 0.3s ease;
}
.agent-card.active {
    border-color: #facc15;
    background-color: #2a2410;
}
.agent-card.done {
    border-color: #22c55e;
    background-color: #0f2417;
}
.agent-card.waiting {
    opacity: 0.4;
}
.agent-title {
    font-size: 16px;
    font-weight: 600;
    margin-bottom: 4px;
}
.agent-desc {
    font-size: 13px;
    color: #aaa;
}
.spinner {
    display: inline-block;
    width: 14px;
    height: 14px;
    border: 2px solid #facc15;
    border-top: 2px solid transparent;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
    margin-left: 6px;
    vertical-align: middle;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}
</style>
""", unsafe_allow_html=True)

st.title("🔍 Multi-Agent Research Assistant")
st.write("4 AI agents collaborate to research any topic — Planner, Search, Analyst, and Writer.")

topic = st.text_input("Enter a research topic:", placeholder="e.g. Impact of AI on entry-level jobs")
start = st.button("Start Research", use_container_width=True)

# ── Agent card placeholders ───────────────────────────────────
col1, col2, col3, col4 = st.columns(4)
card_planner = col1.empty()
card_search = col2.empty()
card_analyst = col3.empty()
card_writer = col4.empty()

def render_card(placeholder, emoji, title, desc, status):
    spinner_html = '<span class="spinner"></span>' if status == "active" else ""
    placeholder.markdown(f"""
    <div class="agent-card {status}">
        <div class="agent-title">{emoji} {title}{spinner_html}</div>
        <div class="agent-desc">{desc}</div>
    </div>
    """, unsafe_allow_html=True)

def render_all(planner="waiting", search="waiting", analyst="waiting", writer="waiting"):
    render_card(card_planner, "🧠", "Planner", "Breaks topic into sub-questions", planner)
    render_card(card_search, "🔎", "Search", "Finds real web sources", search)
    render_card(card_analyst, "📊", "Analyst", "Extracts key insights", analyst)
    render_card(card_writer, "✍️", "Writer", "Compiles final report", writer)

render_all()  # initial state, all waiting

if start:
    if not topic.strip():
        st.warning("Please enter a topic first.")
    elif not is_topic_safe(topic):
        st.error("⚠️ This topic isn't appropriate for this research tool. Please try a different topic.")
    else:
        graph = build_graph()
        initial_state = {
            "topic": topic,
            "questions": [],
            "search_data": [],
            "analyses": [],
            "report": ""
        }

        results_area = st.container()
        final_state = None

        render_all(planner="active")

        for chunk in graph.stream(initial_state):
            node_name = list(chunk.keys())[0]
            node_output = chunk[node_name]

            if node_name == "planner":
                render_all(planner="done", search="active")
                with results_area.expander("📋 Sub-Questions Generated", expanded=True):
                    for q in node_output["questions"]:
                        st.write(f"- {q}")

            elif node_name == "search":
                render_all(planner="done", search="done", analyst="active")

            elif node_name == "analyst":
                render_all(planner="done", search="done", analyst="done", writer="active")
                with results_area.expander("🔍 Insights Extracted", expanded=False):
                    for a in node_output["analyses"]:
                        st.markdown(f"**{a['question']}**")
                        st.write(a["insight"])

            elif node_name == "writer":
                render_all(planner="done", search="done", analyst="done", writer="done")
                final_state = node_output

        st.subheader("📄 Final Research Report")
        st.markdown(final_state["report"])