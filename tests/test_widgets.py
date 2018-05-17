from shiny import widgets as wg


def test_lable():
    label = wg.Label()
    label.value("hello")
    # TODO assert
