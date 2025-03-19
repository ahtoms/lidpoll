
import sys

if len(sys.argv) != 3:
    print("Invalid number of arguments, specify lid_path and script location")
    exit(1)

SCRIPT_LOC = sys.argv[1]
LID_PATH = sys.argv[2]

PYTHON_CMD = "python {} {}".format(SCRIPT_LOC, LID_PATH)

script = """
PIDLOCK_FILE='~/.lid_poll.pidlock'
if test -f $PIDLOCK_FILE; then
  PIDLOCK_PID=$(cat $PIDLOCK_FILE)
  kill -0 $PIDLOCK_PID
  KRET=$?
  if test $KRET -ne 0; then
    {pycmd} &
  fi
else
  {pycmd} &
fi
    
""".format(pycmd=PYTHON_CMD)

print(script)
