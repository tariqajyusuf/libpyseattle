# Seattle City Light Integration for Home Assistant

A Selenium-powered integration with Home Assistant that connects to your Seattle
City Light usage history. This is not an official Seattle City Light
integration.

# Requirements

* Python 3.10+

# Setup Instructions

```py
python -m venv .venv
.venv/Scripts/activate
pip install -r requirements.txt
```

# Running

Currently there is just a utility that reads from the Seattle City Light website
and pulls the last 30 days of data. Your username and password is sent directly
to the city website and not stored or logged anywhere.

```py
python -m main
```