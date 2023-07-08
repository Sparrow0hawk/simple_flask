[![Flask CI/CD](https://github.com/Sparrow0hawk/simple_flask/actions/workflows/ci.yaml/badge.svg)](https://github.com/Sparrow0hawk/simple_flask/actions/workflows/ci.yaml)
# Simple Flask

A simple flask application following from the [Flask
Tutorial](https://flask.palletsprojects.com/en/2.3.x/tutorial/) with a couple of
addition/deviations. 

## Basic stack

- Flask
- Flask-Bootstrap for Bootstrap5
- Sqlite3 for database
- Flask WTForms

## Quick Start

To get started you should clone this repository and create a virtual
environment:

```bash
git clone https://github.com/Sparrow0hawk/simple_flask

cd simple_flask

python -m venv venv
```

Activate the virtual environment and install this project and it's dependencies:

```bash
. venv/bin/activate

pip install .

# to install with dev dependencies
pip install .[dev]
```

With the project installed you can run the following command to initialise the
sqlite3 database:

```bash
flask --app simple_flask init-db
```

This will return `Initializing database.` if all is well and from there you can
run the application with the flask development server via:

```bash
flask --app simple_flask run --debug
```

And open it in the browser at [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

## Prerequisites

- Python >=3.9

## Development environment

This repository was created from a [cookie-cutter
template](https://github.com/candidtim/cookiecutter-flask-minimal) that includes
a Makefile with the following commands:

 - `make venv`: creates a virtualenv with dependencies and this application
   installed (latter is installed in [development mode](http://setuptools.readthedocs.io/en/latest/setuptools.html#development-mode))

 - `make run`: runs a development server in debug mode (changes in source code
   are reloaded automatically)

 - `make format`: reformats code

 - `make lint`: runs flake8

 - `make mypy`: runs type checks by mypy

 - `make test`: runs tests (see also: [Testing Flask Applications](https://flask.palletsprojects.com/en/2.1.x/testing/))

 - `make dist`: creates a wheel distribution (will run tests first)

 - `make clean`: removes virtualenv and build artifacts

 - add application dependencies in `pyproject.toml` under `project.dependencies`;
   add development dependencies under `project.optional-dependencies.*`

 - to modify configuration, pass it in environment variables prefixed with
   `FLASK_`; e.g., `FLASK_DEBUG`, etc.;

