from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from GptClient import GptClient
from GptFile import GptFile
from cmd import Cmd
from GptMessage import GptMessage
import asyncio


async def main():
    client = GptClient()
    file = GptFile()

    command_completer = WordCompleter(['b', 'bd', 'w', 'q', 'wq'])
    session = PromptSession(multiline=True, completer=command_completer)

    while True:
        try:
            input = await session.prompt_async(
                '[YOU]: ',
                accept_default=True,
                default='',
            )

            lines = input.split('\n')
            while lines and not lines[-1].strip():
                lines.pop()
            input = '\n'.join(lines)

            if not input:
                continue

            if Cmd.is_cmd(input):
                cmd = Cmd(input)
                should_exit = cmd.run(file)

                if should_exit:
                    break

                continue

            user_message = GptMessage(role='human', content=input)
            file.append(user_message)

            print()
            print('Thinking...')

            response = await client.query(file)
            file.append(response)

            print()
        except KeyboardInterrupt:
            print("Goodbye!")
            break
        except Exception as e:
            GptMessage.app_message(str(e), error=True)


if __name__ == '__main__':
    asyncio.run(main())
