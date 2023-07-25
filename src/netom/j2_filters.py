import ipaddress
from ipaddress import IPv4Address

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
