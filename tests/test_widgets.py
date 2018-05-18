from shiny import widgets as wg
from shiny.util import randstr
from bs4 import BeautifulSoup


def new_soup(element):
    return BeautifulSoup(str(element), "lxml")


def test_lable():
    id = randstr(5)
    val = randstr(5)
    label = wg.Label(id, val)
    soup = new_soup(label)
    tag = soup.span

    assert tag.name == "span"
    assert tag["id"] == id
    assert tag.text == val


def test_panel():
    id = randstr(5)
    panel = wg.Panel(id, header="Header")
    soup = new_soup(panel)

    panel_tag = soup.div

    assert "panel" in panel_tag["class"]
    assert "panel-default" in panel_tag["class"]
    assert panel_tag["id"] == id

    panel_header = soup.find_all("div", class_="panel-heading")[0]
    panel_body = soup.find_all("div", class_="panel-body")[0]

    assert panel_header.name == "div"
    assert panel_body.name == "div"


def test_date():
    id = randstr(5)
    name = randstr(5)
    date = wg.Date(id, name=name)
    soup = new_soup(date)

    input_tag = soup.input

    assert input_tag.name == "input"
    assert input_tag["id"] == id
    assert input_tag["name"] == name
    assert input_tag["type"] == "date"


def test_date_label():
    id = randstr(5)
    lab = randstr(10)
    name = randstr(5)

    date = wg.Date(id, name=name, label=lab)
    soup = new_soup(date)

    container = soup.div
    label_tag = container.label
    input_tag = container.input

    assert label_tag.name == "label"
    assert label_tag["for"] == id
    assert input_tag.name == "input"
    assert input_tag["id"] == id
    assert input_tag["name"] == name
    assert input_tag["type"] == "date"


def test_file():
    pass


def test_file_label():
    pass
