import unittest
import dice
import random

class DiceTestCase(unittest.TestCase):
    def test_raw_number(self):
        for _ in range(1, 101):
            self.assertEqual(dice.roll(str(_)), _)

    def test_k_gt_n(self):
        for _ in range(1, 101):
            number_of_dice = random.randint(1, 101)
            number_of_sides = random.randint(1, 101)

            k_val = number_of_dice + random.randint(1, 101)

            self.assertRaises(
                ValueError, dice.roll, f"{number_of_dice}d{number_of_sides}k{k_val}"
            )

    def test_l_gt_n(self):
        for _ in range(1, 101):
            number_of_dice = random.randint(1, 101)
            number_of_sides = random.randint(1, 101)

            l_val = number_of_dice + random.randint(1, 101)

            self.assertRaises(
                ValueError, dice.roll, f"{number_of_dice}d{number_of_sides}l{l_val}"
            )

    def test_standard(self):
        for _ in range(1, 101):
            number_of_dice = random.randint(1, 101)
            number_of_sides = random.randint(1, 101)

            self.assertTrue(
                number_of_dice
                <= dice.roll(f"{number_of_dice}d{number_of_sides}")
                <= number_of_dice * number_of_sides
            )

    def test_standard_with_modifier(self):
        for _ in range(1, 101):
            number_of_dice = random.randint(1, 101)
            number_of_sides = random.randint(1, 101)
            modifier = random.randint(1, 101)

            self.assertTrue(
                number_of_dice + modifier
                <= dice.roll(f"{number_of_dice}d{number_of_sides}+{modifier}")
                <= (number_of_dice * number_of_sides) + modifier
            )

    def test_k_without_modifier(self):
        for _ in range(1, 101):
            number_of_dice = random.randint(1, 101)
            number_of_sides = random.randint(1, 101)

            k_val = random.randint(1, number_of_dice)

            self.assertTrue(
                k_val
                <= dice.roll(f"{number_of_dice}d{number_of_sides}k{k_val}")
                <= (k_val * number_of_sides)
            )

    def test_l_without_modifier(self):
        for _ in range(1, 101):
            number_of_dice = random.randint(1, 101)
            number_of_sides = random.randint(1, 101)

            l_val = random.randint(1, number_of_dice)

            self.assertTrue(
                l_val
                <= dice.roll(f"{number_of_dice}d{number_of_sides}l{l_val}")
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
                <= dice.roll(f"{number_of_dice}d{number_of_sides}k{k_val}+{modifier}")
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
                <= dice.roll(f"{number_of_dice}d{number_of_sides}l{l_val}+{modifier}")
                <= (l_val * number_of_sides) + modifier
            )

    def test_advantage_raw_number(self):
        for _ in range(1, 101):
            roll = dice.RollDice(str(_))
            result1 = roll.value
            roll.advantage()
            result2 = roll.value
            self.assertEqual(result1, result2)

    def test_advantage_standard(self):
        for _ in range(1, 101):
            number_of_dice = random.randint(1, 101)
            number_of_sides = random.randint(1, 101)

            roll = dice.RollDice(f"{number_of_dice}d{number_of_sides}")
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

            roll = dice.RollDice(f"{number_of_dice}d{number_of_sides}+{modifier}")
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

            roll = dice.RollDice(f"{number_of_dice}d{number_of_sides}k{k_val}")
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

            roll = dice.RollDice(f"{number_of_dice}d{number_of_sides}l{l_val}")
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

            roll = dice.RollDice(
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

            roll = dice.RollDice(
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
            roll = dice.RollDice(str(_))
            result1 = roll.value
            roll.disadvantage()
            result2 = roll.value
            self.assertEqual(result1, result2)

    def test_disadvantage_standard(self):
        for _ in range(1, 101):
            number_of_dice = random.randint(1, 101)
            number_of_sides = random.randint(1, 101)

            roll = dice.RollDice(f"{number_of_dice}d{number_of_sides}")
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

            roll = dice.RollDice(f"{number_of_dice}d{number_of_sides}+{modifier}")
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

            roll = dice.RollDice(f"{number_of_dice}d{number_of_sides}k{k_val}")
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

            roll = dice.RollDice(f"{number_of_dice}d{number_of_sides}l{l_val}")
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

            roll = dice.RollDice(
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

            roll = dice.RollDice(
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
    print(dice.RollDice("1d20*1d20").value)
    print(dice.RollDice("1d20+1d20").average)
    unittest.main()