#!/usr/bin/env

RUNCMD_DIR="~/.lidpoll"

if test -d $RUNCMD_DIR; then
  echo "Removing $RUNCMD_DIR"
  rm -r $RUNCMD_DIR
  echo "lidpoll has been uninstalled"
else
  echo "$RUNCMD_DIR is missing, are you sure this was installed?"
fi
