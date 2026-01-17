#!/usr/bin/env python3
import sys
import os
from Tokenizer import Tokenizer
from Interpreter import Interpreter

if len(sys.argv)<2:
    print("Usage: disassembly <filename>.ds")
    sys.exit(1)

filename = sys.argv[1]

if not filename.endswith(".ds"):
    print("Error[FILEERROR]: File must end with .ds")
    sys.exit(1)

if not os.path.isfile(filename):
    print(f"Error[FILEERROR]: '{filename}' not found")
    sys.exit(1)

pathdir = filename.split("/")
pathdir = "/".join(pathdir[:len(pathdir)-1])

with open(filename, "r") as f:
    code = f.read()

CodeLines = Tokenizer().HandleCode(code)
Interpreter(pathdir).Interpret(0,CodeLines)
