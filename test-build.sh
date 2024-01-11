#!/bin/sh

poetry run pyinstaller src/acat/__main__.py --name A-CAT --onefile --windowed --onedir -y --log-level=WARN --clean