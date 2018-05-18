from shiny.ui import UI
from shiny.util import randstr
from bs4 import BeautifulSoup


def test_ui():
    tit = randstr(10)
    ui = UI(title=tit)

    soup = BeautifulSoup(str(ui), "lxml")
    html = soup.find("html")
    head = html.head
    title = head.find("title")
    body = html.body

    assert html.name == "html"
    assert head.name == "head"
    assert body.name == "body"

    assert title.name == "title"
    assert title.text == tit

    css_links = head.find_all("link")
    for css in css_links:
        assert css.name == "link"
        assert css["rel"][0] == "stylesheet"
        assert css["type"] == "text/css"
        assert css["href"] is not None

    scripts = head.find_all("script")
    for script in scripts:
        assert script.name == "script"
        assert script["type"] == "text/javascript"
        assert script["src"] is not None
