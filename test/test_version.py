import pytest
from mymodule.version import VERSION, get_version

@pytest.mark.parametrize("style,expected", [
    ('branch', '{}.{}'.format(*VERSION)),
    ('short', '{}.{}.{}{[0]}'.format(*VERSION)),
    ('normal', '{}.{}.{} pre-{}'.format(*VERSION)),
    ('verbose', '{}.{}.{} pre-{}'.format(*VERSION)),
    ('all', {'branch': '{}.{}'.format(*VERSION),
             'normal': '{}.{}.{} pre-{}'.format(*VERSION),
             'short': '{}.{}.{}{[0]}'.format(*VERSION),
             'verbose': '{}.{}.{} pre-{}'.format(*VERSION),
             }),
])
def test_version(style, expected):
    assert get_version(style) == expected
