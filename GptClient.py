import anthropic
from GptMessage import GptMessage
from GptFile import GptFile


class GptClient:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=self.get_api_key())
        self.model = 'claude-3-sonnet-20240229'
        self.max_tokens = 1024

    def get_api_key(self) -> str:
        with open('.key', 'r') as file:
            return file.read().replace('\n', '')

    async def query(self, file: GptFile) -> GptMessage:
        messages = [{'role': m.role, 'content': m.content} for m in file.messages]
        message = GptMessage(role="assistant", content="")
        message.print_header()
        async with self.client.messages.stream(
            model=self.model,
            messages=messages,
            max_tokens=self.max_tokens,
        ) as stream:
            buffer = []
            async for message in stream:
                if message.type == 'content_block_delta':
                    delta = message.delta.text
                    buffer.append(delta)
                    print(delta, end='', flush=True)

            response = ''.join(buffer)
            message.content = response
            return message
