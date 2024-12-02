import pytest
import hashlib

from chord import ChordNode

def test_can_make_chordnode():
    n = ChordNode("1.2.3.4", 5)

    assert n is not None
    assert n.ip == "1.2.3.4"
    assert n.port == 5

def test_can_make_key():
    ip = "1.2.3.4"
    port = 5
    n = ChordNode(ip, port)

    key = f"{ip}:{port}"
    expected = int(hashlib.sha1(key.encode()).hexdigest(), 16) % (2**16)

    assert expected == n.node_id

def test_can_create_ring():
    n = ChordNode("1.2.3.4", 5)

    n.create()

    assert n.successor is not None
    assert n.successor == n

