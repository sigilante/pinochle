# Pinochle:  Nock in Python

![](https://d7hftxdivxxvm.cloudfront.net/?height=675&quality=80&resize_to=fill&src=https%3A%2F%2Fartsy-media-uploads.s3.amazonaws.com%2FB3-xVAQfM3480N-sdByhCA%252Fcustom-Custom_Size___A_Friend_in_Need_1903_C.M.Coolidge.jpg&width=1200)

Extends Urbit's [`pynoun`](https://github.com/urbit/tools/blob/master/pkg/pynoun/noun.py) project to a basic Python interpreter.

## Installation

```bash
git clone https://github.com/sigilante/pinochle.git
pip install ./packages/nock
# or from GitHub:
pip install git+https://github.com/sigilante/pinochle.git#subdirectory=packages/pinochle
```

A Jupyter kernel for interactive Nock evaluation.

**Installation:**
```bash
# Install the core library first
pip install ./packages/nock

# Then install the kernel
pip install ./packages/nock_kernel
jupyter kernelspec install ./packages/nock_kernel/kernelspec --user --name=nock
```

## License

This project is licensed under the MIT License - see [the LICENSE file](./LICENSE) for details.
