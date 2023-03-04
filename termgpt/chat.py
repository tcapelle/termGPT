import os, argparse

import openai

from rich.text import Text
from rich.console import Console

console = Console()

# set api key
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    console.print("[bold red]Please set OPENAI_API_KEY environment variable[/]")
    exit(1)

history = [
    {"role": "system", "content": "You are a helpful assistant."},
]


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=str, nargs="?", default=None, help="File to read [optional]")
    return parser.parse_args()


args = parse_args()
if args.file:
    with open(args.file, "r") as f:
        history.append({"role": "user", "content": "I will ask question about this file" + f.read()})

def main():
    while q := console.input("[bold red]> [/]"):
        history.append({"role": "user", "content": q})

        r = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=history,
        )
        out = r["choices"][0]["message"]["content"]
        formated_out = Text(out, justify="right")
        history.append({"role": "assistant", "content": out})
        console.print(f"\n[bold green]{out}[/]\n")
