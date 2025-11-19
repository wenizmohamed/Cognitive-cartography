import streamlit as st
import networkx as nx
import time
import json
import uuid
import random
import streamlit.components.v1 as components

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
    .block-container {
        padding-top: 2rem;
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
    }
    .stButton>button:hover {
        background-color: #2ea043;
    }
    div[data-testid="stMarkdownContainer"] p {
        font-size: 1.1rem;
    }
    </style>
""", unsafe_allow_html=True)

# --- Session State Initialization ---
if 'graph_data' not in st.session_state:
    st.session_state.graph_data = {"nodes": [], "links": []}
if 'logs' not in st.session_state:
    st.session_state.logs = []
if 'is_running' not in st.session_state:
    st.session_state.is_running = False

# --- Helper Classes ---

class CognitiveNode:
    def __init__(self, label, node_type, description, confidence=1.0, parent_id=None):
        self.id = str(uuid.uuid4())
        self.label = label
        self.type = node_type  # input, reasoning, retrieval, data, decision
        self.description = description
        self.confidence = confidence
        self.parent_id = parent_id
        self.timestamp = time.time()

    def to_dict(self):
        # Map types to colors for the visualizer
        colors = {
            "input": "#ffffff",     # White
            "reasoning": "#58a6ff", # Blue
            "retrieval": "#d29922", # Orange (Qdrant)
            "data": "#a371f7",      # Purple
            "decision": "#238636",  # Green
            "error": "#f85149"      # Red
        }
        return {
            "id": self.id,
            "name": self.label,
            "val": self.confidence * 10, # Size based on confidence
            "color": colors.get(self.type, "#8b949e"),
            "desc": self.description,
            "type": self.type
        }

class MockAgent:
    """
    Simulates the Gemini + Qdrant loop for demo purposes 
    without needing live API keys.
    """
    def generate_steps(self, scenario):
        steps = []
        
        if scenario == "Medical Diagnosis":
            steps = [
                ("input", "User: Patient has high fever, chest pain, productive cough.", "Input received."),
                ("reasoning", "Analyze Symptoms", "Gemini: Identifying potential respiratory conditions based on symptoms."),
                ("retrieval", "Query Qdrant: 'Respiratory + Fever + Chest Pain'", "Qdrant: Searching medical vector DB for semantic matches."),
                ("data", "Retrieved: Pneumonia, Acute Bronchitis", "Qdrant: Found 2 high-confidence matches in current medical literature."),
                ("reasoning", "Hypothesis Evaluation", "Gemini: Evaluating Pneumonia vs Bronchitis. 'Productive cough' leans towards Pneumonia."),
                ("retrieval", "Query Qdrant: 'Pneumonia differentiating factors'", "Qdrant: Searching for specific exclusionary symptoms."),
                ("data", "Retrieved: X-Ray opacity patterns", "Qdrant: Found diagnostic criteria reference."),
                ("reasoning", "Formulate Recommendation", "Gemini: Confidence is 85%. Recommending immediate X-Ray to confirm."),
                ("decision", "Final Output: Suspected Pneumonia", "Gemini: Recommend Chest X-Ray and CBC panel.")
            ]
        elif scenario == "Marketing Strategy":
            steps = [
                ("input", "User: Launch plan for 'Air from 2050' product.", "Input received."),
                ("reasoning", "Deconstruct Request", "Gemini: This is a novelty/conceptual product. Needs high-concept branding."),
                ("retrieval", "Query Qdrant: 'Successful novelty campaigns'", "Qdrant: Searching history for Pet Rock, Canned Air, NFT drops."),
                ("data", "Retrieved: Scarcity tactics & Eco-futurism", "Qdrant: Found patterns linking 'future anxiety' to high engagement."),
                ("reasoning", "Strategy Generation", "Gemini: Propose angle: 'Breathe the future you are saving'."),
                ("reasoning", "Channel Selection", "Gemini: Target Instagram & TikTok for visual storytelling."),
                ("decision", "Final Output: 'Future Breath' Campaign", "Gemini: Detailed roadmap generated.")
            ]
        
        return steps

# --- 3D Graph Visualization Component ---
def render_3d_graph(graph_data):
    """
    Embeds a 3D Force-Directed Graph using HTML/JS within Streamlit.
    Using 3d-force-graph library via CDN.
    """
    nodes_json = json.dumps(graph_data["nodes"])
    links_json = json.dumps(graph_data["links"])
    
    html_code = f"""
    <head>
        <style> body {{ margin: 0; }} </style>
        <script src="//unpkg.com/3d-force-graph"></script>
    </head>
    <body>
        <div id="3d-graph"></div>
        <script>
            const gData = {{
                nodes: {nodes_json},
                links: {links_json}
            }};

            const Graph = ForceGraph3D()
                (document.getElementById('3d-graph'))
                .graphData(gData)
                .nodeLabel('desc') // Show description on hover
                .nodeColor('color')
                .nodeVal('val')
                .linkColor(() => '#30363d')
                .linkOpacity(0.5)
                .linkWidth(1)
                .backgroundColor('#0d1117') // Matches dark theme
                .width(window.innerWidth)
                .height(600);

            // Auto-rotate for "Alive" feel
            let angle = 0;
            setInterval(() => {{
                Graph.cameraPosition({{
                    x: 200 * Math.sin(angle),
                    z: 200 * Math.cos(angle)
                }});
                angle += Math.PI / 600;
            }}, 30);
        </script>
    </body>
    """
    components.html(html_code, height=600)

# --- Main Layout ---

st.title("Cognitive Cartography")
st.markdown("### 🧠 AI's Mind Unveiled | Powered by Gemini & Qdrant")
st.caption("Visualizing live chain-of-thought reasoning in 3D space.")

# Sidebar controls
with st.sidebar:
    st.header("Mission Control")
    
    mode = st.radio("Operation Mode", ["Simulation (Demo)", "Live Agent (Requires API)"])
    
    if mode == "Live Agent (Requires API)":
        gemini_key = st.text_input("Gemini API Key", type="password")
        qdrant_url = st.text_input("Qdrant URL", value="localhost:6333")
        st.warning("⚠️ Live mode requires valid API keys. Switching to Simulation for Demo.")
        mode = "Simulation (Demo)" # Force simulation for safety in this generated code

    scenario = st.selectbox(
        "Select Test Scenario",
        ["Medical Diagnosis", "Marketing Strategy"]
    )
    
    speed = st.slider("Reasoning Speed (ms)", 100, 2000, 1000)
    
    if st.button("Clear Memory", type="primary"):
        st.session_state.graph_data = {"nodes": [], "links": []}
        st.session_state.logs = []
        st.rerun()

    st.markdown("---")
    st.markdown("#### Legend")
    st.markdown("⚪ **Input**")
    st.markdown("🔵 **Gemini Reasoning**")
    st.markdown("🟠 **Qdrant Retrieval**")
    st.markdown("🟣 **Data Object**")
    st.markdown("🟢 **Final Decision**")

# Main Input Area
col1, col2 = st.columns([1, 3])

with col1:
    st.subheader("Input Task")
    user_query = st.text_area("Enter complex query:", height=150, 
                             value="Patient presents with high fever, productive cough, and chest pain. History of smoking. Diagnose." if scenario == "Medical Diagnosis" else "Create a viral marketing campaign for a startup selling 'Air from 2050'.")
    
    start_btn = st.button("🚀 Initiate Reasoning", use_container_width=True)

    st.subheader("Live Reasoning Log")
    log_container = st.empty()

    # Update log display
    with log_container.container():
        for log in st.session_state.logs:
            st.text(f"> {log}")

with col2:
    st.subheader("3D Cognitive Map")
    # Placeholder for the graph
    graph_placeholder = st.empty()

# --- Logic Execution ---

if start_btn:
    st.session_state.is_running = True
    st.session_state.graph_data = {"nodes": [], "links": []}
    st.session_state.logs = []
    
    # 1. Create Root Node
    root_node = CognitiveNode("User Input", "input", f"Query: {user_query}")
    st.session_state.graph_data["nodes"].append(root_node.to_dict())
    st.session_state.logs.append(f"INPUT: {user_query[:30]}...")
    
    # Initial Render
    with graph_placeholder:
        render_3d_graph(st.session_state.graph_data)
    
    # 2. Run Mock Agent Steps
    agent = MockAgent()
    steps = agent.generate_steps(scenario)
    
    last_node_id = root_node.id
    
    for type_code, label, desc in steps:
        time.sleep(speed / 1000)  # Simulate thinking time
        
        # Logic to branch or chain (Simplified for demo)
        parent_id = last_node_id
        
        # If it's a retrieval, it usually spawns from reasoning
        # If it's data, it spawns from retrieval
        
        new_node = CognitiveNode(
            label=label,
            node_type=type_code,
            description=desc,
            confidence=random.uniform(0.8, 1.0),
            parent_id=parent_id
        )
        
        # Add to graph state
        st.session_state.graph_data["nodes"].append(new_node.to_dict())
        st.session_state.graph_data["links"].append({
            "source": parent_id,
            "target": new_node.id
        })
        
        # Log update
        st.session_state.logs.append(f"[{type_code.upper()}] {label}")
        with log_container.container():
            # Re-render logs to show animation
            st.markdown("\n".join([f"`{l}`" for l in st.session_state.logs]))

        # Update Graph
        with graph_placeholder:
            render_3d_graph(st.session_state.graph_data)
        
        last_node_id = new_node.id

    st.session_state.is_running = False
    st.success("Reasoning Complete. Final Answer Generated.")

else:
    # Render graph if data exists
    with graph_placeholder:
        render_3d_graph(st.session_state.graph_data)
        
    with log_container.container():
        st.markdown("\n".join([f"`{l}`" for l in st.session_state.logs]))