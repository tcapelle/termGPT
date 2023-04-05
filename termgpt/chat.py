import os, argparse, json, atexit, subprocess
from sys import platform

import openai

from rich.text import Text
from rich.console import Console

console = Console()

GPT3 = "gpt-3.5-turbo"
GPT4 = "gpt-4"  # if you have access...


# # set api key
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    console.print("[bold red]Please set `OPENAI_API_KEY` environment variable[/]")
    exit(1)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=str, nargs="?", default=None, help="File to read [optional]")
    parser.add_argument("-r", "--resume", action="store_true", help="Resume previous session")
    parser.add_argument("-c", "--command", type=str, default=None, help="Command to run [optional]")
    parser.add_argument("-o", "--outfile", type=str, default=None, help="Output file [optional]")
    return parser.parse_args()


class Chat:
    """Class to handle chat with chatGPT, supports history and load from file"""

    def __init__(self, model_name=GPT3, file=None, resume=False, command=None, out_file=None):
        self.history_file = "chatgpt_history.json"
        self.out_file=out_file
        self.model_name=model_name
        if command:
            self.history = [{"role": "system", "content": f"Reply only with the terminal command required to perform the action on {platform}. Nothing else. In plain text, no fancy output."}, ]
            cmd = self(command)
            self.exec(cmd=cmd)
        else:
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
            model=self.model_name,
            messages=self.history,
        )
        out = r["choices"][0]["message"]["content"]
        self.add("assistant", out)
        console.print(Text(out, style="bold green"))
        return out

    def exec(self, cmd):
        """Refine the command to be executed"""
        cmd = cmd.replace("`", "")
        q = console.input(f"[bold red]Execute this command:[/] `${cmd}` (y/n) ")
        if q.lower() == "y":
            self.run_cmd(cmd)
        else:
            pass

    def run_cmd(self, cmd):
        try:
            subprocess.run(cmd, shell=True, check=True)
        except Exception as e:
            console.print("[bold red]Error executing command: [/]" + str(e))

    def input(self):
        q = console.input("[bold red]> [/]")
        return q

    def save(self):
        print(f"Saving history to {self.history_file}, you can restore this session with `--resume`")
        with open(self.history_file, "w") as f:
            json.dump(self.history, f)
        if self.out_file is not None:
            with open(self.out_file, "w") as out_f:
                print(f"Saving output to {self.out_file}")
                out_f.writelines("".join([h["content"] for h in self.history]))

def main(model_name):
    args = parse_args()
    chat = Chat(model_name, file=args.file, resume=args.resume, command=args.command, out_file=args.outfile)
    atexit.register(chat.save)
    if not args.command:
        while q := chat.input():
            _ = chat(q)

def gpt3(): main(GPT3)
def gpt4(): main(GPT4)