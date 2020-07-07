from broker.messages.handlers import authentication, publishers, subscribers

import json

class MessageHandler:
    
    def __init__(self, server):
        self.server = server

        self.module_handlers = [authentication, publishers, subscribers]
    
    async def handle_msg(self, client, line):
        try:
            decoded_line = await self.decode_json(line)
            function_name = decoded_line.pop('action').lower()

            for module in self.module_handlers:
                module_functions = [curr_name for curr_name, func in module.__dict__.items() \
                                    if hasattr(func, '__call__')]
                if function_name in module_functions:
                    return await getattr(module, function_name)(client, **decoded_line)

            self.server.logger.warn(f'Action function {function_name} does not exist to handle')
        except TypeError:
            self.server.logger.warn('Could not parse invalid JSON message for action')
    
    async def encode_json(self, **kwargs):
        return json.dumps(kwargs, separators=(',', ':'))

    async def decode_json(self, line):
        return json.loads(line)