# Knowledgebase

## Motivation
I realized that while there are many great online resources out on the internet, the chances of quality information being present in a book is far higher than it being present in a tweet or an article. The two biggest problems with books that I found were that:

1. they often cost money
2. some are dense and take a while to read to extract and consume the main ideas behind the book.

So, I created knowledgebase so that I (and others) can access any book for free using online libraries and read the core information from those books. 

## Objective
The objective of knowledgebase is to solve the two outlined problems, to make books freely accessible and easy to consume. Knowledgebase can access almost any book in existence and produces a shortened version of the book containing the main points that can be read in 1-2 minutes. 

## How to Use
1. Install the dependencies by running `npm install -r requirements.txt`
2. Set the OpenAI API Key in the .env file or copy paste it directly into main.py line 34.
3. Run `main.py` and query it title of any book you want
4. navigate to `/books` by doing `cd books`.
5. There will be an AI-generated shortened version of the book inside named `knowledge.txt`.

## Legality
Due to copyright issues that could get me and the users in trouble, the downloaded books are instantly deleted after the summary is created. Knowledgebase takes only the knowledge and insights from a book and shares them.
