from transformers import load_tool

text_summarizer = load_tool("summarization")

book_text = ""

with open('Flourishing: Why We Need Religion in a Globalized World .txt', 'r') as file:
    book_text = file.read()
    
summary = text_summarizer(book_text)
print(summary)