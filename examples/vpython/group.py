import math
import vpython


box = vpython.box(pos=vpython.vec(0,0,0))
other = vpython.box(pos=vpython.vec(10, 0, 0))
g = vpython.compound([box, other])

while True:
    vpython.rate(30)
    box.rotate(angle=0.0001 * 180/math.pi)
