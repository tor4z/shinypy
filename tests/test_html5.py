from shiny.html5 import Element


def test_new_element():
    title = "title"
    h1 = Element("h1")
    h1.text(title)
    assert str(h1) == f"<h1>{title}</h1>"
