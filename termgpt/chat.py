import os, argparse, json, atexit, subprocess, time
from dataclasses import dataclass

import openai

from rich.text import Text
from rich.console import Console
from rich.markdown import Markdown

from termgpt.roles import assistant_role, document_role, commander_role

console = Console()

GPT3 = "gpt-3.5-turbo"
GPT4 = "gpt-4"  # if you have access...
PRICING = {GPT3: (0.02, 0.02), GPT4: (0.03, 0.06)} # prices per 1k tokens

if not os.getenv("OPENAI_API_KEY"):
    console.print("[bold red]Please set `OPENAI_API_KEY` environment variable[/]")
    exit(1)

def parse_args():
    parser = argparse.ArgumentParser(usage="termGPT [options] [file]", description="Chat with GPT-3/4. If no file is provided, you will be prompted to enter a question.")
    parser.add_argument("file", type=str, nargs="?", default=None, help="File to read [optional]")
    parser.add_argument("-r", "--resume", action="store_true", help="Resume previous session")
    parser.add_argument("-c", "--command", type=str, default=None, help="Command to run [optional]")
    parser.add_argument("-o", "--outfile", type=str, default=None, help="Output file [optional]")
    parser.add_argument("-no_md", "--no_markdown", action="store_false", help="Disable markdown rendering")
    return parser.parse_args()

@dataclass
class APIStats:
    """Class to handle API usage stats"""
    model_name: str = GPT3
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0

    def cost(self):
        token_prices = PRICING[self.model_name]
        return (token_prices[0] * self.prompt_tokens + token_prices[1] * self.completion_tokens) / 1000

    def update(self, stats):
        self.prompt_tokens += stats['prompt_tokens']
        self.completion_tokens += stats['completion_tokens']
        self.total_tokens += stats['total_tokens']

    def __str__(self):
        return (f"Prompt tokens: {self.prompt_tokens}, Completion tokens: {self.completion_tokens}, "
                f"Total tokens: {self.total_tokens}, Estimated cost: ${self.cost():.2f}")

class Chat:
    """Class to handle chat with chatGPT, supports history and load from file"""

    def __init__(self, model_name=GPT3, file=None, resume=False, command=None, out_file=None, markdown=True):
        self.history_file = "chatgpt_history.json"
        self.out_file=out_file
        self.model_name=model_name
        self.usage = APIStats(model_name=model_name)
        self.output_render = Markdown if markdown else Text
        if command:
            self.history = [{"role": "system", "content": commander_role}, ]
            cmd = self(command)
            self.exec(cmd=cmd)
        else:
            self.history = [{"role": "system", "content": assistant_role}, ]
        if resume:
            with open(self.history_file, "r") as f:
                self.history = json.load(f)
                self._print_history(self.history)
        if file:
            with open(file, "r") as f:
                self.history = [{"role": "system", "content":  document_role + f.read()}, ]

    def _print_history(self, history):
        console.print("--Resuming previous session--")
        for h in history:
            if h["role"] == "system":
                console.print(Text("[System] " + h["content"] +"\n", style="bold green"))
            elif h["role"] == "user":
                console.print("[bold red]> [/]" + h["content"])
            else:
                console.print(self.output_render(h["content"]))

    def add(self, role, content):
        self.history.append({"role": role, "content": content})
    
    def __call__(self, question):
        self.add("user", question)
        t0 = time.perf_counter()
        r = openai.ChatCompletion.create(
            model=self.model_name,
            messages=self.history,
        )
        out = r["choices"][0]["message"]["content"]
        self.usage.update(r['usage'])
        self.add("assistant", out)
        total_time = time.perf_counter() - t0
        console.print(self.output_render(out, style="bold green"))
        console.print(f"Time taken: {total_time:.2f} seconds")
        return out

    def exec(self, cmd):
        """Refine the command to be executed"""
        cmd = cmd.replace("`", "")
        q = console.input(f"[bold red]Execute this command (press return to run):[/] \n$ {cmd}").lower()
        if (q == "y") or (q == ""):
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
        console.print(f"-------------\nSaving history to {self.history_file}, you can restore this session with `--resume`")
        console.print(str(self.usage))
        with open(self.history_file, "w") as f:
            json.dump(self.history, f)
        if self.out_file is not None:
            with open(self.out_file, "w") as out_f:
                print(f"Saving output to {self.out_file}")
                out_f.writelines([h["content"] for h in self.history])

exit_commands = ["exit", "quit", "q", "bye", "goodbye", "stop", "end", "finish", "done"]

def main(model_name):
    args = parse_args()
    chat = Chat(model_name, file=args.file, resume=args.resume, command=args.command, out_file=args.outfile, markdown=args.no_markdown)
    atexit.register(chat.save)
    if not args.command:
        while q := chat.input():
            if q in exit_commands:
                break
            _ = chat(q)

def gpt3(): main(GPT3)
def gpt4(): main(GPT4)