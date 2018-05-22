from aiohttp import web
from .const import assets
from .wstream import Wstream
from .exchanger import Exchanger


class App:
    def __init__(self, ui, server):
        self.ui = ui
        self.server = server
        self.app = web.Application()
        self.app.add_routes([web.get('/', self.handler),
                             web.get('/ws', self.ws_handler)])
        self.app.router.add_static(assets[0], assets[1])

    async def handler(self, request):
        headers = {"Content-Type": "text/html"}
        return web.Response(text=str(self.ui), headers=headers)

    async def ws_handler(self, request):
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        wstream = Wstream(ws)
        exchanger = Exchanger(wstream)

    def start(self, port=None, host=None):
        web.run_app(self.app, port=port, host=host)
