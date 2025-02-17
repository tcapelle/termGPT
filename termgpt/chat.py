import argparse, atexit
from dataclasses import dataclass

import simple_parsing as sp

from termgpt.llm import LLM

DEFAULT_LLM = "gpt-4o"

@dataclass
class Args:
    resume: bool = False # Resume previous session
    command: str = None # Command mode, ask for a command to run
    outfile: str = None # Output file to save conversation
    no_markdown: bool = True # Disable markdown rendering


exit_commands = ["exit", "quit", "q", "bye", "goodbye", "stop", "end", "finish", "done"]

def main(model_name):
    args = sp.parse(Args)
    chat = LLM(
        model_name=model_name, 
        resume=args.resume, 
        command=args.command, 
        out_file=args.outfile, 
        markdown=args.no_markdown
        )
    atexit.register(chat.save)
    if not args.command:
        try:
            while (q := chat.input()) not in exit_commands:
                _ = chat(q)
        except (KeyboardInterrupt, EOFError):
            print()  # Add a newline for cleaner exit
            pass

def llm(): main(DEFAULT_LLM)