
from pkg_resources import get_distribution

import confu
from confu import schema
import tmpl
import os

# TODO move out of this namespace
from .models import BgpNeighbor
from .exception import NetomValidationError


__version__ = get_distribution("netom").version


def make_variable_name(value):
    value = value.translate(str.maketrans(" .", "__"))
    return value


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
        # self.engine.search_path = os.path.dirname(search_path)

    def _render(self, filename, data, fobj):
        #engine.engine.undefined = IgnoreUndefined
        output = self.engine._render(src=filename, env=data)
        fobj.write(output)
        #ctx.tmpl.update(engine=engine)

    def bgp_neighbors(self, data, fobj, validate=True):
#        if validate:
#            validate(BgpNeighbor(), data)

        filename = "bgp/neighbors.j2"
        return self._render(filename, data, fobj)

    def bgp_neighbor(self, data, fobj, validate=True):
        """
        Renders a single BGP neighbor using `template/{{ typ }}/bgp/neighbors`.
        """

        if validate:
            success, errors, warnings = validate(BgpNeighbor(), data)


def validate(model, data, strict=True):
    schema.apply_defaults(model, data)
    success, errors, warnings = schema.validate(model, data, log=print)
    # TODO make this throw actual errors, etc
    if errors:
        raise NetomValidationError("validation has errors")

    if strict and warnings:
        raise NetomValidationError("validation has warnings")

    return True
