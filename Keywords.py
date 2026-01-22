class Keyword: 
    def __init__(self) -> None:
        self.__Keywords:list = ["out","in","inc","dec", "decv","varchar","int","bool"
                                ,"set","empt", "add", "minus","mult", "div","decf", "endf",
                                "call","temp","decl","endl","!dne","!e","loop"]
        self.__OneDataCommands:list = ["decm"]
        self.__TwoOrMoreDataCommands:list = ["out","inc","dec","decv","decf","set", "add",
                                                "minus","div", "mult","cmpt","cmpf",
                                             "decl", "in", "loop"]
        self.__Datatypes:list = ["varchar","int","float","bool"]
        self.__Commands:list = ["out","in","dec","decv","set","empt","add","minus","mult","div","decf",
                                "endf","in","inc","call","decm","cmpt","decl","cmpf","endl",
                                "loop"]

    def GetKeywords(self) -> list:return self.__Keywords
    def GetOneVariableCommand(self) -> list: return self.__OneDataCommands
    def GetTwoOrMoreVariableCommand(self) -> list: return self.__TwoOrMoreDataCommands
    def GetDataTypes(self) -> list: return self.__Datatypes
    def GetCommands(self)-> list: return self.__Commands
