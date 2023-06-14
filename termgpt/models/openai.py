import os
from dataclasses import dataclass

import openai

from termgpt.models.base import ChatWithHistory


GPT3 = "gpt-3.5-turbo"
GPT4 = "gpt-4"  # if you have access...

PRICING = {GPT3: (0.02, 0.02), GPT4: (0.03, 0.06)} # prices per 1k tokens

@dataclass
class OpenAIAPIStats:
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

    def __repr__(self):
        return (f"Model Name: {self.model_name} -> "
                f"Prompt tokens: {self.prompt_tokens}, Completion tokens: {self.completion_tokens}, "
                f"Total tokens: {self.total_tokens}, Estimated cost: ${self.cost():.2f}")


class OpenAIChat(ChatWithHistory):
    """Class to handle chat with chatGPT, supports history and load from file"""

    def __init__(self, model_name=GPT3, file=None, resume=False, command=None, out_file=None, markdown=True):
        
        if not os.getenv("OPENAI_API_KEY"):
            raise ImportError("[bold red]Please set `OPENAI_API_KEY` environment variable[/]")
        self.model_name=model_name
        self.usage = OpenAIAPIStats(model_name=model_name)
        super().__init__(file=file, resume=resume, command=command, out_file=out_file, markdown=markdown)
    
    def call(self):
        r = openai.ChatCompletion.create(
            model=self.model_name,
            messages=self.history,
        )
        out = r["choices"][0]["message"]["content"]
        self.usage.update(r['usage'])
        return out
    
    def save(self):
        super().save()
        self.console.print(self.usage)