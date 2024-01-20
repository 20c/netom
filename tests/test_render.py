import netom
from ansible.parsing.dataloader import DataLoader
from ansible.template import Templar
from jinja2 import Environment
from netom.filters import (
    address_to_mask,
)

j2env = Environment()
j2env.filters["address_to_mask"] = address_to_mask


class NetomTemplar(Templar):
    """A custom Templar class which includes additional jinja2 filters."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.environment.filters["address_to_mask"] = address_to_mask


def ansible_render(template_string, variables={}):
    # The DataLoader is used to load and parse YAML or JSON objects
    dataloader = DataLoader()

    # Instantiate Templar with the data loader and variable data
    templar = NetomTemplar(loader=dataloader, variables=variables)

    # Use the templar object to render the template string
    rendered = templar.template(template_string)
    return rendered


filter_data = dict(ip4="10.0.0.1/24")
vars = {
    "hello": "Hello",
    "world": "World",
    "hello_world": "{{ hello }} {{ world }}",
    "ugly_variable_name": "$so%ugly^^",
    "ip4": "192.168.0.1/4",
    "recursed_ip4": "{{ ip4 }}",
}


def test_init():
    assert netom.Render("test", "12")


def test_render(data_dir):
    expected = "Hello World\n"
    print(f"this_dir {data_dir}")
    ip4_mask = "192.168.0.1 240.0.0.0"

    netomr = netom.Render("netom0", "platform", data_dir)
    render_template = netomr.render_from_string

    rendered = netomr.render_string("netom0/platform/hello_world.j2", vars)
    assert rendered == expected
    assert expected == render_template("{{ hello }} {{ world }}\n", vars)
    assert ip4_mask == render_template("{{ ip4 | address_to_mask }}", vars)

    render_template = ansible_render

    assert expected == render_template("{{ hello }} {{ world }}\n", vars)
    assert expected == render_template("{{ hello_world }}\n", vars)
    assert ip4_mask == render_template("{{ ip4 | address_to_mask }}", vars)

    netomr = netom.TemplarRender("netom0", "platform", data_dir)
    render_template = netomr.render_from_string
    assert expected == render_template("{{ hello }} {{ world }}\n", vars)
    assert expected == render_template("{{ hello_world }}\n", vars)
    assert ip4_mask == render_template("{{ ip4 | address_to_mask }}", vars)


def test_ansible():
    render_template = ansible_render
    template_string = "{{ hello }} {{ world }}\n"
    recurvsive = "{{ hello_world }}\n"

    rendered_string = render_template(template_string, vars)
    rendered2 = render_template(recurvsive, vars)
    print(rendered_string)  # Output: Hello World
    assert rendered_string == "Hello World\n"
    assert rendered_string == rendered2
