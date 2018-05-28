from shiny import widgets as wg
from shiny.widgets import Model
from shiny.util import randstr
from bs4 import BeautifulSoup
import random
import pytest
import base64


TEST_IMAGE_PATH = "./tests/data/test_image.jpg"
TEST_IMAGE_FMT = "jpeg"


def new_soup(element):
    return BeautifulSoup(str(element), "lxml")


def test_lable():
    id = randstr(5)
    val = randstr(5)
    model = randstr(5)
    label = wg.Label(model, id, val)
    soup = new_soup(label)
    tag = soup.span

    assert tag.name == "span"
    assert tag["id"] == id
    assert tag.text == val


def test_panel():
    id = randstr(5)
    model = randstr()
    panel = wg.Panel(model, id, header="Header")
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
    model = randstr(5)

    date = wg.Date(model)
    soup = new_soup(date)

    input_tag = soup.input

    assert input_tag.name == "input"
    assert input_tag["type"] == "date"


def test_date_label():
    id = randstr(5)
    lab = randstr(10)
    model = randstr(5)

    date = wg.Date(model, None, id=id, label=lab)
    soup = new_soup(date)

    container = soup.div
    label_tag = container.label
    input_tag = container.input

    assert label_tag.name == "label"
    assert label_tag["for"] == id
    assert input_tag.name == "input"
    assert input_tag["id"] == id
    assert input_tag[Model.In] == model
    assert input_tag["type"] == "date"


def test_file():
    id = randstr(5)
    model = randstr(5)
    file = wg.File(model, "path", id=id)
    soup = new_soup(file)

    input_tag = soup.input

    assert input_tag.name == "input"
    assert input_tag["id"] == id
    assert input_tag[Model.In] == model
    assert input_tag["type"] == "file"


def test_file_label():
    id = randstr(5)
    lab = randstr(10)
    model = randstr(5)

    file = wg.File(model, "file/path", id=id, label=lab)
    soup = new_soup(file)

    container = soup.div
    label_tag = container.label
    input_tag = container.input

    assert label_tag.name == "label"
    assert label_tag["for"] == id
    assert input_tag.name == "input"
    assert input_tag["id"] == id
    assert input_tag[Model.In] == model
    assert input_tag["type"] == "file"


def test_email():
    id = randstr(5)
    model = randstr(5)

    email = wg.Email(model, "emai_addr", id=id)
    soup = new_soup(email)

    input_tag = soup.input

    assert input_tag.name == "input"
    assert input_tag["id"] == id
    assert input_tag[Model.In] == model
    assert input_tag["type"] == "email"


def test_email_label():
    id = randstr(5)
    lab = randstr(10)
    model = randstr(5)

    email = wg.Email(model, "email_addr", id=id, label=lab)
    soup = new_soup(email)

    container = soup.div
    label_tag = container.label
    input_tag = container.input

    assert label_tag.name == "label"
    assert label_tag["for"] == id
    assert input_tag.name == "input"
    assert input_tag["id"] == id
    assert input_tag[Model.In] == model
    assert input_tag["type"] == "email"


def test_number():
    id = randstr(5)
    model = randstr(5)
    min = random.randint(0, 10)
    max = random.randint(100, 200)
    step = random.randint(1, 10)
    number = wg.Number(model, random.randint(11, 99), id=id, min=min, max=max,
                       step=step)
    soup = new_soup(number)

    input_tag = soup.input

    assert input_tag.name == "input"
    assert input_tag["id"] == id
    assert input_tag[Model.In] == model
    assert input_tag["type"] == "number"
    assert input_tag["min"] == str(min)
    assert input_tag["max"] == str(max)
    assert input_tag["step"] == str(step)


def test_number_label():
    id = randstr(5)
    lab = randstr(10)
    model = randstr(5)
    min = random.randint(0, 10)
    max = random.randint(100, 200)
    step = random.randint(1, 10)

    number = wg.Number(model, random.randint(11, 99), id=id, min=min, max=max,
                       step=step, label=lab)
    soup = new_soup(number)

    container = soup.div
    label_tag = container.label
    input_tag = container.input

    assert label_tag.name == "label"
    assert label_tag["for"] == id
    assert input_tag.name == "input"
    assert input_tag["id"] == id
    assert input_tag[Model.In] == model
    assert input_tag["type"] == "number"
    assert input_tag["min"] == str(min)
    assert input_tag["max"] == str(max)
    assert input_tag["step"] == str(step)


def test_number_valueerror():
    id = randstr(5)
    lab = randstr(10)
    model = randstr(5)
    value = random.randint(100, 200)

    with pytest.raises(ValueError):
        wg.Number(model, value, id=id, min=random.randint(100, 200),
                  max=random.randint(0, 99), label=lab)

    with pytest.raises(ValueError):
        wg.Number(model, value, id=id, min=random.randint(0, 99),
                  max=random.randint(100, 200),
                  step=random.randint(-100, -1),
                  label=lab)

    value = random.randint(0, 99)
    with pytest.raises(ValueError):
        wg.Number(model, value, id=id, min=random.randint(100, 200),
                  max=random.randint(300, 400), label=lab)

    value = random.randint(401, 500)
    with pytest.raises(ValueError):
        wg.Number(model, value, id=id, min=random.randint(100, 200),
                  max=random.randint(300, 400), label=lab)


def test_password():
    id = randstr(5)
    model = randstr(5)
    pwd = randstr(10)

    passwd = wg.Password(model, pwd, id=id)
    soup = new_soup(passwd)

    input_tag = soup.input

    assert input_tag.name == "input"
    assert input_tag["id"] == id
    assert input_tag[Model.In] == model
    assert input_tag["type"] == "password"


def test_password_label():
    id = randstr(5)
    lab = randstr(10)
    model = randstr(5)
    pwd = randstr(10)

    passwd = wg.Password(model, pwd, id=id, label=lab)
    soup = new_soup(passwd)

    container = soup.div
    label_tag = container.label
    input_tag = container.input

    assert label_tag.name == "label"
    assert label_tag["for"] == id
    assert input_tag.name == "input"
    assert input_tag["id"] == id
    assert input_tag[Model.In] == model
    assert input_tag["type"] == "password"


def test_radio():
    id = randstr(5)
    model = randstr(5)
    options = []
    for i in range(10):
        val = randstr(i * 2)
        options.append((val, val.upper()))

    radio = wg.Radio(model, options)
    soup = new_soup(radio)

    for input_tag in soup.find_all("input"):
        value = input_tag["value"]
        assert input_tag.name == "input"
        assert input_tag[Model.In] == model
        assert input_tag["type"] == "radio"

        label = input_tag.find_next_sibling("label")
        assert label is not None
        label["for"] == id + str(value)
        label.text == value.upper()


def test_checkbox():
    id = randstr(5)
    model = randstr(5)
    options = []
    for i in range(10):
        val = randstr(i * 2)
        options.append((val, val.upper()))

    checkbox = wg.Checkbox(model, options)
    soup = new_soup(checkbox)

    for input_tag in soup.find_all("input"):
        value = input_tag["value"]
        assert input_tag.name == "input"
        assert input_tag[Model.In] == model
        assert input_tag["type"] == "checkbox"

        label = input_tag.find_next_sibling("label")
        assert label is not None
        label["for"] == id + str(value)
        label.text == value.upper()


def test_range():
    id = randstr(5)
    model = randstr(5)
    min = random.randint(0, 10)
    max = random.randint(100, 200)
    range = wg.Range(model, random.randint(11, 99), min=min, max=max, id=id)
    soup = new_soup(range)

    input_tag = soup.input

    assert input_tag.name == "input"
    assert input_tag["id"] == id
    assert input_tag[Model.In] == model
    assert input_tag["type"] == "range"
    assert input_tag["min"] == str(min)
    assert input_tag["max"] == str(max)


def test_range_label():
    id = randstr(5)
    lab = randstr(10)
    model = randstr(5)
    min = random.randint(0, 10)
    max = random.randint(110, 200)
    value = random.randint(11, 100)

    range = wg.Range(model, value, id=id, min=min, max=max, label=lab)
    soup = new_soup(range)

    container = soup.div
    label_tag = container.label
    input_tag = container.input

    assert label_tag.name == "label"
    assert label_tag["for"] == id
    assert input_tag.name == "input"
    assert input_tag["id"] == id
    assert input_tag[Model.In] == model
    assert input_tag["type"] == "range"
    assert input_tag["min"] == str(min)
    assert input_tag["max"] == str(max)


def test_range_valueerror():
    id = randstr(5)
    lab = randstr(10)
    model = randstr(5)
    value = random.randint(100, 200)

    with pytest.raises(ValueError):
        wg.Range(model, value, id=id, min=random.randint(100, 200),
                 max=random.randint(0, 99), label=lab)

    value = random.randint(0, 99)
    with pytest.raises(ValueError):
        wg.Range(model, value, id=id, min=random.randint(100, 200),
                 max=random.randint(300, 400), label=lab)

    value = random.randint(401, 500)
    with pytest.raises(ValueError):
        wg.Range(model, value, id=id, min=random.randint(100, 200),
                 max=random.randint(300, 400), label=lab)


def test_submit():
    value = randstr(5)
    model = randstr(5)

    submit = wg.Submit(model, value)
    soup = new_soup(submit)

    input_tag = soup.input

    assert input_tag.name == "input"
    assert input_tag["type"] == "submit"
    assert input_tag["value"] == value
    assert input_tag[Model.Button] == model


def test_reset():
    value = randstr(5)
    model = randstr(5)
    reset = wg.Reset(model, value)
    soup = new_soup(reset)

    input_tag = soup.input

    assert input_tag.name == "input"
    assert input_tag["type"] == "reset"
    assert input_tag["value"] == value
    assert input_tag[Model.Button] == model


def test_text():
    id = randstr(5)
    model = randstr(5)
    txt = randstr(100)

    text = wg.Text(model, txt, id=id)
    soup = new_soup(text)

    input_tag = soup.input

    assert input_tag.name == "input"
    assert input_tag["id"] == id
    assert input_tag[Model.In] == model
    assert input_tag["type"] == "text"


def test_text_label():
    id = randstr(5)
    lab = randstr(10)
    model = randstr(5)
    value = randstr(10)

    text = wg.Text(model, value, id=id, label=lab)
    soup = new_soup(text)

    container = soup.div
    label_tag = container.label
    input_tag = container.input

    assert label_tag.name == "label"
    assert label_tag["for"] == id
    assert input_tag.name == "input"
    assert input_tag["id"] == id
    assert input_tag[Model.In] == model
    assert input_tag["type"] == "text"


def test_time():
    id = randstr(5)
    model = randstr(5)
    time = wg.Time(model, id=id)
    soup = new_soup(time)

    input_tag = soup.input

    assert input_tag.name == "input"
    assert input_tag["id"] == id
    assert input_tag[Model.In] == model
    assert input_tag["type"] == "time"


def test_time_label():
    id = randstr(5)
    lab = randstr(10)
    model = randstr(5)

    time = wg.Time(model, id=id, label=lab)
    soup = new_soup(time)

    container = soup.div
    label_tag = container.label
    input_tag = container.input

    assert label_tag.name == "label"
    assert label_tag["for"] == id
    assert input_tag.name == "input"
    assert input_tag["id"] == id
    assert input_tag[Model.In] == model
    assert input_tag["type"] == "time"


def test_url():
    id = randstr(5)
    model = randstr(5)
    value = randstr(10)
    url = wg.Url(model, value, id=id)
    soup = new_soup(url)

    input_tag = soup.input

    assert input_tag.name == "input"
    assert input_tag["id"] == id
    assert input_tag[Model.In] == model
    assert input_tag["type"] == "url"


def test_url_label():
    id = randstr(5)
    lab = randstr(10)
    model = randstr(5)
    value = randstr(10)

    url = wg.Url(model, value, id=id, label=lab)
    soup = new_soup(url)

    container = soup.div
    label_tag = container.label
    input_tag = container.input

    assert label_tag.name == "label"
    assert label_tag["for"] == id
    assert input_tag.name == "input"
    assert input_tag["id"] == id
    assert input_tag[Model.In] == model
    assert input_tag["type"] == "url"


def test_textarea():
    id = randstr(5)
    model = randstr(5)
    value = randstr(100)
    textarea = wg.Textarea(model, value, id=id, rows=random.randint(1, 100),
                           cols=random.randint(1, 100))
    soup = new_soup(textarea)

    textarea_tag = soup.textarea

    assert textarea_tag is not None
    assert textarea_tag.name == "textarea"
    assert textarea_tag["id"] == id
    assert textarea_tag[Model.In] == model


def test_textarea_label():
    id = randstr(5)
    lab = randstr(10)
    model = randstr(5)
    value = randstr(100)

    textarea = wg.Textarea(model, value, id=id, rows=random.randint(1, 100),
                           cols=random.randint(1, 100),
                           label=lab)
    soup = new_soup(textarea)

    container = soup.div
    label_tag = container.label
    textarea_tag = container.textarea

    assert label_tag.name == "label"
    assert label_tag["for"] == id
    assert textarea_tag is not None
    assert textarea_tag.name == "textarea"
    assert textarea_tag["id"] == id
    assert textarea_tag[Model.In] == model


def test_form():
    id = randstr(5)
    model = randstr(5)

    form = wg.Form(model, id=id)
    soup = new_soup(form)

    form_tag = soup.form

    assert form_tag is not None
    assert form_tag.name == "form"
    assert form_tag["id"] == id
    assert form_tag[Model.Layout] == model


def test_form_with_widgets():
    id = randstr(5)
    model = randstr(5)

    form = wg.Form(model, id=id)
    form.append(wg.Text(randstr(5), randstr(5)))
    form.append(wg.Url(randstr(5), randstr(5)))
    form.append(wg.Email(randstr(5), randstr(5)))
    form.append(wg.Number(randstr(5), randstr(5)))

    soup = new_soup(form)
    form_tag = soup.form

    assert form_tag is not None
    assert form_tag.name == "form"
    assert form_tag["id"] == id

    input_tags = soup.find_all("input")
    assert len(input_tags) == 4 + 2

    reset = False
    submit = False

    for input_tag in input_tags:
        if input_tag["type"] == "text":
            continue
        elif input_tag["type"] == "url":
            continue
        elif input_tag["type"] == "email":
            continue
        elif input_tag["type"] == "number":
            continue
        elif input_tag["type"] == "submit":
            submit = True
            continue
        elif input_tag["type"] == "reset":
            reset = True
            continue
        else:
            assert False

    assert submit
    assert reset


def test_image_exp():
    id = randstr(5)
    model = randstr(5)

    with pytest.raises(ValueError):
        wg.Image(model, id)

    with pytest.raises(FileNotFoundError):
        wg.Image(model, id, path=randstr(10))


def test_read_image():
    img, fmt = wg.Image.get_img(TEST_IMAGE_PATH)

    assert img is not None
    assert fmt == TEST_IMAGE_FMT


def test_image():
    id = randstr(5)
    alt = randstr(5)
    model = randstr(5)
    image = wg.Image(model, id, path=TEST_IMAGE_PATH, alt=alt)

    soup = new_soup(image)
    img_tag = soup.img

    fp = open(TEST_IMAGE_PATH, "rb")
    img = fp.read()
    fp.close()
    b64_img = base64.b64encode(img).decode("utf-8")

    assert img_tag is not None
    assert img_tag.name == "img"
    assert img_tag["id"] == id
    assert img_tag[Model.Out] == model
    assert img_tag["alt"] == alt
    assert img_tag["src"] == f'data:image/{TEST_IMAGE_FMT};base64, {b64_img}'
