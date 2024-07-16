import yaml
from openai import AzureOpenAI
from GptMessage import GptMessage
from GptFile import GptFile


class GptClient:
    def __init__(self):
        with open('secrets.yaml', 'r') as file:
            config = yaml.safe_load(file)

        self.client = AzureOpenAI(
                api_key=config['api_key'],
                azure_endpoint=config['url'],
                api_version=config['api_version']
        )
        self.model = config['deployment']

    async def query(self, file: GptFile) -> GptMessage:
        message = GptMessage(role='assistant', content='')
        message.print_header()

        messages = [{'role': m.role, 'content': m.content} for m in file.messages]

        stream = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            stream=True
        )

        async for chunk in stream:
            content = chunk.choices[0].delta.content
            message.content += content
            print(content, end='', flush=True)

        return message
