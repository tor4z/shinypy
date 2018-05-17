from aiohttp import web
from .const import assets


class App:
    def __init__(self, ui, server):
        self.ui = ui
        self.server = server
        self.app = web.Application()
        self.app.add_routes([web.get('/', self.handle)])
        print(assets)
        self.app.router.add_static(assets[0], assets[1])

    async def handle(self, request):
        # name = request.match_info.get('name', "Anonymous")
        headers = {"Content-Type": "text/html"}
        return web.Response(text=str(self.ui), headers=headers)

    def start(self, port=None):
        web.run_app(self.app)
