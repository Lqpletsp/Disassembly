# Disassembly

**A high-level interpreter that uses command-execution line format with simulated memory.**

## Installation for linux/mac

```bash
#Clone
git clone https://github.com/Lqpletsp/Disassembly.git
cd Disassembly

#Make executable
printf '#!/usr/bin/env bash\npython3 /path/to/project/main.py "$@"\n' | sudo tee /usr/local/bin/disasm > /dev/null
sudo chmod +x /usr/local/bin/disasm

#Run
disasm <filename>.ds
```

## Installation for Windows 

```bash
#Create a file named disasm.cmd next to main.py

@echo off
python "%~dp0\main.py" %*

#Make sure Python 3 is installed and that the folder is in PATH.

#Run
disasm <filename>.ds
```

## Example Code 
#### Declaration (arrays,variables, ane memory), assigning, and output
```
|This is a comment|
| Each disasm file must have '.ds' extension |
out "Hello World!" |outputs "Hello world"|
decm 10; | declares memory of 10 spaces | 
decv !i variable1 !ai array1*10; |declares integer (!i) variable, variable1 and declares integer array (!ai) array1 of 10 spaces (*10)|
set variable1,array1@0 10; |Stores 10 in variable1 and 0th index in array1|
out variable1,array1; |output data in variable1 and whole array1|
```
#### Fibonacci series (Iterative)
```
decm 200; 
decv !i n1,n2,n3,count; 
set n1,n2 1; 
set count 0; 
out n1;
out n2; 
decl fibo !dne;
add n1,n2 n3; 
out n3; 
set n1 n2; 
set n2 n3; 
endl; 
loop 0,10 i fibo;
```
#### Fibonacci series (recursive)
```
decm 200; 
decv !i num1,num2,count;
set num1,num2 1; 
set count 0; 
decf fibo n1,n2,count; 
decv !i n3; 
add n1,n2 n3; 
set n1 n2; 
set n2 n3; 
out n3; 
inc count; 
cmpt count,10 <= calllabel; 
decl calllabel !dne; 
call fibo n1,n2,count; 
endl; 
endf; 
call fibo num1,num2,count;
```
