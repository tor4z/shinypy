from aiohttp import web
from .const import assets
from exchanger import In, Out, Mapping


class App:
    def __init__(self, ui, server):
        self.ui = ui
        self.server = server
        self.mapping = Mapping()
        self.app = web.Application()
        self.app.add_routes([web.get('/', self.handler)])
        self.app.router.add_static(assets[0], assets[1])

    async def handler(self, request):
        resp = web.WebSocketResponse()
        available = resp.can_prepare(request)
        if not available:
            headers = {"Content-Type": "text/html"}
            return web.Response(text=str(self.ui), headers=headers)

        await resp.prepare(request)
        try:
            async for msg in resp:
                if msg.type == web.WSMsgType.TEXT:
                    out = Out(In(msg.data, self.mapping))
                    self.mapping.inited()
                    self.server(out)
                    await resp.send_str(str(out))
                else:
                    return resp
            return resp
        finally:
            # disconnected
            await resp.close()

    def start(self, port=None, host=None):
        web.run_app(self.app, port=port, host=host)


def ShinyApp(ui, server, *, host=None, port=None):
    app = App(ui, server, host=host, port=port)
    app.start()
