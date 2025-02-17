from sys import platform

from rich.text import Text
from rich.console import Console
from rich.markdown import Markdown


from litellm import completion

from termgpt.tools import run_command, generate_json_schema
from termgpt.history import get_terminal_history

TOOLS = [generate_json_schema(run_command)]

DEFAULT_LLM = "gemini/gemini-2.0-flash"

SYSTEM_PROMPT = f"""You are a terminal assistant, you will help me find the right terminal command to perform the given action.
- We are running on {platform}.
- Reply in plain text, no fancy output.
- If the question is not related to the terminal, just say "I'm not sure how to respond to that"
- Warn the user of nefarious commands, and help them to find the right command.
- If there are multiple ways of performing the same action, reply the simplest one.
For example, if the questions is "How do I create a new file named "hello.txt?", 
reply: touch hello.txt instead of echo > hello.txt

You have access to the terminal history of the user. You need to be pedagogical, and help the user to find the right command. Explain the commands to the user, and help them to understand the commands. The idea is to teach the user how to find the right command.
<terminal_history>
{get_terminal_history()}
</terminal_history>
"""

console = Console()

class MyConsole:
    def print(self, *args, **kwargs):
        console.print(*args, **kwargs)

    @staticmethod
    def chat_response_start() -> None:
        pass

    @staticmethod
    def chat_message_content_delta(message_content_delta: str) -> None:
        console.print(message_content_delta, end="")

    @staticmethod
    def chat_response_complete() -> None:
        console.print("\n")

    def input(self) -> str:
        return console.input("[bold red]> [/]")

class LLM:
    """Class to handle chat with LLM, supports history."""

    def __init__(
            self, 
            model_name: str = DEFAULT_LLM, 
            debug: bool = False,
            ):
        self.model_name = model_name
        self.console = MyConsole()
        self.history_file = "llm_history.json"
        self.messages = [{"role": "system", "content": SYSTEM_PROMPT}, ]
        self.debug = debug

    def call(self):
        self.console.chat_response_start()
        if self.debug:
            console.print(self.messages)
        response = completion(
            model=self.model_name,
            messages=self.messages,
            max_tokens=1000,
            stream=True,
        )
        final_response = ""
        for chunk in response:
            if chunk.choices[0].delta.content:
                final_response += chunk.choices[0].delta.content
                self.console.chat_message_content_delta(f"[bold green]{chunk.choices[0].delta.content}[/bold green]")
        self.console.chat_response_complete()
        return final_response

    def append(self, role, content):
        self.messages.append({"role": role, "content": content})

    def __call__(self, question):
        self.append("user", question)
        out = self.call()
        self.append("assistant", out)
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
        run_command(cmd)

    def input(self):
        return self.console.input()