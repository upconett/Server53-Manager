from aiomcrcon import Client


class Whitelist:
    client: Client

    def __parse_whitelist(self, response: str) -> list:
        response = ': '.join(response.replace('\n', '').split(': ')[1:])
        return response.split(', ')


    def __init__(self, client: Client):
        self.client = client
    

    async def get(self) -> list:
        await self.client.connect()
        response = await self.client.send_cmd('whitelist list')
        await self.client.close()
        whitelist = self.__parse_whitelist(response[0])
        return whitelist

    
    async def add(self, nick: str) -> bool:
        await self.client.connect()
        response = await self.client.send_cmd(f'whitelist add {nick}')
        await self.client.close()
        if 'add.failed' in response[0]: return False
        else: return True


    async def remove(self, nick: str) -> bool:
        await self.client.connect()
        response = await self.client.send_cmd(f'whitelist remove {nick}')
        await self.client.close()
        if 'remove.failed' in response[0]: return False
        else: return True


class MCRcon:
    host: str
    port: int
    password: str

    client: Client

    whitelist: Whitelist


    def __init__(self, host: str, port: str, password: str):
        self.host = host
        self.port = port
        self.password = password

        self.client = Client(
            host = host,
            port = port,
            password = password
        )

        self.whitelist = Whitelist(
            client=self.client
        )
        
    
    async def command(self, command: str) -> str:
        await self.client.connect()
        response = await self.client.send_cmd(command)
        await self.client.close()
        return response[0]

    
    async def say(self, message: str) -> str:
        await self.client.connect()
        response = await self.client.send_cmd(f'say {message}')
        await self.client.close()
        return response[0]


    async def tell(self, who: str, message: str) -> str:
        await self.client.connect()
        response = await self.client.send_cmd(f'tell {who} {message}')
        await self.client.close()
        return response[0]
