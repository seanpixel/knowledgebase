# Getting book to .txt
from libgen_api import LibgenSearch
import requests
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import PyPDF2
import os

# Summarize & Questions from .txt
from langchain.chains.summarize import load_summarize_chain
from langchain.chains.question_answering import load_qa_chain
from langchain import OpenAI
from langchain.text_splitter import TokenTextSplitter
from langchain.docstore.document import Document

# Misc Imports
import openai
from dotenv import load_dotenv

load_dotenv()

def generate(prompt):
    completion = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role":"system", "content": "You are a highly skilled book writer"},
        {"role": "user", "content": prompt},
        ]
    )

    return completion.choices[0].message["content"]

OPENAI_API_KEY = "" or os.environ["OPENAI_API_KEY"] # Set key in .env or put it between the quotation marks

openai.api_key = OPENAI_API_KEY

# Getting Text from book
def extract_text_from_epub(epub_path):
    book = epub.read_epub(epub_path)

    text = ''
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            soup = BeautifulSoup(item.get_content(), 'html.parser')
            text += soup.get_text()

    return text

def extract_text_from_pdf(pdf_path):
    pdf_file_obj = open(pdf_path, 'rb')  # Open the PDF file in binary read mode
    pdf_reader = PyPDF2.PdfFileReader(pdf_file_obj)  # Create a PDF reader object
    text = ""

    # Loop through all the pages in the PDF file
    for page_num in range(pdf_reader.numPages):
        page_obj = pdf_reader.getPage(page_num)  # Get a page object
        text += page_obj.extractText()  # Extract text from the page object

    pdf_file_obj.close()  # Close the PDF file object
    return text


# Load Langchain LLM and Chains
llm = OpenAI(temperature=0.3, openai_api_key=OPENAI_API_KEY)
summary_chain = load_summarize_chain(llm, chain_type="map_reduce")
qa_chain = load_qa_chain(llm, chain_type="map_reduce")


# str: Long Text --> Langchain Docs
def makeDocs(text):
    text_splitter = TokenTextSplitter(chunk_size=3000)
    texts = text_splitter.split_text(text)
    docs = [Document(page_content=t) for t in texts]
    return docs

# Long Text --> str: Summary of Long Text
def summarize(text):
    docs = None
    if(type(text) == str):
        docs = makeDocs(text)
    else:
        docs = text
    
    summary = summary_chain.run(docs)
    return summary

# Long Text, Question --> str: Answer to question based on Long Text
def answerQuestion(text, question):
    docs = None
    if(type(text) == str):
        docs = makeDocs(text)
    else:
        docs = text

    query = [question]
    answer = qa_chain.run(input_documents=docs, question=query)
    return answer


while True:
    # User Interaction
    isPdf = False
    isEpub = False
    book_title = input("Enter Book Title: ")
    book_text = ""
    s = LibgenSearch()
    title_filters = {"Extension": "pdf"}
    pdf_results = s.search_title_filtered(book_title, title_filters)

    title_filters = {"Extension": "epub"}
    epub_results = s.search_title_filtered(book_title, title_filters)

    if(len(pdf_results) > 0):
        isPdf = True

    if(len(epub_results) > 0):
        isEpub = True

    os.makedirs(f"books/{book_title}")
    
    if(isEpub):
        item_to_download = epub_results[0]
        download_links = s.resolve_download_links(item_to_download)
        # print("is Epub")
        # print(download_links)
        response = requests.get(download_links['GET'])

        # Save the content to a file
        book_path = f'books/{book_title}/book.epub'


        with open(book_path, 'wb') as f:
            f.write(response.content)

        # Extract text from book
        book_text += extract_text_from_epub(book_path)

        with open(f'books/{book_title}/full_text.txt', 'w') as file:
            file.write(book_text)


    elif(isPdf):
        item_to_download = pdf_results[0]
        download_links = s.resolve_download_links(item_to_download)
        # print("is Pdf")
        # print(download_links)
        response = requests.get(download_links['GET'])

        # Save the content to a file
        book_path = f'books/{book_title}/book.pdf'

        with open(book_path, 'wb') as f:
            f.write(response.content)

        # Extract text from book
        book_text += extract_text_from_pdf(book_path)

        with open(f'books/{book_title}/full_text.txt', 'w') as file:
            file.write(book_text)
    else:
        print("No book found")
        continue

    summary = summarize(book_text)
    #print(summary)
    main_points = answerQuestion(book_text, "What are some main points in this text?")
    #print(main_points)

    
    # Writing Summary & Shortened Versions
    with open(f'books/{book_title}/summary.txt', 'a') as file:
        file.write(summary + "\n\n" + main_points)

    prompt = f"The following is a summary and key points from a book. Given the information, recreate a short version of the book\n\nSummary: {summary}\n\nMain Points: {main_points}\n\nShortened version of the book: "
    short_version = generate(prompt)

    with open(f'books/{book_title}/shortened.txt', 'a') as file:
        file.write(short_version)
    

    


