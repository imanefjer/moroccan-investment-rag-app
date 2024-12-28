# Morocco Investment Knowledge Base

## Purpose of the Project
The Morocco Investment Knowledge Base is an intelligent web application designed to provide accurate, context-aware information about investing in Morocco. Using advanced natural language processing and a RAG (Retrieval-Augmented Generation) architecture, the system offers real-time responses to queries about investment opportunities, regulations, and economic conditions in Morocco.

### Key Features
- 🤖 AI-powered question answering about Morocco investment topics
- 🔄 Automatic web scraping for content updates (with robots.txt compliance)
- 💻 User-friendly interface with responsive design
- 🔍 Source transparency with viewable reference links
- 🤝 Ethical web scraping with robots.txt verification

## Technologies Used

### Backend
- Python 3.10+
- Flask (Web Framework)
- LangChain (LLM Framework)
- Ollama (Local LLM Integration)
- ChromaDB (Vector Database)
- BeautifulSoup4 (Web Scraping)

### Frontend
- HTML5
- CSS3
- Vanilla JavaScript
- Inter Font Family

## Installation

### Prerequisites
1. Python 3.10 or higher
2. Ollama installed and running locally
3. Git
4. Modern web browser

### Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/imanefjer/moroccan-investment-rag-app.git
cd morocco-investment-rag-app
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Ensure Ollama is running with the Llama3.2 model:
```bash
ollama pull llama3.2
ollama run llama3.2
```

## Usage

1. Start the Flask application:
```bash
export FLASK_ENV=development
flask run
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

3. Use the application:
- Type your investment-related question in the input field
- Click "Ask" or press Enter to submit
- View the AI-generated response based on the knowledge base
- View current sources using the "Show Sources" button


## Project Structure

### Key Components
- `app.py`: Main Flask application and API endpoints
- `scraper.py`: Web scraping functionality
- `vectorstore.py`: Vector database management
- `templates/`: HTML templates
- `static/`: CSS, JavaScript, and other static assets

### Using the Application

1. **Ask Questions**:
   - Type your investment-related question in the input field
   - Click "Ask" or press Enter to submit
   - View the AI-generated response based on the knowledge base

2. **Manage Sources**:
   - Click "Show Sources" to view current knowledge base sources
   - View source links for transparency
