from .html5 import Element
from .util import randstr


class Widget(Element):
    _TAG = "div"
    _DEFAULT_ID_LEN = 5

    def __init__(self, id=None, value=None, *, width=None,
                 height=None):
        super().__init__(self._TAG)
        self.id = id or randstr(self._DEFAULT_ID_LEN)
        self.set("id", self.id)
        self.width(width)
        self.height(height)
        self.value = value
        self._class = ""

    def width(self, val):
        if val is not None:
            self.set("width", val)

    def height(self, val):
        if val is not None:
            self.set("height", val)

    def add_class(self, val):
        self._class += f" {val}"
        self.set("class", self._class)

    def __str__(self):
        self.render()
        return super().__str__()

    def render(self):
        raise NotImplementedError


class Label(Widget):
    _TAG = "div"

    def render(self):
        if self.value:
            self.text = self.value
