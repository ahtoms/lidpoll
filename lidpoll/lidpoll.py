
from signal import signal, SIGINT
from time import sleep
from pathlib import Path
import sys
import os

CMD_NAME = 'lid_poll.py'
PID_LOCK_FNAME = Path.home() / '.lid_poll.pidlock'
POLL_TIME = 5

def open_file(path):
    f = open(path, 'r')
    if f is not None:
        return (f, True)
    else:
        return (None, False)


def watch_lid_poll_loop(lidevent, file):

    while lidevent.get_watcher().is_watching():
        lidevent.handle_event(file)
        sleep(POLL_TIME) # approx
        file.seek(0)

def pid_lock_write():
    pid_n = os.getpid()
    pidfname = PID_LOCK_FNAME
    pidfile = open(pidfname, 'w')
    pidfile.write('{}\n'.format(str(pid_n)))
    pidfile.close()

def pid_lock_delete():
    pidfname = PID_LOCK_FNAME
    os.remove(pidfname)


class LidWatcher:

    def __init__(self):
        self.lid_closed = False
        self.keep_watching = True

    def lid_toggle(self):
        self.lid_closed = not self.lid_closed

    def is_lid_open(self):
        return not self.lid_closed

    def is_lid_closed(self):
        return self.lid_closed

    def stop_watching(self):
        self.keep_watching = False

    def is_watching(self):
        return self.keep_watching

    def emit_suspend(self):
        #print('TEST: Emitting suspend')
        os.system('systemctl suspend')
        
    def parse_line(self, line):
        line = line.strip()
        line = line.replace(' ', '')
        spl = line.split(':')
        if len(spl) == 2:
            state_txt = spl[1]
            if state_txt == 'open':
                if self.is_lid_closed():
                    self.lid_toggle()

            elif state_txt == 'closed':
                if self.is_lid_open():
                     self.lid_toggle()
                     self.emit_suspend()
                     
                    
        else:
            print("Unable to split line into two parts")
            
 
class LidEventHandler():

    def __init__(self, watcher):
        super().__init__()
        self.watcher = watcher

    def handle_event(self, fileobj):
        lines = fileobj.readlines()
        if len(lines) >= 1:
            lastline = lines[-1]
        
            self.watcher.parse_line(lastline)
        else:
            print("No lines available")

    def get_watcher(self):
        return self.watcher



def start_watcher():

    watcher = LidWatcher()

    def sigint_handler(sig, frame):
        watcher.stop_watching()

            
    signal(SIGINT, sigint_handler)
    arglen = len(sys.argv)

    if arglen == 2:
        argpath = sys.argv[1]
        #sel = selectors.DefaultSelector()
        (watchfile, isvalid) = open_file(argpath)

        if isvalid:
            pid_lock_write()
            print("Lid Watcher has started")
            
            levent = LidEventHandler(watcher)
            watch_lid_poll_loop(levent, watchfile)
            end_watcher(watchfile)
        else:
            print("Cannot open file: {}, check path is valid".format(argpath))
    else:
        print("Watcher cannot start, missing argpath")


def end_watcher(watchfile):
    if not watchfile.closed:
        watchfile.close()
    pid_lock_delete()

if __name__ == '__main__':
    start_watcher()

