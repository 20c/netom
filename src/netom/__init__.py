import io
import ipaddress
import os

import confu
import tmpl
from confu import schema
from pkg_resources import get_distribution

from . import filters
from .exception import NetomValidationError

# TODO move out of this namespace
from .models import BgpNeighbor

__version__ = get_distribution("netom").version


class Render:
    """
    Renders data to defined type.
    """

    def __init__(self, model_version, model_type, search_path=None):
        """
        Create a render object.

        model_version is the data model version (currently at "netom0")

        subtype is typically vendor name
        """

        self.version = model_version
        self.type = model_type

        if not search_path:
            # FIXME use pkg resources
            search_path = os.path.join(
                os.getcwd(), "src/netom/templates/", self.version, self.type
            )  # , "bgp")
        self.set_search_path(search_path)

    def set_search_path(self, search_path):
        self.engine = tmpl.get_engine("jinja2")(search_path=search_path)
        # self.engine.search_path = os.path.dirname(search_path)

        for name in filters.__all__:
            self.engine.engine.filters[name] = getattr(filters, name)

    def _render(self, filename, data, fobj):
        # engine.engine.undefined = IgnoreUndefined
        output = self.engine._render(src=filename, env=data)
        fobj.write(output)
        # ctx.tmpl.update(engine=engine)

    def render_string(self, filename, data):
        with io.StringIO() as fobj:
            self._render(filename, data, fobj)
            return fobj.getvalue()

    def bgp_neighbors(self, data, fobj, validate=True):
        """
        Renders BGP neighbors using `template/{{ typ }}/bgp/neighbors`.
        """

        groups = dict()
        # collate by group
        for each in data["neighbors"]:
            if validate:
                validate(BgpNeighbor(), each)
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
