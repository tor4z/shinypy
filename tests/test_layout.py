from shiny.layout import DashboardLayout
from bs4 import BeautifulSoup
from shiny.util import randstr


def test_dashboard():
    name = randstr(5)
    dbl = DashboardLayout(name)

    soup = BeautifulSoup(str(dbl), "lxml")
    navbar = soup.div.nav
    container = soup.find("div", class_="container-fluid")
    sideabr = container.find("nav", class_="sidebar")
    main = container.find("main")

    assert navbar.name == "nav"
    assert container.name == "div"
    assert sideabr.name == "nav"
    assert main.name == "main"
    # TODO test attribute
