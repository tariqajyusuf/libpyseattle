# Python-based Seattle Data Library

A data framework for accessing City of Seattle data programatically. This
primarily focuses on accessing utility and other individual data. This is not
officially endorsed by the City of Seattle.

# Current Features

- Login
  - Supports web-based authentication and session preservation.
- Seattle City Light
  - Retrieve usage information in kWH.

# Requirements

- Python 3.10+
- [Poetry](https://python-poetry.org)

# Setup Instructions

```py
poetry install
```

# Running

Currently there is just a utility that reads from the Seattle City Light website
and pulls the last 30 days of data. Your username and password is sent directly
to the city website and not stored or logged anywhere.

```py
poetry run python -m libpyseattle
```
