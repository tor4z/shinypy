from shiny import widgets as wg
from shiny.util import randstr
from bs4 import BeautifulSoup


def test_lable():
    id = randstr(5)
    val = randstr(5)
    label = wg.Label(id, val)
    soup = BeautifulSoup(str(label), "lxml")
    tag = soup.div

    assert tag.name == "div"
    assert tag["id"] == id
    assert tag.text == val
