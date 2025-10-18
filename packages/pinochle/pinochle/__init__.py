"""
Pinochle - Python implementation of the Nock 4K Combinator Calculus
"""

from .nock import (
    nock,
    to_noun,
    isatom,
    iscell,
    head,
    tail,
    wut,
    lus,
    tis,
    fas,
    hax,
    tru,
    bad,
)
from .noun import (
    Cell,
    deep,
    parse,
    noun,
    pretty,
    mug,
    jam,
    cue,
)

# Convenience alias
parse_noun = parse

__version__ = '1.0.0'
__all__ = [
    'nock',
    'to_noun',
    'isatom',
    'iscell', 
    'head',
    'tail',
    'wut',
    'lus',
    'tis',
    'fas',
    'hax',
    'tru',
    'bad',
    'Cell',
    'deep',
    'parse',
    'parse_noun',
    'noun',
    'pretty',
    'mug',
    'jam',
    'cue',
]