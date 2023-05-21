# Knowledgebase

## Goal
The purpose of knowledgebase is to remove the barrier between online users and books. It can access almost any book in existence and produces a shortened version containing the main points that can be read in 1-2 minutes.

## How to Use
1. Install the dependencies by running `npm install -r requirements.txt`
2. Set the OpenAI API Key in the .env file or copy paste it directly into main.py line 34.
3. Run `main.py` and query it title of any book you want
4. navigate to `/books` by doing `cd books`. It will have all the books you queried in separate folders and the generated summaries

## What's inside each book folder?
1. A pdf/epub version of the full book
2. Text-only .txt version of the book
3. Summary of the book
4. Shortened version of the full book
