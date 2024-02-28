import ast
import random
import re

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
            self.check_op()
            self.advantage()

        # If dice starts with "d", call roll() and disadvantage()
        elif dice.startswith('d'):
            self.dice = dice[1:]
            self.check_op()
            self.disadvantage()

        # Otherwise just call roll()
        else:
            self.check_op()

    # Check dice string for operators
    def check_op(self):
        dicecopy = str(self.dice)
        averagecopy = str(self.dice)
        minimumcopy = str(self.dice)
        maximumcopy = str(self.dice)
        parts = re.findall("[^\+\-\*\/]*(?=$|[\+\-\*\/])", self.dice)
        for part in parts:
            if part != '':
                part_value = self.roll(part)
                dicecopy = dicecopy.replace(part, str(part_value['value']), 1)
                averagecopy = averagecopy.replace(part, str(part_value['average']), 1)
                minimumcopy = minimumcopy.replace(part, str(part_value['minimum']), 1)
                maximumcopy = maximumcopy.replace(part, str(part_value['maximum']), 1)

        validate_expression(dicecopy)
        validate_expression(averagecopy)
        validate_expression(minimumcopy)
        validate_expression(maximumcopy)
        self.value = eval(dicecopy, {}, {})
        self.average = eval(averagecopy, {}, {})
        self.minimum = eval(minimumcopy, {}, {})
        self.maximum = eval(maximumcopy, {}, {})

    # Roll dice and calculate results
    def roll(self, dice):
        if "d" not in dice:
            dice = int(dice)
            self.rolls = [dice]
            self.crit = False
            roll_result = {
                "value": dice,
                "average": dice,
                "minimum": dice,
                "maximum": dice,
            }
            return roll_result
        split_d = dice.split("d")

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
        roll_result = {
            "value":sum(sorted(self.rolls, reverse=reverse_sort)[:k_value]),
            "average":(number_of_dice * dice_sides + 1) / 2,
            "minimum":number_of_dice,
            "maximum":number_of_dice * dice_sides,
        }
        return roll_result

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


def roll(dice: str = "1d6") -> int:
    """Rolls dice

    Args:
        d (str): Required: '(int)d(int)' Optional parameters:[k(int),('+', '*', '/', '//', '-', '**')(int||roll)]

    Returns:
        Int
    """
    return RollDice(dice).value


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


# Thank you https://gist.github.com/nitori for the expression validation
class ValidateExpression(ast.NodeVisitor):
    allowed = (
        ast.Add,
        ast.Sub,
        ast.Mult,
        ast.FloorDiv,
        ast.Div,
        ast.Pow,
        ast.BinOp,
        ast.Expression,
        ast.Constant
    )

    def visit(self, node):
        if not isinstance(node, tuple(self.allowed)):
            raise SyntaxError(f"Invalid node: {node}")

        if isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name):
                # might not be ast.Name, e.g.: foo(bar)(spam)
                raise SyntaxError(f"Invalid function: {node.func}")

        if isinstance(node, ast.Constant):
            if not isinstance(node.value, int) and not isinstance(node.value, float):
                raise SyntaxError(
                    f'Non Int or Float {type(node.value)}({node.value})')

        return super().visit(node)


def validate_expression(expr_str: str) -> None:
    expr_ast = ast.parse(expr_str, mode="eval")
    ValidateExpression().visit(expr_ast)

if __name__ == "__main__":
    testdata = RollDice("1d20*1d20")
    print(testdata.value)
    print(testdata.average)
    print(RollDice("1d20+1d20").average)
