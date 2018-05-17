from .html5 import Element
from .util import randstr


class Widget(Element):
    _TAG = "div"
    _DEFAULT_ID_LEN = 5

    def __init__(self, id=None):
        super().__init__(self._TAG)
        self.id = id or randstr(self._DEFAULT_ID_LEN)
        self.set("id", self.id)
        self._value = None
        self._class = ""

    def width(self, val):
        self.set("width", val)

    def height(self, val):
        self.set("height", val)

    def value(self, val):
        self._value = val

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
        self.text(self._value)
