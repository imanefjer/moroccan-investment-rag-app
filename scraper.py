import bs4
import urllib.robotparser
import os
import requests
from PyPDF2 import PdfReader
from io import BytesIO
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain.schema import Document
os.environ['USER_AGENT'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'

def is_allowed_to_scrape(url, user_agent='*'):
    # Check robots.txt
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(url + "/robots.txt")
    try:
        rp.read()
        return rp.can_fetch(user_agent, url)
    except:
        # If robots.txt doesn't exist or can't be read, assume it's allowed
        return True

def is_pdf_url(url):
    return url.lower().endswith('.pdf')

def scrape_pdf(url):
    try:
        response = requests.get(url)
        pdf = PdfReader(BytesIO(response.content))
        
        # Extract text from all pages
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
            
        # Create a document with the PDF content
        return [Document(
            page_content=text,
            metadata={"source": url}
        )]
    except Exception as e:
        print(f"Error processing PDF {url}: {e}")
        return None

def scrape_websites(urls):
    # Separate PDFs and web pages
    pdf_urls = [url for url in urls if is_pdf_url(url)]
    web_urls = [url for url in urls if not is_pdf_url(url)]
    
    documents = []

    # Process PDFs without robots.txt check
    for url in pdf_urls:
        pdf_docs = scrape_pdf(url)
        if pdf_docs:
            documents.extend(pdf_docs)
        else:
            print(f"Failed to process PDF: {url}")

    # Process web pages with robots.txt check
    allowed_web_urls = [url for url in web_urls if is_allowed_to_scrape(url)]
    if allowed_web_urls:
        bs4_strainer = bs4.SoupStrainer(['article', 'main', 'div'])
        loader = WebBaseLoader(
            web_paths=allowed_web_urls,
            bs_kwargs={"parse_only": bs4_strainer}
        )
        try:
            web_docs = loader.load()
            documents.extend(web_docs)
        except Exception as e:
            print(f"Error loading websites: {e}")

    return documents if documents else None
