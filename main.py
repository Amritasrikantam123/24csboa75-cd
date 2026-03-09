from compiler import compile_nl_to_code

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