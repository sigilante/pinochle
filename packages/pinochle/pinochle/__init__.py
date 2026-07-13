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
from . import jets
from .jets import register as register_jet

# Convenience alias
parse_noun = parse

__version__ = '1.3.0'
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
    'jets',
    'register_jet',
]