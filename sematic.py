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