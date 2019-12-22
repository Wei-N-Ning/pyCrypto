# Learn Blockchains by Building One

source: <https://hackernoon.com/learn-blockchains-by-building-one-117428612f46>

## Running and testing

this sub project is built by poetry.

### New project initialization

`poetry new --src blockchain` creates the project skeleton and puts
blockchain package in the toplevel `src` directory

**TODO: find out how to locallly installed 3rd party packages (instead
of adding package to the containing virtualenv)**

Beware that `*.egg-info` directories are not added to gitignore by
default; I need to do that manually

### Testing

`pytest`

pytest package dependency is added in the toml file as part of the
initial skeleton

### Running

`poetry run main`

```text
[tool.poetry.scripts]
main = "blockchain.app:main"
```

main target must be defined in the project toml file; `app:main`
points to the main() function inside app module; no need to use
`__main__.py` here

### Use relative import

app.py uses relative import;
