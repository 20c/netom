import io
import ipaddress
import os

import confu
import tmpl
from confu import schema
from pkg_resources import get_distribution

import netom.filters

from .exception import NetomValidationError

# TODO move out of this namespace
from .models import BgpNeighbor

__version__ = get_distribution("netom").version


from ansible.parsing.dataloader import DataLoader
from ansible.template import Templar


class NetomTemplar(Templar):
    """A custom Templar class which includes additional jinja2 filters."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in netom.filters.__all__:
            self.environment.filters[name] = getattr(netom.filters, name)


class PathLoader(DataLoader):
    def __init__(self, search_path):
        self._search_path = search_path
        super().__init__()

    def path_dwim_relative(self, path):
        raise Exception("die")
        return super().path_dwim_relative(self._search_path, path)


class TemplarEngine:
    """Engine for Ansible's Templar system for lazy vars."""

    def __init__(self, *args, search_path="", **kwargs):
        print(f"INIT searchPath {search_path}")
        self.dataloader = PathLoader(search_path)
        print(f"searchPath2 {self.dataloader._search_path}")

    def _render_str_to_str(self, instr, data):
        # Instantiate Templar with the data loader and variable data
        templar = NetomTemplar(loader=self.dataloader, variables=data)

        print(f"searchPath {self.dataloader._search_path}")
        print(instr)
        # Use the templar object to render the template string
        return templar.template(instr)


class Render:
    """
    Renders data to defined type.
    """

    def __init__(self, model_version, model_type, search_path=None, engine="jinja2", filters=None):
        """
        Create a render object.

        model_version is the data model version (currently at "netom0")

        subtype is typically vendor name
        """

        self.version = model_version
        self.type = model_type
        self.filters = {}
        self._engine_type = engine

        for name in netom.filters.__all__:
            self.filters[name] = getattr(netom.filters, name)

        if filters:
            self.filters.update(filters)

        if not search_path:
            # FIXME use pkg resources
            search_path = os.path.join(
                os.getcwd(), "src/netom/templates/", self.version, self.type
            )  # , "bgp")
        self.set_search_path(search_path)

    def set_search_path(self, search_path):
        self._search_path = search_path

        if self._engine_type == "templar":
            self.engine = TemplarEngine(search_path=search_path)
        else:
            self.engine = tmpl.get_engine(self._engine_type)(search_path=search_path)
            self.engine.engine.filters.update(self.filters)
            self.engine.engine.add_extension('jinja2.ext.loopcontrols')

    def _render(self, filename, data, fobj):
        # engine.engine.undefined = IgnoreUndefined
        output = self.engine._render(src=filename, env=data)
        fobj.write(output)
        # ctx.tmpl.update(engine=engine)

    def render_string(self, filename, data):
        with io.StringIO() as fobj:
            self._render(filename, data, fobj)
            return fobj.getvalue()

    def render_from_string(self, instr: str, data: dict):
        return self.engine._render_str_to_str(instr, data)

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


class TemplarRender(Render):

    def __init__(self, *args, **kwargs):
        kwargs["engine"] = "templar"
        super().__init__(*args, **kwargs)

    def render_string(self, filename, data):
        with open(os.path.join(self._search_path, filename), 'r') as file:
            template_string = file.read()
            return self.render_from_string(template_string, data)

    def render_from_string(self, instr, data):
        return self.engine._render_str_to_str(instr, data)



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
