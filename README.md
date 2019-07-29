## Solving a differential equation with a 6502
An example how to solve a ordinary differential equation (ODL) on a 6502 with Woz's floating point assembly code.

## How and Why?
I'm really into computer history and math. I liked how the whole home computer thing started and the time where people actually coded in assembly. I'm not into games, so if I had one I would try to do lots of math stuff. There are always differential equations in physics which have to be solved with numerical methods. But I will solve a really easy one to show you how to do it.


Fortunately, some floating point routines were already programmed by Roy Rankin and Steve Wozniak (http://www.6502.org/source/floats/wozfp1.txt). I'll use this code and the py65mon (https://github.com/mnaberez/py65) to run it. But it'll work on the VICE emulator too. And on real machines I guess (if you use the already converted binary code. Woz's original doesn't support labels).

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
u[n+1] = u[n] -1/(RC) * h * u[n]
with a = -1/(RC)
u[n+1] = u[n] + a * h * u[n]

```

The last formula will be implemented in our program.

## An easy introduction

Open the code.bin and copy the floating point code. Paste it in the monitor. Now we have to put two number at location 0x4 and 0x8 (both 4 bytes).

The floating point algorithm requires the binary format, so we have to convert numbers. A short description is in the document:

```
In the Exponent:
00 Represents -128
      ...
7F Represents -1
80 Represents 0
81 Represents +1
      ...
FF Represents +127

Exponent    Two's Complement Mantissa
SEEEEEEE    SM.MMMMMM  MMMMMMMM  MMMMMMMM
    n           n+1       n+2       n+3
```

So lets divide 3 through 0.125

```
3.0:
Integer:    3 = 11
Fraction:   0.0 | 0
Exp:        11.0 * 2^0
            1.10 * 2^1 | Normalisation
Converted:  0x81 0b01100000 (0x60) 0x0 0x0

0.125:
Integer:    0 = 0
Fraction:   0.125 * 2 = 0.25 | 0
            0.25  * 2 = 0.5  | 0
            0.5   * 2 = 1.0  | 1
Exp:        0.001 * 2^0
            1.000 * 2^-3
Converted:  0x7D 0b01000000 (0x40) 0x0 0x0
```

Doesn't matter which operation we use (plus, mul or div). The result will always in the second position (0x8). In division the second one (0x8) is the divisor.

So we put the numbers in position in the monitor (radix: hex):

```
fill 4 81 60 0 0 7D 40 0 0
```

A small routine will jump to the floating point code and back (just copy it):

```
assemble 10
jsr fdiv
brk
```

We start the program:

```
goto 10
```

After finishing, it jumps back and reaches a brk (0x0) which gets us back to the monitor.
From there we check the result:

```
mem 4:b
```

Which gives us:

```
84 60 0 0
```

Which means:

```
84 = 2^4
60 = 1.1
1.1 * 2^4 = 11000 = 24 (DEC)
```

It's a little bit funny if you see this kind of stuff the first time. Play with it, you'll figure it out. Attention: If you want to convert negative numbers, you have to use the 2's complement.

## Solving the differential equation

It was:

```
u[n+1] = u[n] + a * h * u[n]
with a = -1/(RC)
```

We have to determine the step size h (which represents the time). It should be small, but I want to have an error effect to show you so we choose 0.5 (0.01 would be a much better choice).

```
a = -1/(200 * 0.1) = -0.05
```

