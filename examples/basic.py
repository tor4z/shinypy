from shiny.ui import UI
from shiny.server import Server
from shiny.app import App
from shiny.html5 import Element


ui = UI()
server = Server()

ui.append(Element("div"))

if __name__ == "__main__":
    app = App(ui, server)
    app.start()
