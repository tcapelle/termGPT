import argparse, atexit
from dataclasses import dataclass

import simple_parsing as sp

from termgpt.llm import LLM

DEFAULT_LLM = "gemini/gemini-2.0-flash"
EXIT_COMMANDS = ["exit", "quit", "q", "bye", "goodbye", "stop", "end", "finish", "done"]

@dataclass
class Args:
    model: str = sp.field(default=DEFAULT_LLM, help="Model name")
    debug: bool = sp.field(default=False, help="Debug mode")


def main():
    args = sp.parse(Args)
    chat = LLM(
        model_name=args.model,
        debug=args.debug,
        )
    try:
        while (q := chat.input()) not in EXIT_COMMANDS:
            _ = chat(q)
    except (KeyboardInterrupt, EOFError):
        print()  # Add a newline for cleaner exit
        pass

def llm(): main()