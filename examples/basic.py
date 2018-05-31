from shiny.ui import UI
from shiny.app import App
from shiny.layout import DashboardLayout
from shiny import widgets as wg


ui = UI()
dashboard = DashboardLayout("Test")
ui.layout = dashboard
dashboard.sidebar.append(
    wg.Text("test", "test", label="Test"),
    wg.Password('passwd', "Password"),
    wg.Checkbox('checkbox', 'option1', 'Option1', False),
    wg.Checkbox('checkbox', 'option2', 'Option2', False),
    wg.Checkbox('checkbox', 'option3', 'Option3', False),
    wg.Checkbox('checkbox1', 'option4', 'Option4', True),
    wg.Radio("radio", [('radio1', 'Radio1', True),
                       ('radio2', 'Radio3'),
                       ('radio4', 'Radio4')], "RADIO"),
    wg.File('file', 'File'),
    wg.Range('range', 10, 'Range', min=0, max=100),
    wg.Number('number', 10, 'Number'),
    wg.Time('time', 'Now'),
    wg.Date('date', 'Date'),
    wg.Url('url', 'https://www.google.com', "Address"),
    wg.Email('email', 'xx@xxx.com', 'Email'),
    wg.Select('select', [('option1', 'Option1', True),
                         ('option2', 'Option2'),
                         ('option3', 'Option3'),
                         ('option3', 'Option3')], 'Option'),
    wg.Textarea('testarea', "some text", "Textarea"),
    wg.Form('form'))

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
