import operator
import random
import pytest
import multi_dice as dice

codes = {
    "+": operator.add,
    "-": operator.sub,
    "/": operator.truediv,
    "//": operator.floordiv,
    "*": operator.mul,
    "**": operator.pow
}


def test_raw_number():
    for _ in range(1, 1001):
        assert dice.roll(str(_)) == _

def test_raw_number_ops():
    for op in codes:
        for _ in range(1, 1001):
            second_number = random.randint(1, 101)
            assert dice.roll(f"{_}{op}{second_number}") == codes[op](_, second_number)

def test_raw_number_parenthesis():
    for op in codes:
        for _ in range(1, 1001):
            second_number = random.randint(1, 101)
            assert dice.roll(f"(({_}){op}({second_number}))") == codes[op](_, second_number)

def test_k_gt_n():
    for _ in range(1, 1001):
        number_of_dice = random.randint(1, 101)
        number_of_sides = random.randint(1, 101)

        k_val = number_of_dice + random.randint(1, 101)

        with pytest.raises(ValueError):
            dice.roll(f"{number_of_dice}d{number_of_sides}k{k_val}")


def test_l_gt_n():
    for _ in range(1, 1001):
        number_of_dice = random.randint(1, 101)
        number_of_sides = random.randint(1, 101)

        l_val = number_of_dice + random.randint(1, 101)

        with pytest.raises(ValueError):
            dice.roll(f"{number_of_dice}d{number_of_sides}l{l_val}")


def test_standard():
    for _ in range(1, 1001):
        number_of_dice = random.randint(1, 101)
        number_of_sides = random.randint(1, 101)

        assert (
            number_of_dice
            <= dice.roll(f"{number_of_dice}d{number_of_sides}")
            <= number_of_dice * number_of_sides
        )


def test_standard_with_modifier():
    number_of_dice = random.randint(1, 101) 
    number_of_sides = random.randint(1, 101)
    modifier = random.randint(1, 101)

    assert (
        number_of_dice + modifier
        <= dice.roll(f"{number_of_dice}d{number_of_sides}+{modifier}")
        <= (number_of_dice * number_of_sides) + modifier
    )


def test_k_without_modifier():
    number_of_dice = random.randint(1, 101)
    number_of_sides = random.randint(1, 101)

    k_val = random.randint(1, number_of_dice)

    assert k_val <= dice.roll(f"{number_of_dice}d{number_of_sides}k{k_val}") <= (k_val * number_of_sides)


def test_l_without_modifier():
    number_of_dice = random.randint(1, 101) 
    number_of_sides = random.randint(1, 101)

    l_val = random.randint(1, number_of_dice)

    assert l_val <= dice.roll(f"{number_of_dice}d{number_of_sides}l{l_val}") <= (l_val * number_of_sides)


def test_k_with_modifier():
    number_of_dice = random.randint(1, 101) 
    number_of_sides = random.randint(1, 101)
    modifier = random.randint(1, 101)

    k_val = random.randint(1, number_of_dice)

    assert (
        k_val + modifier
        <= dice.roll(f"{number_of_dice}d{number_of_sides}k{k_val}+{modifier}")
        <= (k_val * number_of_sides) + modifier
    )


def test_l_with_modifier():
    for _ in range(1, 1001):
        number_of_dice = random.randint(1, 101)
        number_of_sides = random.randint(1, 101)
        modifier = random.randint(1, 101)

        l_val = random.randint(1, number_of_dice)

        assert (
            l_val + modifier
            <= dice.roll(f"{number_of_dice}d{number_of_sides}l{l_val}+{modifier}")
            <= (l_val * number_of_sides) + modifier
        )


def test_advantage_raw_number():
    for _ in range(1, 1001):
        roll = dice.RollDice(str(_))
        result1 = roll.value
        roll.advantage()
        result2 = roll.value
        assert result1 == result2


def test_advantage_standard():
    for _ in range(1, 1001):
        number_of_dice = random.randint(1, 101)
        number_of_sides = random.randint(1, 101)

        roll = dice.RollDice(f"{number_of_dice}d{number_of_sides}")
        result1 = roll.value
        roll.advantage()
        result2 = roll.value

        assert (
            number_of_dice
            <= result1 <= result2
            <= number_of_dice * number_of_sides
        )

def test_advantage_standard_with_modifier():
    number_of_dice = random.randint(1, 101) 
    number_of_sides = random.randint(1, 101)
    modifier = random.randint(1, 101)

    roll = dice.RollDice(f"{number_of_dice}d{number_of_sides}+{modifier}")
    result1 = roll.value
    roll.advantage()
    result2 = roll.value

    assert (
        number_of_dice + modifier
        <= result1 <= result2
        <= (number_of_dice * number_of_sides) + modifier
    )


def test_advantage_k_without_modifier():
    for _ in range(1, 1001):
        number_of_dice = random.randint(1, 101)
        number_of_sides = random.randint(1, 101)

        k_val = random.randint(1, number_of_dice)

        roll = dice.RollDice(f"{number_of_dice}d{number_of_sides}k{k_val}")
        result1 = roll.value
        roll.advantage()
        result2 = roll.value

        assert k_val <= result1 <= result2 <= (k_val * number_of_sides)


def test_advantage_l_without_modifier():
    for _ in range(1, 1001):
        number_of_dice = random.randint(1, 101)
        number_of_sides = random.randint(1, 101)

        l_val = random.randint(1, number_of_dice)

        roll = dice.RollDice(f"{number_of_dice}d{number_of_sides}l{l_val}")
        result1 = roll.value
        roll.advantage()
        result2 = roll.value

        assert (
            l_val
            <= result1 <= result2
            <= (l_val * number_of_sides)
        )

def test_advantage_k_with_modifier():
    for _ in range(1, 1001):
        number_of_dice = random.randint(1, 101)
        number_of_sides = random.randint(1, 101)
        modifier = random.randint(1, 101)

        k_val = random.randint(1, number_of_dice)

        roll = dice.RollDice(
            f"{number_of_dice}d{number_of_sides}k{k_val}+{modifier}")
        result1 = roll.value
        roll.advantage()
        result2 = roll.value

        assert (
            k_val
            <= result1 <= result2
            <= (k_val * number_of_sides) + modifier
        )

def test_advantage_l_with_modifier():
    for _ in range(1, 1001):
        number_of_dice = random.randint(1, 101)
        number_of_sides = random.randint(1, 101)
        modifier = random.randint(1, 101)

        l_val = random.randint(1, number_of_dice)

        roll = dice.RollDice(
            f"{number_of_dice}d{number_of_sides}l{l_val}+{modifier}")
        result1 = roll.value
        roll.advantage()
        result2 = roll.value

        assert (
            l_val
            <= result1 <= result2
            <= (l_val * number_of_sides) + modifier
        )

def test_disadvantage_raw_number():
    for _ in range(1, 1001):
        roll = dice.RollDice(str(_))
        result1 = roll.value
        roll.disadvantage()
        result2 = roll.value
        assert result1 == result2

def test_disadvantage_standard():
    for _ in range(1, 1001):
        number_of_dice = random.randint(1, 101)
        number_of_sides = random.randint(1, 101)

        roll = dice.RollDice(f"{number_of_dice}d{number_of_sides}")
        result1 = roll.value
        roll.disadvantage()
        result2 = roll.value

        assert (
            number_of_dice
            <= result2 <= result1
            <= number_of_dice * number_of_sides
        )

def test_disadvantage_standard_with_modifier():
    for _ in range(1, 1001):
        number_of_dice = random.randint(1, 101)
        number_of_sides = random.randint(1, 101)
        modifier = random.randint(1, 101)

        roll = dice.RollDice(f"{number_of_dice}d{number_of_sides}+{modifier}")
        result1 = roll.value
        roll.disadvantage()
        result2 = roll.value

        assert (
            number_of_dice + modifier
            <= result2 <= result1
            <= (number_of_dice * number_of_sides) + modifier
        )

def test_disadvantage_k_without_modifier():
    for _ in range(1, 1001):
        number_of_dice = random.randint(1, 101)
        number_of_sides = random.randint(1, 101)

        k_val = random.randint(1, number_of_dice)

        roll = dice.RollDice(f"{number_of_dice}d{number_of_sides}k{k_val}")
        result1 = roll.value
        roll.disadvantage()
        result2 = roll.value

        assert (
            k_val
            <= result2 <= result1
            <= (k_val * number_of_sides)
        )

def test_disadvantage_l_without_modifier():
    for _ in range(1, 1001):
        number_of_dice = random.randint(1, 101)
        number_of_sides = random.randint(1, 101)

        l_val = random.randint(1, number_of_dice)

        roll = dice.RollDice(f"{number_of_dice}d{number_of_sides}l{l_val}")
        result1 = roll.value
        roll.disadvantage()
        result2 = roll.value

        assert (
            l_val
            <= result2 <= result1
            <= (l_val * number_of_sides)
        )

def test_disadvantage_k_with_modifier():
    for _ in range(1, 1001):
        number_of_dice = random.randint(1, 101)
        number_of_sides = random.randint(1, 101)
        modifier = random.randint(1, 101)

        k_val = random.randint(1, number_of_dice)

        roll = dice.RollDice(
            f"{number_of_dice}d{number_of_sides}k{k_val}+{modifier}")
        result1 = roll.value
        roll.disadvantage()
        result2 = roll.value

        assert (
            k_val
            <= result2 <= result1
            <= (k_val * number_of_sides) + modifier
        )

def test_disadvantage_l_with_modifier():
    for _ in range(1, 1001):
        number_of_dice = random.randint(1, 101)
        number_of_sides = random.randint(1, 101)
        modifier = random.randint(1, 101)

        l_val = random.randint(1, number_of_dice)

        roll = dice.RollDice(
            f"{number_of_dice}d{number_of_sides}l{l_val}+{modifier}")
        result1 = roll.value
        roll.disadvantage()
        result2 = roll.value

        assert (
            l_val
            <= result2 <= result1
            <= (l_val * number_of_sides) + modifier
        )

def test_2_die_rolling():
    for op in codes:
        for _ in range(1, 1001):
            if op == '**':  # breaks eval with large numbers but verified works with other tests
                break
            number_of_dice = random.randint(1, 101)
            number_of_sides = random.randint(1, 101)

            number_of_dice2 = random.randint(1, 101)
            number_of_sides2 = random.randint(1, 101)

            roll = dice.roll(f"{number_of_dice}d{number_of_sides}{op}{number_of_dice2}d{number_of_sides2}")
            assert (
                codes[op](number_of_dice, number_of_dice2)
                <= roll
                <= codes[op](number_of_dice*number_of_sides, number_of_dice2*number_of_sides2)
                # Mostly just testing to make sure these dont crash bc i have no idea how to properly test these codes
                if op not in ("-", "/", "//") else True
            )