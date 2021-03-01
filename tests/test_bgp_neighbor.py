import pytest
from confu.schema import validate

import netom
from netom import exception
from netom.models import BgpNeighbor

INVALID0 = dict(
    neighbor_address="not an ip",
)


VALID0 = dict(
    neighbor_address="10.0.0.1",
    peer_as=65001,
    peer_group="ixpeers",
    auth_password="s3cr3t",
    local_address="10.0.0.2",
    local_as=63311,
    enabled=True,
    import_policy="peer-in",
    export_policy="peer-out",
)


# FIXME
def no_test_invalid():
    model = BgpNeighbor()
    data = INVALID0

    with pytest.raises(exception.NetomValidationError):
        netom.validate(model, data)


def test_valid():
    model = BgpNeighbor()

    data = VALID0

    netom.validate(model, data)
