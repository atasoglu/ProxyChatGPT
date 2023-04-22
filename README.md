# ProxyChatGPT
A semantic search based QA (question answering) implementation using ChatGPT conversations as proxy. 

## What is this for?

The purpose of this is to avoid repeated requests to ChatGPT asking for similar things (like general topics).

## Install

Install requirements:

`python -m pip install -r requirements.txt`

Also **spacy** model for lemmatizer:

`python -m spacy download en_core_web_md`


## Usage

First, you must export a chat history. You can use [
chatgpt-exporter](https://github.com/pionxzh/chatgpt-exporter) for this. Ensure that history is exported as **markdown** files. See [exported one](example/example.md).

Then parse the chat history to JSON:

`python parser.py -d my-history/ -o history.json`

Create index:

`python indexer.py history.json -o my-index`

Finally, query over it:

`python query.py my-index "say something about life"`