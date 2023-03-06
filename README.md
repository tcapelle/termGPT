[![PyPI version](https://badge.fury.io/py/termgpt.svg)](https://badge.fury.io/py/termgpt)

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

## [New] you can resume you previous conversation

We keep track of your conversation on a file now `chatgpt_history.json` so we can resume from it by passing the `-r` flag.

```bash
$ gpt -r
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
$ gpt -c "list all files in this folder with sizes"
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