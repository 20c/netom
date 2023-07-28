import ipaddress
import re
from ipaddress import IPv4Address
from jinja2 import pass_context


r_ip_nn = re.compile("[\d.]{7,15}/\d{1,2}")

__all__ = [
    "address_to_mask",
    "address_to_wildcard",
    "ip_address",
    "ip_interface",
    "ip_to_ipv4",
    "ip_version",
    "line_to_mask",
    "line_to_wildcard",
    "make_variable_name",
    "render_template",
]


@pass_context
def render_template(context, value):
    """
    Renders a template from the value.

    Does not get local variables.
    """
    template = context.eval_ctx.environment.from_string(value)
    #    print(f"parent {context.parent}")
    #    print(f"ENV {context.get_all()['self_id']}")
    #    print(f"self-id {context.get('self_id')}")
    result = template.render(**context)

    # not sure we need this
    #    if context.eval_ctx.autoescape:
    #        result = Markup(result)

    return result


def make_variable_name(value):
    """
    Makes passed value into a variable name.
    """
    value = str(value).translate(str.maketrans(" .:", "___"))
    return value


def ip_address(value):
    """
    Returns address of passed IP interface.
    """
    return ipaddress.ip_interface(value).ip


# XXX use this
def ip_interface(value):
    """
    Returns ip_interface of passed value.
    """
    return ipaddress.ip_interface(value)


# XXX when was interface added?
def ip_version(value):
    """
    Returns version of passed IP address.
    """
    return ipaddress.ip_interface(value).version


def address_to_mask(addr):
    """
    Transform A.B.C.D/nn into A.B.C.D M.M.M.M subnet mask format.
    """
    ipaddr4 = ipaddress.ip_interface(addr)
    return f"{ipaddr4.ip} {ipaddr4.netmask}"


def address_to_wildcard(addr):
    """
    Transform A.B.C.D/nn into A.B.C.D W.W.W.W subnet wildcard format.

    credit for the mask shenanigans to George Shuklin
    https://medium.com/opsops/wildcard-masks-operations-in-python-16acf1c35683
    """
    ipnet4 = ipaddress.ip_network(addr)
    wildcard = str(IPv4Address(int(IPv4Address(ipnet4.netmask))^(2**32-1)))
    return f"{ipnet4.network_address} {wildcard}"


def line_to_mask(line):
    """
    Search for any IPv4/nn tokens in the `line` argument and transform them into mask format.
    E.g. `permit ip 10.0.0.0/8` any -> `permit ip 10.0.0.0 255.0.0.0 any`
    """
    tokens = line.split()
    return " ".join([address_to_mask(token) if r_ip_nn.match(token) else token for token in tokens])


def line_to_wildcard(line):
    """
    Search for any IPv4/nn tokens in the `line` argument and transform them into wildcard format.
    E.g. `permit ip 10.0.0.0/8` any -> `permit ip 10.0.0.0 0.255.255.255 any`
    """
    tokens = line.split()
    return " ".join([address_to_wildcard(token) if r_ip_nn.match(token) else token for token in tokens])

def ip_to_ipv4(line):
    """
    Replace token "ip" with "ipv4" to satisfy IOS-XR syntax.
    """
    tokens = line.split()
    return " ".join(["ipv4" if token == "ip" else token for token in tokens])

