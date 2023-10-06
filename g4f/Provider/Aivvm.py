from __future__ import annotations

from ..requests import StreamSession
from .base_provider import AsyncGeneratorProvider
from ..typing import AsyncGenerator

models = {
    'gpt-3.5-turbo': {'id': 'gpt-3.5-turbo', 'name': 'GPT-3.5'},
    'gpt-3.5-turbo-0613': {'id': 'gpt-3.5-turbo-0613', 'name': 'GPT-3.5-0613'},
    'gpt-3.5-turbo-16k': {'id': 'gpt-3.5-turbo-16k', 'name': 'GPT-3.5-16K'},
    'gpt-3.5-turbo-16k-0613': {'id': 'gpt-3.5-turbo-16k-0613', 'name': 'GPT-3.5-16K-0613'},
    'gpt-4': {'id': 'gpt-4', 'name': 'GPT-4'},
    'gpt-4-0613': {'id': 'gpt-4-0613', 'name': 'GPT-4-0613'},
    'gpt-4-32k': {'id': 'gpt-4-32k', 'name': 'GPT-4-32K'},
    'gpt-4-32k-0613': {'id': 'gpt-4-32k-0613', 'name': 'GPT-4-32K-0613'},
}

class Aivvm(AsyncGeneratorProvider):
    url                   = 'https://chat.aivvm.com'
    supports_stream       = True
    working               = True
    supports_gpt_35_turbo = True
    supports_gpt_4        = True

    @classmethod
    async def create_async_generator(
        cls,
        model: str,
        messages: list[dict[str, str]],
        stream: bool,
        timeout: int = 30,
        **kwargs
    ) -> AsyncGenerator:
        if not model:
            model = "gpt-3.5-turbo"
        elif model not in models:
<<<<<<< HEAD
            raise ValueError(f"Model are not supported: {model}")
    
        headers = {
            "authority"          : "chat.aivvm.com",
            "accept"             : "*/*",
            "accept-language"    : "en,fr-FR;q=0.9,fr;q=0.8,es-ES;q=0.7,es;q=0.6,en-US;q=0.5,am;q=0.4,de;q=0.3",
            "content-type"       : "application/json",
            "origin"             : "https://chat.aivvm.com",
            "referer"            : "https://chat.aivvm.com/",
            "sec-ch-ua"          : '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
            "sec-ch-ua-mobile"   : "?0",
            "sec-ch-ua-platform" : '"macOS"',
            "sec-fetch-dest"     : "empty",
            "sec-fetch-mode"     : "cors",
            "sec-fetch-site"     : "same-origin",
            "user-agent"         : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
        }
=======
            raise ValueError(f"Model is not supported: {model}")
>>>>>>> 31354a68afba030e506abda0c865f6aa74a318ab

        json_data = {
            "model"       : models[model],
            "messages"    : messages,
            "key"         : "",
            "prompt"      : "You are ChatGPT, a large language model trained by OpenAI. Follow the user's instructions carefully. Respond using markdown.",
            "temperature" : kwargs.get("temperature", 0.7)
        }
<<<<<<< HEAD

        response = requests.post(
            "https://chat.aivvm.com/api/chat", headers=headers, json=json_data, stream=True)

        for line in response.iter_content(chunk_size=1048):
            yield line.decode('utf-8')
=======
        headers = {
            "Accept": "*/*",
            "Origin": cls.url,
            "Referer": f"{cls.url}/",
        }
        async with StreamSession(impersonate="chrome107", headers=headers, timeout=timeout) as session:
            async with session.post(f"{cls.url}/api/chat", json=json_data) as response:
                response.raise_for_status()
                async for chunk in response.iter_content():
                    yield chunk.decode()
>>>>>>> 31354a68afba030e506abda0c865f6aa74a318ab

    @classmethod
    @property
    def params(cls):
        params = [
            ('model', 'str'),
            ('messages', 'list[dict[str, str]]'),
            ('stream', 'bool'),
            ('temperature', 'float'),
        ]
        param = ', '.join([': '.join(p) for p in params])
        return f'g4f.provider.{cls.__name__} supports: ({param})'