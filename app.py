import streamlit as st
import time
import json
import uuid
import random
import streamlit.components.v1 as components
import google.generativeai as genai

# --- Page Config ---
st.set_page_config(
    page_title="Cognitive Cartography",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for "Dark/Neon" Look ---
st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
        color: #c9d1d9;
    }
    h1 {
        color: #58a6ff; 
        text-shadow: 0 0 10px rgba(88, 166, 255, 0.5);
    }
    .stButton>button {
        background-color: #238636;
        color: white;
        border: none;
        border-radius: 4px;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #2ea043;
    }
    </style>
""", unsafe_allow_html=True)

# --- Session State ---
if 'graph_data' not in st.session_state:
    st.session_state.graph_data = {"nodes": [], "links": []}
if 'logs' not in st.session_state:
    st.session_state.logs = []

# --- Helper Classes ---
class CognitiveNode:
    def __init__(self, label, node_type, description, confidence=1.0):
        self.id = str(uuid.uuid4())
        self.label = label
        self.type = node_type  # input, reasoning, retrieval, data, decision
        self.description = description
        self.confidence = confidence

    def to_dict(self):
        colors = {
            "input": "#ffffff",
            "reasoning": "#00f3ff",
            "retrieval": "#ffd700",
            "data": "#d946ef",
            "decision": "#39ff14",
            "error": "#ff003c"
        }
        return {
            "id": self.id,
            "label": self.label,
            "val": 5,
            "color": colors.get(self.type, "#8b949e"),
            "desc": self.description,
            "type": self.type,
            "confidence": self.confidence
        }

# --- Gemini Logic ---
def get_gemini_reasoning(prompt, api_key):
    """Calls Gemini to get structured reasoning steps."""
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.0-flash')
    
    system_prompt = """
    You are the backend for 'Cognitive Cartography'. Break down the user's query into a 5-10 step reasoning chain.
    Return ONLY a raw JSON array of objects. No markdown.
    Format: [{"type": "reasoning", "label": "Short Title", "desc": "Detailed thought", "confidence": 0.9}]
    Types: 'reasoning', 'retrieval' (simulated DB lookup), 'data' (simulated search result), 'decision'.
    """
    
    try:
        response = model.generate_content(f"{system_prompt}\nUser Query: {prompt}")
        text = response.text.replace("```json", "").replace("```", "").strip()
        return json.loads(text)
    except Exception as e:
        st.error(f"Gemini Error: {e}")
        return []

# --- Mock Logic ---
def get_mock_steps(scenario):
    if scenario == "Medical":
        return [
            {"type": "reasoning", "label": "Analyze Symptoms", "desc": "Checking fever and cough patterns."},
            {"type": "retrieval", "label": "Query Qdrant", "desc": "Searching medical vector DB for 'productive cough'."},
            {"type": "data", "label": "Result: Pneumonia", "desc": "High correlation found in knowledge base."},
            {"type": "decision", "label": "Diagnosis", "desc": "Recommend Chest X-Ray."}
        ]
    return [
        {"type": "reasoning", "label": "Analyze Market", "desc": "Looking for viral trends."},
        {"type": "retrieval", "label": "Query Qdrant", "desc": "Searching 'eco-futurism' campaigns."},
        {"type": "decision", "label": "Strategy", "desc": "Launch 'Time Traveler' TikTok campaign."}
    ]

# --- 3D Graph Component ---
def render_graph(data):
    nodes_json = json.dumps(data["nodes"])
    links_json = json.dumps(data["links"])
    
    html = f"""
    <script src="//unpkg.com/3d-force-graph"></script>
    <div id="3d-graph" style="width: 100%; height: 600px; background-color: #000000;"></div>
    <script>
        const gData = {{ nodes: {nodes_json}, links: {links_json} }};
        ForceGraph3D()
            (document.getElementById('3d-graph'))
            .graphData(gData)
            .nodeLabel('desc')
            .nodeColor('color')
            .nodeVal('val')
            .linkWidth(1)
            .linkColor(() => '#334155')
            .backgroundColor('#000000');
    </script>
    """
    components.html(html, height=600)

# --- UI Layout ---
st.sidebar.title("Mission Control")
api_key = st.sidebar.text_input("Gemini API Key", type="password")
scenario = st.sidebar.selectbox("Scenario", ["Custom (Live AI)", "Medical (Mock)", "Marketing (Mock)"])
custom_prompt = st.sidebar.text_area("Custom Prompt", "Explain quantum physics to a child.") if scenario == "Custom (Live AI)" else ""
speed = st.sidebar.slider("Speed (ms)", 100, 2000, 800)
run_btn = st.sidebar.button("🚀 Run")
clear_btn = st.sidebar.button("Reset")

if clear_btn:
    st.session_state.graph_data = {"nodes": [], "links": []}
    st.session_state.logs = []

col1, col2 = st.columns([1, 3])

with col1:
    st.subheader("Reasoning Log")
    for log in st.session_state.logs:
        st.caption(log)

with col2:
    st.subheader("3D Mind Map")
    render_graph(st.session_state.graph_data)

# --- Execution Logic ---
if run_btn:
    st.session_state.graph_data = {"nodes": [], "links": []}
    st.session_state.logs = []
    
    # Input Node
    prompt = custom_prompt if scenario == "Custom (Live AI)" else scenario
    root = CognitiveNode("Input", "input", prompt)
    st.session_state.graph_data["nodes"].append(root.to_dict())
    st.session_state.logs.append(f"INPUT: {prompt}")
    
    # Get Steps
    if scenario == "Custom (Live AI)" and api_key:
        steps = get_gemini_reasoning(prompt, api_key)
    else:
        steps = get_mock_steps(scenario)
    
    # Animate
    last_id = root.id
    for step in steps:
        time.sleep(speed / 1000)
        node = CognitiveNode(step['label'], step['type'], step['desc'])
        st.session_state.graph_data["nodes"].append(node.to_dict())
        st.session_state.graph_data["links"].append({"source": last_id, "target": node.id})
        st.session_state.logs.append(f"[{step['type'].upper()}] {step['label']}")
        last_id = node.id
        st.rerun()