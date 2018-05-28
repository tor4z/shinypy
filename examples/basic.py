from shiny.ui import UI
from shiny.app import App
from shiny.layout import DashboardLayout
from shiny import widgets as wg


ui = UI()
dashboard = DashboardLayout("Test")
ui.layout = dashboard
dashboard.sidebar.append(
    wg.Text("test", "test", label="Test"),
    wg.Password('passwd', label="Password"),
    wg.Checkbox('checkbox', [('option1', 'Option1', True),
                             ('option2', 'Option2')]))
dashboard.main.append(
    wg.Label("test"))


def server(OUT):
    @wg.Label.render
    def do_test(IN):
        return IN["test"]
    OUT["test"] = do_test


if __name__ == "__main__":
    app = App(ui, server)
    app.start()
