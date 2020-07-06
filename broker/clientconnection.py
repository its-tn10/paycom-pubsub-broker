
class ClientConnection:

    def __init__(self, server, reader, writer):
        self.reader = reader
        self.writer = writer

        self.server = server
    
    async def keep_connection_alive(self):
        while not self.writer.is_closing():
            data = await self.reader.readline()
            if not data:
                break
            
            self.server.logger.debug(f'Received data: {data}')
        
        self.writer.close()