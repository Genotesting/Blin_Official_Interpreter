import os

# ======================================== #
# ================= Blin ================= #
# ============== Binary Line============== #

filename = "blin_code.txt"

try:
    with open(filename, "r") as f:
        code = f.read()
except FileNotFoundError:
    print(f"Error: '{filename}' not found")
    exit()

tokens = []
i = 0
while i < len(code):
    if code[i:i+3] == "@$#":
        i += 3
        while i < len(code) and code[i:i+3] != "#$@":
            i += 1
        i += 3 if i < len(code) else 0
    elif code[i] == "_":
        tokens.append("_")
        i += 1
    elif code[i].isspace():
        i += 1
    elif code[i:i+5] == "{Bin}":
        tokens.append("{Bin}")
        i += 5
    else:
        tokens.append(code[i])
        i += 1

def to_bool(token):
    if token == "+":
        return True
    elif token == "-":
        return False
    else:
        raise ValueError(f"Invalid boolean token '{token}'")

def execute(tokens):
    stack = []
    output_buffer = []
    last_bin_index = -1

    def exec_block(block, depth=0):
        nonlocal last_bin_index
        i = 0
        while i < len(block):
            token = block[i]
            try:
                if token in "+-":
                    stack.append(to_bool(token))
                elif token == "!":
                    if not stack:
                        raise ValueError(f"NOT (!) with empty stack at pos {i}")
                    stack.append(not stack.pop())
                elif token == "&":
                    if len(stack) < 2:
                        raise ValueError(f"AND (&) with <2 items at pos {i}")
                    b, a = stack.pop(), stack.pop()
                    stack.append(a and b)
                elif token == "|":
                    if len(stack) < 2:
                        raise ValueError(f"OR (|) with <2 items at pos {i}")
                    b, a = stack.pop(), stack.pop()
                    stack.append(a or b)
                elif token == "^":
                    if len(stack) < 2:
                        raise ValueError(f"XOR (^) with <2 items at pos {i}")
                    b, a = stack.pop(), stack.pop()
                    stack.append(a != b)
                elif token == "?":
                    if not stack:
                        raise ValueError(f"Ternary (?) with empty stack at pos {i}")
                    cond = stack.pop()
                    true_block = []
                    false_block = []
                    i += 1
                    while i < len(block) and block[i] != "_":
                        true_block.append(block[i])
                        i += 1
                    i += 1
                    while i < len(block) and block[i] != "_":
                        false_block.append(block[i])
                        i += 1
                    exec_block(true_block if cond else false_block, depth+1)
                elif token == "*":
                    if not stack:
                        raise ValueError(f"Loop (*) with empty stack at pos {i}")
                    body_start = i + 1
                    body_block = []
                    i += 1
                    while i < len(block) and block[i] != "_":
                        body_block.append(block[i])
                        i += 1
                    while stack and stack[-1]:
                        exec_block(body_block, depth+1)
                        stack.pop()
                elif token == ".":
                    bits_collected = []
                    j = i + 1
                    while j < len(block) and len(bits_collected) < 8:
                        if block[j] in "+-":
                            bits_collected.append(block[j])
                        j += 1
                    if len(bits_collected) < 8:
                        raise ValueError(f"Not enough bits for output at pos {i}")
                    byte = 0
                    for bit in bits_collected:
                        byte = (byte << 1) | (1 if bit == "+" else 0)
                    output_buffer.append(chr(byte))
                    i = j - 1
                elif token == "_":
                    pass
                elif token == "{Bin}":
                    bin_output = []
                    start_index = last_bin_index + 1
                    for tok in block[start_index:i]:
                        if tok == "+":
                            bin_output.append("1")
                        elif tok == "-":
                            bin_output.append("0")
                        elif tok == "_":
                            bin_output.append(" ")
                    print("".join(bin_output))
                    last_bin_index = i
                else:
                    raise ValueError(f"Unknown token '{token}' at pos {i}")
            except ValueError as e:
                print("Execution error:", e)
                return
            i += 1

    exec_block(tokens)
    if output_buffer:
        print("Output:", "".join(output_buffer))
    print("Final stack:", stack)

try:
    execute(tokens)
except Exception as e:
    print("Fatal error:", e)

input("\nExecution finished. Press Enter to exit...")
