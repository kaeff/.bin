#! /usr/bin/env bash
brew install virtualenv
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
virtualenv "$DIR/.venv"
source "$DIR/.venv/bin/activate"
pip3 install -r "$DIR/requirements.txt"

echo ""
echo ""
echo "Please run:"
echo "source '$DIR/.venv/bin/activate'"
