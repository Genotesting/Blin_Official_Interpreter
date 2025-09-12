"""
Blin Official Interpreter
========================
Author: Geno
Language: Blin (Binary Line)
Version: 1.0.0
Description: Official Python interpreter for the esolang Blin.
"""

import os
import sys

# ======================================== #
# ================= Blin ================= #
# ============== Binary Line============== #

FILENAME = "blin_code.txt"

def read_code(filename):
    """Read Blin source code from a file."""
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Error: '{filename}' not found")
    with open(filename, "r") as f:
        return f.read()

def tokenize(code):
    """Convert raw Blin code into a list of tokens."""
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
    return tokens

def to_bool(token):
    """Convert '+' or '-' token into Boolean value."""
    if token == "+":
        return True
    elif token == "-":
        return False
    else:
        raise ValueError(f"Invalid boolean token '{token}'")

class BlinInterpreter:
    def __init__(self, tokens):
        self.tokens = tokens
        self.stack = []
        self.output_buffer = []
        self.last_bin_index = -1

    def execute(self):
        """Execute the full token stream."""
        try:
            self._exec_block(self.tokens)
            if self.output_buffer:
                print("Output:", "".join(self.output_buffer))
            print("Final stack:", self.stack)
        except Exception as e:
            print("Fatal error:", e)

    def _exec_block(self, block, depth=0):
        """Execute a block of tokens recursively."""
        i = 0
        while i < len(block):
            token = block[i]
            try:
                if token in "+-":
                    self.stack.append(to_bool(token))
                elif token == "!":
                    self._unary_op(lambda x: not x, "NOT", i)
                elif token in "&|^":
                    self._binary_op(token, i)
                elif token == "?":
                    i = self._ternary_op(block, i)
                elif token == "*":
                    i = self._loop_op(block, i)
                elif token == ".":
                    i = self._output_byte(block, i)
                elif token == "_":
                    pass
                elif token == "{Bin}":
                    self._binary_output(block, i)
                else:
                    raise ValueError(f"Unknown token '{token}' at pos {i}")
            except ValueError as e:
                print("Execution error:", e)
                return
            i += 1

    def _unary_op(self, func, name, pos):
        if not self.stack:
            raise ValueError(f"{name} with empty stack at pos {pos}")
        self.stack.append(func(self.stack.pop()))

    def _binary_op(self, token, pos):
        if len(self.stack) < 2:
            raise ValueError(f"{token} with <2 items at pos {pos}")
        b, a = self.stack.pop(), self.stack.pop()
        if token == "&":
            self.stack.append(a and b)
        elif token == "|":
            self.stack.append(a or b)
        elif token == "^":
            self.stack.append(a != b)

    def _ternary_op(self, block, i):
        if not self.stack:
            raise ValueError(f"Ternary (?) with empty stack at pos {i}")
        cond = self.stack.pop()
        true_block, false_block = [], []
        i += 1
        while i < len(block) and block[i] != "_":
            true_block.append(block[i])
            i += 1
        i += 1
        while i < len(block) and block[i] != "_":
            false_block.append(block[i])
            i += 1
        self._exec_block(true_block if cond else false_block)
        return i

    def _loop_op(self, block, i):
        if not self.stack:
            raise ValueError(f"Loop (*) with empty stack at pos {i}")
        body_block = []
        i += 1
        while i < len(block) and block[i] != "_":
            body_block.append(block[i])
            i += 1
        while self.stack and self.stack[-1]:
            self._exec_block(body_block)
            self.stack.pop()
        return i

    def _output_byte(self, block, i):
        bits = []
        j = i + 1
        while j < len(block) and len(bits) < 8:
            if block[j] in "+-":
                bits.append(block[j])
            j += 1
        if len(bits) < 8:
            raise ValueError(f"Not enough bits for output at pos {i}")
        byte = sum((1 if bit == "+" else 0) << (7-k) for k, bit in enumerate(bits))
        self.output_buffer.append(chr(byte))
        return j - 1

    def _binary_output(self, block, i):
        bin_output = []
        start_index = self.last_bin_index + 1
        for tok in block[start_index:i]:
            if tok == "+":
                bin_output.append("1")
            elif tok == "-":
                bin_output.append("0")
            elif tok == "_":
                bin_output.append(" ")
        print("".join(bin_output))
        self.last_bin_index = i

def main():
    try:
        code = read_code(FILENAME)
        tokens = tokenize(code)
        interpreter = BlinInterpreter(tokens)
        interpreter.execute()
    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print("Fatal error:", e)
    finally:
        input("\nExecution finished. Press Enter to exit...")

if __name__ == "__main__":
    main()
