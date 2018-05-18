from shiny.html5 import Element
from shiny.util import randstr
from bs4 import BeautifulSoup


def test_element():
    h1 = Element("h1")
    text = randstr(5)
    h1.text = text

    key = randstr(5)
    value = randstr(5)
    h1.set(key, value)

    a = Element("a")
    a.set("href", "/")
    h1.append(a)

    soup = BeautifulSoup(str(h1), "lxml")
    tag = soup.h1

    assert tag.name == "h1"
    assert tag.text == text
    assert tag[key] == value

    link = tag.a
    assert link.name == "a"
    assert link["href"] == "/"
