# Pinochle

Python implementation of the Nock 4K Combinator Calculus with a Jupyter kernel for interactive evaluation.  Extends Urbit's [`pynoun`](https://github.com/urbit/tools/blob/master/pkg/pynoun/noun.py).

![](https://d7hftxdivxxvm.cloudfront.net/?height=675&quality=80&resize_to=fill&src=https%3A%2F%2Fartsy-media-uploads.s3.amazonaws.com%2FB3-xVAQfM3480N-sdByhCA%252Fcustom-Custom_Size___A_Friend_in_Need_1903_C.M.Coolidge.jpg&width=1200)

This project consists of two packages:

1. `pinochle`: Core library implementing Nock 4K evaluation.
2. `nock-kernel`: Jupyter kernel for interactive Nock 4K evaluation.

## Pinochle - Core Library

Library supplying a Python implementation of the Nock 4K Combinator Calculus.

### Installation

```bash
git clone https://github.com/sigilante/pinochle.git
pip install ./packages/nock
# or from GitHub:
pip install git+https://github.com/sigilante/pinochle.git#subdirectory=packages/pinochle
```

### Usage

```python
from pinochle import nock, parse_noun

# Parse and evaluate Nock expressions
result = nock(42, parse_noun("[0 1]"))
print(result)  # 42

# Increment
result = nock(41, parse_noun("[4 0 1]"))
print(result)  # 42
```

See the [README](packages/pinochle/README.md) for further details.

## Nock Kernel

A Jupyter kernel for interactive Nock evaluation.

### Installation

```bash
# Install the core library first
pip install pinochle

# Then install the kernel
pip install nock-kernel
nock-kernel-install
```

### Usage

Start Jupyter:

```bash
jupyter notebook
```

Create a new notebook and select "Nock 4K" as the kernel.

```
:subject [1 2 3 4 5]
```

```
:formula [4 4 4 4 0 6]
```

See the [README](packages/nock_kernel/README.md) for further details and the [TUTORIAL](packages/nock_kernel/TUTORIAL.ipynb) for more examples of use.

## Examples

* [~timluc-miptev (2025), “Nock for Everyday Coders”, _Urbit Systems Technical Journal_ II:1, pp. 1–45](https://mybinder.org/v2/gh/Urbit-Systems-Technical-Journal/nocksite/master?urlpath=[…]content/examples/timluc-miptev--nock-for-everyday-coders.ipynb).

## License

This project is licensed under the MIT License - see [LICENSE](./LICENSE) for details.

## Versions

- 1.0.0 - Initial release of Pinochle with Nock 4K core library and Jupyter kernel.
- 1.1.0 - Added variable definition and substitution in Nock kernel.
- 1.2.0 - Improved variable substitution and `:show` precision in Nock kernel.
