import argparse, atexit
from dataclasses import dataclass

from termgpt.models import AnthropicChat, CLAUDE, OpenAIChat, GPT3, GPT4

def parse_args():
    parser = argparse.ArgumentParser(usage="termGPT [options] [file]", description="Chat with GPT-3/4. If no file is provided, you will be prompted to enter a question.")
    parser.add_argument("file", type=str, nargs="?", default=None, help="File to read [optional]")
    parser.add_argument("-r", "--resume", action="store_true", help="Resume previous session")
    parser.add_argument("-c", "--command", type=str, default=None, help="Command to run [optional]")
    parser.add_argument("-o", "--outfile", type=str, default=None, help="Output file [optional]")
    parser.add_argument("-no_md", "--no_markdown", action="store_false", help="Disable markdown rendering")
    return parser.parse_args()

exit_commands = ["exit", "quit", "q", "bye", "goodbye", "stop", "end", "finish", "done"]

def main(model_name):
    args = parse_args()
    if model_name == CLAUDE:
        chat = AnthropicChat(model_name=CLAUDE, file=args.file, resume=args.resume, command=args.command, out_file=args.outfile, markdown=args.no_markdown)
    else:
        chat = OpenAIChat(model_name, file=args.file, resume=args.resume, command=args.command, out_file=args.outfile, markdown=args.no_markdown)
    atexit.register(chat.save)
    if not args.command:
        while (q := chat.input()) not in exit_commands:
            _ = chat(q)

def gpt3(): main(GPT3)
def gpt4(): main(GPT4)
def claude(): main(CLAUDE)