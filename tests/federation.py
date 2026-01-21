import random

from libravatar import (
    normalized_target,
    sanitize_target,
    service_name,
    srv_hostname,
)


def test_sanitize_target() -> None:
    # normal responses
    assert sanitize_target(("example.com", 80)) == ("example.com", 80)
    assert sanitize_target(("A.example.com", 443)) == ("A.example.com", 443)
    assert sanitize_target(("avatars.example.org", 8080)) == (
        "avatars.example.org",
        8080,
    )

    # invalid responses
    assert sanitize_target(("example.com", "abc")) == (None, None)
    assert sanitize_target(("example.com", None)) == (None, None)
    assert sanitize_target(("example.com", 80000)) == (None, None)
    assert sanitize_target(("example.com$", 80)) == (None, None)
    assert sanitize_target(("example.com/", 80)) == (None, None)
    assert sanitize_target((None, 80)) == (None, None)


def test_srv_hostname() -> None:
    # missing params
    assert srv_hostname([]) == (None, None)
    assert srv_hostname([{"target": None, "port": None}]) == (None, None)

    # no need to look at weights
    assert srv_hostname([{"target": "example.com", "port": 81}]) == (
        "example.com",
        81,
    )
    assert srv_hostname(
        [
            {
                "target": "a.example.org",
                "port": 81,
                "priority": 0,
                "weight": 0,
            },
            {
                "target": "b.example.org",
                "port": 82,
                "priority": 10,
                "weight": 0,
            },
        ]
    ) == ("a.example.org", 81)
    assert srv_hostname(
        [
            {
                "target": "a.example.org",
                "port": 81,
                "priority": 10,
                "weight": 0,
            },
            {
                "target": "b.example.org",
                "port": 82,
                "priority": 1,
                "weight": 0,
            },
            {
                "target": "c.example.org",
                "port": 83,
                "priority": 10,
                "weight": 0,
            },
            {
                "target": "d.example.org",
                "port": 84,
                "priority": 10,
                "weight": 0,
            },
        ]
    ) == ("b.example.org", 82)

    # The following ones are randomly selected which is why we
    # have to initialize the random number to a canned value
    random.seed(42)

    assert srv_hostname(
        [
            {
                "target": "a.example.org",
                "port": 81,
                "priority": 10,
                "weight": 1,
            },
            {
                "target": "b.example.org",
                "port": 82,
                "priority": 10,
                "weight": 5,
            },
            {
                "target": "c.example.org",
                "port": 83,
                "priority": 10,
                "weight": 10,
            },
            {
                "target": "d.example.org",
                "port": 84,
                "priority": 10,
                "weight": 50,
            },
            {
                "target": "e.example.org",
                "port": 85,
                "priority": 10,
                "weight": 0,
            },
        ]
    ) == ("c.example.org", 83)

    assert srv_hostname(
        [
            {
                "target": "a.example.org",
                "port": 81,
                "priority": 10,
                "weight": 40,
            },
            {
                "target": "b.example.org",
                "port": 82,
                "priority": 10,
                "weight": 0,
            },
            {
                "target": "c.example.org",
                "port": 83,
                "priority": 10,
                "weight": 0,
            },
            {
                "target": "e.example.org",
                "port": 85,
                "priority": 10,
                "weight": 0,
            },
        ]
    ) == ("a.example.org", 81)

    assert srv_hostname(
        [
            {
                "target": "a.example.org",
                "port": 81,
                "priority": 10,
                "weight": 1,
            },
            {
                "target": "b.example.org",
                "port": 82,
                "priority": 10,
                "weight": 0,
            },
            {
                "target": "c.example.org",
                "port": 83,
                "priority": 20,
                "weight": 0,
            },
            {
                "target": "e.example.org",
                "port": 85,
                "priority": 20,
                "weight": 0,
            },
        ]
    ) == ("a.example.org", 81)

    assert srv_hostname(
        [
            {
                "target": "a.example.org",
                "port": 81,
                "priority": 10,
                "weight": 0,
            },
            {
                "target": "b.example.org",
                "port": 82,
                "priority": 10,
                "weight": 0,
            },
            {
                "target": "c.example.org",
                "port": 83,
                "priority": 10,
                "weight": 10,
            },
            {
                "target": "e.example.org",
                "port": 85,
                "priority": 20,
                "weight": 0,
            },
        ]
    ) == ("c.example.org", 83)

    assert srv_hostname(
        [
            {
                "target": "a.example.org",
                "port": 81,
                "priority": 10,
                "weight": 1,
            },
            {
                "target": "b.example.org",
                "port": 82,
                "priority": 10,
                "weight": 5,
            },
            {
                "target": "c.example.org",
                "port": 83,
                "priority": 10,
                "weight": 10,
            },
            {
                "target": "d.example.org",
                "port": 84,
                "priority": 10,
                "weight": 30,
            },
            {
                "target": "e.example.org",
                "port": 85,
                "priority": 10,
                "weight": 50,
            },
            {
                "target": "f.example.org",
                "port": 86,
                "priority": 20,
                "weight": 0,
            },
        ]
    ) == ("d.example.org", 84)


def test_service_name() -> None:
    assert service_name(None, False) is None
    assert service_name("example.com", False) == "_avatars._tcp.example.com"
    assert service_name("example.org", True) == "_avatars-sec._tcp.example.org"
    assert (
        service_name("example.co.nz", False) == "_avatars._tcp.example.co.nz"
    )


def test_normalized_target() -> None:
    # missing params
    assert (
        normalized_target(
            [{"target": "avatars.example.com", "port": None}], False
        )
        is None
    )
    assert normalized_target([{"target": None, "port": 80}], False) is None
    assert normalized_target([{"target": None, "port": None}], True) is None

    # normal cases
    assert (
        normalized_target([{"target": "example.com", "port": 80}], False)
        == "example.com"
    )
    assert (
        normalized_target([{"target": "example.org", "port": 443}], True)
        == "example.org"
    )
    assert (
        normalized_target([{"target": "example.com", "port": 8080}], False)
        == "example.com:8080"
    )
    assert (
        normalized_target([{"target": "example.com", "port": 3000}], True)
        == "example.com:3000"
    )

    # weird but valid cases
    assert (
        normalized_target([{"target": "example.com", "port": 80}], True)
        == "example.com:80"
    )
    assert (
        normalized_target([{"target": "example.org", "port": 443}], False)
        == "example.org:443"
    )
