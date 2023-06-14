import json, subprocess, time

from rich.text import Text
from rich.console import Console
from rich.markdown import Markdown

from termgpt.roles import assistant_role, document_role, commander_role

class ChatWithHistory:
    """Class to handle chat with chatGPT, supports history and load from file"""

    def __init__(self, file=None, resume=False, command=None, out_file=None, markdown=True):
        self.console = console = Console()
        self.history_file = "chatgpt_history.json"
        self.out_file=out_file
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
        self.console.print("--Resuming previous session--")
        for h in history:
            if h["role"] == "system":
                self.console.print(Text("[System] " + h["content"] +"\n", style="bold green"))
            elif h["role"] == "user":
                self.console.print("[bold red]> [/]" + h["content"])
            else:
                self.console.print(self.output_render(h["content"]))

    def append(self, role, content):
        self.history.append({"role": role, "content": content})
    
    def call(self, question):
        pass

    def __call__(self, question):
        self.append("user", question)
        t0 = time.perf_counter()
        out = self.call()
        self.append("assistant", out)
        total_time = time.perf_counter() - t0
        self.console.print(self.output_render(out, style="bold green"))
        self.console.print(f"Time taken: {total_time:.2f} seconds")
        return out

    def exec(self, cmd):
        """Refine the command to be executed"""
        cmd = cmd.replace("`", "")
        q = self.console.input(f"[bold red]Execute this command (press return to run):[/] \n$ {cmd}").lower()
        if (q == "y") or (q == ""):
            self.run_cmd(cmd)
        else:
            pass

    def run_cmd(self, cmd):
        try:
            subprocess.run(cmd, shell=True, check=True)
        except Exception as e:
            self.console.print("[bold red]Error executing command: [/]" + str(e))

    def input(self):
        return self.console.input("[bold red]> [/]")

    def save(self):
        with open(self.history_file, "w") as f:
            json.dump(self.history, f)
        if self.out_file is not None:
            with open(self.out_file, "w") as out_f:
                print(f"Saving output to {self.out_file}")
                out_f.writelines([h["content"] for h in self.history])
        self.console.print(f"-------------\nSaving history to {self.history_file}, you can restore this session with `--resume`")
