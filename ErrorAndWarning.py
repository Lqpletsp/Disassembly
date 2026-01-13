class Errors:
    def OutError(self,ErrorType,ErrorPointer) -> None: 
        print(f"ERROR[{ErrorPointer}] : {ErrorType}")   
        exit()


class Warnings:
    def OutWarning(self,WarningType) -> None: 
        print(f"WARNING : {WarningType}")
