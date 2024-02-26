# Overview

multi_dice.py provides functions for rolling dice and calculating results for tabletop RPGs and other dice games. It handles standard dice rolls, advantage/disadvantage, modifiers, and selecting highest/lowest rolls.

## Usage

To use the multi_dice module, first import it:

```py
import multi_dice
```

To roll dice, call the roll function and pass the dice string:

```py
result = multi_dice.roll("2d20+5")
```

To roll with advantage, add an 'a' before the dice string:

```py
result = multi_dice.roll("a2d20+5")
```

To roll with disadvantage, add a 'd' before the dice string:

```py
result = multi_dice.roll("d2d20+5")
```

## Examples

* "2d20" - Roll 2d20
* "a2d20" - Roll advantage on 2d20
* "d2d20" - Roll disadvantage on 2d20
* "2d20+5" - Roll 2d20 and add 5
* "4d6k3" - Roll 4d6 keep highest 3
* "2d20l1-5" - Roll 2d20 keep lowest 1 and subtract 5
* "2d8+1d6" - Roll 1d6 and add it to a roll of 2d8

## Dice String Rules

Here are the rules for constructing a valid dice string:

* "a" xor "d" (optional)
* int
* "d"
* int
* "k" xor "l" (optional)
  * int   (requried if k xor l)
* opcode (+, -, /, //, *) (optional)
  * int or another dice string    (required if opcode)

OR

* int

___

"a" = advantage\
"d" = disadvantage\
"k" = keep highest int rolls\
"l" = keep lowest int rolls\
\
Note:\
When using multiple opcodes to do multiple dice, PEMDAS is not followed. Instead the right most value is calculated first and works leftward.

## Limits

The only checks on whether a roll is performed is if either the number of rolls or if the sides of the dice are over 1000, and if k and l are <= to the number of sides.

## Functions

### roll(dice)

Rolls dice according to the provided dice string and returns the result.

* dice (str): The dice rolling string
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
dice = multi_dice.RollDice("3d6")
print(dice.value)
```

Roll with dis/advantage:

```py
dice = multi_dice.RollDice("a2d20")
print(dice.value)

dice2 = multi_dice.RollDice("d2d20")
print(dice2.value)
```
