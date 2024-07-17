from aiomcrcon import Client


class Whitelist:
    client: Client

    def __parse_whitelist(self, response: str) -> list:
        response = ': '.join(response.replace('\n', '').split(': ')[1:])
        return response.split(', ')

    def __init__(self, client: Client):
        self.client = client

    async def get(self) -> list:
        response = await self.client.send_cmd('whitelist list')
        whitelist = self.__parse_whitelist(response[0])
        return whitelist

    async def add(self, nick: str) -> bool:
        response = await self.client.send_cmd(f'whitelist add {nick}')
        if 'add.failed' in response[0]:
            return False
        else:
            return True

    async def remove(self, nick: str) -> bool:
        response = await self.client.send_cmd(f'whitelist remove {nick}')
        if 'remove.failed' in response[0]:
            return False
        else:
            return True


class MCRcon:
    def __init__(self, host: str, port: int, password: str):
        self.host = host
        self.port = port
        self.password = password

        self.client = Client(
            host=host,
            port=port,
            password=password
        )

        self.whitelist = Whitelist(self.client)

    async def connect(self):
        await self.client.connect()

    async def reconnect(self):
        await self.client.connect()

    async def close(self):
        await self.client.close()

    async def command(self, command: str) -> str:
        response = await self.client.send_cmd(command)
        return response[0]

    async def say(self, message: str) -> str:
        response = await self.client.send_cmd(f'say {message}')
        return response[0]

    async def tell(self, who: str, message: str) -> str:
        response = await self.client.send_cmd(f'tell {who} {message}')
        return response[0]

    async def list(self) -> list[str]:
        response = (await self.client.send_cmd('list'))[0]
        response = ': '.join(response.replace('\n', '').split(': ')[1:])
        return response.split(', ')
