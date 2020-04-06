m2r readme.md
python3 setup.py sdist
python3 setup.py bdist_wheel sdist
python3 -m twine upload dist/*