# Kaitai Struct Engine for Python

Kaitai Struct Engine is a REST API web service, providing virtual machine which allows to:

* load Kaitai Struct specification (in .ksy form), compiling it into target language (in this case - Python) and importing into the engine
* load data files that are supposed to be parsed according to the spec
* run the compiled parser on provided data files
* explore the parsed data in a tree-like manner

This repository contains a Python implementation of the engine. It conforms to the [Kaitai Struct Engine OpenAPI standard](https://github.com/kaitai-io/kaitai_struct_engine_openapi).

It's not supposed to be used directly by end users, but rather visualizers can attach to it and provide a user-friendly interface, thus decoupling UI (in the visualizer) and parsing logic (in the engine).

## Developer workflow

```sh
# Set up Python venv (once after checkout)
python3 -m venv env

# Activate Python venv (every time in a new shell)
. env/bin/activate

# Restore dependencies and install package in a developer-friendly way (once after checkout)
python3 -m pip install -e ./

# Run server
python3 -m kaitai_struct_python_engine

# Restore dependencies + `[tests]` suffix allows to install optional dependencies for running tests
python3 -m pip install -e ./[tests]

# Run tests
pytest
```
