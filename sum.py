import requests
from bs4 import BeautifulSoup
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import nltk

nltk.download('punkt')


def fetch_webpage(url):
    try:
        response=requests.get(url=url)
        response.raise_for_status()
        return response.text 
    except Exception as e:
        print(f"Error Fetching the webpage {e}")
        return None 
    
def text_from_webpage(complete_html):
    soup=BeautifulSoup(complete_html,'html.parser')              
    for items in soup(['script', 'style']):            
        items.decompose()           
    
    text_elements = []
    for tag in ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
        for element in soup.find_all(tag):
            text_elements.append(element.get_text(strip=True))
    
    full_text = ' '.join(text_elements)
    return full_text

def summarize_text(text: str, sentence_count: int = 5) -> str:
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, sentence_count)
    return " ".join(str(sentence) for sentence in summary)

def main():
    url = input("Enter the URL of the webpage to summarize: ")
    sentence_count = int(input("Enter the number of sentences for the summary: "))

    try:
        html_content = fetch_webpage(url)
        text_content = text_from_webpage(html_content)
        summary = summarize_text(text_content, sentence_count)
        print("\nSummary:")
        print(summary)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
