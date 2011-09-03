from nose.tools import eq_

from libravatar import libravatar_url

COMMON_HASH   = 'ce0064bb30c22b618f814c389e7941ce1bfff0659910523192868d2b71632c77'
COMMON_OPENID = 'http://example.com/id'
COMMON_PREFIX_HTTP  = 'http://cdn.libravatar.org/avatar/'
COMMON_PREFIX_HTTPS = 'https://seccdn.libravatar.org/avatar/'

def test_simple_url():
    eq_(libravatar_url(openid = COMMON_OPENID),
        COMMON_PREFIX_HTTP + COMMON_HASH)
    eq_(libravatar_url(openid = COMMON_OPENID, https = True),
        COMMON_PREFIX_HTTPS + COMMON_HASH)
    eq_(libravatar_url(openid = COMMON_OPENID, https = False),
        COMMON_PREFIX_HTTP + COMMON_HASH)

def test_openid_hashing():
    # equivalent URLs
    eq_(libravatar_url(openid = 'http://example.COM/id'),
        COMMON_PREFIX_HTTP + COMMON_HASH)
    eq_(libravatar_url(openid = 'HTTP://example.com/id', https = True),
        COMMON_PREFIX_HTTPS + COMMON_HASH)

    # different URLs
    eq_(libravatar_url(openid = 'https://example.com/id'),
        COMMON_PREFIX_HTTP + '43e813cfff429662436728ef4fb1cc12bcf20414cab78811137f7d718c1ddedb')
    eq_(libravatar_url(openid = 'http://example.com/ID'),
        COMMON_PREFIX_HTTP + 'ad8ce775cc12cba9bb8af26e00f55c473a3fcd3f554595a5ad9dd924a546a448')

def test_other_params():
    eq_(libravatar_url(openid = COMMON_OPENID, default = '/local.png'),
        COMMON_PREFIX_HTTP + COMMON_HASH + '?d=%2Flocal.png')
    eq_(libravatar_url(openid = COMMON_OPENID, size = 150, https = True, default = 'mm'),
        COMMON_PREFIX_HTTPS + COMMON_HASH + '?d=mm&s=150')
