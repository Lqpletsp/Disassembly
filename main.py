from Tokenizer import Tokenizer 
from Interpreter import Interpreter



Code = """
decm 200; 
decv store int; 
minus 10,2 store; 
out store; 
"""
Code = Code.split(";")
CodeLines = []
for each in Code:
    each.strip("\n").rstrip()
    if "\n" in each:
        each = [char.strip("\n") for char in each.split()]
        each = " ".join(each)
    each += ';'
    CodeLine = Tokenizer().Tokenize(each)
    CodeLines.append(CodeLine)
Interpreter(CodeLines).Interpret(0) 
