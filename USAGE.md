# Usage Guide - Cognitive Cartography

## Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/wenizmohamed/Cognitive-cartography.git
cd Cognitive-cartography

# Install dependencies
pip install -r requirements.txt
```

### 2. Running the App

**Option A: Using Mock AI Agent (No API Key Required)**
```bash
streamlit run app.py
```

**Option B: Using Gemini API**
```bash
# Set your API key
export GEMINI_API_KEY="your-gemini-api-key"
streamlit run app.py
```

Or provide the API key through the web interface.

## How to Use

### Step 1: Configure the AI Agent
- In the sidebar, choose between Mock AI Agent or Gemini API
- If using Gemini, enter your API key
- Adjust the "Number of reasoning steps" slider (3-10 steps)

### Step 2: Generate Reasoning
1. Enter a question in the "Enter your query" field
   - Example: "What is consciousness?"
   - Example: "How does machine learning work?"
2. Click the "🚀 Generate Reasoning" button
3. Watch as the AI generates reasoning steps in real-time

### Step 3: Explore the Mind Map
- **3D Visualization**: The left panel shows a 3D force-directed graph
- **Auto-rotation**: The graph rotates automatically for better viewing
- **Node colors**: Different colors represent different thought groups
- **Click nodes**: Click any node to see detailed information
- **Drag**: Drag to manually rotate the view

### Step 4: View Reasoning Steps
- The right panel shows all generated reasoning steps
- Click on any step to expand and see full details
- Each step includes a Vector ID showing its storage in memory

### Step 5: Search Memory
- Use the "Memory Search" feature to find similar thoughts
- Type a search query (e.g., "consciousness")
- Click "Search" to find the top 3 most similar stored vectors
- Results show similarity scores

### Step 6: Monitor Vector Memory
The sidebar shows real-time statistics:
- **Stored Vectors**: Total number of thoughts in memory
- **Vector Dimension**: Size of each embedding (384)
- **Memory Size**: Total memory usage in MB

## Example Queries

Try these queries to explore different reasoning patterns:

### Philosophy
- "What is consciousness?"
- "What is the nature of reality?"
- "Do we have free will?"

### Science
- "How does quantum computing work?"
- "What is dark matter?"
- "How do neural networks learn?"

### Technology
- "What is artificial intelligence?"
- "How does blockchain work?"
- "What are Large Language Models?"

### Abstract Concepts
- "What is creativity?"
- "How does memory work?"
- "What is intelligence?"

## Tips and Tricks

### 1. Adjusting Reasoning Depth
- Start with 3-5 steps for quick exploration
- Use 7-10 steps for deeper analysis
- More steps = more detailed mind map

### 2. Using Gemini API Effectively
- Use clear, specific questions
- Gemini provides more sophisticated reasoning
- Check your API quota to avoid rate limits

### 3. Exploring the Mind Map
- Let the auto-rotation run to see all angles
- Click nodes to pause and examine connections
- The graph shows how thoughts connect

### 4. Memory Search
- Search for key concepts from your queries
- Use partial words to find related thoughts
- Similarity scores help identify relevance

### 5. Clearing the Mind Map
- Use "Clear Mind Map" button to start fresh
- This also clears the vector memory
- Useful when switching topics

## Troubleshooting

### Issue: App won't start
**Solution**: Make sure all dependencies are installed
```bash
pip install -r requirements.txt --upgrade
```

### Issue: Gemini API not working
**Solution**: 
1. Verify your API key is correct
2. Check your internet connection
3. Ensure you have API credits available
4. The app will fall back to Mock Agent if Gemini fails

### Issue: 3D graph not showing
**Solution**: 
- Make sure JavaScript is enabled in your browser
- Try refreshing the page
- Check browser console for errors
- Some ad blockers may interfere with external libraries

### Issue: Memory search returns no results
**Solution**: 
- Generate some reasoning steps first
- Make sure vectors are stored (check sidebar stats)
- Try different search terms

## Advanced Usage

### Environment Variables
Set these before running the app:
```bash
export GEMINI_API_KEY="your-key"  # For Gemini API
export STREAMLIT_SERVER_PORT=8502  # Custom port
```

### Custom Port
```bash
streamlit run app.py --server.port 8502
```

### Headless Mode
```bash
streamlit run app.py --server.headless true
```

## Understanding the Output

### Node Types
- **Query Nodes**: Your original question (root of the graph)
- **Reasoning Nodes**: Individual thinking steps
- **Connected by Edges**: Show the flow of reasoning

### Vector IDs
Each reasoning step is assigned a unique Vector ID when stored in the simulated Qdrant database. This ID can be used to trace thoughts in memory.

### Similarity Scores
- Range from -1.0 to 1.0
- Higher scores = more similar
- Based on cosine similarity of vector embeddings

## Next Steps

Once you're comfortable with the basics:
1. Try complex, multi-part questions
2. Compare Mock Agent vs. Gemini reasoning
3. Explore how different topics create different graph structures
4. Use memory search to find connections between different reasoning sessions

## Support

For issues, questions, or contributions:
- Open an issue on GitHub
- Check the README.md for more information
- Review the code in app.py for implementation details

Happy exploring! 🧠✨
