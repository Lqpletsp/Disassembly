import sys 
import os 
from ErrorAndWarning import Errors as Error
from ErrorAndWarning import Warnings 
from Keywords import Keyword
from Tokenizer import Tokenizer

sys.setrecursionlimit(810)

class Interpreter: 
    def __init__(self,pathtoffiledir) -> None: 
        self.__code:list = []
        self.__infunction:bool = False
        self.__functioncall:bool = False 
        self.__inlabel:bool = False
        self.__labelcall:bool = False
        self.__memory:list = [[],[],[],[],[[]],[],[],[],[23455432,23455432,None],0,[],[]]
        self.__totalmemory:int = 0 
        self.__secondpass:bool = False
        self.__firstpass:bool = False 
        self.__storewarnings:list = []
        self.__recursioncount:int = 0
        self.__dirpath:str = pathtoffiledir
        self.__broughtlines:list = []
        self.__broughtfiles:list = []
        self.__appendline:bool = True
        self.__currentfile:str = "main"

        """MEMORY FORMAT: 

            [[<variable list>],[<function stack>],[<functionstack reference>],[<temp>],[tempstore variable list],[tempstore fncstack],
            [<paramters>],[<call arguments>],[<Top function>,<current function>,<current label>],<memory used>,[<label stack>],[<User-made commands>]

            NOTE: MEMORY USED IN THE PROGRAM IS JUST A SIMULATION. IT ONLY STORES DATA THAT IS BEING USED IN THE CODE WRITTEN IN Disassembly
            AND NOT IN THE CODE THAT IS USED TO MAKE Disassembly
           """
    def getMemory(self) -> list: return self.__memory
    def getrecursioncount(self) -> int: return self.__recursioncount
    def getVariablelist(self) -> list: return self.__memory[0]
    def gettemp(self) -> list: return self.__memory[3]

    def Interpret(self,startpointer,code) -> None: 
        if not self.__firstpass: 
            self.__code.append("F!le:main")
            self.firstpass(code)
        for iter1 in range(len(self.__broughtlines)):
            self.__appendline = False
            self.firstpass(self.__broughtlines[iter1])
            self.__code = self.__broughtlines[iter1] + self.__code
        self.__currentfile,self.__firstpass,self.__memory[11]= "main",True,[]
        if not self.__secondpass: 
            self.secondpass(startpointer)
            self.__firstpass,self.__functioncall,self.__infunction,self.__inlabel,self.__labelcall = True,False,False,False,False
        self.thirdpass(startpointer)
        if (self.__infunction or (self.__infunction and self.__functioncall)) and self.__memory[8][1] != 23455432:
            Error().OutError(f"Module '{self.__memory[8][1]}' declared but not ended.",len(self.__code))            
        if self.__totalmemory == 0: self.__storewarnings.append("Memory was not declared.")
        for each in self.__storewarnings:Warnings().OutWarning(each)

    def firstpass(self,code):
        for iter1 in range(len(code)):
            tokenizedline = code[iter1]
            if not tokenizedline: continue
            tokenizedline = [each for each in tokenizedline if each != '']
            if not tokenizedline:
                self.__code.append([])
                continue
            if tokenizedline[0] not in Keyword().GetCommands():
                if "@" not in tokenizedline[0]:
                    if  tokenizedline[:5] == "F!le" or ''.join(tokenizedline[:5]) == "F!le:":
                        self.__currentfile = ''.join(tokenizedline[5:])
                        continue
                    cmddata = self.searchcmd(tokenizedline[0])
                    if not cmddata: 
                        Error().OutError(f"Command not found: {tokenizedline[0]} \n Each line must begin with a valid command. None found. \n '{tokenizedline}'",iter1)
                else: 
                    filename,command = tokenizedline[0].split("@")
                    if filename not in self.__broughtfiles: 
                        Error().OutError(f"No code files '{filename}' loaded to reference a module for '{command}' command.",iter1)
                    else: self.__memory[11].append(tokenizedline[0])
            if (tokenizedline[0] == "endf" or tokenizedline[0] == "endl") and len(tokenizedline) > 1:
                Error().OutError(f"end commands do not take any execution data. Invalid execution-data: {tokenizedline[1:]}",iter1)
            if tokenizedline[0] in Keyword().GetOneVariableCommand() and len(tokenizedline) != 2: 
                Error().OutError(f"'{tokenizedline[0]}' is a one executing data command. Malformed line for one-execution-data commands",iter1)
            elif tokenizedline[0] in Keyword().GetTwoOrMoreVariableCommand() and len(tokenizedline) < 2: 
                Error().OutError("'{tokenizedline[0]}' is a two-or-more executing data command. Malformed line for two-or more execution-data commands",iter1)
            if tokenizedline[0] == "mkcmd" and len(tokenizedline) == 3:
                self.verifyName(tokenizedline[1])
                for cmdname in tokenizedline[1:]:self.__memory[11].append([cmdname,None])
            if tokenizedline[0] == "bring" and len(tokenizedline) > 2:
                if tokenizedline[1] == "/":path = self.__dirpath + "/" + tokenizedline[2] + '.ds'
                else: 
                    if not os.path.isdir(tokenizedline[1]):Error().OutError(f"Directory path '{tokenizedline[1]}' not found",iter1)
                    path = tokenizedline[1] + '/' + tokenizedline[2]+ ".ds"
                try: 
                    file = open(path,'r')
                except:Error().OutError(f"File '{tokenizedline[2]}' does not exist",f"FILEERROR@{iter1}")
                self.__broughtfiles.append(path.split("/")[-1][:len(tokenizedline[2])])
                Codelines = Tokenizer().HandleCode(f"!File:{path}")
                self.handlebring(Codelines,tokenizedline[2])
                self.__code.append([])
                continue
            if self.__appendline:
                self.__code.append(tokenizedline)
    def secondpass(self,startpointer):
       #_______SECOND PASS______
        try:self.__code[startpointer]
        except: Error().OutError("No code line(s) found for the called function",startpointer) 
        for iter1 in range(startpointer,len(self.__code)): #Second pass. Declares memory/functions/variables. This does not impact the memory.
            tokenizedline = self.__code[iter1]
            if not tokenizedline: continue
            if tokenizedline[0] == "":
                self.__code[iter1] = []
                continue
            if len(tokenizedline) == 1 and tokenizedline[0] == "endf":
                if self.__memory[8][1] == 23455432: Error().OutError("Invalid usage of 'endf'. No funciton declared to end... \n Current function is None",iter1)
                else: self.__infunction = False 
                if self.__functioncall: break
                self.__memory[8][1] = self.__memory[8][0]
                try:self.__memory[2].pop()
                except:self.__infunction = False 
                try:self.__memory[8][0] = self.__memory[2][-2]
                except:self.__memory[8][0] == 23455432
                if self.__memory[2]:self.__infunction = True 
                continue
            if len(tokenizedline) > 1 and tokenizedline[0] == "endf":
                Error().OutError("Invalid usage of 'endf' command",iter1)
            if (self.__infunction or self.__inlabel) and not self.__functioncall:
                continue
            if tokenizedline[0] == "decm": 
                if not tokenizedline[1].isdigit(): Error().OutError(f"Cannot create memory of '{tokenizedline[1]}' places.",iter1)
                self.__totalmemory = tokenizedline[1]
            elif tokenizedline[0] == "decv":
                if not self.verifyName(tokenizedline[1]): Error().OutError(f"Invalid name for variable. Cannot create '{tokenizedline[1]}'",iter1)
                returnval,returnstate = self.decv(tokenizedline[1:])
                if not returnval: Error().OutError(returnstate,iter1)
            elif tokenizedline[0] == "decf":
                if not self.verifyName(tokenizedline[1]): Error().OutError(f"Invalid name for module. Cannot create '{tokenizedline[1]}'",iter1)
                self.__infunction = True 
                self.__memory[1].append([self.__memory[8][0],tokenizedline[1],iter1,"fnc"]) #Function format: [<Top function>,<fncname>,<fncpointer>,"fnc"]
                self.__memory[2].append(tokenizedline[1])
                self.__memory[8][1] = tokenizedline[1]
                try:self.__memory[8][0] = self.__memory[2][-2]
                except:self.__memory[8][0] = 23455432
            elif tokenizedline[0] == "decl" and (len(tokenizedline) < 2 or len(tokenizedline)>3):Error().OutError("Malformed line for 'decl' command",iter1)
            elif tokenizedline[0] == "decl" and len(tokenizedline) == 3 and (tokenizedline[2] == "dne" or tokenizedline[2] == "e"):
                if not self.verifyName(tokenizedline[1]): Error().OutError(f"Invalid name for label. Cannot create '{tokenizedline[1]}'",iter1)
                self.__memory[1].append([self.__memory[8][0],tokenizedline[1],iter1,"lab"]) #Label format: [<Top funciton>,<Label name>,<Label pointer>,"lab"]
                self.__memory[8][2] = tokenizedline[1]
            elif tokenizedline[0] == "decl" and len(tokenizedline) == 2: 
                if not self.verifyName(tokenizedline[1]): Error().OutError(f"Invalid name for label. Cannot create '{tokenizedline[1]}'",iter1)
                self.__memory[1].append([self.__memory[8][0],tokenizedline[1],iter1,"lab"]) #Label format: [<Top funciton>,<Label name>,<Label pointer>,"lab"]
                self.__memory[10].append(tokenizedline[1])
            elif tokenizedline[0] == "endl" and len(tokenizedline) == 1:
                if self.__memory[8][2] == None: Error().OutError("No label declared to end",iter1)
                try:self.__memory[10].pop()
                except:pass
            elif tokenizedline[0] == "mkcmd" and len(tokenizedline) == 3:
                fncdata = self.findfnc(tokenizedline[2])
                if not fncdata: Error().OutError(f"Cannot create a user command with a non-existing module: '{tokenizedline[1]}'",iter1)
                if self.__currentfile != "main":
                    self.__memory[11].append([self.__currentfile + "@" + tokenizedline[1],fncdata[2]]) # Format: [<command name>,<function pointer>]
                else: self.__memory[11].append([tokenizedline[1],fncdata[2]])
            elif tokenizedline[:5] == "F!le:" or ''.join(tokenizedline[:5]) == "F!le:":
                try:self.__currentfile = ''.join(tokenizedline[5:])
                except: self.__currentfile = tokenizedline[5:]
                continue
    def thirdpass(self,startpointer):
        try:self.__code[startpointer]
        except: Error().OutError("No code line(s) found for the called function",startpointer) 
        for iter1 in range(startpointer,len(self.__code)):
            try:self.__code[iter1]
            except:Error().OutError("No executing line found.",iter1)
            line = self.__code[iter1]
            if not line or (len(line) == 1 and not line[0]): continue
            if ''.join(line) and ''.join(line)[:5] == "F!le:":
                self.__currentfile = ''.join(line)[5:]
                continue
            elif line[0] == "decv" or line[0] == "mkcmd" or line[0] == "decm": continue
            elif line[0] == "endf" and len(line) == 1 and not self.__inlabel:
                if not self.__infunction and self.__functioncall: Error().OutError("No function found to end",iter1) 
                if self.__infunction and not self.__functioncall:self.__infunction = False
                else:return 
            elif line[0] == "endl" and len(line) == 1:
                if not self.__inlabel and self.__labelcall: Error().OutError("No label found to end",iter1)
                if self.__inlabel and not self.__labelcall and not self.__memory[10]: self.__inlabel = False 
                elif self.__inlabel and self.__labelcall:return
                elif not self.__inlabel and not self.__labelcall and self.__infunction: continue
                else:continue
            elif line[0] == "decl":
                if len(line) == 1 or (len(line) == 3 and line[2] == "e"):
                    self.__labelcall = False
                    self.__inlabel = False
                    continue
                elif len(line) == 3 and line[2] == "dne":
                    self.__inlabel = True
                    self.__labelcall = False
                else: return False, "Invalid way of declaring a label. Mid-line commands as 'dne' or 'e' can only be used. "

            if (self.__infunction and not self.__functioncall) or (self.__inlabel and not self.__labelcall):continue
            if line[0] == "call":
                self.__recursioncount += 1 
                if self.__recursioncount >= 800: 
                    Error().OutError("Recursion limit (8000 recursions) reached.",iter1)
                self.__memory[7] = []
                fncdata = self.findfnc(line[1])
                if not fncdata or (fncdata[0] != self.__memory[8][1] and fncdata[1] != self.__memory[8][1]):
                    Error().OutError(f"Function not declared, '{line[1]}'",iter1)
                self.__memory[4].extend([[v[0],v[1],v[2]] for v in self.__memory[0]])
                for each in line[2:]:
                    dt = self.determinedt(each)
                    if not dt: Error().OutError(f"Invalid varchar data given: {each}",iter1)
                    if dt == "var":
                        variabledata = self.searchvariables(each)
                        if not variabledata: Error().OutError(f"Variable not declared, '{each}'",iter1)
                        self.__memory[7].append([variabledata[0],variabledata[1],variabledata[2]])
                    else: self.__memory[7].append(['None',dt,each])
                if len(self.__code[iter1][2:]) != len(self.__memory[7]):
                    Error().OutError(f"Inappropriate amount of parameters given for the arguments called",fncdata[2])
                self.__memory[0] = []
                fncdeclaration = self.__code[fncdata[2]]
                for iter2 in range(len(fncdeclaration[2:])):
                    self.__memory[9] += len(str(self.__memory[7][iter2][2]))
                    self.checkmemory()
                    self.__memory[0].append([fncdeclaration[2:][iter2],self.__memory[7][iter2][1],self.__memory[7][iter2][2]])
                for each in self.__memory[1]:
                    self.__memory[5].append([each[0],each[1],each[2]])
                self.__memory[1] = [fncdata]
                self.__memory[8][0] = self.__memory[8][1]
                self.__memory[8][1] = fncdata[1]
                self.__secondpass,self.__infunction,self.__functioncall = False,True,True
                self.secondpass(fncdata[2]+1)
                self.__infunction, self.__functioncall = True,True
                self.thirdpass(fncdata[2]+1)
                self.__firstpass = True
                self.__memory[8][1] = fncdata[0]
                if self.__memory[8][1] != 23455432:
                    self.__infunction = True 
                self.__memory[0] = self.__memory[4].pop()
                self.__memory[1] = self.__memory[5].pop()
                self.__recursioncount -= 1 
                continue

            elif line[0] == "loop":
                labelname,startval,endval = line[-1],line[1],line[2]
                if len(line) != 4: Error().OutError("Malformed line for loop", iter1)
                labeldata = self.findlabel(labelname)
                if not labeldata: Error().OutError(f"Label not declared, '{labelname}'",iter1)
                if self.determinedt(startval) == "var":
                    variabledata = self.searchvariables(startval)
                    if not variabledata: Error().OutError("Variable not declared, '{startval}'",iter1)
                    if (variabledata[1] != "int" or variabledata[2] != "float"): Error().OutError("Start value for a loop cannot be varchar/boolean data.",iter1)
                    if variabledata[2] == "empt": Error().OutError("Cannot use empt value for start",iter1)
                    else: startval = variabledata[2]
                if self.determinedt(endval) == "var":
                    variabledata = self.searchvariables(endval)
                    if not variabledata: Error().OutError("Variable not declared, '{endval}'",iter1)
                    if (variabledata[1] != "int" or variabledata[2] != "float"): Error().OutError("End value for a loop cannot be varchar/boolean data.",iter1)
                    if variabledata[2] == "empt": Error().OutError("Cannot use empt value for end",iter1)
                    else: endval = variabledata[2]
                if endval > 990: sys.setrecursionlimit(endval + 1)
                for loopcmd in range(int(startval),int(endval)):
                    self.__inlabel = True
                    self.__labelcall = True
                    self.__memory[8][2] = line[1] 
                    self.__memory[10].append(line[1])
                    self.thirdpass(labeldata[2]+1)
                try: self.__memory[8][2] = self.__memory[10].pop()
                except:self.__memory[8][2] = None 
                if not self.__memory[10]: self.__inlabel,self.__labelcall = False, False

            elif line[0] == "decf":
                self.__infunction = True
                self.__functioncall = False
            elif line[0] == "set":
                returnval,returnstate = self.setvar(line[1:])
                if not returnval:Error().OutError(returnstate,iter1)
            elif line[0] == "out":
                returnval,returnstate = self.out(line[1:])
                if not returnval:Error().OutError(returnstate,iter1)
            elif line[0] == "in":
                returnval,returnstate = self.inp(line[1:])
                if not returnval:Error().OutError(returnstate,iter1)

            elif line[0] == "cmpt" or line[0] == "cmpf":
                if len(line) == 2 and line[0] == "cmpt":
                    labeldata = self.findlabel(line[1])
                    if not labeldata:
                        Error().OutError(f"Label not declared, '{line[1]}'",iter1)
                    self.__labelcall, self.__inlabel = True,True 
                    self.__memory[8][2] = line[1]
                    self.__memory[10].append(line[1])
                    self.Interpret(int(labeldata[2])+1)
                    try: self.__memory[8][2] = self.__memory[10].pop()
                    except:self.__memory[8][2] = None 
                    if not self.__memory[10]: self.__inlabel,self.__labelcall = False, False 
                    continue
                elif len(line) == 2 and line[0] == "cmpf": continue
                else:
                    labelname = line[-1]
                    returnstate,returnval = self.logicalstatements(line[:len(line)-1])
                    if not returnstate:
                        Error().OutError(returnval,iter1)
                    elif returnval == "1":
                        labeldata = self.findlabel(labelname)
                        if not labeldata: 
                            Error().OutError(f"Label not declared, '{labelname}'",iter1)
                        self.__labelcall,self.__inlabel = True,True
                        self.__memory[8][2] = labelname
                        self.__memory[10].append(labelname)
                        self.thirdpass(labeldata[2]+1)
                        try:self.__memory[8][2] = self.__memory[10].pop()
                        except:self.__memory[8][2] = None
                        if not self.__memory[10]: self.__inlabel,self.__labelcall = False,False
                        continue
                    elif returnval == "0":continue
            elif line[0] == "add" and len(line) > 3: 
                returnval,returnstate = self.add(line[1:])
                if not returnval:Error().OutError(returnstate,iter1)
            elif line[0] == "inc" and len(line) >= 2: 
                returnval,returnstate = self.inc(line[1:])
                if not returnval: Error().OutError(returnstate,iter1)
            elif line[0] == "dec" and len(line) >= 2: 
                returnval,returnstate = self.dec(line[1:])
                if not returnval: Error().OutError(returnstate,iter1)
            elif line[0] == "minus" and len(line) > 3: 
                returnval,returnstate = self.minus(line[1:])
                if not returnval: Error().OutError(returnstate,iter1)
            elif line[0] == "mult" and len(line) > 3: 
                returnval,returnstate = self.mult(line[1:])
                if not returnval: Error().OutError(returnstate,iter1)
            elif line[0] == "div" and len(line) > 3: 
                returnval,returnstate = self.div(line[1:])
                if not returnval: Error().OutError(returnstate,iter1)
            elif line[0] != "endf" and line[0] != "endl" and line[0] != "": #This is to make sure that other user made commands work 
                cmddata = self.searchcmd(line[0])
                if not cmddata:
                    Error().OutError(f"'{line[0]}' does not reference any function. Invalid command",iter1)
                self.__recursioncount += 1 
                if self.__recursioncount >= 800: 
                    Error().OutError("Recursion limit (800 recursions) reached.",iter1)
                self.__memory[7] = []
                fncname = self.__code[cmddata[1]][1]
                fncdata = self.findfnc(fncname)
                if not fncdata or (fncdata[0] != self.__memory[8][1] and fncdata[1] != self.__memory[8][1]):
                    Error().OutError(f"Function not declared, '{line[0]}'",iter1)
                self.__memory[4].extend([[v[0],v[1],v[2]] for v in self.__memory[0]])
                for each in line[1:]:
                    dt = self.determinedt(each)
                    if not dt: Error().OutError(f"Invalid varchar data given: {each}",iter1)
                    if dt == "var":
                        variabledata = self.searchvariables(each)
                        if not variabledata: Error().OutError(f"Variable not declared, '{each}'",iter1)
                        self.__memory[7].append([variabledata[0],variabledata[1],variabledata[2]])
                    else: self.__memory[7].append(['None',dt,each])
                if len(self.__code[fncdata[2]][2:]) != len(self.__memory[7]):
                    if len(self.__code[iter1][2:]) == 1: 
                        Error().OutError(f"User-made command, '{line[0]}', takes a single data. {len(self.__memory[7])} given.",fncdata[2])
                    elif len(self.__code[iter1][2:]) > 1: 
                        Error().OutError(f"User-made command '{line[0]}', takes one or more than one data. {len(self.__memory[7])} given.",fncdata[2])
                self.__memory[0] = []
                fncdeclaration = self.__code[fncdata[2]]
                for iter2 in range(len(fncdeclaration[2:])):
                    self.__memory[9] += len(str(self.__memory[7][iter2][2]))
                    self.checkmemory()
                    self.__memory[0].append([fncdeclaration[2:][iter2],self.__memory[7][iter2][1],self.__memory[7][iter2][2]])
                for each in self.__memory[1]:
                    self.__memory[5].append([each[0],each[1],each[2]])
                self.__memory[1] = [fncdata]
                self.__memory[8][0] = self.__memory[8][1]
                self.__memory[8][1] = fncdata[1]
                self.__secondpass,self.__infunction,self.__functioncall = False,True,True
                self.secondpass(fncdata[2]+1)
                self.__infunction,self.__functioncall = True,True 
                self.thirdpass(fncdata[2]+1)
                self.__firstpass = True
                self.__memory[8][1] = fncdata[0]
                if self.__memory[8][1] != 23455432:
                    self.__infunction = True 
                self.__memory[0] = self.__memory[4].pop()
                self.__memory[1] = self.__memory[5].pop()
                self.__recursioncount -= 1 
                continue


    def searchcmd(self,cmd) -> tuple[str,int]:
        for each in self.__memory[11]:
            if each[0] == cmd:
                return each
        return []

    def handlebring(self,Codelines,filename):
        for iter1 in range(len(Codelines)):
            self.__bring = True
            tokenizedline = Codelines[iter1]
            if not tokenizedline: continue
            if tokenizedline[0] == "mkcmd" and len(tokenizedline) == 3:
                fncname = tokenizedline[2]
                state = self.fncfromname(fncname,Codelines,filename)
                if not state: Error().OutError(f"'{Codelines[iter1][1]}' does not reference any function. Cannot create the command",f"{filename}@{iter1}")
                self.__broughtlines.extend([[f"F!le:{filename}"] + Codelines[state[0]:state[1]+1] + [tokenizedline]])# This will attach the mkcmd line with the module
            elif tokenizedline[0] == "bring" and len(tokenizedline) > 2:self.__broughtlines.append(tokenizedline)

    def fncfromname(self,fncname,Codelines,filename) -> tuple[int,int]:
        start,end,fncstack = None,None,[]
        for iter1 in range(len(Codelines)):
            if Codelines[iter1][0] == "decf" and Codelines[iter1][1] == fncname:
                start = iter1
                fncstack.append(fncname)
            elif Codelines[iter1][0] == "decf": 
                fncstack.append(Codelines[iter1][1])
            elif Codelines[iter1][0] == "endf":
                topfncname = fncstack.pop()
                if topfncname == fncname: 
                    end = iter1
                    return [start,end]
        if fncstack and len(fncstack) == 1: Error().OutError(f"'{fncname}' module used but not ended.",f"{filename}@{start}")
        elif len(fncstack) > 1: Error().OutError(f"'{fncname}' module has other modules that are used but not ended",f"{filename}@{start}")
        return []
    
    def div(self,divvalues) -> tuple[bool,str]: 
        prioritydata = 0 
        storevalue = divvalues[-1]
        dt = self.determinedt(divvalues[0])
        if not dt: return False,"Cannot operate minus with invalid varchar/boolean data"
        elif dt == "var":
            variabledata = self.searchvariables(divvalues[0])
            if not variabledata: return False, f"Variable not declared, '{minusvalues[0]}'"
            if variabledata[1] != "float" and variabledata[1] != "int": 
                return False,f"'{minusvalues[0]}' contains varchar/boolean data. \n Cannot opreate minus with varchar/boolean data"
            else: 
                if float(variabledata[2]) == 0: return False, "Cannot divide by 0" 
                prioritydata = float(variabledata[2])
        elif dt == "bool" or dt == "varchar": return False, "Cannot operate minus with varchar/boolean data"
        else: 
            if float(divvalues[0]) == 0: return False, "Cannot divide by 0"
            prioritydata = float(divvalues[0])
        storevariabledata = self.searchvariables(storevalue)
        if not storevariabledata: return False, f"Variable not declared, '{storevariabledata}'"
        divvalues = divvalues[1:len(divvalues)-1]
        for each in divvalues: 
            if each == "temp":
                try: 
                    data = self.__memory[3].pop()
                    try: prioritydata = float(data)/prioritydata  
                    except: return False, "temp contains varchar/boolean data. \n Cannot store varchar/boolean data in int/float data-type variables"
                except:
                    return False, "temp is empty."
            else: 
                dt = self.determinedt(each)
                if not dt: return False, "Cannot operate div with invalid varchar/boolean data"
                if dt == "bool" or dt == "varchar": return False, "Cannot operate div with varhcar/boolean data"
                elif dt == "var":
                    variabledata = self.searchvariables(each)
                    if not each: return False, f"Variable not declared, '{each}'"
                    elif variabledata[1] != "float" and variabledata[1] != "int":
                        return False, f"'{each}' contains varchar/boolean data \n Cannot operate div with varchar/boolean data"
                    else: prioritydata = float(variabledata[2])/prioritydata
                else: 
                    prioritydata = float(each)/prioritydata
        if storevariabledata[2] != 'None':
            self.__memory[9] -= len(variabledata[2])
            self.checkmemory()
        self.__memory[9] += len(str(int(prioritydata)))
        self.checkmemory()
        state = self.storedata(storevalue,str(prioritydata))
        return True, ""

    
    def mult(self,multvalues) -> tuple[bool,str]:
        multipliedtotal = 1
        storevalue = multvalues[-1]
        variabledata = self.searchvariables(storevalue)
        if not variabledata: return False, f"Variable not declared, '{storevalue}'"
        multvalues = multvalues[:len(multvalues)-1]
        for each in multvalues:
            if each == "temp":
                try:
                    data = self.__memory[3].pop()
                    try: multipliedtotal *= float(data)
                    except: return False, "'mult' command does not work with varchar or boolean data"
                except: return False, "temp is empty"
            else:
                dt = self.determinedt(each)
                if not dt: return False, "'mult' command does not work with invalid varchar data"
                if dt == 'var':
                    multvardata = self.searchvariables(each)
                    if not multvardata: return False, f"Variable not declared, '{each}'"
                    elif multvardata[1] != "float" and multvardata[1] != "int": return False, "'mult' command does not work with varchar or boolean data"
                    else:multipliedtotal *= float(multvardata[2])
                elif dt == 'var' or dt == 'bool':
                    return False, "'mult' command does not work with varchar or boolean data"
                else: multipliedtotal *= float(each)

        if variabledata[2] != 'None':
            self.__memory[9] -= len(variabledata[2])
            self.checkmemory()
        self.__memory[9] += len(str(int(multipliedtotal)))
        self.checkmemory()
        state = self.storedata(storevalue,str(multipliedtotal))
        return True, ""


    def minus(self,minusvalues) -> tuple[bool,str]:
        prioritydata = 0 
        storevalue = minusvalues[-1]
        dt = self.determinedt(minusvalues[0])
        if not dt: return False,"Cannot operate minus with invalid varchar/boolean data"
        elif dt == "var":
            variabledata = self.searchvariables(minusvalues[0])
            if not variabledata: return False, f"Variable not declared, '{minusvalues[0]}'"
            if variabledata[1] != "float" and variabledata[1] != "int": 
                return False,f"'{minusvalues[0]}' contains varchar/boolean data. \n Cannot opreate minus with varchar/boolean data"
            else: 
                prioritydata = float(variabledata[2])
        elif dt == "bool" or dt == "varchar": return False, "Cannot operate minus with varchar/boolean data"
        else: 
            prioritydata = float(minusvalues[0])
        storevariabledata = self.searchvariables(storevalue)
        if not storevariabledata: return False, f"Variable not declared, '{storevariabledata}'"
        minusvalues = minusvalues[1:len(minusvalues)-1]
        for each in minusvalues: 
            if each == "temp":
                try: 
                    data = self.__memory[3].pop()
                    try: 
                        prioritydata -= float(data)
                    except: return False, "temp contains varchar/boolean data. \n Cannot store varchar/boolean data in int/float data-type variables"
                except:
                    return False, "temp is empty."
            else: 
                dt = self.determinedt(each)
                if not dt: return False, "Cannot operate minus with invalid varchar/boolean data"
                if dt == "bool" or dt == "varchar": return False, "Cannot operate minus with varhcar/boolean data"
                elif dt == "var":
                    variabledata = self.searchvariables(each)
                    if not each: return False, f"Variable not declared, '{each}'"
                    elif variabledata[1] != "float" and variabledata[1] != "int":
                        return False, f"'{each}' contains varchar/boolean data \n Cannot operate minus with varchar/boolean data"
                    else: prioritydata -= float(variabledata[2])
                else: 
                    prioritydata -= float(each)
        if storevariabledata[2] != 'None':
            self.__memory[9] -= len(variabledata[2])
            self.checkmemory()
        self.__memory[9] += len(str(int(prioritydata)))
        self.checkmemory
        state = self.storedata(storevalue,str(prioritydata))
        return True, ""

    def inc(self,incvalues) -> tuple[bool,str]:
        for each in incvalues: 
            dt = self.determinedt(each)
            if dt != 'var':return False,"Can only increment int/float variables"
            variabledata = self.searchvariables(each)
            if not variabledata: return False, f"Variable not declared, {each}"
            if variabledata[1] != "float" and variabledata[1] != "int": return False, "Cannot increment varchar/boolean data"
            if variabledata[2] != "None":
                self.__memory[9] -= len(str(int(float(variabledata[2]))))
                self.checkmemory()
                self.__memory[9] +=  len(str(int(float(variabledata[2])+1)))
                self.checkmemory()
                state = self.storedata(variabledata[0],float(variabledata[2])+1)
            else:
                self.__memory[9] += 1 
                self.checkmemory()
                state = self.storedata(variabledata[0],str(float(1)))
            if not state:return False, "CRITICAL ERROR"
        return True, ""

    def dec(self,decvalues) -> tuple[bool,str]:
        for each in decvalues: 
            dt = self.determinedt(each)
            if dt != 'var':return False,"Can only increment int/float variables"
            variabledata = self.searchvariables(each)
            if not variabledata: return False, f"Variable not declared, {each}"
            if variabledata[1] != "float" and variabledata[1] != "int": return False, "Cannot decrement varchar/boolean data"
            if variabledata[2] != "None":
                self.__memory[9] -= len(str(int(float(variabledata[2]))))
                self.checkmemory()
                self.__memory[9] +=  len(str(int(float(variabledata[2])+1)))
                self.checkmemory()
                state = self.storedata(variabledata[0],float(variabledata[2])-1)
            else:
                self.__memory[9] += 1 
                self.checkmemory()
                state = self.storedata(variabledata[0],str(float(-1)))
            if not state:return False, "CRITICAL ERROR"
        return True, ""

    def add(self,addvalues) -> tuple[bool,str]:
        addedamt = 0
        storevalue = addvalues[-1]
        variabledata = self.searchvariables(storevalue)
        if not variabledata: return False, f"Variable not declared, '{storevalue}'"
        addvalues = addvalues[:len(addvalues)-1]
        for each in addvalues:
            if each == "temp":
                try:
                    data = self.__memory[3].pop()
                    try: addedamt += float(data)
                    except: return False, "'add' command does not work with varchar or boolean data"
                except: return False, "temp is empty"
            else:
                dt = self.determinedt(each)
                if not dt: return False, "Invalid representation of varchar data"
                if dt == 'var':
                    addvardata = self.searchvariables(each)
                    if not addvardata: return False, f"Variable not declard, '{each}'"
                    elif addvardata[1] != "float" and addvardata[1] != "int": return False, "'add' command does not work with varchar or boolean data"
                    else:addedamt += float(addvardata[2])
                elif dt == 'var' or dt == 'bool':
                    return False, "'add' command does not work with varchar or boolean data"
                else: addedamt += float(each)

        if variabledata[2] != 'None':
            self.__memory[9] -= len(variabledata[2])
            self.checkmemory()
        self.__memory[9] += len(str(int(addedamt)))
        self.checkmemory()
        state = self.storedata(storevalue,str(addedamt))
        return True, ""

    def findfnc(self,fncname) -> tuple[str,str,int]: 
        for each in self.__memory[1]:
            if each[1] == fncname and each[3] == "fnc": return each
        return []
    def findlabel(self,labelname) -> tuple[str,str,int]:
        for each in self.__memory[1]:
            if each[1] == labelname and each[3] == "lab": return each 
        return []

    def logicalstatements(self,logic) -> tuple[bool,str]:
        index = 1
        varstack = []
        logicstack = []
        store = 0
        mostsignificantdt = None
        cmd = logic[0]
        logic = logic[1:]
        for each in logic: 
            if (each != "!" and each != "=" and each != "<" and each != ">" and 
                each != "<=" and each != ">=" and each != "&" and each != "~"):
                dt = self.determinedt(each)
                if not dt: return False,"Invalid representation of varchar data."
                if dt == "var":
                    variabledata = self.searchvariables(each)
                    if not variabledata:
                        return False, f"Variable not declared, '{each}'"
                    varstack.append([variabledata[1],variabledata[2]])
                    dt = variabledata[1]
                elif dt == "int":varstack.append(["int",int(float(each))])
                elif dt == "float":varstack.append(["float",float(each)])
                elif dt == "varchar":varstack.append(["varchar",str(each)])
                elif dt == "bool":
                    if each == "T":varstack.append(["bool",True])
                    elif each == "F":varstack.append(["bool",False])
            elif each == "!" or each == "<" or each == ">" or each == "=" or each == "<=" or each == ">=":
                if each == "!":
                    current = str(varstack[0][1])
                    for each1 in varstack:
                        if str(each1[1])!= current:store = 1 
                        else: 
                            store = 0
                            break
                elif each == "=":
                    current = str(varstack[0][1])
                    for each1 in varstack:
                        if str(each1[1]) == current:store = 1 
                        else: 
                            store = 0
                            break
                elif each == "<":
                    try: current = float(varstack[0][1])
                    except:return False, "Cannot compare with varchar data for '<'"
                    for iter1 in range(1,len(varstack)): 
                        try: float(varstack[iter1][1])
                        except:return False, "Cannot compare with varchar data for '<'"
                        if float(current) < float(varstack[iter1][1]):store = 1 
                        else:
                            store = 0 
                            break
                elif each == ">":
                    try: current = float(varstack[0][1])
                    except:
                        return False, "Cannot compare with non-varchar data, '{varstack[0][1]}', for '>'"
                    for iter1 in range(1,len(varstack)):
                        try:float(varstack[iter1][1])
                        except:
                            return False, f"Cannot compare with varchar data, '{varstack[iter1][1]}', for '>'"
                        if float(current) > float(varstack[iter1][1]):store = 1 
                        else: 
                            store = 0 
                            break
                elif each == "<=":
                    try: current = float(varstack[0][1])
                    except:return False, "Cannot compare with varchar data for '<'"
                    for iter1 in range(1,len(varstack)): 
                        try: float(varstack[iter1][1])
                        except:return False, "Cannot compare with varchar data for '<'"
                        if float(current)<= float(varstack[iter1][1]):store = 1 
                        else:
                            store = 0 
                            break
                elif each == ">=":
                    try: current = float(varstack[0][1])
                    except:return False, "Cannot compare with varchar data for '<'";print(varstack[0][1])     
                    for iter1 in range(1,len(varstack)): 
                        try: float(varstack[iter1][1])
                        except:return False, "Cannot compare with varchar data for '<'"
                        if float(current)>= float(varstack[iter1][1]):store = 1 
                        else:
                            store = 0 
                            break
                logicstack.append(store)
                if not varstack: return False, "No data given for logical statement"
                varstack = []
            elif each == "&" or each == "~":
                if len(varstack) == 1: 
                    if varstack[0][0] == "bool" and varstack[0][1]: logicstack.append(0)
                    else: logicstack.append(0)
                logicstack.append(each) # '&' means 'and' and '~' means 'or'
            else:return False,"CRITICAL ERROR"
            count = 0
        if len(logicstack) == 1: 
            if cmd == "cmpt" and logicstack[0] == 0: return True, "0"
            elif cmd == "cmpt" and logicstack[0] == 1: return True, "1"
            elif cmd == "cmpf" and logicstack[0] == 0: return True, "1"
            elif cmd == "cmpf" and logicstack[0] == 1: return True, "0"
            else:return False, "CRITICAL ERROR"
        while True:
            count += 1 
            try: dat1,opt,dat2 = logicstack.pop(),logicstack.pop(),logicstack.pop()
            except: return False, "Invalid logical statement given"
            if opt != "&" and opt != "~":return False,"Invalid logical statement given"
            if opt == "&": store = int(dat1) and int(dat2)
            elif opt == "~": store = int(dat1) or int(dat2)
            logicstack.append(store)
            if len(logicstack) == 1: break
            if count > 99:return False,"Logic statement too long."
        if cmd == "cmpt" and logicstack == [0]: return True, "0"
        elif cmd == "cmpt" and logicstack == [1]: return True, "1"
        elif cmd == "cmpf" and logicstack == [0]: return True, "1"
        elif cmd == "cmpf" and logicstack == [1]: return True, "0"
        else: return False, "CRITICAL ERROR"

    def verifyName(self,name) -> bool:
        validcharacters = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"
        # Allow variables like 'a1','var1'. But do not allow '1a'
        for iter1 in range(len(name)-1): 
            if name[iter1] not in validcharacters: return False
        if name[-1] not in validcharacters + '1234567890': return False
        return True
            
    def inp(self,inpval) -> tuple[bool,str]:
        for iter1 in range(len(inpval)):
            sudostore = str(input(""))
            self.__memory[9] += len(sudostore)
            self.checkmemory()
            try:
                if int(sudostore):dt = "num"
            except:dt = "notnum"
            if inpval[0] == "temp": self.__memory[3].append(sudostore)
            else: 
                variabledata = self.searchvariables(inpval[0])
                if not variabledata: return False, f"Variable not declared, '{inpval[0]}'"
                if dt == "notnum" and (variabledata[1] == "int" or variabledata[1] == "float"):return False, "Cannot store varchar data in non-varchar data-type"
                state = self.storedata(inpval[iter1],sudostore)
                if not state: return False, f"CRITICAL ERROR"   
        return True, ""

    def out(self,outputval) -> tuple[bool,str]:
        for each in outputval:
            dt = self.determinedt(each)
            if not dt: return False,"Inappropriate representation of string data"
            if dt == "var":
                variabledata = self.searchvariables(each)
                if not variabledata: return False, f"Variable not declared, {each}"
                try:
                    if variabledata[1] == "int":print(str(int(float(variabledata[2].strip('"')))),end="")
                    elif variabledata[1] == "float":print(str(float(variabledata[2].strip('"'))),end="")
                except:print("empt",end="")
                if variabledata[1] == "varchar": print(str(variabledata[2].strip('"')),end="")
            elif dt == "int":print(str(int(float(each.strip('"')))),end="")
            elif dt == "varchar":print(str(each.strip('"')),end="")
        print()
        return True,""

    def decv(self,declaration) -> tuple[bool,str]:
        datatype = declaration[-1]
        if datatype not in Keyword().GetDataTypes():return False,"No appropriate data-type given for variable declaration"
        for iter1 in range(len(declaration)-1):
            if declaration[iter1] == "temp":self.__storewarnings.append("Variable name: 'temp'. Can lead to unexpected outputs")
            elif not self.verifyName(declaration[iter1]): return False, f"Invalid variable name given. \n Cannot declare '{declaration[iter1]}'"
            self.__memory[0].append([declaration[iter1],datatype,"None"]) #Variable Format: [<variable name>,<variable data-type>, <data>]
        return True,""

    def setvar(self,declaration) -> tuple[bool,str]: 
        if declaration[-1] != "temp":
            dt = self.determinedt(declaration[-1])
            if not dt: return False, "Inappropriate representation of string data"
            elif dt == "var":
                variabledata = self.searchvariables(declaration[-1])
                data = variabledata[2]
                dt = variabledata[1]
            else: data = declaration[-1]
            self.__memory[9] += len(data)
            self.checkmemory()
            for iter1 in range(len(declaration)-1):
                variabledata = self.searchvariables(declaration[iter1])
                if not variabledata:return False, f"Variable not declared, '{declaration[iter1]}'"
                if variabledata[0] == "temp":self.__storewarnings.append("'temp' variable name detected. Can cause unexpected results.")
                if (variabledata[1] == dt) or (variabledata[1] == "float" and dt == "int") or (variabledata[1] == "int" and dt == "float"): 
                    state = self.storedata(variabledata[0],data)
                    if not state: return False, "CRITICAL ERROR"
                else: 
                    return False, "Cannot store in different data-type variable"
            return True,""
        elif declaration[-1] == "temp":
            if len(declaration) != len(self.__memory[3]):return False, "'temp' does not store enough data to set in declared variable(s)"
            for iter1 in range(len(declaration)):
                datadt = self.determinedt(self.__memory[3][iter1])
                variabledata = self.searchvariables(declaration[iter1])
                if not variabledata:return False,f"Variable not declared, '{declaration[iter1]}'"
                if datadt != variabledata[1]:return False, f"Cannot store data in a different data-type variable, '{variabledata[0]}'"
                state = self.storedata(variabledata[0],self.__memory[3][iter1].pop())
                if not state:return False,f"CRITICAL ERROR" 
            return True,""
        else:return False, "CRITICAL ERROR. INTERPRETER FAIL"

    def determinedt(self,data) -> str|None:
        if not data: return "varchar"
        if data == "F" or data == "T":return "bool"
        if data[0] == '"' and data[-1] == '"':return "varchar"
        if data[0] == '"' and data[-1] != '"' or (data[0] != '"' and data[-1] == '"'):return None
        if (data[0] != '"' and data[-1] != '"') and not data.isdigit(): return "var"
        if float(data) == int(float(data)) and data.isdigit(): return "int"
        if (float(data) != int(float(data)) or float(data) == int(float(data))) and not data.isdigit():return "float"
        return None

    def searchvariables(self,variablename) -> tuple[str,str,str|int|float]:
        for each in self.__memory[0]:
            if each[0] == variablename: return each
        return []

    def storedata(self,variablename,data) -> bool:
        for each in self.__memory[0]:
            if each[0] == variablename:
                each[2] = str(data)
                return True
        return False

    def checkmemory(self) -> None: 
        if int(self.__memory[9]) > int(self.__totalmemory):Error().OutError("Memory usage exceeded the said amount.","MEMERROR")  
        if int(self.__memory[9]) < 0:
            Error().OutError("Memory usage less than 0 \n Current memory : {self.__memory[9]} spaces","MEMCRTICERROR")
