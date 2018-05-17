from lxml import etree


class Element:
    __slots__ = ["_element"]

    def __init__(self, tag):
        self._element = etree.Element(tag)

    def set(self, key, value):
        self._element.set(key, value)

    def get(self, key):
        return self._element.get(key)

    def __setattr__(self, key, value):
        if key not in self.__slots__:
            self.set(key, value)
        else:
            super().__setattr__(key, value)

    def __getattr__(self, key):
        if key not in self.__slots__:
            return self.get(key)
        else:
            return super().__getattribute__(key)

    def append(self, ele):
        self._element.append(ele)

    @property
    def text(self):
        return self._element.text

    @text.setter
    def text(self, text):
        self._element.text = text

    def __str__(self):
        element = etree.tostring(self._element)
        if not isinstance(element, str):
            element = element.decode()
        return element

    __repr__ = __str__
