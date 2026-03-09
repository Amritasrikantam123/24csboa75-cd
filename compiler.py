from lexer import tokenize
from parser import parse
from sematic import semantic_validation
from ir_generator import generate_ir
from code_generator import generate_code_from_ir

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