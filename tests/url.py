from nose.tools import eq_

from libravatar import libravatar_url, compose_avatar_url, parse_user_identity, parse_options

COMMON_HASH  = 'a60fc0828e808b9a6a9d50f1792240c8'
COMMON_EMAIL = 'whatever@wherever.whichever'
COMMON_DOMAIN = 'wherever.whichever'
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

def test_url_composition():
    eq_(compose_avatar_url('', '', '', False),
        COMMON_PREFIX_HTTP)
    eq_(compose_avatar_url(None, None, None, True),
        COMMON_PREFIX_HTTPS)
    eq_(compose_avatar_url('', 'deadbeef', '', False),
        COMMON_PREFIX_HTTP + 'deadbeef')
    eq_(compose_avatar_url('avatar.example.com', 'deadbeef', '', False),
        'http://avatar.example.com/avatar/deadbeef')
    eq_(compose_avatar_url('avatar.example.com', 'deadbeef', '?s=24', True),
        'https://avatar.example.com/avatar/deadbeef?s=24')
    eq_(compose_avatar_url(None, '12345678901234567890123456789012', '?d=404', True),
        COMMON_PREFIX_HTTPS + '12345678901234567890123456789012?d=404')

def test_user_identity():
    eq_(parse_user_identity(None, None),
        (None, None))
    eq_(parse_user_identity(COMMON_EMAIL, None),
        (COMMON_HASH, COMMON_DOMAIN))
    eq_(parse_user_identity(COMMON_EMAIL, 'http://example.com/ID'),
        (COMMON_HASH, COMMON_DOMAIN))

    eq_(parse_user_identity('WHATEVER@wherever.whichever', None),
        (COMMON_HASH, COMMON_DOMAIN))
    eq_(parse_user_identity('Whatever@@Wherever.whichever', None),
        ('63a836cc2f35d9f13d9e9aca3e5f1ea0', COMMON_DOMAIN))
    eq_(parse_user_identity(' Whatever@Wherever.whichever   ', None),
        (COMMON_HASH, COMMON_DOMAIN))

def test_options():
    eq_(parse_options(None, None), '')
    eq_(parse_options('', 0), '')
    eq_(parse_options('404', 80), '?d=404&s=80')

    # default param
    eq_(parse_options('mm', None), '?d=mm')
    eq_(parse_options(404, None), '?d=404')
    eq_(parse_options('http://example.com', None), '?d=http%3A%2F%2Fexample.com')
    eq_(parse_options('http://example.com/An Example Page', None), '?d=http%3A%2F%2Fexample.com%2FAn+Example+Page')
    eq_(parse_options('http://example.com/A-Title', None), '?d=http%3A%2F%2Fexample.com%2FA-Title')
    eq_(parse_options('http://example.com/A+B#C?D=E&F=G', None), '?d=http%3A%2F%2Fexample.com%2FA%2BB%23C%3FD%3DE%26F%3DG')

    # size param
    eq_(parse_options(None, -1), '?s=1')
    eq_(parse_options(None, 1), '?s=1')
    eq_(parse_options(None, '79'), '?s=79')
    eq_(parse_options(None, 512), '?s=512')
    eq_(parse_options(None, 1000000), '?s=512')
    eq_(parse_options(None, 'ABC'), '')
    eq_(parse_options(None, ' '), '')
