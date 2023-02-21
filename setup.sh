#!/bin/bash

if [-d "ssv-keys"]; then
  echo "ssv-keys directory already there"
else
  echo "cloning ssv-keys"
  git clone https://github.com/bloxapp/ssv-keys.git
  cd ssv-keys
  git fetch -a
  git checkout v2
  cd ..
  rm ssv-keys/package.json
  cp ssv/package.json ssv-keys/package.json
  npm install --prefix ssv-keys
  case "$OSTYPE" in
    linux*) npm run package-linux --prefix ssv-keys && cp ssv-keys/bin/linux/ssv-keys-lin ssv/ssv-cli;;
    darwin* ) npm run package-macos --prefix ssv-keys && cp ssv-keys/bin/macos/ssv-keys-mac ssv/ssv-cli;;
    msys* ) npm run package-win --prefix ssv-keys && cp ssv-keys/bin/win/ssv-keys.exe ssv/ssv-cli.exe;;
    cygwin* ) npm run package-win --prefix ssv-keys && cp ssv-keys/bin/win/ssv-keys.exe ssv/ssv-cli.exe;;
  esac
fi

echo "setup for ssv keys cli done"

#echo "downloading dependencies for python"
#
#pip install -r requirements.txt
