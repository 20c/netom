import ipaddress

__all__ = ["make_variable_name", "ip_address", "ip_interface", "ip_version"]


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

