import os

import anthropic

from termgpt.models.base import ChatWithHistory

CLAUDE = "claude-2"

class AnthropicChat(ChatWithHistory):
    """Class to handle chat with Claude, supports history and load from file"""

    def __init__(self, model_name=CLAUDE, file=None, resume=False, command=None, out_file=None, markdown=True):
        try:
            self.client = anthropic.Anthropic()
        except ImportError:
            "Please install anthropic to use this chatbot\nYou can do it with `pip install anthropic`"
        self.model_name = model_name
        super().__init__(file, resume, command, out_file, markdown)

    def call(self):
        prompt = self.preprocess_query()
        response = self.client.completions.create(
            prompt=prompt + anthropic.AI_PROMPT,
            stop_sequences = [anthropic.HUMAN_PROMPT],
            model=self.model_name,
            max_tokens_to_sample=1000,
        )
        return response.completion

    def preprocess_query(self):
        query = ""
        for h in self.history:
            if h["role"] == "user" or h["role"] == "system":
                query += "\n\nHuman: " + h["content"] + "\n"
            elif h["role"] == "assistant":
                query += "\n\nAssistant: "+ h["content"] + "\n"
        return query