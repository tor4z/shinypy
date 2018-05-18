from .html5 import Element
from .util import randstr


__all__ = ["Level", "Widget", "Label", "Panel"]


class Level:
    DEFAULT = "default"
    PRIMARY = "primary"
    SUCCESS = "success"
    INFO = "info"
    WARNING = "warning"
    DANGER = "danger"


class Widget(Element):
    _TAG = "div"
    _BASE_CLASS = ""
    _DEFAULT_ID_LEN = 5

    def __init__(self, id=None, value=None, *, width=None,
                 height=None, tag=None):
        super().__init__(tag or self._TAG)
        self.id = id or randstr(self._DEFAULT_ID_LEN)
        self._class = ""
        self.set("id", self.id)
        self.value = value
        self.width(width)
        self.height(height)
        self.add_class(self._BASE_CLASS)

    def width(self, val):
        if val is not None:
            self.set("width", val)

    def height(self, val):
        if val is not None:
            self.set("height", val)

    def add_class(self, val):
        if val:
            self._class += f" {val}"
            self.set("class", self._class)

    def __str__(self):
        self.render()
        return super().__str__()

    @classmethod
    def level_class(cls, level=None):
        level = level or Level.DEFAULT
        return f"{cls._BASE_CLASS}-{level}"

    def render(self):
        raise NotImplementedError


class Label(Widget):
    _TAG = "span"
    _BASE_CLASS = "label"

    def __init__(self, id=None, value=None, *, level=None, **kwargs):
        super().__init__(id, value, **kwargs)
        self.add_class(self.level_class(level))

    def render(self):
        if self.value:
            self.text = self.value


class Panel(Widget):
    _TAG = "div"
    _BASE_CLASS = "panel"

    def __init__(self, id=None, *, level=None,
                 header=None, **kwargs):
        super().__init__(id, None, **kwargs)
        self.add_class(self.level_class(level))
        self._body = None

        if header:
            self.init_header(header)
        self.init_body()

    def init_header(self, text):
        header = Element("div")
        header.set("class", "panel-heading")
        header.text = text
        super().append(header)

    def init_body(self):
        self._body = Element("div")
        self._body.set("class", "panel-body")

    def append(self, ele):
        self._body.append(ele)

    def render(self):
        super().append(self._body)


class Input(Widget):
    _TAG = "input"
    _TYPE = "text"

    def __init__(self, id, name, value=None, *, label=None, **kwargs):
        if label is None:
            self._input_tag = None
            super().__init__(id, value, **kwargs)
        else:
            self._input_tag = Element(self._TAG)
            super().__init__(id, value, tag="div", *kwargs)
            self.set("class", "form-group")
            label_tag = self._new_label(id, label)
            self.append(label_tag)

        self.set("type", self._TYPE)
        self.set("name", name)
        self.set("class", "form-control")
        self.set("value", self.value)

    def _new_label(self, id, text):
        label_tag = Element("label")
        label_tag.set("for", id)
        label_tag.text = text
        return label_tag

    def set(self, key, value):
        if self._input_tag:
            self._input_tag.set(key, value)
        else:
            super().set(key, value)

    def render(self):
        if self._input_tag:
            self.append(self._input_tag)


class Date(Input):
    _TYPE = "date"


class File(Input):
    _TYPE = "file"


class Email(Input):
    _TYPE = "email"


class Number(Input):
    _TYPE = "number"

    def __init__(self, id, name, value=None, *, min=None, max=None,
                 step=None, label=None, **kwargs):
        super().__init__(id, name, value, label, **kwargs)
        self.set("min", min)
        self.set("max", max)
        self.set("step", step)


class Password(Input):
    _TYPE = "reset"


class Radio(Widget):
    _TAG = "div"
    _TYPE = "radio"

    def __init__(self, id, name, options, *, label=None, **kwargs):
        super().__init__(id, None, label, **kwargs)
        if not isinstance(options, list):
            raise TypeError("List required.")
        self.radios = []

        for option in options:
            value, display = option
            radio = Element("input")
            radio.set("type", self._TYPE)
            radio.set("name", name)
            radio_id = id + str(value)
            radio.set("id", radio_id)
            label = Element("label")
            label.set("for", radio_id)
            self.radios.append((radio, label))

    def set(self, key, value):
        for radio in self.radios:
            rd, _ = radio
            rd.set(key, value)

    def render(self):
        for radio in self.radios:
            rd, lb = radio
            self.append(rd)
            self.append(lb)
            self.append(Element("br"))


class Checkbox(Radio):
    _TYPE = "checkbox"


class Range(Input):
    _TYPE = "range"
    _MIN = 0
    _MAX = 10

    def __init__(self, id, name, value=None, *, min=None, max=None,
                 label=None, **kwargs):
        super().__init__(id, name, value, label, **kwargs)
        self.set("min", min or self._MIN)
        self.set("max", max or self._MAX)


class Submit(Widget):
    _TAG = "input"
    _TYPE = "submit"
    _VALUE = "Submit"

    def __init__(self, value=None):
        super().__init__()
        self.set("value", value or self._VALUE)


class Reset(Submit):
    _TYPE = "reset"
    _VALUE = "Reset"


class Text(Input):
    _TYPE = "text"


class Time(Input):
    _TYPE = "time"


class Url(Input):
    _TYPE = "url"


class Textarea(Widget):
    _TAG = "textarea"

    def __init__(self, id, *, rwos=None, cols=None, value=None,
                 label=None, **kwargs):
        if label is None:
            super().__init__(id, value, **kwargs)
            self._textarea = None
        else:
            super().__init__(id, value, tag="div", **kwargs)
            self._textarea = Element(self._TAG)

        self.set("rwos", rwos)
        self.set("cols", cols)

    def set(self, key, value):
        if self._textarea is None:
            super().set(key, value)
        else:
            self._textarea.set(key, value)

    def render(self):
        if self._textarea is not None:
            self.append(self._textarea)


class Form(Widget):
    _TAG = "form"


class Image(Widget):
    _TYPE = "image"

    def __init__(self):
        pass
