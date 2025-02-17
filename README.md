[![PyPI version](https://badge.fury.io/py/termgpt.svg)](https://badge.fury.io/py/termgpt)

# termGPT: Chatbot in the Terminal

TermGPT v1.0.0 introduces exciting new features including improved conversation history management and experimental function-calling support for executing Linux commands from your terminal. This program uses Gemini Flash by default, but any [LiteLLM model](https://docs.litellm.ai/docs/providers) is supported.

## Now you can use the `llm` command (Like Simon's tool)

In this version, these have been consolidated into a single entry point:

```bash
$ llm "list all files in this folder with sizes"
```

If you want to chat with Claude, you can use the `-m` flag:

```bash
$ llm -m claude-3-5-sonnet-20240620
```

## Install
You will need an GEMINI API key, which should be available as an environment variable named `GEMINI_API_KEY`.

```bash
$ pip install termgpt
```

## Usage

**Interactive Chat:**

```bash
$ llm
> let's check git status
To check the git status, use the command `git status`. This command will show you the current status of your git repository, including any modified, staged, or untracked files.
```

**Run Terminal Commands:**

You can execute commands by passing them as a quoted argument:

```bash
$ llm "list all files in this folder with sizes"
Use `ls -l` to list all files in the current directory, along with their sizes, modification dates, and permissions.
Execute this command (press return to run): 
$ ls -l
-rw-r--r--  1 user staff   2.4K Mar 6 09:43 README.md
...
```

Happy chatting!

