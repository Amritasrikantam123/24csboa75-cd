import re

class ASTNode:
    def __init__(self, node_type, value=None, children=None):
        self.type = node_type
        self.value = value
        self.children = children or []

def tokenize(text):
    text = text.lower()
    return re.findall(r'[a-z]+|\d+', text)

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

def semantic_validation(ast):
    symbol_table = set()

    for node in ast:
        if node.type == "declare":
            if node.value in symbol_table:
                raise Exception(f"Variable '{node.value}' already declared")
            symbol_table.add(node.value)

        elif node.type == "assign":
            l, o, r = node.children
            if l not in symbol_table:
                raise Exception(f"Variable '{l}' not declared")
            if r not in symbol_table and not str(r).isdigit():
                raise Exception(f"Variable '{r}' not declared")
            symbol_table.add(node.value)

        elif node.type == "print":
            if node.value not in symbol_table:
                raise Exception(f"Variable '{node.value}' not declared")

def generate_ir(ast):
    ir = []
    for node in ast:
        if node.type == "declare":
            ir.append(("DECLARE", node.value, node.children[0]))
        elif node.type == "assign":
            l, o, r = node.children
            ir.append(("ASSIGN", node.value, l, o, r))
        elif node.type == "print":
            ir.append(("PRINT", node.value))
    return ir

def generate_code_from_ir(ir):
    code = []
    ops = {
        "plus": "+",
        "minus": "-",
        "times": "*",
        "divide": "/"
    }

    for instr in ir:
        if instr[0] == "DECLARE":
            code.append(f"{instr[1]} = {instr[2]}")
        elif instr[0] == "ASSIGN":
            _, target, l, o, r = instr
            op_symbol = ops[o]
            code.append(f"{target} = {l} {op_symbol} {r}")
        elif instr[0] == "PRINT":
            code.append(f"print({instr[1]})")

    return "\n".join(code)

def compile_nl_to_code(text):
    tokens = tokenize(text)
    print("\nTokens:", tokens)

    ast = parse(tokens)
    print("\nAST:")
    for node in ast:
        print(vars(node))

    semantic_validation(ast)

    ir = generate_ir(ast)
    print("\nIR:")
    for instr in ir:
        print(instr)

    return generate_code_from_ir(ir)

print("=== MiniLang Compiler Interactive Mode ===")
print("Enter your English-like statements line by line.")
print("Type 'RUN' on a new line to execute the program.")
print("Type 'EXIT' to quit.\n")

program_lines = []

while True:
    line = input(">> ").strip()
    
    if line.upper() == "EXIT":
        print("Exiting...")
        break
    elif line.upper() == "RUN":
        try:
            program = "\n".join(program_lines)
            code = compile_nl_to_code(program)
            print("\n--- Generated Python Code ---")
            print(code)
            print("\n--- Output ---")
            exec(code)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            program_lines = []
            print("\nYou can enter a new program now.")
    else:
        program_lines.append(line)