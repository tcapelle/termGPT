import os, argparse, json, atexit

import openai

from rich.text import Text
from rich.console import Console

console = Console()

# set api key
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    console.print("[bold red]Please set OPENAI_API_KEY environment variable[/]")
    exit(1)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=str, nargs="?", default=None, help="File to read [optional]")
    parser.add_argument("-r", "--resume", action="store_true", help="Resume previous session")
    return parser.parse_args()


class Chat:
    """Class to handle chat with chatGPT, supports history and load from file"""

    def __init__(self, file=None, resume=False):
        self.history_file = "chatgpt_history.json"
        self.history = [{"role": "system", "content": "You are a helpful assistant."}, ]
        if resume:
            with open(self.history_file, "r") as f:
                self.history = json.load(f)
                self._print_history(self.history)
        if file:
            with open(file, "r") as f:
                self.history.append({"role": "user", "content": "I will ask question about this file" + f.read()})

    def _print_history(self, history):
        console.print("--Resuming previous session--")
        for h in history:
            if h["role"] == "system":
                console.print(Text("[System] " + h["content"] +"\n", style="bold green"))
            elif h["role"] == "user":
                console.print("[bold red]> [/]" + h["content"])
            else:
                console.print(Text(h["content"], style="bold green"))

    def add(self, role, content):
        self.history.append({"role": role, "content": content})
    
    def __call__(self, question):
        self.add("user", question)
        r = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.history,
        )
        out = r["choices"][0]["message"]["content"]
        self.add("assistant", out)
        console.print(Text(out, style="bold green"))

    def input(self):
        q = console.input("[bold red]> [/]")
        return q

    def save(self):
        with open(self.history_file, "w") as f:
            json.dump(self.history, f)


def main():
    args = parse_args()
    chat = Chat(file=args.file, resume=args.resume)
    atexit.register(chat.save)
    while q := chat.input():
        chat(q)