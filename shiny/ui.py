from .html5 import Element, CSS, JS, Title
from .const import (bootstrap_css_path,
                    bootstrap_js_path,
                    jquery_js_path)


class UI:
    _TITLE = "Shiny App"

    def __init__(self, title=None):
        self.html = Element("html", declarar=True)
        self.title = title
        self.body = None
        self.init_head()
        self.init_body()

    def init_head(self):
        head = Element("head")

        title = Title(self.title or self._TITLE)
        bootstrap_css= CSS(bootstrap_css_path)
        bootstrap_js = JS(bootstrap_js_path)
        jquery_js = JS(jquery_js_path)

        head.append(title)
        head.append(bootstrap_css)
        head.append(bootstrap_js)
        head.append(jquery_js)

        self.html.append(head)

    def init_body(self):
        self.body = Element("body")

    def append(self, ele):
        self.body.append(ele)

    def __str__(self):
        self.html.append(self.body)
        return str(self.html)

    __repr__ = __str__
