
class ClientConnection:

    def __init__(self, server, reader, writer):
        self.reader = reader
        self.writer = writer

        self.server = server
    
    async def keep_connection_alive(self):
        self.server.logger.info('New client connection')

        while not self.writer.is_closing():
            try:
                line = await self.reader.readline()
                
                if line:
                    await self.handle_received_data(line)
                else:
                    self.writer.close()
                
                await self.writer.drain()
                
            except ConnectionResetError:
                self.writer.close()

        await self.handle_client_disconnection()

    async def handle_received_data(self, line):
        line = line.decode().strip()

        await self.server.msg_handler.handle_msg(self, line)
    
    async def send_error_msg(self, error):
        await self.send_json(action='error', message=error)
    
    async def send_success_msg(self, success_msg):
        await self.send_json(action='success', message=success_msg)
    
    async def send_json(self, **kwargs):
        if not self.writer.is_closing():
            line = await self.server.msg_handler.encode_json(**kwargs)
            line += '\n'

            self.writer.write(line.encode('utf-8'))

    async def disconnect_client(self):
        self.writer.close()

        await self.handle_client_disconnection()
    
    async def handle_client_disconnection(self):
        self.server.logger.info('Client disconnection')
    