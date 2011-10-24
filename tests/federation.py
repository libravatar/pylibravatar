from nose.tools import eq_
import random

from libravatar import sanitize_target, srv_hostname, service_name

def test_sanitize_target():
    # normal responses
    eq_(sanitize_target(('example.com', 80)), ('example.com', 80))
    eq_(sanitize_target(('A.example.com', 443)), ('A.example.com', 443))
    eq_(sanitize_target(('avatars.example.org', 8080)), ('avatars.example.org', 8080))

    # invalid responses
    eq_(sanitize_target(('example.com', 'abc')), (None, None))
    eq_(sanitize_target(('example.com', None)), (None, None))
    eq_(sanitize_target(('example.com', 80000)), (None, None))
    eq_(sanitize_target(('example.com$', 80)), (None, None))
    eq_(sanitize_target(('example.com/', 80)), (None, None))
    eq_(sanitize_target((None, 80)), (None, None))

def test_srv_hostname():
    # missing params
    eq_(srv_hostname([]), (None, None))
    eq_(srv_hostname([{'target': None, 'port': None}]), (None, None))

    # no need to look at weights
    eq_(srv_hostname([{'target': 'example.com', 'port': 81}]),
        ('example.com', 81))
    eq_(srv_hostname([{'target': 'a.example.org', 'port': 81, 'priority': 0, 'weight': 0},
                      {'target': 'b.example.org', 'port': 82, 'priority': 10, 'weight': 0}]),
        ('a.example.org', 81))
    eq_(srv_hostname([{'target': 'a.example.org', 'port': 81, 'priority': 10, 'weight': 0},
                      {'target': 'b.example.org', 'port': 82, 'priority': 1, 'weight': 0},
                      {'target': 'c.example.org', 'port': 83, 'priority': 10, 'weight': 0},
                      {'target': 'd.example.org', 'port': 84, 'priority': 10, 'weight': 0}]),
        ('b.example.org', 82))

    # The following ones are randomly selected which is why we
    # have to initialize the random number to a canned value
    random.seed(42)

    eq_(srv_hostname([{'target': 'a.example.org', 'port': 81, 'priority': 10, 'weight': 1},
                      {'target': 'b.example.org', 'port': 82, 'priority': 10, 'weight': 5},
                      {'target': 'c.example.org', 'port': 83, 'priority': 10, 'weight': 10},
                      {'target': 'd.example.org', 'port': 84, 'priority': 10, 'weight': 50},
                      {'target': 'e.example.org', 'port': 85, 'priority': 10, 'weight': 0}]),
        ('d.example.org', 84))

    eq_(srv_hostname([{'target': 'a.example.org', 'port': 81, 'priority': 10, 'weight': 40},
                      {'target': 'b.example.org', 'port': 82, 'priority': 10, 'weight': 0},
                      {'target': 'c.example.org', 'port': 83, 'priority': 10, 'weight': 0},
                      {'target': 'e.example.org', 'port': 85, 'priority': 10, 'weight': 0}]),
        ('a.example.org', 81))

    eq_(srv_hostname([{'target': 'a.example.org', 'port': 81, 'priority': 10, 'weight': 1},
                      {'target': 'b.example.org', 'port': 82, 'priority': 10, 'weight': 0},
                      {'target': 'c.example.org', 'port': 83, 'priority': 20, 'weight': 0},
                      {'target': 'e.example.org', 'port': 85, 'priority': 20, 'weight': 0}]),
        ('b.example.org', 82))

    eq_(srv_hostname([{'target': 'a.example.org', 'port': 81, 'priority': 10, 'weight': 0},
                      {'target': 'b.example.org', 'port': 82, 'priority': 10, 'weight': 0},
                      {'target': 'c.example.org', 'port': 83, 'priority': 10, 'weight': 10},
                      {'target': 'e.example.org', 'port': 85, 'priority': 20, 'weight': 0}]),
        ('c.example.org', 83))

    eq_(srv_hostname([{'target': 'a.example.org', 'port': 81, 'priority': 10, 'weight': 1},
                      {'target': 'b.example.org', 'port': 82, 'priority': 10, 'weight': 5},
                      {'target': 'c.example.org', 'port': 83, 'priority': 10, 'weight': 10},
                      {'target': 'd.example.org', 'port': 84, 'priority': 10, 'weight': 30},
                      {'target': 'e.example.org', 'port': 85, 'priority': 10, 'weight': 50},
                      {'target': 'f.example.org', 'port': 86, 'priority': 20, 'weight': 0}]),
        ('e.example.org', 85))

def test_service_name():
    eq_(service_name(None, False), None)
    eq_(service_name('example.com', False), '_avatars._tcp.example.com')
    eq_(service_name('example.org', True), '_avatars-sec._tcp.example.org')
    eq_(service_name('example.co.nz', False), '_avatars._tcp.example.co.nz')
