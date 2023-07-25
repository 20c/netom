
from netom.j2_filters import address_to_mask, address_to_wildcard, line_to_mask, line_to_wildcard
import pytest


def test_address_to_mask():
    assert address_to_mask("192.168.0.1/4") == "192.168.0.1 240.0.0.0"
    assert address_to_mask("192.168.0.1/8") == "192.168.0.1 255.0.0.0"
    assert address_to_mask("192.168.0.1/9") == "192.168.0.1 255.128.0.0"
    assert address_to_mask("192.168.0.1/16") == "192.168.0.1 255.255.0.0"
    assert address_to_mask("192.168.0.1/24") == "192.168.0.1 255.255.255.0"
    assert address_to_mask("192.168.0.1/25") == "192.168.0.1 255.255.255.128"
    assert address_to_mask("192.168.0.1/30") == "192.168.0.1 255.255.255.252"
    assert address_to_mask("192.168.0.1/31") == "192.168.0.1 255.255.255.254"
    assert address_to_mask("192.168.0.1/32") == "192.168.0.1 255.255.255.255"

def test_address_to_wildcard():
    assert address_to_wildcard("192.0.0.0/4") == "192.0.0.0 15.255.255.255"
    assert address_to_wildcard("192.0.0.0/8") == "192.0.0.0 0.255.255.255"
    assert address_to_wildcard("192.0.0.0/9") == "192.0.0.0 0.127.255.255"
    assert address_to_wildcard("192.168.0.0/16") == "192.168.0.0 0.0.255.255"
    assert address_to_wildcard("192.168.0.0/24") == "192.168.0.0 0.0.0.255"
    assert address_to_wildcard("192.168.0.0/25") == "192.168.0.0 0.0.0.127"
    assert address_to_wildcard("192.168.0.0/30") == "192.168.0.0 0.0.0.3"
    assert address_to_wildcard("192.168.0.0/31") == "192.168.0.0 0.0.0.1"
    assert address_to_wildcard("192.168.0.0/32") == "192.168.0.0 0.0.0.0"

def test_line_to_mask():
    assert line_to_mask("ip route 192.168.0.0/4 198.51.100.1")  == "ip route 192.168.0.0 240.0.0.0 198.51.100.1"
    assert line_to_mask("ip route 192.168.0.0/8 198.51.100.1")  == "ip route 192.168.0.0 255.0.0.0 198.51.100.1"
    assert line_to_mask("ip route 192.168.0.0/9 198.51.100.1")  == "ip route 192.168.0.0 255.128.0.0 198.51.100.1"
    assert line_to_mask("ip route 192.168.0.0/16 198.51.100.1") == "ip route 192.168.0.0 255.255.0.0 198.51.100.1"
    assert line_to_mask("ip route 192.168.0.0/24 198.51.100.1") == "ip route 192.168.0.0 255.255.255.0 198.51.100.1"
    assert line_to_mask("ip route 192.168.0.0/25 198.51.100.1") == "ip route 192.168.0.0 255.255.255.128 198.51.100.1"
    assert line_to_mask("ip route 192.168.0.0/30 198.51.100.1") == "ip route 192.168.0.0 255.255.255.252 198.51.100.1"
    assert line_to_mask("ip route 192.168.0.0/31 198.51.100.1") == "ip route 192.168.0.0 255.255.255.254 198.51.100.1"
    assert line_to_mask("ip route 192.168.0.0/32 198.51.100.1") == "ip route 192.168.0.0 255.255.255.255 198.51.100.1"

def test_line_to_wildcard():
    assert line_to_wildcard("permit tcp 192.0.0.0/4 any eq 22")    == "permit tcp 192.0.0.0 15.255.255.255 any eq 22"
    assert line_to_wildcard("permit tcp 192.0.0.0/8 any eq 22")    == "permit tcp 192.0.0.0 0.255.255.255 any eq 22"
    assert line_to_wildcard("permit tcp 192.0.0.0/9 any eq 22")    == "permit tcp 192.0.0.0 0.127.255.255 any eq 22"
    assert line_to_wildcard("permit tcp 192.168.0.0/16 any eq 22") == "permit tcp 192.168.0.0 0.0.255.255 any eq 22"
    assert line_to_wildcard("permit tcp 192.168.0.0/24 any eq 22") == "permit tcp 192.168.0.0 0.0.0.255 any eq 22"
    assert line_to_wildcard("permit tcp 192.168.0.0/25 any eq 22") == "permit tcp 192.168.0.0 0.0.0.127 any eq 22"
    assert line_to_wildcard("permit tcp 192.168.0.0/30 any eq 22") == "permit tcp 192.168.0.0 0.0.0.3 any eq 22"
    assert line_to_wildcard("permit tcp 192.168.0.0/31 any eq 22") == "permit tcp 192.168.0.0 0.0.0.1 any eq 22"
    assert line_to_wildcard("permit tcp 192.168.0.0/32 any eq 22") == "permit tcp 192.168.0.0 0.0.0.0 any eq 22"
