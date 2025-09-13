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
