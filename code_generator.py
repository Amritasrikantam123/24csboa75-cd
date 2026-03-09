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