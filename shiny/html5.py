from lxml import etree


class Element:
    DOCTYPE = "<!DOCTYPE html>"
    _SIMPLE_TAG = ["link", "br"]
    __slots__ = ["_element", "_declarar"]

    def __init__(self, tag, declarar=False):
        self._declarar = declarar
        self._element = etree.Element(tag)
        if tag not in self._SIMPLE_TAG:
            self._element.text = ""

    def set(self, key, value):
        if not (key is None or value is None):
            self._element.set(key, str(value))

    def get(self, key):
        return self._element.get(key)

    def __setitem__(self, key, value):
        self.set(key, value)

    def __getitem__(self, key):
        return self.get(key)

    @property
    def element(self):
        return self._element

    def append(self, ele):
        if not isinstance(ele, Element):
            raise TypeError("Element reqquired.")
        self._element.append(ele.element)

    @property
    def text(self):
        return self._element.text

    @text.setter
    def text(self, text):
        self._element.text = text

    def __str__(self):
        doctype = self.DOCTYPE if self._declarar else None
        element = etree.tostring(self.element, doctype=doctype)
        if not isinstance(element, str):
            element = element.decode()
        return element

    __repr__ = __str__


class CSS(Element):
    def __init__(self, href):
        super().__init__("link")
        self.set("type", "text/css")
        self.set("rel", "stylesheet")
        self.set("href", href)


class JS(Element):
    def __init__(self, src):
        super().__init__("script")
        self.set("type", "text/javascript")
        self.set("src", src)


class Title(Element):
    def __init__(self, title):
        super().__init__("title")
        self.text = title
