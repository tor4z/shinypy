from shiny.ui import UI
from shiny.app import App
from shiny.layout import DashboardLayout


ui = UI()
dashboard = DashboardLayout("Test")
ui.layout = dashboard
dashboard.sidebar.text("sidebar")
dashboard.main.text("main")


def server(input, output):
    pass


if __name__ == "__main__":
    app = App(ui, server)
    app.start()
