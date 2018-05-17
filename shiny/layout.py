from .html5 import Element, CSS
from .const import dashboard_css_path


class Layout(Element):
    def render(self):
        raise NotImplementedError

    @property
    def element(self):
        self.render()
        return self._element


class DashboardLayout(Layout):
    _CSS_PATH = dashboard_css_path

    def __init__(self, name):
        super().__init__("div")
        self._name = name
        self.sidebar = Element("div")
        self.main = Element("div")
        css = CSS(self._CSS_PATH)
        self.append(css)

    def _navbar(self):
        nav = Element("nav")
        nav.set("class", "navbar navbar-dark fixed-top bg-dark\
                          flex-md-nowrap p-0 shadow")

        title_link = Element("a")
        title_link.set("class", "navbar-brand col-sm-3 col-md-2 mr-0")
        title_link.set("href", "/")
        title_link.text(self._name)
        nav.append(title_link)
        return nav

    def _sidebar(self):
        nav = Element("nav")
        nav.set("class", "col-md-2 d-none d-md-block bg-light sidebar")
        sidebar_sticky = Element("div")
        sidebar_sticky.set("class", "sidebar-sticky")
        sidebar_sticky.append(self.sidebar)
        nav.append(sidebar_sticky)
        return nav

    def _main(self):
        main = Element("main")
        main.set("role", "main")
        main.set("class", "col-md-9 ml-sm-auto col-lg-10 px-4 main")
        main.append(self.main)
        return main

    def _fluid(self):
        sidebar = self._sidebar()
        main = self._main()

        row_layout = Element("div")
        row_layout.set("class", "row")
        row_layout.append(sidebar)
        row_layout.append(main)

        container = Element("div")
        container.set("class", "container-fluid")
        container.append(row_layout)
        return container

    def render(self):
        navbar = self._navbar()
        container = self._fluid()
        self.append(navbar)
        self.append(container)
