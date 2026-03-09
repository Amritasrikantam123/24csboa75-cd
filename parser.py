from astnode import ASTNode

def parse(tokens):
    ast = []
    i = 0

    while i < len(tokens):

        if tokens[i] == 'create':
            if i + 5 >= len(tokens):
                raise SyntaxError("Incomplete create statement")

            if tokens[i+1] != 'variable' or tokens[i+3] != 'with' or tokens[i+4] != 'value':
                raise SyntaxError("Invalid create syntax")

            if not tokens[i+5].isdigit():
                raise SyntaxError("Value must be integer")

            var = tokens[i+2]
            val = int(tokens[i+5])

            ast.append(ASTNode("declare", var, [val]))
            i += 6

        elif tokens[i] == 'set':
            if i + 5 >= len(tokens):
                raise SyntaxError("Incomplete set statement")

            if tokens[i+2] != 'to':
                raise SyntaxError("Missing 'to' in set statement")

            var = tokens[i+1]
            left = tokens[i+3]
            op = tokens[i+4]
            right = tokens[i+5]

            if op not in ["plus", "minus", "times", "divide"]:
                raise SyntaxError("Invalid operator")

            ast.append(ASTNode("assign", var, [left, op, right]))
            i += 6

        elif tokens[i] == 'print':
            if i + 1 >= len(tokens):
                raise SyntaxError("Print missing variable")

            ast.append(ASTNode("print", tokens[i+1]))
            i += 2

        else:
            raise SyntaxError("Invalid English statement")

    return ast