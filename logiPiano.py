import websockets
from websockets import WebSocketServerProtocol
import asyncio
import logging
import logi_led as logi_led
import time,sys,signal


def signal_handler(sig,frame):
    print("EXIT")
    logi_led.logi_led_shutdown()
    sys.exit(0)


class Server:
    def __init__(self):
        self.clients = set()
        self.loop = asyncio.get_event_loop()
        self.logger = _create_logger()
        self._client_timeout = 5
        self._wake_up_task = None
        self.keys ={"Q" : 0x10,"W" : 0x11,"E" : 0x12,"R" : 0x13,"T" : 0x14,"Y" : 0x15,"U" : 0x16,"I" : 0x17,"O" : 0x18,"P" : 0x19,"A" : 0x1e,"S" : 0x1f,"D" : 0x20,
        "F" : 0x21,"G" : 0x22,"H" : 0x23,"J" : 0x24,"K" : 0x25,"L" : 0x26,"Z" : 0x2c,"X" : 0x2d,"C" : 0x2e,"V" : 0x2f,"B" : 0x30,"N" : 0x31,"M" : 0x32, "1" : 0x02,"2" : 0x03,"3" : 0x04,
        "4" : 0x05,"5" : 0x06,"6" : 0x07,"7" : 0x08,"8" : 0x09,"9" : 0x0a,"0" : 0x0b,"SHIFT":0x2a,"!" : 0x02,"@" : 0x03,"#" : 0x04,"$" : 0x05,"%" : 0x06,"^" : 0x07,"&" : 0x08,"*" : 0x09,"(" : 0x0a,")" : 0x0b,}

    def listen(self, host='localhost', port=1299):
        self.logger.info("listening on {}:{}".format(host, port))
        ws_server = websockets.serve(self.connect_client, host, port)

        self.loop.run_until_complete(ws_server)
        self._wake_up_task = asyncio.ensure_future(_wake_up())

        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            self.logger.debug('caught keyboard interrupt')
            self.exit()

    async def connect_client(self, client: WebSocketServerProtocol, path):
        self.clients.add(client)
        self.logger.info('new client connected from {}:{}'.format(*client.remote_address))
        keep_alive_task = asyncio.ensure_future(self.keep_alive(client))

        try:
            await self.handle_messages(client)
        except websockets.ConnectionClosed:
            keep_alive_task.cancel()
            await self.disconnect_client(client)

    async def handle_messages(self, client):
        while True:
            message = await client.recv()
            #key = str(message)[0].upper()

            led_color(0.0,0.0,0.0)
            for key in message:
                try:

                    if(str(key).isupper()):
                        logi_led.logi_led_set_lighting_for_key_with_key_name(self.keys["SHIFT"],int(0),int(255),int(255))
                        
                    logi_led.logi_led_set_lighting_for_key_with_key_name(self.keys[str(key).upper()],int(0),int(255),int(255))

                except Exception as e:
                    pass

            


            



            self.logger.info('recieved message from {}:{}: {}'.format(*client.remote_address, message))
            await asyncio.wait([client.send(message) for client in self.clients])

    async def disconnect_client(self, client):
        await client.close()
        self.clients.remove(client)
        self.logger.info('client {}:{} disconnected'.format(*client.remote_address))

    async def keep_alive(self, client: WebSocketServerProtocol):
        while True:
            await asyncio.sleep(self._client_timeout)
            try:
                self.logger.info('pinging {}:{}'.format(*client.remote_address))
                await asyncio.wait_for(client.ping(), self._client_timeout)
            except asyncio.TimeoutError:
                self.logger.info('client {}:{} timed out'.format(*client.remote_address))
                await self.disconnect_client(client)

    def exit(self):
        self.logger.info("exiting")
        self._wake_up_task.cancel()
        try:
            self.loop.run_until_complete(self._wake_up_task)
        except asyncio.CancelledError:
            self.loop.close()


def _create_logger():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("chat.server")
    logger.setLevel(logging.INFO)
    ws_logger = logging.getLogger('websockets.server')
    ws_logger.setLevel(logging.ERROR)
    ws_logger.addHandler(logging.StreamHandler())
    return logger


async def _wake_up():
    while True:
        await asyncio.sleep(1)

def led_color(r,g,b):
    print(logi_led.logi_led_set_lighting(int(r*100),int(g*100),int(b*100)))

def start_up_led():
    led_color(1,0,0)
    time.sleep(.25)
    led_color(0,1,0)
    time.sleep(.25)
    led_color(0.3,0.3,0.3)
    time.sleep(.25)
    #led_color(.5,.5,.5)
    print("Init done")

def main():
    
    logi_led.logi_led_init()
    print(logi_led.led_dll)
    time.sleep(1)
    start_up_led()

   
    server = Server()
    server.listen()


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    main()