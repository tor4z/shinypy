import os
import base64
import imghdr
import datetime
from .html5 import Element
from .util import randstr


__all__ = ["Level", "Model", "Widget", "Label", "Panel", "Date", "File",
           "Email", "Number", "Password", "Radio", "Checkbox", "Range",
           "Submit", "Reset", "Text", "Time", "Url", "Textarea", "Form",
           "Image", "WidgetExp"]


class Level:
    DEFAULT = "default"
    PRIMARY = "primary"
    SUCCESS = "success"
    INFO = "info"
    WARNING = "warning"
    DANGER = "danger"


class Model:
    In = "model-in"
    Out = "model-out"
    Layout = "model-layout"
    Button = "model-button"


class Widget(Element):
    _TAG = "div"
    _BASE_CLASS = ""
    _MODEL = None
    _DEFAULT_ID_LEN = 10

    def __init__(self, model, value=None, *, id=None, tag=None, **kwargs):
        super().__init__(tag or self._TAG)
        self.id = id
        self.model = model
        self._class = ""
        self.set("id", self.id)
        self.value = value
        self.add_class(self._BASE_CLASS)
        self.set_model(model or self.id or randstr(10))

    def set_model(self, model):
        if self._MODEL is None:
            raise WidgetExp("MODEL undefined.")
        if not isinstance(model, str):
            raise TypeError("model should be a string.")
        self.set(self._MODEL, model)

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
    _MODEL = Model.Out

    def __init__(self, model, id=None, value=None, *, level=None, **kwargs):
        super().__init__(model, value, id=id, **kwargs)
        self.add_class(self.level_class(level))

    def _render(self):
        if self.value:
            self.text = self.value


class Panel(Widget):
    _TAG = "div"
    _BASE_CLASS = "panel"
    _MODEL = Model.Layout

    def __init__(self, model=None, id=None, *, level=None,
                 header=None, **kwargs):
        super().__init__(model, None, id=id, **kwargs)
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

    def append(self, *elements):
        for element in elements:
            self._body.append(element)

    def _render(self):
        super().append(self._body)


class Input(Widget):
    _TAG = "input"
    _TYPE = "text"
    _MODEL = Model.In

    def __init__(self, model, value, label, *, id=None, **kwargs):
        if label is None:
            self._input_tag = None
            self._label_tag = None
            super().__init__(model, value, id=id, **kwargs)
        else:
            id = id or randstr(10)   # id must be not None
            self._input_tag = Element(self._TAG)
            super().__init__(model, value, id=id, tag="div", **kwargs)
            super().set("class", "form-group")
            self._label_tag = self._new_label(id, label)

        self.set("type", self._TYPE)
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
        if self._label_tag:
            self.append(self._label_tag)
        if self._input_tag:
            self.append(self._input_tag)


class Date(Input):
    _TYPE = "date"

    def __init__(self, model, label, value=None, **kwargs):
        if value is not None and not isinstance(value, datetime.date):
            raise TypeError("datetime.date required.")
        date = value or datetime.date.today()
        date_str = date.strftime("%Y-%m-%d")
        super().__init__(model, date_str, label, **kwargs)


class File(Input):
    _TYPE = "file"

    def __init__(self, model, label, **kwargs):
        super().__init__(model, None, label, **kwargs)


class Email(Input):
    # TODO verify email addr
    _TYPE = "email"


class Number(Input):
    _TYPE = "number"

    def __init__(self, model, value, label, *, id=None, min=None, max=None,
                 step=1, **kwargs):
        super().__init__(model, value, id=id, label=label, **kwargs)
        if min is not None and max is not None and max < min:
            raise ValueError("max should be greater than min.")
        if step is not None and step <= 0:
            raise ValueError("step should be greater than 0")
        if (min is not None and value < min) or\
           (max is not None and value > max):
            raise ValueError("value should be less than max and\
                             greater then min")

        self.set("min", min)
        self.set("max", max)
        self.set("step", step)


class Password(Input):
    _TYPE = "password"

    def __init__(self, model, label, **kwargs):
        super().__init__(model, None, label, **kwargs)


class Radio(Widget):
    _TAG = "div"
    _TYPE = "radio"
    _MODEL = Model.In

    def __init__(self, model, options, label, **kwargs):
        if not isinstance(options, list):
            raise TypeError("List required.")
        self.radios = []
        self._model = model
        for option in options:
            if isinstance(option, str):
                value = option
                display = option
                checked = False
            else:
                opt_len = len(option)
                if opt_len == 3:
                    value, display, checked = option
                elif opt_len == 2:
                    value, display = option
                    checked = False
                else:
                    raise TypeError

            radio = Element("input")
            radio.set("type", self._TYPE)
            radio.set("value", value)
            if checked:
                radio.set("checked", 'true')
            self.radios.append((radio, display))

        self._label_tag = Element('label')
        self._label_tag.text = label
        super().__init__(model, None, **kwargs)

    def set(self, key, value):
        for radio in self.radios:
            rd, _ = radio
            rd.set(key, value)

    def new_item(self, radio):
        rd, dis = radio
        id = randstr(10)
        div = Element('div')
        div.set('class', 'form-check')

        rd.set('id', id)
        rd.set('name', self._model)
        rd.set('class', 'form-check-input')

        label = Element('label')
        label.set('class', 'form-check-label')
        label.set('for', id)
        label.text = dis

        div.append(rd, label)
        return div

    def _render(self):
        self.append(self._label_tag)
        for radio in self.radios:
            item = self.new_item(radio)
            self.append(item)


class Checkbox(Widget):
    _TAG = "div"
    _TYPE = "checkbox"
    _MODEL = Model.In

    def __init__(self, model, value, label, checked=False, **kwargs):
        id = randstr(10)
        self._input_tag = Element('input')
        self._label_tag = Element('label')

        self._label_tag.text = label
        self._label_tag.set('for', id)
        self._label_tag.set('class', 'form-check-label')

        self.set('id', id)
        self.set('class', 'form-check-input')
        self.set('value', value)
        self.set('type', self._TYPE)

        super().__init__(model, **kwargs)
        super().set('class', 'form-check')

    def set(self, key, value):
        self._input_tag.set(key, value)

    def _render(self):
        self.append(self._input_tag)
        self.append(self._label_tag)

class Range(Input):
    _TYPE = "range"
    _MIN = 0
    _MAX = 100

    def __init__(self, model, value, label, *,id=None, min=None, max=None,
                 **kwargs):
        super().__init__(model, value, id=id, label=label, **kwargs)
        min = min or self._MIN
        max = max or self._MAX
        if (value < min) or (value > max):
            raise ValueError("value should be less than max and\
                             greater then min")

        self.set("min", min)
        self.set("max", max)
        if min is not None and max is not None and max < min:
            raise ValueError("max should be great than min.")


class Submit(Widget):
    _TAG = "input"
    _TYPE = "submit"
    _VALUE = "Submit"
    _BASE_CLASS = "btn btn-primary"
    _MODEL = Model.Button

    def __init__(self, model, value=None):
        super().__init__(model)
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

    def __init__(self, model, label, value=None, **kwargs):
        if value is None:
            value = datetime.datetime.now()
        if value is not None and isinstance(value, datetime.datetime):
            value = value.strftime("%H:%M")
        else:
            raise TypeError("datetime required.")
        super().__init__(model, value, label, **kwargs)


class Url(Input):
    _TYPE = "url"


class Textarea(Widget):
    _TAG = "textarea"
    _MODEL = Model.In

    def __init__(self, model, value, label, *, id=None, rows=5, cols=5,
                 **kwargs):
        if label is None:
            self._textarea = None
            super().__init__(model, value, id=id, **kwargs)
        else:
            id = id or randstr(10)
            self._textarea = Element(self._TAG)
            super().__init__(model, value, id=id, tag="div", **kwargs)
            label_tag = Element("label")
            label_tag.set("for", id)
            label_tag.text = label
            br = Element("br")
            self.append(label_tag)
            self.append(br)

        super().set('class', 'form-group')
        self.set("rows", rows)
        self.set("cols", cols)
        self.set('class', 'form-control')

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
    _MODEL = Model.Layout

    def __init__(self, model):
        super().__init__(model)

    def _render(self):
        submit = Submit(self.model)
        reset = Reset(self.model)
        self.append(submit)
        self.append(reset)


class Image(Widget):
    _TAG = "img"
    _MODEL = Model.Out

    def __init__(self, model, id=None, *, img=None, path=None, url=None,
                 alt=None, **kwargs):
        super().__init__(model, None, id=id, **kwargs)
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


class Select(Widget):
    _TAG = "div"
    _MODEL = Model.In

    def __init__(self, model, optinos, label, **kwargs):
        if not isinstance(optinos, list):
            raise TypeError('List required.')

        self._select_tag = Element('select')
        for optino in optinos:
            tag = self._new_item(optino)
            self._select_tag.append(tag)

        label_tag = Element('label')
        label_tag.text = label
        self._select_tag.set('class', 'custom-select')
        super().__init__(model, None, **kwargs)
        self.append(label_tag)

    def _new_item(self, optino):
        opt_len = len(optino)
        if opt_len == 3:
            value, display, selected = optino
        elif opt_len == 2:
            value, display = optino
            selected = False
        else:
            raise ValueError

        tag = Element('option')
        tag.text = display
        if selected:
            tag.set('selected', 'true')
        return tag

    def set(self, key, value):
        self._select_tag.set(key, value)

    def _render(self):
        self.append(self._select_tag)


class WidgetExp(Exception):
    pass
