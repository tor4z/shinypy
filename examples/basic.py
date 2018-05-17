from shiny.ui import UI
from shiny.server import Server
from shiny.app import App
from shiny.layout import DashboardLayout


ui = UI()
server = Server()
dashboard = DashboardLayout("Test")
ui.layout = dashboard

dashboard.sidebar.text("sidebar")
dashboard.main.text("main")

if __name__ == "__main__":
    app = App(ui, server)
    app.start()
