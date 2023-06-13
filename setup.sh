#!/bin/bash

npm install
if [ -d "ssv-keys" ]; then
  echo "ssv-keys directory already there"
else
  echo "cloning ssv-keys"
  git clone https://github.com/bloxapp/ssv-keys.git
  cd ssv-keys
  git fetch -a
  git checkout main
  cd ..
  rm ssv-keys/package.json
  cp ssv/package.json ssv-keys/package.json
  yarn install --cwd ssv-keys
  case "$OSTYPE" in
    linux*) yarn --cwd ssv-keys package-linux  && cp ssv-keys/bin/linux/ssv-keys-lin ssv/ssv-cli;;
    darwin* ) yarn --cwd ssv-keys package-macos && cp ssv-keys/bin/macos/ssv-keys-mac ssv/ssv-cli;;
    msys* ) yarn --cwd ssv-keys package-win  && cp ssv-keys/bin/win/ssv-keys.exe ssv/ssv-cli.exe;;
    cygwin* ) yarn --cwd ssv-keys package-win && cp ssv-keys/bin/win/ssv-keys.exe ssv/ssv-cli.exe;;
  esac
fi

echo "setup for ssv keys cli done"

echo "downloading dependencies for python"

pip install -r requirements.txt
