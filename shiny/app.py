from aiohttp import web
from .const import assets
from .exchanger import In, Out, Mapping
from .wstream import WStream, WStreamExp


class App:
    def __init__(self, ui, server):
        self.ui = ui
        self.server = server
        self.mapping = Mapping()
        self.app = web.Application()
        self.app.add_routes([web.get('/', self.handler)])
        self.app.router.add_static(assets[0], assets[1])

    async def resolve_msg(self, msg, ws):
        out = Out(In(msg, self.mapping, ws))
        self.server(out)
        await out.execute()
        return out.msg

    async def _init_connction(self, ws):
        msg, _ = await ws.receive_msg()
        out = Out(In(msg, self.mapping, ws))
        self.server(out)
        await out.init_execute()
        await ws.send_msg(out.msg)
        self.mapping.inited = True

    async def handler(self, request):
        resp = web.WebSocketResponse()
        available = resp.can_prepare(request)
        if not available:
            headers = {"Content-Type": "text/html"}
            return web.Response(text=str(self.ui), headers=headers)

        await resp.prepare(request)
        ws = WStream(resp)
        await self._init_connction(ws)
        try:
            async for msg, _ in ws:
                try:
                    result = await self.resolve_msg(msg, ws)
                    await ws.send_msg(result)
                except WStreamExp:
                    return ws.raw
            return ws.raw
        finally:
            # disconnected
            await ws.close()

    def start(self, port=None, host=None):
        web.run_app(self.app, port=port, host=host)


def ShinyApp(ui, server, *, host=None, port=None):
    app = App(ui, server, host=host, port=port)
    app.start()
