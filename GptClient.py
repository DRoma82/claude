import anthropic
from GptMessage import GptMessage
from GptFile import GptFile


class GptClient:
    def __init__(self):
        self.client = anthropic.AsyncAnthropic(api_key=self.get_api_key())
        print(self.client.api_key)
        self.model = 'claude-3-sonnet-20240229'
        self.max_tokens = 1024

    def get_api_key(self) -> str:
        with open('.key', 'r') as file:
            return file.read().replace('\n', '').strip()

    async def query(self, file: GptFile) -> GptMessage:
        messages = [{'role': m.role, 'content': m.content} for m in file.messages]

        response = await self.client.messages.create(
            model=self.model,
            messages=messages,
            max_tokens=self.max_tokens,
        )

        return GptMessage(role='ASSISTANT', content=response.content[0].text)
