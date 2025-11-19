import streamlit as st
import numpy as np
import json
import time
from typing import List, Dict, Any, Optional
import os

# Streamlit page configuration
st.set_page_config(
    page_title="Cognitive Cartography - AI Mind Visualization",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'nodes' not in st.session_state:
    st.session_state.nodes = []
if 'edges' not in st.session_state:
    st.session_state.edges = []
if 'reasoning_steps' not in st.session_state:
    st.session_state.reasoning_steps = []
if 'vector_memory' not in st.session_state:
    st.session_state.vector_memory = []
if 'current_node_id' not in st.session_state:
    st.session_state.current_node_id = 0


class MockAIAgent:
    """Mock AI Agent that generates reasoning steps"""
    
    def __init__(self):
        self.reasoning_templates = [
            "Analyzing the problem: {}",
            "Breaking down into components: {}",
            "Considering approach: {}",
            "Evaluating options for: {}",
            "Synthesizing solution for: {}",
            "Validating reasoning about: {}",
        ]
    
    def generate_reasoning(self, query: str, num_steps: int = 5) -> List[str]:
        """Generate mock reasoning steps"""
        steps = []
        for i in range(num_steps):
            template = self.reasoning_templates[i % len(self.reasoning_templates)]
            step = template.format(f"'{query}' - step {i+1}")
            steps.append(step)
        return steps


class GeminiAgent:
    """Gemini API Agent for real AI reasoning"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        try:
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-pro')
            self.available = True
        except Exception as e:
            st.warning(f"Gemini API not available: {e}")
            self.available = False
    
    def generate_reasoning(self, query: str, num_steps: int = 5) -> List[str]:
        """Generate reasoning steps using Gemini"""
        if not self.available:
            return MockAIAgent().generate_reasoning(query, num_steps)
        
        try:
            prompt = f"""Break down your reasoning about this query into {num_steps} distinct thinking steps.
Query: {query}

Provide each step as a separate line starting with 'Step N:'.
Focus on showing your cognitive process."""
            
            response = self.model.generate_content(prompt)
            steps = []
            for line in response.text.split('\n'):
                line = line.strip()
                if line and ('step' in line.lower() or len(steps) < num_steps):
                    steps.append(line)
                if len(steps) >= num_steps:
                    break
            return steps[:num_steps]
        except Exception as e:
            st.error(f"Error with Gemini API: {e}")
            return MockAIAgent().generate_reasoning(query, num_steps)


class QdrantSimulator:
    """Simulates Qdrant vector database for memory storage"""
    
    def __init__(self):
        self.vectors = []
        self.metadata = []
    
    def add_vector(self, text: str, vector: Optional[np.ndarray] = None) -> int:
        """Add a vector to memory"""
        if vector is None:
            # Generate mock embedding
            vector = np.random.randn(384).astype(np.float32)
            # Normalize
            vector = vector / np.linalg.norm(vector)
        
        vector_id = len(self.vectors)
        self.vectors.append(vector)
        self.metadata.append({
            'id': vector_id,
            'text': text,
            'timestamp': time.time()
        })
        return vector_id
    
    def search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Search for similar vectors"""
        if not self.vectors:
            return []
        
        # Generate query vector
        query_vector = np.random.randn(384).astype(np.float32)
        query_vector = query_vector / np.linalg.norm(query_vector)
        
        # Calculate similarities
        similarities = []
        for i, vec in enumerate(self.vectors):
            sim = np.dot(query_vector, vec)
            similarities.append((i, sim))
        
        # Sort by similarity
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        # Return top_k results
        results = []
        for i, sim in similarities[:top_k]:
            result = self.metadata[i].copy()
            result['similarity'] = float(sim)
            results.append(result)
        
        return results
    
    def get_stats(self) -> Dict[str, Any]:
        """Get memory statistics"""
        return {
            'total_vectors': len(self.vectors),
            'vector_dimension': 384,
            'memory_size_mb': len(self.vectors) * 384 * 4 / (1024 * 1024)
        }


def create_3d_graph_html(nodes: List[Dict], edges: List[Dict]) -> str:
    """Create HTML for 3D force-directed graph visualization"""
    
    nodes_json = json.dumps(nodes)
    edges_json = json.dumps(edges)
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ margin: 0; overflow: hidden; background: #000; }}
            #graph {{ width: 100%; height: 600px; }}
            #info {{
                position: absolute;
                top: 10px;
                left: 10px;
                color: white;
                font-family: monospace;
                background: rgba(0,0,0,0.7);
                padding: 10px;
                border-radius: 5px;
                font-size: 12px;
            }}
        </style>
        <script src="https://unpkg.com/3d-force-graph"></script>
    </head>
    <body>
        <div id="info">
            <div>🧠 Cognitive Cartography - AI Mind Map</div>
            <div>Nodes: <span id="node-count">0</span></div>
            <div>Links: <span id="link-count">0</span></div>
            <div>Click nodes to explore | Drag to rotate</div>
        </div>
        <div id="graph"></div>
        <script>
            const nodes = {nodes_json};
            const links = {edges_json};
            
            document.getElementById('node-count').textContent = nodes.length;
            document.getElementById('link-count').textContent = links.length;
            
            const Graph = ForceGraph3D()
                (document.getElementById('graph'))
                .graphData({{ nodes, links }})
                .nodeLabel('label')
                .nodeColor(node => {{
                    const colors = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#ffa07a', '#98d8c8'];
                    return colors[node.group % colors.length];
                }})
                .nodeRelSize(6)
                .nodeOpacity(0.9)
                .linkColor(() => 'rgba(255,255,255,0.2)')
                .linkWidth(2)
                .linkOpacity(0.5)
                .backgroundColor('#000000')
                .onNodeClick(node => {{
                    console.log('Clicked node:', node);
                    const info = document.getElementById('info');
                    info.innerHTML = `
                        <div>🧠 Cognitive Cartography - AI Mind Map</div>
                        <div><strong>Selected Node:</strong> ${{node.label}}</div>
                        <div><strong>ID:</strong> ${{node.id}}</div>
                        <div><strong>Type:</strong> ${{node.type || 'thought'}}</div>
                        <div>Nodes: ${{nodes.length}}</div>
                        <div>Links: ${{links.length}}</div>
                    `;
                }})
                .d3Force('charge', null)
                .d3Force('charge', 
                    window.d3.forceManyBody()
                        .strength(-120)
                );
            
            // Auto-rotate
            let angle = 0;
            setInterval(() => {{
                angle += 0.3;
                Graph.cameraPosition({{
                    x: 300 * Math.sin(angle * Math.PI / 180),
                    z: 300 * Math.cos(angle * Math.PI / 180)
                }});
            }}, 50);
        </script>
    </body>
    </html>
    """
    return html


def add_node_and_edge(label: str, node_type: str = "thought", parent_id: Optional[int] = None):
    """Add a node to the graph and connect it to parent if specified"""
    node_id = st.session_state.current_node_id
    st.session_state.current_node_id += 1
    
    node = {
        'id': node_id,
        'label': label[:50] + ('...' if len(label) > 50 else ''),
        'type': node_type,
        'group': len(st.session_state.nodes) % 5
    }
    st.session_state.nodes.append(node)
    
    if parent_id is not None:
        edge = {
            'source': parent_id,
            'target': node_id
        }
        st.session_state.edges.append(edge)
    
    return node_id


def main():
    st.title("🧠 Cognitive Cartography - AI Mind Visualization")
    st.markdown("*Visualizing the AI reasoning process in real-time*")
    
    # Sidebar controls
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Agent selection
        use_gemini = st.checkbox("Use Gemini API (requires API key)", value=False)
        
        if use_gemini:
            api_key = st.text_input("Gemini API Key", type="password", 
                                   value=os.getenv("GEMINI_API_KEY", ""))
            if api_key:
                agent = GeminiAgent(api_key)
            else:
                st.warning("Please provide API key")
                agent = MockAIAgent()
        else:
            agent = MockAIAgent()
            st.info("Using Mock AI Agent")
        
        # Reasoning parameters
        st.header("🎯 Reasoning Parameters")
        num_steps = st.slider("Number of reasoning steps", 3, 10, 5)
        
        # Qdrant simulator info
        st.header("💾 Vector Memory (Qdrant)")
        if 'qdrant' not in st.session_state:
            st.session_state.qdrant = QdrantSimulator()
        
        stats = st.session_state.qdrant.get_stats()
        st.metric("Stored Vectors", stats['total_vectors'])
        st.metric("Vector Dimension", stats['vector_dimension'])
        st.metric("Memory Size (MB)", f"{stats['memory_size_mb']:.2f}")
        
        # Controls
        st.header("🎮 Controls")
        if st.button("Clear Mind Map", type="secondary"):
            st.session_state.nodes = []
            st.session_state.edges = []
            st.session_state.reasoning_steps = []
            st.session_state.current_node_id = 0
            st.rerun()
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("🌐 3D Mind Map Visualization")
        
        # Create and display 3D graph
        if st.session_state.nodes:
            graph_html = create_3d_graph_html(
                st.session_state.nodes,
                st.session_state.edges
            )
            st.components.v1.html(graph_html, height=620, scrolling=False)
        else:
            st.info("👆 Enter a query to start visualizing the AI's reasoning process")
            # Show placeholder graph
            placeholder_nodes = [
                {'id': 0, 'label': 'Start Here', 'type': 'root', 'group': 0}
            ]
            placeholder_edges = []
            graph_html = create_3d_graph_html(placeholder_nodes, placeholder_edges)
            st.components.v1.html(graph_html, height=620, scrolling=False)
    
    with col2:
        st.header("💭 Reasoning Process")
        
        # Query input
        query = st.text_input("Enter your query:", 
                             placeholder="e.g., What is consciousness?")
        
        if st.button("🚀 Generate Reasoning", type="primary"):
            if query:
                with st.spinner("AI is thinking..."):
                    # Generate reasoning steps
                    steps = agent.generate_reasoning(query, num_steps)
                    
                    # Add root node
                    root_id = add_node_and_edge(f"Query: {query}", "query", None)
                    
                    # Add each reasoning step as a node
                    parent_id = root_id
                    for i, step in enumerate(steps):
                        # Add to Qdrant memory
                        vector_id = st.session_state.qdrant.add_vector(step)
                        
                        # Add to graph
                        node_id = add_node_and_edge(
                            f"Step {i+1}: {step}",
                            "reasoning",
                            parent_id
                        )
                        parent_id = node_id
                        
                        # Store reasoning step
                        st.session_state.reasoning_steps.append({
                            'step': i + 1,
                            'text': step,
                            'vector_id': vector_id
                        })
                        
                        time.sleep(0.1)  # Simulate thinking time
                    
                    st.success(f"Generated {len(steps)} reasoning steps!")
                    st.rerun()
            else:
                st.warning("Please enter a query first")
        
        # Display reasoning steps
        if st.session_state.reasoning_steps:
            st.subheader("📝 Reasoning Steps")
            for step_data in st.session_state.reasoning_steps[-10:]:
                with st.expander(f"Step {step_data['step']}", expanded=False):
                    st.write(step_data['text'])
                    st.caption(f"Vector ID: {step_data['vector_id']}")
        
        # Memory search
        st.subheader("🔍 Memory Search")
        search_query = st.text_input("Search in memory:", 
                                     placeholder="Search past reasoning...")
        
        if search_query and st.button("Search"):
            results = st.session_state.qdrant.search(search_query, top_k=3)
            if results:
                st.write("**Top Results:**")
                for result in results:
                    st.write(f"- {result['text'][:100]}...")
                    st.caption(f"Similarity: {result['similarity']:.3f}")
            else:
                st.info("No results found")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    **Features:**
    - 🤖 **AI Mind Simulation**: Mock agent or Gemini API for reasoning
    - 🌐 **3D Visualization**: Interactive force-directed graph
    - 💾 **Vector Memory**: Qdrant simulation for memory storage & retrieval
    - 🎮 **Interactive**: Click nodes, zoom, rotate, watch reasoning unfold
    """)


if __name__ == "__main__":
    main()
