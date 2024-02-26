import unittest
import random
import operator


# Class to roll dice and calculate results
class RollDice:
    def __init__(self, dice: str = "1d6", crit: int = 20):
        dice = dice.replace(" ","")
        self.dice = dice
        self.crit_val = crit

        # If no "d" in dice string, set as integer
        if "d" not in dice:
            dice = int(dice)
            self.rolls = [dice]
            self.crit = False
            self.value = dice
            self.average = dice
            self.lowrange = dice
            self.highrange = dice

        # If dice starts with "a", call roll() and advantage()
        elif dice.startswith('a'):
            self.dice = dice[1:]
            self.roll()
            self.advantage()

        # If dice starts with "d", call roll() and disadvantage()
        elif dice.startswith('d'):
            self.dice = dice[1:]
            self.roll()
            self.disadvantage()

        # Otherwise just call roll()
        else:
            self.roll()

    # Dictionary of operator codes
    codes = {
        "+": operator.add,
        "*": operator.mul,
        "/": operator.truediv,
        "//": operator.floordiv,
        "-": operator.sub,
    }

    # Check dice string for operators
    def check_op(self):
        for code in self.codes:
            if code in self.dice:
                inp, mod = self.dice.split(code,1)
                return inp, code, RollDice(mod)
        return self.dice, "+", RollDice("0")

    # Roll dice and calculate results
    def roll(self):

        # Check for operators
        split_d, op, mod = self.check_op()
        split_d = split_d.split("d")

        # Get number of dice and sides
        number_of_dice = int(split_d[0])
        dice_sides = split_d[1]

        # Check for keeping highest/lowest rolls
        k_value = number_of_dice

        reverse_sort = False
        if "k" in dice_sides:
            dice_sides, k_value = dice_sides.split("k")
            k_value = int(k_value)
            reverse_sort = True
        elif "l" in dice_sides:
            dice_sides, k_value = dice_sides.split("l")
            k_value = int(k_value)
            reverse_sort = False

        dice_sides = int(dice_sides)

        # Validate inputs
        if number_of_dice > 1000 or dice_sides > 1000 or k_value > number_of_dice:
            raise ValueError

        # Roll dice
        self.rolls = []
        self.crit = False

        for c in range(number_of_dice):
            roll = random.randint(1, dice_sides)
            self.crit = True if roll >= self.crit_val else self.crit
            self.rolls.append(roll)

        # Calculate results
        self.value = self.codes[op](sum(sorted(self.rolls, reverse=reverse_sort)[:k_value]), mod.value)
        self.average = self.codes[op](((number_of_dice * dice_sides + 1) / 2), mod.average)
        self.lowrange = self.codes[op](number_of_dice, mod.lowrange)
        self.highrange = self.codes[op]((number_of_dice * dice_sides), mod.highrange)

    # Reroll with advantage
    def advantage(self):
        roll = RollDice(self.dice, self.crit_val)
        if roll.value > self.value:
            self = roll

    # Reroll with disadvantage
    def disadvantage(self):
        roll = RollDice(self.dice, self.crit_val)
        if roll.value < self.value:
            self = roll


def roll(dice: str = "1d6", crit: int = 20) -> int:
    """Rolls dice

    Args:
        d (str): Required: '(int)d(int)' Optional parameters:[k(int),('+', '*', '/', '//', '-')(int||roll)]
        crit (int): only used if object == True, if any roll > than crit self.crit == Trues

    Returns:
        Int
    """
    return RollDice(dice, crit).value


def greater_than(a, b):
    return a if a > b else b


def less_than(a, b):
    return a if a < b else b


def advantage(func, *args, **kwargs):
    """Calls a function twice and returns higher value

    Args:
        func (function): The function
        *args: the arguments for the function

    Returns:
        (int): Highest int value
    """
    return greater_than(func(*args, **kwargs), func(*args, **kwargs))


def disadvantage(func, *args, **kwargs):
    """Calls a function twice and returns lower value

    Args:
        func (function): The function
        *args: the arguments for the function

    Returns:
        (int): lowest int value
    """
    return less_than(func(*args, **kwargs), func(*args, **kwargs))


class DiceTestCase(unittest.TestCase):
    def test_raw_number(self):
        for _ in range(1, 101):
            self.assertEqual(roll(str(_)), _)

    def test_k_gt_n(self):
        for _ in range(1, 101):
            number_of_dice = random.randint(1, 101)
            number_of_sides = random.randint(1, 101)

            k_val = number_of_dice + random.randint(1, 101)

            self.assertRaises(
                ValueError, roll, f"{number_of_dice}d{number_of_sides}k{k_val}"
            )

    def test_l_gt_n(self):
        for _ in range(1, 101):
            number_of_dice = random.randint(1, 101)
            number_of_sides = random.randint(1, 101)

            l_val = number_of_dice + random.randint(1, 101)

            self.assertRaises(
                ValueError, roll, f"{number_of_dice}d{number_of_sides}l{l_val}"
            )

    def test_standard(self):
        for _ in range(1, 101):
            number_of_dice = random.randint(1, 101)
            number_of_sides = random.randint(1, 101)

            self.assertTrue(
                number_of_dice
                <= roll(f"{number_of_dice}d{number_of_sides}")
                <= number_of_dice * number_of_sides
            )

    def test_standard_with_modifier(self):
        for _ in range(1, 101):
            number_of_dice = random.randint(1, 101)
            number_of_sides = random.randint(1, 101)
            modifier = random.randint(1, 101)

            self.assertTrue(
                number_of_dice + modifier
                <= roll(f"{number_of_dice}d{number_of_sides}+{modifier}")
                <= (number_of_dice * number_of_sides) + modifier
            )

    def test_k_without_modifier(self):
        for _ in range(1, 101):
            number_of_dice = random.randint(1, 101)
            number_of_sides = random.randint(1, 101)

            k_val = random.randint(1, number_of_dice)

            self.assertTrue(
                k_val
                <= roll(f"{number_of_dice}d{number_of_sides}k{k_val}")
                <= (k_val * number_of_sides)
            )

    def test_l_without_modifier(self):
        for _ in range(1, 101):
            number_of_dice = random.randint(1, 101)
            number_of_sides = random.randint(1, 101)

            l_val = random.randint(1, number_of_dice)

            self.assertTrue(
                l_val
                <= roll(f"{number_of_dice}d{number_of_sides}l{l_val}")
                <= (l_val * number_of_sides)
            )

    def test_k_with_modifier(self):
        for _ in range(1, 101):
            number_of_dice = random.randint(1, 101)
            number_of_sides = random.randint(1, 101)
            modifier = random.randint(1, 101)

            k_val = random.randint(1, number_of_dice)

            self.assertTrue(
                k_val + modifier
                <= roll(f"{number_of_dice}d{number_of_sides}k{k_val}+{modifier}")
                <= (k_val * number_of_sides) + modifier
            )

    def test_l_with_modifier(self):
        for _ in range(1, 101):
            number_of_dice = random.randint(1, 101)
            number_of_sides = random.randint(1, 101)
            modifier = random.randint(1, 101)

            l_val = random.randint(1, number_of_dice)

            self.assertTrue(
                l_val + modifier
                <= roll(f"{number_of_dice}d{number_of_sides}l{l_val}+{modifier}")
                <= (l_val * number_of_sides) + modifier
            )

    def test_advantage_raw_number(self):
        for _ in range(1,101):
            roll = RollDice(str(_))
            result1 = roll.value
            roll.advantage()
            result2 = roll.value
            self.assertEqual(result1, result2)

    def test_advantage_standard(self):
        for _ in range(1, 101):
            number_of_dice = random.randint(1, 101)
            number_of_sides = random.randint(1, 101)

            roll = RollDice(f"{number_of_dice}d{number_of_sides}")
            result1 = roll.value
            roll.advantage()
            result2 = roll.value

            self.assertTrue(
                number_of_dice
                <= result1 <= result2
                <= number_of_dice * number_of_sides
            )

    def test_advantage_standard_with_modifier(self):
        for _ in range(1, 101):
            number_of_dice = random.randint(1, 101)
            number_of_sides = random.randint(1, 101)
            modifier = random.randint(1, 101)

            roll = RollDice(f"{number_of_dice}d{number_of_sides}+{modifier}")
            result1 = roll.value
            roll.advantage()
            result2 = roll.value

            self.assertTrue(
                number_of_dice + modifier
                <= result1 <= result2
                <= (number_of_dice * number_of_sides) + modifier
            )

    def test_advantage_k_without_modifier(self):
        for _ in range(1, 101):
            number_of_dice = random.randint(1, 101)
            number_of_sides = random.randint(1, 101)

            k_val = random.randint(1, number_of_dice)

            roll = RollDice(f"{number_of_dice}d{number_of_sides}k{k_val}")
            result1 = roll.value
            roll.advantage()
            result2 = roll.value

            self.assertTrue(
                k_val
                <= result1 <= result2
                <= (k_val * number_of_sides)
            )

    def test_advantage_l_without_modifier(self):
        for _ in range(1, 101):
            number_of_dice = random.randint(1, 101)
            number_of_sides = random.randint(1, 101)

            l_val = random.randint(1, number_of_dice)

            roll = RollDice(f"{number_of_dice}d{number_of_sides}l{l_val}")
            result1 = roll.value
            roll.advantage()
            result2 = roll.value

            self.assertTrue(
                l_val
                <= result1 <= result2
                <= (l_val * number_of_sides)
            )

    def test_advantage_k_with_modifier(self):
        for _ in range(1, 101):
            number_of_dice = random.randint(1, 101)
            number_of_sides = random.randint(1, 101)
            modifier = random.randint(1, 101)

            k_val = random.randint(1, number_of_dice)

            roll = RollDice(
                f"{number_of_dice}d{number_of_sides}k{k_val}+{modifier}")
            result1 = roll.value
            roll.advantage()
            result2 = roll.value

            self.assertTrue(
                k_val
                <= result1 <= result2
                <= (k_val * number_of_sides) + modifier
            )

    def test_advantage_l_with_modifier(self):
        for _ in range(1, 101):
            number_of_dice = random.randint(1, 101)
            number_of_sides = random.randint(1, 101)
            modifier = random.randint(1, 101)

            l_val = random.randint(1, number_of_dice)

            roll = RollDice(
                f"{number_of_dice}d{number_of_sides}l{l_val}+{modifier}")
            result1 = roll.value
            roll.advantage()
            result2 = roll.value

            self.assertTrue(
                l_val
                <= result1 <= result2
                <= (l_val * number_of_sides) + modifier
            )

    def test_disadvantage_raw_number(self):
        for _ in range(1, 101):
            roll = RollDice(str(_))
            result1 = roll.value
            roll.disadvantage()
            result2 = roll.value
            self.assertEqual(result1, result2)

    def test_disadvantage_standard(self):
        for _ in range(1, 101):
            number_of_dice = random.randint(1, 101)
            number_of_sides = random.randint(1, 101)

            roll = RollDice(f"{number_of_dice}d{number_of_sides}")
            result1 = roll.value
            roll.disadvantage()
            result2 = roll.value

            self.assertTrue(
                number_of_dice
                <= result2 <= result1
                <= number_of_dice * number_of_sides
            )

    def test_disadvantage_standard_with_modifier(self):
        for _ in range(1, 101):
            number_of_dice = random.randint(1, 101)
            number_of_sides = random.randint(1, 101)
            modifier = random.randint(1, 101)

            roll = RollDice(f"{number_of_dice}d{number_of_sides}+{modifier}")
            result1 = roll.value
            roll.disadvantage()
            result2 = roll.value

            self.assertTrue(
                number_of_dice + modifier
                <= result2 <= result1
                <= (number_of_dice * number_of_sides) + modifier
            )

    def test_disadvantage_k_without_modifier(self):
        for _ in range(1, 101):
            number_of_dice = random.randint(1, 101)
            number_of_sides = random.randint(1, 101)

            k_val = random.randint(1, number_of_dice)

            roll = RollDice(f"{number_of_dice}d{number_of_sides}k{k_val}")
            result1 = roll.value
            roll.disadvantage()
            result2 = roll.value

            self.assertTrue(
                k_val
                <= result2 <= result1
                <= (k_val * number_of_sides)
            )

    def test_disadvantage_l_without_modifier(self):
        for _ in range(1, 101):
            number_of_dice = random.randint(1, 101)
            number_of_sides = random.randint(1, 101)

            l_val = random.randint(1, number_of_dice)

            roll = RollDice(f"{number_of_dice}d{number_of_sides}l{l_val}")
            result1 = roll.value
            roll.disadvantage()
            result2 = roll.value

            self.assertTrue(
                l_val
                <= result2 <= result1
                <= (l_val * number_of_sides)
            )

    def test_disadvantage_k_with_modifier(self):
        for _ in range(1, 101):
            number_of_dice = random.randint(1, 101)
            number_of_sides = random.randint(1, 101)
            modifier = random.randint(1, 101)

            k_val = random.randint(1, number_of_dice)

            roll = RollDice(
                f"{number_of_dice}d{number_of_sides}k{k_val}+{modifier}")
            result1 = roll.value
            roll.disadvantage()
            result2 = roll.value

            self.assertTrue(
                k_val
                <= result2 <= result1
                <= (k_val * number_of_sides) + modifier
            )

    def test_disadvantage_l_with_modifier(self):
        for _ in range(1, 101):
            number_of_dice = random.randint(1, 101)
            number_of_sides = random.randint(1, 101)
            modifier = random.randint(1, 101)

            l_val = random.randint(1, number_of_dice)

            roll = RollDice(
                f"{number_of_dice}d{number_of_sides}l{l_val}+{modifier}")
            result1 = roll.value
            roll.disadvantage()
            result2 = roll.value

            self.assertTrue(
                l_val
                <= result2 <= result1
                <= (l_val * number_of_sides) + modifier
            )

if __name__ == "__main__":
    print(RollDice("1d20*1d20").value)
    print(RollDice("1d20+1d20").average)
    unittest.main()
