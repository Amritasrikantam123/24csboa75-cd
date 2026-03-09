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