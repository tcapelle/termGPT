# OpenAI Chatbot

This program uses the OpenAI API to create a chatbot that can converse with users. The chatbot is powered by the GPT-3.5-turbo language model and can answer a wide range of questions.


## Install
> You will need and `openAI` api key, the app expects that the key is available as an environment variable: `OPENAI_API_KEY`.

```bash
$ pip install termgpt
```

## Usage

```bash
$ gpt 
> who are you?

I am an AI language model created by OpenAI. My purpose is to be of assistance and respond to your queries to the best of my abilities.
```

or ask question about a file:

```bash
$ gpt lotr.txt
> what is this file about?

This file is about The Lord of the Rings, a high-fantasy novel by J.R.R. Tolkien. It describes the plot, characters, and setting of the book, as well as its publication history, critical 
reception, and cultural impact. It also mentions Tolkien's influences and the numerous adaptations and derivative works that the novel has inspired.
```
