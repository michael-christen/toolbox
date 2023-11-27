# Useful Commands

This is just a place for me to put small commands that I find myself looking up frequently.

### Reload udev rules:

```
sudo udevadm control --reload-rules
sudo udevadm trigger
```

### Bash

#### Common Operations

```
# If

if [ CONDITIONAL ]; then
  ...
fi

# Conditionals
'-z "${variable}"'   is this variable set
```

#### Parameters

https://www.gnu.org/software/bash/manual/html_node/Shell-Parameter-Expansion.html
```
${v-unset}  # if v is unset will read as "unset"
```

#### Argument shortcuts

```
$@      all arguments

# https://stackoverflow.com/questions/4009412/how-to-use-arguments-from-previous-command
!^      first argument
!$      last argument
!*      all arguments
!:2     second argument

!:2-3   second to third arguments
!:2-$   second to last arguments
!:2*    second to last arguments
!:2-    second to next to last arguments

!:0     the command
!!      repeat the previous line
```

#### Package Commands

Get package dependencies:

```
apt-cache depends --recurse --no-recommends --no-suggests --no-replaces --no-breaks --no-conflicts <package>
```
