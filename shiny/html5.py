from lxml import etree


class Element:
    __slots__ = ["_element"]

    def __init__(self, tag):
        self._element = etree.Element(tag)

    def __setattribute__(self, key, value):
        if not key[0] == '_':
            self._element.set(key, value)

    def __getattr__(self, key):
        if not key[0] == '_':
            self._element.get(key)

    def append(self, ele):
        pass

    def text(self, text):
        self._element.text = text

    def __str__(self):
        element = etree.tostring(self._element)
        if not isinstance(element, str):
            element = element.decode()
        return element

    __repr__ = __str__
