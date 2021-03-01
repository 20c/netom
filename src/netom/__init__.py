
import ipaddress
import os
from pkg_resources import get_distribution

import confu
from confu import schema
import tmpl

# TODO move out of this namespace
from .models import BgpNeighbor
from .exception import NetomValidationError


__version__ = get_distribution("netom").version


def make_variable_name(value):
    """
    Makes passed value into a variable name.
    """
    value = str(value).translate(str.maketrans(" .:", "___"))
    return value


def ip_version(value):
    """
    Returns version of passed IP address.
    """
    return ipaddress.ip_address(value).version


class Render(object):
    """
    Renders data to defined type.
    """

    def __init__(self, model_version, model_type):
        """
        Create a render object.

        subtype is typically vendor name
        version is the model version to use
        """

        self.version = model_version
        self.type = model_type

        # FIXME use pkg resources
        search_path = os.path.join(os.getcwd(), "src/netom/templates/", self.version, self.type) #, "bgp")
        self.engine = tmpl.get_engine("jinja2")(search_path=search_path)
        self.engine.engine.filters["make_variable_name"] = make_variable_name
        self.engine.engine.filters["ip_version"] = ip_version
        # self.engine.search_path = os.path.dirname(search_path)

    def _render(self, filename, data, fobj):
        #engine.engine.undefined = IgnoreUndefined
        output = self.engine._render(src=filename, env=data)
        fobj.write(output)
        #ctx.tmpl.update(engine=engine)

    def bgp_neighbors(self, data, fobj, validate=True):
        """
        Renders BGP neighbors using `template/{{ typ }}/bgp/neighbors`.
        """

        groups = dict()
        # collate by group
        for each in data["neighbors"]:
            if validate:
                validate_data(BgpNeighbor(), each)
            groups.setdefault(each["peer_group"], []).append(each)

        groups = dict(peer_groups=groups)

        filename = "bgp/neighbors.j2"
        return self._render(filename, groups, fobj)


def validate(model, data, strict=True):
    schema.apply_defaults(model, data)
    success, errors, warnings = schema.validate(model, data, log=print)
    # TODO make this throw actual errors, etc
    return True

    if errors:
        raise NetomValidationError("validation has errors")

    if strict and warnings:
        raise NetomValidationError("validation has warnings")

    return True
