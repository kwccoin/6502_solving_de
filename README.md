## Solving a differential equation with a 6502
An example how to solve a ordinary differential equation (ODL) on a 6502 with Woz's floating point assembly code.

## How and Why?
I'm really into computer history and math. I liked how the whole home computer thing started and the time where people actually coded in assembly. I'm not into games, so if I had one I would try to do lots of math stuff. There are always differential equations in physics which have to be solved with numerical methods.


Fortunately, some floating point routines were already programmed by Roy Rankin and Steve Wozniak (http://www.6502.org/source/floats/wozfp1.txt). I'll use this code and the py65mon monitor (https://github.com/mnaberez/py65) to run it. But it'll work on the VICE emulator too. And on real machines I guess.

## Sketch
<img src="img/circuit.svg?sanitize=true">

The example will be the discharging of a capacitor. I wanr to know how the voltage is decreasing over the time. Following differential equation is used:

```
ODL:
u(t)' = -1/(RC) * u(t)

START VALUES:
t0 = 0
u(0) = 9V

```

## Solution

The exact solution is easy and known for this equation. Which is good, so I can compare the results at the end. To solve it approximately step by step I'm using the Euler method which leads to:

```
u[n+1] = u[n] + h * ( -1/(RC) * u[n] )
u[n+1] = u[n] -1/(RC) * h * u[n]
with a = -1/(RC)
u[n+1] = u[n] + a * h * u[n]

```

The last formula will be implemented in our program.

## An easy introduction

Open the code.bin and copy the floating point code. Paste it in the monitor. Now we have to put two numbers at location 0x4 and 0x8 (both 4 bytes).

The floating point algorithm requires the binary format, so we have to convert numbers. A short description can be found in the floating point document (wozfp1.txt) by Woz:

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

Example: Lets divide 3 through 0.125

```
3.0:
Integer:    3 = 11
Fraction:   0.0 | 0
Exp:        11.0 * 2^0
            1.10 * 2^1 | Normalization
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

So we put the numbers in position with the monitor (radix: hex):

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

It's a little bit funny if you see this kind of stuff the first time. Play with it, you'll figure it out. Attention: If you want to convert negative numbers, you have to use the 2's complement (after the normalization).

## Solving the differential equation

It was:

```
u[n+1] = u[n] + a * h * u[n]
with a = -1/(RC)
```

We have to determine the step size h (which represents the time). It should be small, but I want to have an error effect to show you so we choose 0.5 (0.01 would be a much better choice).

```
h = 0.5
a = -1/(20 * 0.1) = -0.5
```

To work with variables we have to initialise them. Here are their positions:

```
t:         0x20 0x21 0x22 0x23
u:         0x24 0x25 0x26 0x27
a:         0x28 0x29 0x2A 0x2B
h:         0x2C 0x2D 0x2E 0x2F
list:      0x30
counter:   0x31
t_list:    0x2000
u_list:    0x2100
```

Function positions:

```
fadd:       1f50
fmul:       1f77
fdiv:       1f9d
save2list:  40
equation:   60
```

t = current time. Which is saved to a list each step

u = current voltage. Which is also saved to a list each step (for plotting later)

a = constant value

h = step size, constant

list = is used as an addition to the initial list location to store the time and voltage values each step

counter = counts steps so I can stop the execution after reaching a chosen value.

t_list = start position for time values

x_list = start position for voltage values


fadd = floating point function for adding

fmul = floating point function for multiplication

fdiv = floating point function for division

save2list = save current time and voltage to lists

equation = calculates one step


Set up (initial) values with the monitor:

```
fill 20 80  0  0  0 
fill 24 83 48  0  0
fill 28 7F C0  0  0
fill 2C 7F 40  0  0
fill 30  0
fill 31  0
fill 32  0
```
Function which saves current time and voltage to list positions.

```
assemble 40
ldx 30
lda $20
sta 2000,x
lda $24
sta 2100,x
inx
lda $21
sta 2000,x
lda $25
sta 2100,x
inx
lda $22
sta 2000,x
lda $26
sta 2100,x
inx
lda $23
sta 2000,x
lda $27
sta 2100,x
inx
stx 30
rts
```

Creating the calculation

u[n+1] = u[n] + a * h * u[n]
```

assemble 60
;
jsr save2list
;
;              a
lda $28
sta $4
lda $29
sta $5
lda $2a
sta $6
lda $2b
sta $7
;              h
lda $2c
sta $8
lda $2d
sta $9
lda $2e
sta $a
lda $2f
sta $b
;              a*h
jsr fmul
;
;u_n
lda $24
sta $4
lda $25
sta $5
lda $26
sta $6
lda $27
sta $7
;
;                 u_n*(a*h)
jsr fmul
;
;                 u_n
lda $24
sta $4
lda $25
sta $5
lda $26
sta $6
lda $27
sta $7
;
;                u_n + (h*a*u_n)
jsr fadd
;
;                u = u_n+1
lda $8
sta $24
lda $9
sta $25
lda $a
sta $26
lda $b
sta $27
;
;               h
lda $2c
sta $8
lda $2d
sta $9
lda $2e
sta $a
lda $2f
sta $b
;
;               t
lda $20
sta $4
lda $21
sta $5
lda $22
sta $6
lda $23
sta $7
;
;               t+h
jsr fadd
;
;               t = t+h
lda $8
sta $20
lda $9
sta $21
lda $a
sta $22
lda $b
sta $23
;
rts

```







