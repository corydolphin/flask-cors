requirements files
##################

The subdirectories in ``requirements/`` contain ``pyproject.toml`` files
with minimal Poetry configurations to define tool requirements for testing.

To update the exported ``requirements.txt`` files in the subdirectories,
run the included tox label, ``update``.

..  code-block::

    tox run -m update


If the flask-cors Python support changes,
update the Python requirements in the ``pyproject.toml`` files.
For example, when Python 3.8 support is dropped,
change ``">=3.8"`` to ``">=3.9"`` and run the tox ``update`` label.
