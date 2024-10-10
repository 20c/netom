import ipaddress
import re
from ipaddress import IPv4Address

from jinja2 import pass_context

r_ip_nn = re.compile(r"[\d.]{7,15}/\d{1,2}")

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
    "render_template_slug",
]


@pass_context
def render_template_slug(context, value, slug):
    """
    Renders a template from the value.

    Does not get local variables.
    """
    template = context.eval_ctx.environment.from_string(str(value))
    vars = dict(slug=slug)
    # print(f"parent {context.parent}")
    # print(f"VARS {context.vars.items()}")
    # print(f"ENV {context.get_all()}")
    # print(f"slug {context.get('slug')}")
    # print(f"resolve slug {context.resolve('slug')}")
    # print(f"vars slug {context.vars.get('slug')}")
    result = template.render({**context, **vars})

    # not sure we need this
    #    if context.eval_ctx.autoescape:
    #        result = Markup(result)

    return result


@pass_context
def render_template(context, value):
    """
    Renders a template from the value.

    Does not get local variables.
    """
    template = context.eval_ctx.environment.from_string(str(value))
    # print(f"parent {context.parent}")
    # print(f"VARS {context.vars.items()}")
    # print(f"ENV {context.get_all()}")
    # print(f"slug {context.get('slug')}")
    # print(f"resolve slug {context.resolve('slug')}")
    # print(f"vars slug {context.vars.get('slug')}")
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


def ip_interface(value):
    """
    Returns ip_interface of passed IP interface.
    """
    return ipaddress.ip_interface(value)

def ip_prefixlen(addr):
    """
    Returns the prefix length for passed IP interface.
    """
    return ipaddress.ip_interface(addr).prefixlen

def ip_netmask(addr):
    """
    Returns a subnet mask for passed IP interface.
    """
    return ipaddress.ip_interface(addr).netmask

def ip_hostmask(addr):
    """
    Returns a wilcard or hostmask for passed IP interface.

    Example:
    ip_netmask('10.10.10.5/24')
    > 0.0.0.255
    """
    return ipaddress.ip_interface(addr).hostmask

def ip_network(addr):
    """
    Returns a network address for a combination of IP address and subnet mask

    Example:
    ip_network('10.10.10.5/24')
    > 10.10.10.0
    """
    return ipaddress.ip_network(addr).network


def ip_broadcast(addr):
    """
    Returns a broadcast address for a combination of IP address and subnet mask

    Example:
    ip_network('10.10.10.5/24')
    > 10.10.10.255
    """
    return ipaddress.ip_network(addr).broadcast

def ip_network_hosts_size(addr):
    """
    Returns the size of the subnet for a combination of IP address and subnet mask

    Example:
    ip_network_hosts_size('10.10.10.5/24')
    > 253
    """
    return ipaddress.ip_network(addr).size


def ip_network_first(addr):
    """
    Returns the first usable address in network address for a combination of IP address and subnet mask

    Example:
    ip_network('10.10.10.5/24')
    > 10.10.10.1
    """
    net = ipaddress.ip_network(addr)
    return ipaddress.ip_address(net[1]).__str__()


def ip_network_last(addr):
    """
    Returns the last usable address in network address for a combination of IP address and subnet mask

    Example:
    ip_network('10.10.10.5/24')
    > 10.10.10.254
    """
    return ipaddress.ip_address(ipaddress.ip_network(addr)[-2]).__str__()


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
    wildcard = str(IPv4Address(int(IPv4Address(ipnet4.netmask)) ^ (2**32 - 1)))
    return f"{ipnet4.network_address} {wildcard}"


def line_to_mask(line):
    """
    Search for any IPv4/nn tokens in the `line` argument and transform them into mask format.
    E.g. `permit ip 10.0.0.0/8` any -> `permit ip 10.0.0.0 255.0.0.0 any`
    """
    tokens = line.split()
    return " ".join(
        [address_to_mask(token) if r_ip_nn.match(token) else token for token in tokens]
    )


def line_to_wildcard(line):
    """
    Search for any IPv4/nn tokens in the `line` argument and transform them into wildcard format.
    E.g. `permit ip 10.0.0.0/8` any -> `permit ip 10.0.0.0 0.255.255.255 any`
    """
    tokens = line.split()
    return " ".join(
        [
            address_to_wildcard(token) if r_ip_nn.match(token) else token
            for token in tokens
        ]
    )


def ip_to_ipv4(line):
    """
    Replace token "ip" with "ipv4" to satisfy IOS-XR syntax.
    """
    tokens = line.split()
    return " ".join(["ipv4" if token == "ip" else token for token in tokens])
