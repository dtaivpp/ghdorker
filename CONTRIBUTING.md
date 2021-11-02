# Contributing

Hello and welcome! If you are here to contribute thank you for helping!

## Getting Setup

When contributing you will want to Fork the repo and there are a few practices we ask you setup first.

1. Install all the requirements. We have them seperated out into development and working requirements. This just helps us keep them organized so we can keep build tools seperate from dependancies.
```bash
python -m pip install -r requirements.txt
python -m pip install -r requirements_dev.txt
```

2. Setup pre-commit. This is our framework for linting and validating commits before they are ever made. Setup is fairly simple:

```bash
pre-commit install
```

With that precommit will install itself and will test all of your commits before you add them with a commit message.


## Coding Guidelines

Spacing... Well this may be a bit controversial but we use two spaces instead of four. I just persoally like how it looks. If you contribute ensure you are using two spaces (it should be picked up by vscode)

We use pylint to check the validity of all our code. For code to be accepted in it must be above an 8. This generally means good type hints, docstrings, and proper naming conventions.

Pytest is what we use to ensure that it will work as expected after we make changes. If you see missing tests or add functionality please add or update the tests.

Thank you all for contributing and if you have any questions feel free to reach out!

#### Publish to PyPi

More of documentation for me but here is my process before uploading to PyPi
```bash
pylint GHDorker/*.py
pytest
python setup.py sdist bdist_wheel
twine check dist/*
twine upload dist/*
```
