#!/bin/sh
pandoc --from=markdown --to=rst --output=README.rst README.md
cd docs
make clean
make html
cd ..