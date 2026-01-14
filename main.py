from Tokenizer import Tokenizer 
from Interpreter import Interpreter
Code = """
|Declare an array|
decm 200; 
decf X a,b,c; 
out a;
out b;
out c;
endf;
call X 10,20,30
"""
Code = Code.split("\n")
for iter1 in range(len(Code)):
    Code[iter1] = Code[iter1].strip()
    try:
        if Code[iter1][-1] != ";":Code[iter1]+=";"
    except:Code[iter1] = ";"
Code = "\n".join(Code)
Code = Code.split(";")
CodeLines = []
for counter in range(len(Code)):
    Code[counter].strip("\n").rstrip()
    if "\n" in Code[counter]:
        Code[counter] = [char.strip("\n") for char in Code[counter].split()]
        Code[counter] = " ".join(Code[counter])
    Code[counter] += ';'
    CodeLine = Tokenizer().Tokenize(Code[counter])
    CodeLines.append(CodeLine)
Interpreter(CodeLines).Interpret(0)
