from .html5 import Element
import os
import base64
import imghdr


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
                 height=None, tag=None, **kwargs):
        super().__init__(tag or self._TAG)
        self.id = id
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
        self._render()
        return super().__str__()

    @classmethod
    def level_class(cls, level=None):
        level = level or Level.DEFAULT
        return f"{cls._BASE_CLASS}-{level}"

    def _render(self):
        raise NotImplementedError

    @classmethod
    def render(cls, func):
        def _exec(*args, **kwargs):
            return func(*args, **kwargs)
        return _exec

class Label(Widget):
    _TAG = "span"
    _BASE_CLASS = "label"

    def __init__(self, id=None, value=None, *, level=None, **kwargs):
        super().__init__(id, value, **kwargs)
        self.add_class(self.level_class(level))

    def _render(self):
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

    def _render(self):
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
            super().__init__(id, value, tag="div", **kwargs)
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

    def _render(self):
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
                 step=1, label=None, **kwargs):
        super().__init__(id, name, value, label=label, **kwargs)
        if min is not None and max is not None and max < min:
            raise ValueError("max should be great than min.")
        if step is not None and step <= 0:
            raise ValueError("step should be great than 0")
        self.set("min", min)
        self.set("max", max)
        self.set("step", step)


class Password(Input):
    _TYPE = "password"


class Radio(Widget):
    _TAG = "div"
    _TYPE = "radio"

    def __init__(self, id, name, options, **kwargs):
        if not isinstance(options, list):
            raise TypeError("List required.")
        self.radios = []
        for option in options:
            value, display = option
            radio = Element("input")
            radio.set("type", self._TYPE)
            radio.set("name", name)
            radio.set("value", value)
            radio_id = id + str(value)
            radio.set("id", radio_id)
            label = Element("label")
            label.set("for", radio_id)
            label.text = display
            self.radios.append((radio, label))

        super().__init__(None, None, **kwargs)

    def set(self, key, value):
        for radio in self.radios:
            rd, _ = radio
            rd.set(key, value)

    def _render(self):
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
        super().__init__(id, name, value, label=label, **kwargs)
        self.set("min", min or self._MIN)
        self.set("max", max or self._MAX)
        if min is not None and max is not None and max < min:
            raise ValueError("max should be great than min.")


class Submit(Widget):
    _TAG = "input"
    _TYPE = "submit"
    _VALUE = "Submit"

    def __init__(self, value=None):
        super().__init__()
        self.set("value", value or self._VALUE)
        self.set("type", self._TYPE)

    def _render(self):
        pass


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

    def __init__(self, id, name, *, rows=5, cols=5, value=None,
                 label=None, **kwargs):
        if label is None:
            self._textarea = None
            super().__init__(id, value, **kwargs)
        else:
            self._textarea = Element(self._TAG)
            super().__init__(id, value, tag="div", **kwargs)
            label = Element("label")
            label.set("for", id)
            br = Element("br")
            self.append(label)
            self.append(br)

        self.set("name", name)
        self.set("rows", rows)
        self.set("cols", cols)

    def set(self, key, value):
        if self._textarea is None:
            super().set(key, value)
        else:
            self._textarea.set(key, value)

    def _render(self):
        if self._textarea is not None:
            self.append(self._textarea)


class Form(Widget):
    _TAG = "form"

    def _render(self):
        submit = Submit()
        reset = Reset()
        self.append(submit)
        self.append(reset)


class Image(Widget):
    _TAG = "img"

    def __init__(self, id=None, *, img=None, path=None, url=None,
                 alt=None, **kwargs):
        super().__init__(id, **kwargs)
        if img is None and path is None and url is None:
            raise ValueError("not image input.")
        if url is not None:
            src = url
        else:
            # Use base64 image
            src = self.base64_src(path, img)

        self.set("src", src)
        self.set("alt", alt)

    @classmethod
    def get_img(cls, path, img=None):
        if img is not None:
            return img, imghdr.what(None, img)
        if not os.path.exists(path):
            raise FileNotFoundError("image not exist.")

        fp = open(path, "rb")
        img = fp.read()
        fp.close()
        return img, imghdr.what(path)

    @classmethod
    def base64_src(cls, path, img):
        img, fmt = cls.get_img(path, img)
        base64_img = base64.b64encode(img)
        return f'data:image/{fmt};base64, {base64_img.decode("utf-8")}'

    def _render(self):
        pass

    @classmethod
    def render(cls, func):
        def _exec(*args, **kwargs):
            img = func(*args, **kwargs)
            return cls.base64_src(None, img)
        return _exec
