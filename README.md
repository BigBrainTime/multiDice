# Overview

multi_dice.py provides functions for rolling dice and calculating results for tabletop RPGs and other dice games. It handles standard dice rolls, advantage/disadvantage, modifiers, and selecting highest/lowest rolls.

## Usage

Import the module:

```py
import multi_dice
```

Roll dice:

```py
result = dice.roll("2d20+5")
```

Roll with advantage:

```py
result = dice.roll("a2d20+5")
```

Roll with disadvantage:

```py
result = dice.roll("d2d20+5")
```

The dice rolling string supports:

* (int)d(int) - Number of dice and sides
* k(int) - Keep highest X rolls
* l(int) - Keep lowest X rolls
* (+, -, *, /) - Modifiers

## Examples

* "2d20" - Roll 2d20
* "a2d20" - Roll advantage on 2d20
* "d2d20" - Roll disadvantage on 2d20
* "2d20+5" - Roll 2d20 and add 5
* "4d6k3" - Roll 4d6 keep highest 3
* "2d20l1-5" - Roll 2d20 keep lowest 1 and subtract 5

## Breakdown

Rules to making dice string

* "a" or "d" (optional)
* int
* "d"
* int
* "k" or "l" (optional)
* int   (requried if k or l)
* opcode (+, -, /, //, *) (optional)
* int or another dice string    (required if opcode)

OR

* int

## Functions

### roll(dice, crit=20)

Rolls dice according to the provided dice string and returns the result.

* dice (str): The dice rolling string
* crit (int): The value that causes a critical (default 20)
* Returns: (int) Result of the dice roll

### advantage(*func,*args, *kwargs)

Calls a function twice and returns the higher result. Used for rolling with advantage.

* func (function): The function to call
* *args: Positional args to pass to the function
* **kwargs: Keyword args to pass to the function
* Returns: (int) The higher of the two function calls

### disadvantage(*func,*args,*kwargs)

Calls a function twice and returns the lower result. Used for rolling with disadvantage.

* func (function): The function to call
* *args: Positional args to pass to the function
* **kwargs: Keyword args to pass to the function
* Returns: (int) The lower of the two function calls

## Classes

### RollDice

Class for rolling dice and calculating results. Handles parsing dice strings, rolling, modifiers, advantage/disadvantage, etc.

`_init_(dice, crit=20)`

* dice (str): Dice rolling string

* crit (int): Value that causes critical hit

```py
.advantage(): Reroll with advantage, keeping higher value

.disadvantage(): Reroll with disadvantage, keeping lower value

.value: Result of the roll

.rolls: List of each individual dice roll

.average: Average possible roll result

.lowrange: Minimum possible roll result

.highrange: Maximum possible roll result

.crit: True if a critical hit was rolled
```

## Class Examples

Regular usage

```py
dice = RollDice("3d6")
print(dice.value)
```

Roll with dis/advantage:

```py
dice = RollDice("a2d20")
print(dice.value)

dice2 = RollDice("d2d20")
print(dice2.value)
```
