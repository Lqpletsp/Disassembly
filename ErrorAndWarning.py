import sys
class Errors:
    def OutError(self,ErrorType,ErrorPointer,currentfile) -> None:
        try:
            if int(ErrorPointer) < 0 and currentfile == "!/main": 
                print("CRASH:Negative line-pointer for '!/main' metadata.")
                print("High probability of an edge case.")
                exit()
            elif int(ErrorPointer) < 0 and currentfile != "!/main":
                print("CRASH:Negative line-pointer for non '!/main' metadata.")
                print("High probability of an edge case.")
                sys.exit(1)
        except:pass
        print(f"ERROR[{currentfile}@{ErrorPointer}] : {ErrorType}")   
        sys.exit(1)


class Warnings:
    def OutWarning(self,WarningType) -> None: 
        print(f"WARNING : {WarningType}")
