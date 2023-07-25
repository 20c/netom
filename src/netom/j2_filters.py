import ipaddress
import re
from ipaddress import IPv4Address


r_ip_nn = re.compile("[\d.]{7,15}/\d{1,2}")


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

