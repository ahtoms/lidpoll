#!/usr/bin/env

RUNCMD_DIR="~/.lidpoll"
ACPI_LID_PATH="/proc/acpi/button/lid"

if ! test -d $RUNCMD_DIR; then
  mkdir $RUNCMD_DIR
fi

if test -d $ACPI_LID_PATH; then
  LID_COUNT=$(ls $ACPI_LID_PATH | wc -l)
  if test $LID_COUNT -eq 1; then
    ACPI_LID_ENTRY=$(ls $ACPI_LID_PATH)
    # generate the run command and path
    LID_STATE_PATH="$ACPI_LID_PATH/$ACPI_LID_ENTRY/state"
    GEN_OUTPUT=$(python gen_script.py $RUNCMD_DIR/lidpoll.py $LID_STATE_PATH)
    CMDRC_OUT="$RUNCMD_DIR/lidpoll_start.sh"
    cp lidpoll.py $RUNCMD_DIR/lidpoll.py
    echo $GEN_OUTPUT > $RUNCMD_DIR/lidpoll_start.sh
    echo "Add '$CMDRC_OUT 2> /dev/null' to your run-command file (Example: .bashrc/.zshrc)"
    
  elif test $LID_COUNT -gt 1; then
    echo "More than one lid detected"
    echo "This has not been implemented yet"
    
  else
    echo "Unable to find lid buttons"
    echo "Cannot continue with installation"
  fi
else
  echo "No lid directory, check that acpi events have been configured for lid"
  echo "Cannot continue with installation"
fi

