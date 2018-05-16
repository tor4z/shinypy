from shiny.ui import UI
from shiny.server import Server
from shiny.app import App

ui = UI()
server = Server()

if __name__ == "__main__":
    app = App(ui, server)
    app.start()
