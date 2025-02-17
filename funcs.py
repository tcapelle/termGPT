import openai
import json

# Example dummy function hard coded to return the same weather
# In production, this could be your backend API or an external API
def list_linux_available_programs(os="linux"):
    """Get the system programs available in a linux system"""
    if os != "linux":
        raise ValueError("This function only works for linux")
    programs = ["ls", "cd", "pwd", "cat", "grep", "awk", "sed", "find", "kill"]
    results = {
        "programs": programs,
    }
    return json.dumps(programs)

def execute_linux_cmd(cmd):
    """Execute a linux command"""
    

# Step 1, send model the user query and what functions it has access to
def run_conversation():
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=[{"role": "user", "content": "What program I should use to see the files in my current directory?"}],
        functions=[
            {
                "name": "list_linux_available_programs",
                "description": "Get the system programs available in a linux system",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "os": {
                            "type": "string",
                            "description": "The operating system to get the programs for",
                        },
                    },
                    "required": ["os"],
                }
            },
        ],
        function_call="auto",
    )

    message = response["choices"][0]["message"]

    # Step 2, check if the model wants to call a function
    if message.get("function_call"):
        function_name = message["function_call"]["name"]

        # Step 3, call the function
        # Note: the JSON response from the model may not be valid JSON
        function_response = list_linux_available_programs()

        # Step 4, send model the info on the function call and function response
        second_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=[
                {"role": "user", "content": "What program I should use to see the files in my current directory?"},
                message,
                {
                    "role": "function",
                    "name": function_name,
                    "content": function_response,
                },
            ],
        )
        return second_response

print(run_conversation())