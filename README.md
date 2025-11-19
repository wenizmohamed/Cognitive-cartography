# 🧠 Cognitive Cartography - AI Mind Visualization

An interactive application that simulates and visualizes the AI reasoning process using 3D force-directed graphs. Watch as the AI "thinks" and see how thoughts connect in real-time!

## 🎯 What This App Does

1. **Simulates the "AI Mind"**: Runs a mock agent (or connects to Gemini API if you have a key) to generate reasoning steps
2. **Visualizes the Mind Map**: Uses an embedded 3D force-directed graph (via JavaScript inside Streamlit) to show thoughts connecting in real-time
3. **Simulates Qdrant**: Mimics the vector storage and retrieval process to show how memory works
4. **Interactive**: Click nodes, zoom, rotate, and watch the reasoning unfold

## 🚀 Features

- 🤖 **AI Agent Options**:
  - Mock AI Agent (no API key required) - generates simulated reasoning steps
  - Google Gemini API integration for real AI reasoning

- 🌐 **3D Visualization**:
  - Interactive force-directed graph showing thought connections
  - Auto-rotating view for better perspective
  - Color-coded nodes by thought groups
  - Click nodes to see details

- 💾 **Vector Memory System**:
  - Simulates Qdrant vector database
  - Stores reasoning steps as embeddings
  - Search functionality to find similar thoughts
  - Real-time memory statistics

- 🎮 **Interactive Controls**:
  - Adjustable reasoning depth (3-10 steps)
  - Memory search functionality
  - Clear mind map option
  - Node clicking for detailed information

## 📦 Installation

1. Clone the repository:
```bash
git clone https://github.com/wenizmohamed/Cognitive-cartography.git
cd Cognitive-cartography
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## 🎮 Usage

### Running with Mock AI Agent (No API Key Required)

```bash
streamlit run app.py
```

The app will start with a mock AI agent that generates simulated reasoning steps.

### Running with Gemini API

1. Get a Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

2. Run the app:
```bash
streamlit run app.py
```

3. In the sidebar:
   - Check "Use Gemini API"
   - Enter your API key
   - Start generating reasoning!

Alternatively, set your API key as an environment variable:
```bash
export GEMINI_API_KEY="your-api-key-here"
streamlit run app.py
```

## 🎨 How to Use

1. **Enter a Query**: Type your question or topic in the query input box
2. **Generate Reasoning**: Click the "🚀 Generate Reasoning" button
3. **Watch the Visualization**: See the 3D mind map grow as the AI thinks
4. **Interact with Nodes**: Click on nodes to see detailed information
5. **Search Memory**: Use the search feature to find related thoughts
6. **Adjust Parameters**: Use the sidebar to control reasoning depth

## 🏗️ Architecture

### Components

1. **MockAIAgent**: Generates simulated reasoning steps using templates
2. **GeminiAgent**: Connects to Google's Gemini API for real AI reasoning
3. **QdrantSimulator**: Simulates vector database functionality
   - Generates mock embeddings (384-dimensional)
   - Performs similarity search
   - Tracks memory statistics

4. **3D Visualization**: 
   - Uses `3d-force-graph` JavaScript library
   - Embedded in Streamlit via `st.components.v1.html`
   - Real-time updates as reasoning progresses

## 🔧 Technical Details

- **Frontend**: Streamlit for UI, 3D Force Graph for visualization
- **Vector Embeddings**: 384-dimensional normalized vectors
- **Graph Structure**: Nodes represent thoughts, edges represent connections
- **Memory**: In-memory vector storage with similarity search

## 📝 Example Queries

Try these queries to see the AI reasoning process:

- "What is consciousness?"
- "How does learning work?"
- "Explain quantum computing"
- "What is the nature of reality?"
- "How do neural networks think?"

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- 3D visualization powered by [3d-force-graph](https://github.com/vasturiano/3d-force-graph)
- AI reasoning via [Google Gemini API](https://ai.google.dev/)
- Inspired by Qdrant vector database concepts

## 📞 Support

For questions or issues, please open an issue on GitHub.