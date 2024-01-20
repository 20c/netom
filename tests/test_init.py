import os

import netom

filter_data = dict(ip4="10.0.0.1/24")


def test_init():
    assert netom.Render("test", "12")


def test_filters(this_dir):
    expected = """
ip_address 10.0.0.1
ip_interface 10.0.0.1/24
ip_version 4
"""

    robj = netom.Render("netom0", "test-0", os.path.join(this_dir, "templates"))
    output = robj.render_string("filters.j2", filter_data)
    print(output)
    assert expected == output
