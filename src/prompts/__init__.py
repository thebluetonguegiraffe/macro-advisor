from dotenv import load_dotenv
from langsmith import Client

load_dotenv()

client = Client()


def load_prompt(name: str) -> str:
    prompt_template = client.pull_prompt(name)
    return prompt_template.messages[0].prompt.template
