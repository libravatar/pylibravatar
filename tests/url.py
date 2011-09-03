from nose.tools import eq_

from libravatar import libravatar_url

COMMON_HASH  = 'a60fc0828e808b9a6a9d50f1792240c8'
COMMON_EMAIL = 'whatever@wherever.whichever'
COMMON_PREFIX_HTTP  = 'http://cdn.libravatar.org/avatar/'
COMMON_PREFIX_HTTPS = 'https://seccdn.libravatar.org/avatar/'

def test_simple_url():
    eq_(libravatar_url(email = COMMON_EMAIL),
        COMMON_PREFIX_HTTP + COMMON_HASH)
    eq_(libravatar_url(email = COMMON_EMAIL, https = True),
        COMMON_PREFIX_HTTPS + COMMON_HASH)
    eq_(libravatar_url(email = COMMON_EMAIL, https = False),
        COMMON_PREFIX_HTTP + COMMON_HASH)

def test_email_hashing():
    eq_(libravatar_url(email = 'WHATEVER@wherever.whichever'),
        COMMON_PREFIX_HTTP + COMMON_HASH)
    eq_(libravatar_url(email = 'Whatever@Wherever.whichever'),
        COMMON_PREFIX_HTTP + COMMON_HASH)
    eq_(libravatar_url(email = ' Whatever@Wherever.whichever   '),
        COMMON_PREFIX_HTTP + COMMON_HASH)

def test_default_param():
    # relative URL
    eq_(libravatar_url(email = COMMON_EMAIL, default = '/local.png'),
        COMMON_PREFIX_HTTP + COMMON_HASH + '?d=%2Flocal.png')

    # absolute URL
    eq_(libravatar_url(email = COMMON_EMAIL, default = 'http://example.com/My Image.jpg'),
        COMMON_PREFIX_HTTP + COMMON_HASH + '?d=http%3A%2F%2Fexample.com%2FMy+Image.jpg')

    # built-in "special" values
    for special in ['identicon', 'mm', 'monsterid', 'retro', 'wavatar']:
        eq_(libravatar_url(email = COMMON_EMAIL, default = special),
            COMMON_PREFIX_HTTP + COMMON_HASH + '?d=%s' % special)
        eq_(libravatar_url(email = COMMON_EMAIL, default = special, https = True),
            COMMON_PREFIX_HTTPS + COMMON_HASH + '?d=%s' % special)

def test_size_param():
    # missing size
    eq_(libravatar_url(email = COMMON_EMAIL, size = 0),
        COMMON_PREFIX_HTTP + COMMON_HASH)
    eq_(libravatar_url(email = COMMON_EMAIL, size = None),
        COMMON_PREFIX_HTTP + COMMON_HASH)

    # normal sizes
    for i in [1, 20, 80, 120, 512]:
        eq_(libravatar_url(email = COMMON_EMAIL, size = i),
            COMMON_PREFIX_HTTP + COMMON_HASH + '?s=%s' % i)
        eq_(libravatar_url(email = COMMON_EMAIL, size = i, https = True, default = 'mm'),
            COMMON_PREFIX_HTTPS + COMMON_HASH + '?d=mm&s=%s' % i)

    # out of bounds
    eq_(libravatar_url(email = COMMON_EMAIL, size = 1024),
        COMMON_PREFIX_HTTP + COMMON_HASH + '?s=%s' % 512)
    eq_(libravatar_url(email = COMMON_EMAIL, size = -45),
        COMMON_PREFIX_HTTP + COMMON_HASH + '?s=%s' % 1)
