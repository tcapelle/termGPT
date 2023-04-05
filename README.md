[![PyPI version](https://badge.fury.io/py/termgpt.svg)](https://badge.fury.io/py/termgpt)

# OpenAI Chatbot

This program uses the OpenAI API to create a chatbot that can converse with users. The chatbot is powered by the GPT-3.5-turbo (or 4) language model and can answer a wide range of questions. If you are like me and want to stay in the terminal, this is the tool for you.

# Breaking change: Now you can call gpt3 or gpt4 (if you have an api key for it)
Beware that using gpt4 is expensive (15x more than 3.5-turbo), so use it with care.

## Install
You will need and `openAI` api key, the app expects that the key is available as an environment variable: `OPENAI_API_KEY`.

```bash
$ pip install termgpt
```

## Usage

```bash
$ gpt3 
> who are you?

I am an AI language model created by OpenAI. My purpose is to be of assistance and respond to your queries to the best of my abilities.
```

or ask question about a file:

```bash
$ gpt3 lotr.txt
> what is this file about?

This file is about The Lord of the Rings, a high-fantasy novel by J.R.R. Tolkien. It describes the plot, characters, and setting of the book, as well as its publication history, critical 
reception, and cultural impact. It also mentions Tolkien's influences and the numerous adaptations and derivative works that the novel has inspired.
```

## [New] you can resume you previous conversation

We keep track of your conversation on a file now `chatgpt_history.json` so we can resume from it by passing the `-r` flag.

```bash
$ gpt3 -r
--Resuming previous session--
[System] You are a helpful assistant.

> what is relu
ReLU (Rectified Linear Unit) is an activation function commonly used in deep neural networks. It is defined as f(x) = max(0, x). In other 
words, the output of the function is zero when the input is negative, and equal to the input when the input is positive. ReLU has become 
popular in deep learning because it helps to address the vanishing gradient problem and allows for faster training of neural networks.
> and gelu?
GeLU (Gaussian Error Linear Unit) is another activation function used in deep neural networks. It is defined as f(x) = 0.5 * x * (1 + erf(x /
sqrt(2))), where erf is the error function. GeLU is a smooth approximation of the ReLU function, and has been shown to work well in certain 
types of neural networks. It is particularly useful in sequence modeling tasks such as natural language processing, where the input data 
often has a Gaussian distribution. GeLU is similar to ReLU in terms of its computational efficiency, but can potentially improve the 
performance of a neural network by providing a more accurate representation of the input data.
> 
```


## [New] Run commands in your Terminal (at your own risk!)

```bash
$ gpt3 -c "list all files in this folder with sizes"
```
ls -lh
```
total 40
-rw-r--r--  1 tcapelle  staff   2.4K Mar  6 09:43 README.md
drwxr-xr-x  4 tcapelle  staff   128B Mar  3 16:22 build
-rw-r--r--  1 tcapelle  staff   276B Mar  6 13:55 chatgpt_history.json
drwxr-xr-x  4 tcapelle  staff   128B Mar  3 17:07 dist
-rw-r--r--  1 tcapelle  staff    51B Mar  3 15:33 key
-rw-r--r--  1 tcapelle  staff   2.5K Mar  3 16:40 lotr.txt
-rw-r--r--  1 tcapelle  staff   955B Mar  3 18:17 setup.py
drwxr-xr-x  6 tcapelle  staff   192B Mar  6 09:00 termgpt
drwxr-xr-x  8 tcapelle  staff   256B Mar  6 08:34 termgpt.egg-info
```

## Recover output

The history of your conversation is stored in `chatgpt_history.json` so you can recover it later. You also use the `-o` flago to store the output in a plain text file.

```bash
$ Can you write a short poem about chatbots, guacamole and cars?

Chatbots beep and bloop,
Serving customers with ease,
Guac and chips in hand.

Cars race on, onwards,
As chatbots assist the ride,
Dipping chips divine.

Time taken: 2.27 seconds
Saving history to chatgpt_history.json, you can restore this session with `--resume`
Saving output to poem.txt
```

