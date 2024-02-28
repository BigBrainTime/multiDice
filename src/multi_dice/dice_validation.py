import ast

# Thank you https://gist.github.com/nitori for the expression validation
class ValidateExpression(ast.NodeVisitor):
    allowed = (
        ast.Add,
        ast.Sub,
        ast.Mult,
        ast.FloorDiv,
        ast.Div,
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
            if not isinstance(node.value,int) and not isinstance(node.value,float):
                raise SyntaxError(f'Non Int or Float {type(node.value)}({node.value})')

        return super().visit(node)


def validate_expression(expr_str: str) -> None:
    expr_ast = ast.parse(expr_str, mode="eval")
    ValidateExpression().visit(expr_ast)