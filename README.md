# Chord
implementation of chord

right now, we're thinking we implement chord (in python) and set it up so we 
can run it on mininet, then we run the simulations they describe in the paper 
on that network, and we implement one of the applications they run on top - in
the paper, they describe large-scale distributed combinatorialsearch, so we 
could write a password cracking program that runs distributed on the chord 
network.

## Files
- `.python-version`: specifies python version for pyenv.
- `chk_config.py`: simple script for verifying setup. if you get a mininet import error, this can help debug. make sure you can run it with `sudo`.
- `chord_paper.pdf`: the research paper we're working from.
- `requirements.txt`: python dependencies
- `requirements-dev.txt`: development dependencies. installs from `requirements.txt` first, then adds dev dependencies, so no need to run `pip install` for both.

## Dependencies
- mininet
- a recent python. we use 3.11, installed via pyenv.

## Installation
We developed on an ubuntu instance on aws EC2.
1. ensure that mininet is installed.
    - `sudo apt install mininet`
    - you can verify installation with `mn --version`, which will
      print the mininet version if correctly installed.
2. get the path to mininet module (run with system python).
remember/copy&paste this for later.
    - `python3 -c "import mininet; print(mininet.__file__)"`
    - this should print something like 
    `/usr/lib/python3/dist-packages/mininet/__init__.py`
3. add this path (up to and not including `mininet/`) to your `PYTHONPATH`
env variable:
    `export PYTHONPATH=$PYTHONPATH:/usr/lib/python3/dist-packages/`
    - to have this persist, add to your shell config file (`.bashrc`, etc)
4. (optional) install [`pyenv`](https://github.com/pyenv/pyenv)
    - once installed, you'll also need to install python 3.11 to
    match our version. pyenv will automatically pick up the `.python-version`
    file in this repo.
        - `pyenv install 3.11`
5. clone this repo. from inside the repo, create and activate a virtual
environment:
    - `python -m venv [.venv | venv | ...]`
    - `source .venv/bin/activate`
6. now run `python -c "import mininet; print(mininet.__file__)"` again.
this should output the same path as when running with system python.
7. install dependencies:
    - `pip install --upgrade pip`
    - to work on this: `pip install -r requirements-dev.txt`
    - to just run: `pip install -r requirements.txt`
At this point, you should be installed and good to go.

## Usage

To run scripts using mininet, the full command format is:

`sudo [pass PYTHONPATH up] [path/to/venv/python] some_script.py`

So to check config, it will be:

`sudo PYTHONPATH=$PYTHONPATH /home/ubuntu/chord/.venv/bin/python chk_config.py`

for quality of life, add an alias to your shell config:

`alias pychord="sudo PYTHONPATH=\$PYTHONPATH /home/ubuntu/chord/.venv/bin/python "`

that way checking config will be:

`pychord chk_config.py`

**explanation:** running python programs is a little weird, since we're using system-installed
mininet with python in a virtual env (we'd avoid this by not using a venv, but system python
doesn't seem to be compatible with pip). mininet needs root privileges,
but sudo doesn't inherit `env` variables by default. to invoke, we need
to pass our PYTHONPATH to the root environment, and also use the full python
path (to the venv python, otherwise it will use system python).
