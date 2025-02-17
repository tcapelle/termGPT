from sys import platform
from typing import Optional
from pydantic import BaseModel, Field
from rich.console import Console



from litellm import completion

from termgpt.tools import run_command, generate_json_schema
from termgpt.history import get_terminal_history

TOOLS = [generate_json_schema(run_command)]

DEFAULT_LLM = "gemini/gemini-2.0-flash"

SYSTEM_PROMPT = f"""
You are a terminal assistant. Your role is to help the user execute terminal commands and understand their usage. Follow these guidelines:

1. **Platform Awareness**: We are running on {platform}. Tailor your responses accordingly.
2. **Action-Specific Help**: Provide the simplest and safest terminal command that accomplishes the user’s request.  
   - *Example*: If asked “How do I create a new file named 'hello.txt'?”, reply with:
     ```
     touch hello.txt
     ```
     rather than a more complex alternative.
3. **Context Use**: You have access to the terminal history (shown below). Use this context to inform your answer, but do not explicitly mention that you are referencing the history.
4. **Pedagogical Explanation**: Along with the command, include a brief explanation so the user understands what it does and why it’s the simplest solution.
5. **Safety Precautions**: If the user asks for a command that might be harmful or is potentially nefarious, warn them and suggest a safer alternative.
6. **Terminal-Focused Responses**: If the user asks an open question, always asume that he is referring to the terminal history.
7. **Avoid Meta-References**: Do not mention the use of an LLM or that you are analyzing terminal history. Do not start your answer with phrases like "Based on your recent terminal history..."

Below is the terminal history available for context:
<terminal_history>
{get_terminal_history()}
</terminal_history>
"""

console = Console()

class LLMResponse(BaseModel):
    response: str = Field(description="A one-liner explanation of the command to execute.")
    command: Optional[str] = Field(description="The command to execute, if applicable")

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

    def input(self, prompt="[bold red]> [/]") -> str:
        return console.input(prompt)

class LLM:
    """Class to handle chat with LLM, supports history."""

    def __init__(
            self, 
            model_name: str = DEFAULT_LLM, 
            debug: bool = False,
            interactive: bool = True,
            ):
        self.model_name = model_name
        self.console = MyConsole()
        self.history_file = "llm_history.json"
        self.messages = [{"role": "system", "content": SYSTEM_PROMPT}, ]
        self.debug = debug
        self.interactive = interactive
    
    def call(self):
        self.console.chat_response_start()
        if self.debug:
            console.print(self.messages)
        if not self.interactive:
            response = completion(
                model=self.model_name,
                messages=self.messages,
                max_tokens=1000,
                response_format=LLMResponse,
            )
            response = response.choices[0].message.content
            final_response = LLMResponse.model_validate_json(response)
            self.console.print(f"[bold green]{final_response.response}[/bold green]")
            self.exec(final_response.command)
            return final_response.response
        else:
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
        if cmd:
            cmd = cmd.replace("`", "")
            q = self.console.input(f"[bold red]Execute this command (press return to run):[/] \n$ {cmd}").lower()
            if (q == "y") or (q == ""):
                output = run_command(cmd)
                self.console.print(output["output"])
            else:
                pass
        else:
            self.console.print("[bold red]No command to execute[/]")


    def input(self):
        return self.console.input()