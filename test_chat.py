import unittest
from unittest.mock import MagicMock

import openai
from termgpt import Chat

class ChatTestCase(unittest.TestCase):
    def setUp(self):
        # Mock the openai API
        openai.ChatCompletion.create = MagicMock()
        openai.ChatCompletion.create.return_value = {
            "choices": [
                {
                    "message": {
                        "content": "Mocked content"
                    }
                }
            ]
        }
        self.chat = Chat("gpt-3.5-turbo")


    def test_init_with_command(self):
        command = "echo 'Hello, World!'"
        mocked_cmd_output = "echo 'Hello, World!'"

        with unittest.mock.patch("subprocess.run") as subprocess_run:
            subprocess_run.return_value.returncode = 0
            
            chat_with_command = Chat("gpt-3.5-turbo", command=command)

            # Check if subprocess.run is called with the expected command.
            subprocess_run.assert_called_once_with(command, shell=True, check=True)

        # Check if the command has been added to history.
        self.assertEqual(chat_with_command.history[1]["role"], "user")
        self.assertEqual(chat_with_command.history[1]["content"], command)

        # Check if the mocked response has been added to history.
        self.assertEqual(chat_with_command.history[2]["role"], "assistant")
        self.assertEqual(chat_with_command.history[2]["content"], mocked_cmd_output)

    def test_init_without_command(self):
        chat_without_command = Chat("gpt-3.5-turbo")

        # Check for a single "system" message in the history.
        self.assertEqual(len(chat_without_command.history), 1)
        self.assertEqual(chat_without_command.history[0]["role"], "system")
        self.assertEqual(chat_without_command.history[0]["content"], "You are a helpful assistant.")

    def test_call(self):
        question = "What is 2 + 2?"
        expected_response = "Mocked content"
        
        response = self.chat(question)
        
        openai.ChatCompletion.create.assert_called_once()
        
        for call_arg in openai.ChatCompletion.create.call_args[1]["messages"]:
            if call_arg["role"] == "user":
                self.assertEqual(call_arg["content"], question, "Incorrect question being passed to the model")

        self.assertEqual(response, expected_response, "Did not receive the expected response from the mocked call")

if __name__ == "__main__":
    unittest.main()