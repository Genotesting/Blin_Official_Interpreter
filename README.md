# Blin Official Interpreter

**Official Python interpreter for the esolang Blin (Binary Line)**

This repository contains the official Python implementation of **Blin**, a stack-based esolang that uses binary logic (`+`/`-`) and structured control flow (`*`, `?`, `_`, `{Bin}`) for computation. This interpreter is the authoritative source for executing Blin programs.

---

## Table of Contents

1. [Introduction](#introduction)  
2. [Language Specification](#language-specification)  
3. [Installation](#installation)  
4. [Usage](#usage)  
5. [Interpreter Behavior and Credibility](#interpreter-behavior-and-credibility)  
6. [Contributing](#contributing)  
7. [License](#license)  

---

## Introduction

**Blin** is a binary-line esolang with stack-based logic. Programs consist of the following core elements:

- `+` : Boolean True  
- `-` : Boolean False  
- `_` : Block or token separator  
- `{Bin}` : Outputs the binary representation of tokens since the previous `{Bin}`  
- `!` : Logical NOT  
- `&` : Logical AND  
- `|` : Logical OR  
- `^` : Logical XOR  
- `?` : Conditional block execution (ternary-like)  
- `*` : Loop execution based on top-of-stack Boolean  
- `.` : Outputs the next 8 tokens as a character  

This interpreter **faithfully executes all valid Blin programs** and provides deterministic output with clear error messages for invalid operations.

---

## Language Specification

1. **Tokens**: All program elements are single-character or multi-character tokens: `+`, `-`, `_`, `{Bin}`, etc.  
2. **Stack Operations**: Blin is stack-based. All logic operations consume elements from the stack.  
3. **Control Flow**:  
   - `*` executes a block while the top of the stack is True  
   - `?` chooses between two blocks based on a top-of-stack Boolean  
4. **Output**:  
   - `.` outputs the next 8 binary tokens as a character  
   - `{Bin}` prints a binary representation of tokens since the last `{Bin}`  

This interpreter’s behavior is fully deterministic and matches the official language semantics.

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/Genotesting/Blin_Official_Interpreter.git
cd Blin_Official_Interpreter
