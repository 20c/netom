import ipaddress

__all__ = [
    "make_variable_name",
    "render_template",
    "ip_address",
    "ip_interface",
    "ip_version",
]

from jinja2 import pass_context


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
