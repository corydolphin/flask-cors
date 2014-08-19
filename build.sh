#!/bin/sh
pandoc --from=markdown_github --to=rst --output=README.rst README.md
cd docs
make html
cd ..