class Errors:
    def OutError(self,ErrorType,ErrorPointer) -> None:
        from Interpreter import Interpreter
        currentfile = Interpreter().getCurrentfile()
        actuallines = Interpreter().getactuallines()
        try:
            if int(ErrorPointer) < 0 and currentfile == "!/main": 
                print("CRASH:Negative line-pointer for '!/main' metadata.")
                print("Try changing the file-name(s) if 'bring' command is used")
                exit()
            elif int(ErrorPointer) < 0 and currentfile != "!/main":
                print("CRASH:Negative line-pointer for non '!/main' metadata.")
                print("High probability of an edge case.")
                exit()
        except:pass
        print(f"ERROR[{currentfile}@{actuallines}] : {ErrorType}")   
        exit()


class Warnings:
    def OutWarning(self,WarningType) -> None: 
        print(f"WARNING : {WarningType}")
