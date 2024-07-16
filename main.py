from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.keys import Keys
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
    kb = KeyBindings()

    @kb.add(Keys.Escape, Keys.Enter)  # Alt-Enter
    def _(event):
        event.current_buffer.validate_and_handle()

    session = PromptSession(multiline=True, completer=command_completer, key_bindings=kb)

    while True:
        try:
            input = await session.prompt_async(
                '[YOU]: ',
                accept_default=False
            )

            input = input.strip()

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

            try:
                response = await client.query(file)
                response.print()
                file.append(response)
                print()
            except Exception as e:
                GptMessage.app_message(f"Error: {str(e)} ", error=True)

        except KeyboardInterrupt:
            print("Goodbye!")
            break
        except Exception as e:
            GptMessage.app_message(str(e), error=True)


if __name__ == '__main__':
    asyncio.run(main())
