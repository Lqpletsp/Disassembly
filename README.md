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
```
|This is a comment|
| Each disasm file must have '.ds' extension |
out "Hello World!" |outputs "Hello world"|
decm 10; | declares memory of 10 spaces | 
decv !i variable1 !ai array1*10; |declares integer (!i) variable, variable1 and declares integer array (!ai) array1 of 10 spaces (*10)|
set variable1,array1@0 10; |Stores 10 in variable1 and 0th index in array1|
out variable1,array1; |output data in variable1 and whole array1|
