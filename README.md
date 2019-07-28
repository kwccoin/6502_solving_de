## Solving a differential equation with a 6502
An example how to solve a ordinary differential equation (ODL) on a 6502 with Woz's floating point assembly code.

## How and Why?
I'm really into computer history and math. I liked how the whole home computer thing started and the time where people actually coded in assembly. I'm not into games, so if I had one I would try to do lots of math stuff. There are always differential equations in physics which have to be solved with numerical methods. But I will solve a really easy one to show you how to do it.


Fortunately, some floating point routines were already programmed by Roy Rankin and Steve Wozniak (http://www.6502.org/source/floats/wozfp1.txt). I'll use this code and the py65mon (https://github.com/mnaberez/py65) to run it.

## Sketch
<img src="img/circuit.svg?sanitize=true">

The example will be the discharging of a capacitor. We are interested how the voltage is decreasing over the time. We can describe this with following differential equation:

```
ODL:
u(t)' = -1/(RC) * u(t)

START VALUES:
t0 = 0
u(0) = 9V

```

## Solution

The exact solution is easy and known for this equation. Which is good, so we can compare the results later. To solve it approximately step by step I'm using the Euler method which leads to:

```
u[n+1] = u[n] + h * ( -1/(RC) * u[n] )

u[n+1] = u[n] - h/(RC) * u[n]

with a = -h/(RC)

u[n+1] = u[n] + a * u[n]

```
