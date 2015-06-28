# -*- coding: utf-8 -*-
from nose.tools import eq_

from libravatar import libravatar_url, parse_user_identity

COMMON_HASH   = 'ce0064bb30c22b618f814c389e7941ce1bfff0659910523192868d2b71632c77'
COMMON_OPENID = 'http://example.com/id'
COMMON_DOMAIN = 'example.com'
COMMON_PREFIX_HTTP  = 'http://cdn.libravatar.org/avatar/'
COMMON_PREFIX_HTTPS = 'https://seccdn.libravatar.org/avatar/'

UTF8_URL = u'http://example.com/François'
UTF8_HASH = '5c323abb04553a28f44490b21effdf8f4a9878d07775c9a3c3f4a9ec9a95ff33'

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

    # UTF-8 in URLs
    eq_(libravatar_url(openid = UTF8_URL), COMMON_PREFIX_HTTP + UTF8_HASH)
    eq_(libravatar_url(openid = UTF8_URL, https = True), COMMON_PREFIX_HTTPS + UTF8_HASH)

def test_other_params():
    eq_(libravatar_url(openid = COMMON_OPENID, default = '/local.png'),
        COMMON_PREFIX_HTTP + COMMON_HASH + '?d=%2Flocal.png')
    eq_(libravatar_url(openid = COMMON_OPENID, size = 150, https = True, default = 'mm'),
        COMMON_PREFIX_HTTPS + COMMON_HASH + '?d=mm&s=150')

def test_user_identity():
    eq_(parse_user_identity(None, COMMON_OPENID),
        (COMMON_HASH, COMMON_DOMAIN))

    eq_(parse_user_identity(None, 'http://example.COM/id'),
        (COMMON_HASH, COMMON_DOMAIN))
    eq_(parse_user_identity(None, '  HTTP://example.com/id  '),
        (COMMON_HASH, COMMON_DOMAIN))
    eq_(parse_user_identity(None, 'http://user:password@Example.com/id'),
        ('e1cf8061371aa00b82c0cf0b9b1140546bc31cd4a15cb8adc84ad01823bdf71e', COMMON_DOMAIN))
    eq_(parse_user_identity(None, 'http://User:Password@Example.com/id'),
        ('50f60bb4c1b47fffdd6e2ce65f8bf37b65a2fb960596fa6789ef7b0044b931a2', COMMON_DOMAIN))
    eq_(parse_user_identity(None, 'http://openid.example.COM/id'),
        ('a108913053c4949f18d9eef7a4a68f27591297cdd7a7e2e375702aa87b6d3c05', 'openid.example.com'))
