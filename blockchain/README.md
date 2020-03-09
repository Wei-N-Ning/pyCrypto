# Learn Blockchains by Building One

source: <https://hackernoon.com/learn-blockchains-by-building-one-117428612f46>

## Running and testing

this sub project is built by poetry (and also uses pyenv's global interpreter
version control).

pyenv: <https://github.com/pyenv/pyenv-installer>

### New project initialization

`poetry new --src blockchain` creates the project skeleton and puts
blockchain package in the toplevel `src` directory

**TODO: find out how to locallly installed 3rd party packages (instead
of adding package to the containing virtualenv)**

Beware that `*.egg-info` directories are not added to gitignore by
default; I need to do that manually

**UPDATE**: Ubuntu18 setup

.venv works on U18 - I need to:

- read <https://python-poetry.org/docs/configuration/#available-settings> and deactivate virtualenv; remove virtualenv activation from bash-rc
- read <https://github.com/pyenv/pyenv#installation> and properly install pyenv; remove any custom python exec symbolic links and clean up \$PATH
- make sure pyenv init pyenv virtual-env init is in the rc file;
- run `pyenv install <python version>`, then pyenv global to choose this version
- now running `python` in the poetry project dir will see the expect version of python interpreter
- run `poetry config` (see link 1) to enable environment isolation, e.g.
  `poetry config virtualenvs.in-project true`
  NOTE: if I forgot to this step and the dependencies were installed in the global dir I have to 
        use `poetry config --list` to find the global dir and **DELETE ITS CONTENTS** in order to force
        poetry respect the local `.venv` strategy
- poetry install works now; .venv directory is created
- make sure .venv is add in .gitignore

after changing version in the toml file, I need to run `poetry update` to download all the new packages;

to run pytest using the isolated environment, run `poetry run pytest`

TODO: how to get rid of the "deprecation" warnings thrown frmo pytest ????

### Testing

`pytest` to run the unit tests;

pytest package dependency is added in the toml file as part of the
initial skeleton

use postman to test the endpoint; use `-p <port>` to run multiple "nodes" to test the consensus algorithm

### Running

```bash
poetry run main
poetry run main -p 6000
poetry run main -a 0.0.0.0 -p 24325
```

Note: **poetry does not use -- to separate target from its arguments**

```text
[tool.poetry.scripts]
main = "blockchain.app:main"
```

main target must be defined in the project toml file; `app:main`
points to the main() function inside app module; no need to use
`__main__.py` here

### Use relative import

app.py uses relative import;
