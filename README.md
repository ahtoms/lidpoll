# Lidpoll

Lidpoll simply creates a watcher in the background and checks
the lidstate every 5 seconds to see if it has changed.

If it changes, it will invoke `systemctl suspend`.

There are some big assumptions made here:

* You must have systemd
* suspend must work in some form
* acpi lid folder must also exist (installation will detect this)
* 5 seconds for poll is just 'fine' for everyone and doesn't cause
any excessive usage on a light read of the file.
* `state` file returns `open` and `closed` strings

This was constructed while I am waiting for lid-close suspend
to be implemented on my laptop. For the most part, this software
is jank and use it your own risk.

## Installation

* Run `install.sh`, it will detect the acpi folder in `/proc` and the
`lid` folder.

* `install.sh` will create a `~/.lidpoll` directory and copy the required
contents

* Lastly, you will receive a run-command string to add to your run command
file for your user. Make sure you copy this and paste it into the correct file.


## Uninstall

* Simply call `uninstall.sh` and it will remove the `~/.lidpoll` folder

* You will need to remove the run command line that you would have copied over



