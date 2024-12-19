from flask import Flask, request, jsonify, send_from_directory, render_template
from scraper import scrape_websites
from vectorstore import create_vectorstore
from langchain_ollama.llms import OllamaLLM
# from old.pdf_loader import load_pdfs

app = Flask(__name__)

# Define the initial sources
urls = [
    "https://investingmorocco.com/why-morocco-2/",
    "https://legacy.export.gov/article?id=Morocco-Market-Overview",
    "https://legacy.export.gov/article?id=Morocco-Market-Challenges",
    "https://legacy.export.gov/article?id=Morocco-Market-Opportunities",
    "https://legacy.export.gov/article?id=Morocco-Market-Entry-Strategy",
    "https://www.state.gov/u-s-relations-with-morocco/",
    "https://legacy.export.gov/article?id=Morocco-Trade-Barriers",
    "https://legacy.export.gov/article?id=Morocco-Import-Tariffs",
    "https://legacy.export.gov/article?id=Morocco-Import-Requirements-and-Documentation",
    "https://legacy.export.gov/article?id=Morocco-Labeling-Marking-Requirements",
    # "https://pwcmaroc.pwc.fr/fr/pwc-au-maroc/invest-in-morocco.html",
    # "https://en.wikipedia.org/wiki/Economy_of_Morocco",
    "https://www.morocconow.com/wp-content/uploads/2021/11/PitchGeneraliste.pdf",
    "https://www.morocconow.com/wp-content/uploads/2021/10/Guide_des_affaires.pdf",
    
]

# Load both sources
web_docs = scrape_websites(urls)

# Combine documents
all_docs = web_docs


# Create vectorstore with combined documents
vectorstore = create_vectorstore(all_docs)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask_question():
    question = request.json['question']
    print(f"Question: {question}, Type: {type(question)}")
    
    if vectorstore:
        retrieved_docs = vectorstore.similarity_search(question, k=5)
        context = ''.join([doc.page_content for doc in retrieved_docs])
        
        prompt = f"""You are an investment advisor for Morocco.
Question: {question}
Context: {context}
Instructions:
- Only include facts directly stated in the context
- Do not elaborate beyond the given information
- If the information isn't explicitly in the context, say: "I cannot find this specific information in the available data."
- Do not make predictions or assumptions
- Keep the response focused and factual
IMPORTANT: Only use information that is explicitly present in the provided context. Do not add any external knowledge or make assumptions.
Response:"""
        llm = OllamaLLM(
            model="llama2",
            temperature=0.5,  # Very low temperature for consistent, fact-based responses
            system="You are an investment advisor for Morocco. Only provide information that is explicitly mentioned in the given context. Do not make assumptions or add external knowledge."
        )
        
        try:
            response = llm.invoke(prompt)
            return jsonify({'answer': str(response)})
        except Exception as e:
            print(f"Error generating response: {e}")
            return jsonify({'answer': 'An error occurred while generating the response'}), 500
    else:
        return jsonify({'answer': 'No content available to answer the question.'}), 400

@app.route('/add_url', methods=['POST'])
def add_url():
    global urls, vectorstore, all_docs
    new_url = request.json.get('url')
    
    if not new_url:
        return jsonify({'error': 'No URL provided'}), 400
        
    # Add the new URL to the list
    urls.append(new_url)
    
    # Scrape the new URL
    new_docs = scrape_websites([new_url])
    
    if new_docs:
        # Add new documents to existing ones
        all_docs.extend(new_docs)
        # Update vectorstore with all documents
        vectorstore = create_vectorstore(all_docs)
        print("vectorstore created url added")
        return jsonify({'message': 'URL added and processed successfully'})
    else:
        urls.remove(new_url)  # Remove URL if scraping failed
        return jsonify({'error': 'Failed to process URL'}), 400

@app.route('/sources', methods=['GET'])
def get_sources():
    if all_docs:
        # Extract unique sources from all_docs
        sources = list(set(doc.metadata.get('source', '') for doc in all_docs))
        return jsonify({'sources': sources})
    return jsonify({'sources': []})

if __name__ == '__main__':
    app.run()
