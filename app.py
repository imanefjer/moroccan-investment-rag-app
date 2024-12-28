from flask import Flask, request, jsonify, render_template
from scraper import scrape_websites
from vectorstore import create_vectorstore
from langchain_ollama.llms import OllamaLLM
from sentence_transformers import  util
from langchain_ollama import OllamaEmbeddings

app = Flask(__name__)

# Define the initial sources
urls = [
    "https://legacy.export.gov/article?id=Morocco-Market-Overview",
    "https://legacy.export.gov/article?id=Morocco-Market-Challenges",
    "https://legacy.export.gov/article?id=Morocco-Market-Opportunities",
    "https://legacy.export.gov/article?id=Morocco-Market-Entry-Strategy",
    "https://www.morocconow.com/wp-content/uploads/2021/11/PitchGeneraliste.pdf",
    "https://www.morocconow.com/wp-content/uploads/2021/10/Guide_des_affaires.pdf",
    "https://www.mcinet.gov.ma/en/content/industry-0/industrial-acceleration-plan-2014-2020-0",
    "https://www.mcinet.gov.ma/en/content/commerce-0/digitalization-trade",
    "https://www.mcinet.gov.ma/en/content/tatwir-green-growth",
    "https://www.mcinet.gov.ma/en/content/export-support-programs",
    "https://www.mcinet.gov.ma/en/content/consumer-protection",
    
]

# Load both sources
web_docs = scrape_websites(urls)

# Combine documents
all_docs = web_docs

# Create vectorstore with combined documents
vectorstore = create_vectorstore(all_docs)

# Load a pre-trained model for semantic similarity
similarity_model = OllamaEmbeddings(model="all-minilm")
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask_question():
    question = request.json['question']
    print(f"Question: {question}, Type: {type(question)}")
    
    if vectorstore:
        retriever = vectorstore.as_retriever(search_type="similarity",search_kwargs={"k":5})
        retrieved_docs = retriever.invoke(question)
        context = ''.join([doc.page_content for doc in retrieved_docs])        
        # Calculate semantic similarity
        question_embedding = similarity_model.embed_query(question)
        context_embedding = similarity_model.embed_documents([context])[0] 
        similarity_score = util.pytorch_cos_sim(question_embedding, context_embedding).item()
        
        relevance_threshold = 0.2
       
        # # Check if the context is relevant to the question
        if similarity_score < relevance_threshold:
            return jsonify({'answer': 'The context does not contain relevant information for your question.'})
        
        prompt = f"""You are an investment advisor for Morocco. 
IMPORTANT: Only use information that is explicitly present in the provided context. Do not add any external knowledge or make assumptions.
Instructions:
- Only use information explicitly mentioned in the context.
- Do not elaborate beyond the given information.
- If the information isn't explicitly  in the context, say : "I cannot find this specific information in the available data."
- Keep responses short and professional unless the user specifically requests more detail.
- Do not make predictions or assumptions.
- Keep the response focused, factual and to the point.
Question: {question}
Context: {context}
Response:"""
        llm = OllamaLLM(
            model="llama3.2",
            temperature=0.5,
        )
        
        try:
            response = llm.invoke(prompt)
            return jsonify({'answer': response})
        except Exception as e:
            print(f"Error generating response: {e}")
            return jsonify({'answer': 'An error occurred while generating the response'}), 500
    else:
        return jsonify({'answer': 'No content available to answer the question.'}), 400

@app.route('/sources', methods=['GET'])
def get_sources():
    if all_docs:
        # Extract unique sources from all_docs
        sources = list(set(doc.metadata.get('source', '') for doc in all_docs))
        return jsonify({'sources': sources})
    return jsonify({'sources': []})

if __name__ == '__main__':
    app.run()
