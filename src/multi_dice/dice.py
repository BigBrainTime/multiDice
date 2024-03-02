import ast
import random
import re

# Class to roll dice and calculate results
class RollDice:
    def __init__(self, dice: str = "1d6", crit: int = 20) -> None:
        dice: str = dice.replace(" ","").replace("^","**")
        self.dice: str = dice
        self.crit_val:int  = crit

        # If dice starts with "a", call roll() and advantage()
        if dice.startswith('a'):
            self.parse_dice()
            self.advantage()

        # If dice starts with "d", call roll() and disadvantage()
        elif dice.startswith('d'):
            self.parse_dice()
            self.disadvantage()

        # Otherwise just call roll()
        else:
            self.parse_dice()

    # Check dice string for operators
    def parse_dice(self):
        dice: str = str((self.dice.replace('d', '',1) if self.dice.startswith('d') else self.dice).replace('a', ''))
        dicecopy: str = str(dice)
        averagecopy: str = str(dice)
        minimumcopy: str = str(dice)
        maximumcopy: str = str(dice)
        parts: list = re.findall("[^+*/()-]+", dice)
        self.rolls: list = []
        for part in parts:
            if part != '':
                part_value: dict = self.roll(part)
                dicecopy: str = dicecopy.replace(part, str(part_value['value']), 1)
                averagecopy: str = averagecopy.replace(part, str(part_value['average']), 1)
                minimumcopy: str = minimumcopy.replace(part, str(part_value['minimum']), 1)
                maximumcopy: str = maximumcopy.replace(part, str(part_value['maximum']), 1)

        validate_expression(dicecopy)
        validate_expression(averagecopy)
        validate_expression(minimumcopy)
        validate_expression(maximumcopy)
        self.value: int = eval(dicecopy, {}, {})
        self.average: int = eval(averagecopy, {}, {})
        self.minimum: int = eval(minimumcopy, {}, {})
        self.maximum: int = eval(maximumcopy, {}, {})
        self.data: dict = {
            "die": self.dice,
            "rolls": self.rolls,
            "value": self.value,
            "crit": self.crit,
            "average": self.average,
            "minimum": self.minimum,
            "maximum": self.maximum
        }

    # Roll dice and calculate results
    def roll(self, die):
        if "d" not in die:
            die = int(die)
            self.rolls = [die]
            self.crit = False
            roll_result = {
                "value": die,
                "average": die,
                "minimum": die,
                "maximum": die,
            }
            return roll_result
        
        split_d = die.split("d")

        # Get number of dice and sides
        rolladvantage = False
        rolldisadvantage = False
        if split_d[0].startswith("A"):
            rolladvantage = True
            split_d[0] = split_d[0][1:]
        elif split_d[0].startswith("D"):
            rolldisadvantage = True
            split_d[0] = split_d[0][1:]

        number_of_dice = int(split_d[0])
        die_sides = split_d[1]

        # Check for keeping highest/lowest rolls
        k_value = number_of_dice

        reverse_sort = False
        if "k" in die_sides:
            die_sides, k_value = die_sides.split("k")
            k_value = int(k_value)
            reverse_sort = True
        elif "l" in die_sides:
            die_sides, k_value = die_sides.split("l")
            k_value = int(k_value)

        die_sides = int(die_sides)

        # Validate inputs
        if number_of_dice > 1000 or die_sides > 1000 or k_value > number_of_dice:
            raise ValueError

        # Roll dice
        self.crit = False
        rolls = []
        for c in range(number_of_dice):
            roll = random.randint(1, die_sides)
            self.crit = True if roll >= self.crit_val else self.crit
            rolls.append(roll)
        total = sum(sorted(rolls, reverse=reverse_sort)[:k_value])

        if rolladvantage or rolldisadvantage:
            secondrolls = []
            for c in range(number_of_dice):
                roll = random.randint(1, die_sides)
                secondcrit = True if roll >= self.crit_val else self.crit
                secondrolls.append(roll)
            secondtotal = sum(sorted(secondrolls, reverse=reverse_sort)[:k_value])

            if rolladvantage and secondtotal > total:
                total = secondtotal
                rolls = secondrolls
                self.crit = secondcrit

            elif rolldisadvantage and secondtotal < total:
                total = secondtotal
                rolls = secondrolls
                self.crit = secondcrit

        for value in rolls:
            self.rolls.append(value)

        # Calculate results
        roll_result = {
            "value":total,
            "average":(k_value * die_sides + 1) / 2,
            "minimum": k_value,
            "maximum":number_of_dice * die_sides,
        }
        return roll_result

    # Reroll with advantage
    def advantage(self):
        roll = RollDice(self.dice.replace('a',''), self.crit_val)
        if roll.value >= self.value:
            self.value = roll.value
            self.rolls = roll.rolls
            self.crit = roll.crit

    # Reroll with disadvantage
    def disadvantage(self):
        roll = RollDice(self.dice.replace('d','', 1) if self.dice.startswith('d') else self.dice, self.crit_val)
        if roll.value <= self.value:
            self.value = roll.value
            self.rolls = roll.rolls
            self.crit = roll.crit

    def __str__(self):
        return str(self.data)


def roll(dice: str = "1d6") -> int:
    """Rolls dice and returns only an int

    Args:
        dice (str): Required: '(int)d(int)' Optional parameters:[k(int),('+', '*', '/', '//', '-', '**')(int||roll)]

    Returns:
        Int
    """
    return RollDice(dice).value


def advantage(func, *args, **kwargs) -> int:
    """Calls a function twice and returns higher value

    Args:
        func (function): The function
        *args: the arguments for the function

    Returns:
        (int): Highest int value
    """
    return max(func(*args, **kwargs), func(*args, **kwargs))


def disadvantage(func, *args, **kwargs) -> int:
    """Calls a function twice and returns lower value

    Args:
        func (function): The function
        *args: the arguments for the function

    Returns:
        (int): lowest int value
    """
    return min(func(*args, **kwargs), func(*args, **kwargs))


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
    print(RollDice("aA1d20*A1d20"))
    print(RollDice("a(A1d12+A1d6)**3"))
    print(roll("1+1"))
