# Useful Commands

This is just a place for me to put small commands that I find myself looking up frequently.

### Reload udev rules:

```
sudo udevadm control --reload-rules
sudo udevadm trigger
```

### Bash

#### Argument shortcuts

https://stackoverflow.com/questions/4009412/how-to-use-arguments-from-previous-command
```
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
