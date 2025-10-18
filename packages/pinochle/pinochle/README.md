# Pinochle - Core Library

Python implementation of the Nock 4K Combinator Calculus.

## Components

* `noun.py`:  [`pynoun` from Urbit](https://github.com/urbit/tools/blob/master/pkg/pynoun/noun.py)
* `nock.py`:  Nock tree-walking interpreter

## Installation

```bash
pip install pinochle
```

Or from source:
```bash
git clone https://github.com/sigilante/pinochle.git
cd pinochle/packages/pinochle
pip install .
```

## Usage

```python
from pinochle import nock, parse_noun

# Parse and evaluate Nock expressions
result = nock(42, parse_noun("[0 1]"))
print(result)  # 42

# Increment
result = nock(41, parse_noun("[4 0 1]"))
print(result)  # 42
```

## API Reference

See full documentation in the repository.

## License

MIT License