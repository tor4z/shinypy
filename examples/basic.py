from shiny.ui import UI
from shiny.app import App
from shiny.layout import DashboardLayout
from shiny import widgets as wg


ui = UI()
dashboard = DashboardLayout("Test")
ui.layout = dashboard
dashboard.sidebar.append(
    wg.Text("test", "test", label="Test"))
dashboard.main.append(
    wg.Label("test"))


def server(OUT):
    @wg.Label.render
    async def do_a(IN):
        return await IN["test"]
    OUT["test"] = do_a


if __name__ == "__main__":
    app = App(ui, server)
    app.start()
