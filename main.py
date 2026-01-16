from Tokenizer import Tokenizer 
from Interpreter import Interpreter

Code = """
decm 200; 
decf X a,b,c; 
out a;
out b;
out c;
endf;
call X 10,20,30
"""
Interpreter(Tokenizer().HandleCode(Code)).Interpret(0)
