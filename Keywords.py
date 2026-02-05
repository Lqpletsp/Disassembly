class Keyword: 
    def __init__(self) -> None:
        self.__Keywords:list = ["out","in","inc","dec", "decv","varchar","int","bool"
                                ,"set", "add", "minus","mult", "div","decf", "endf",
                                "call", "temp"]
        self.__OneDataCommands:list = ["empt","decm","else"]
        self.__TwoOrMoreDataCommands:list = ["out","inc","dec","decv","decf","set", "add",
                                                "minus","div", "mult","cmpt","cmpf",
                                             "decl", "in", "loop","mkcmd"]
        self.__Commands:list = ["out","in","dec","decv","set","add","minus","mult","div","decf",
                                "endf","in","inc","call","decm","cmpt","decl","cmpf","endl",
                                "loop","mkcmd","bring","else","trns"]

    def GetKeywords(self) -> list:return self.__Keywords
    def GetOneVariableCommand(self) -> list: return self.__OneDataCommands
    def GetTwoOrMoreVariableCommand(self) -> list: return self.__TwoOrMoreDataCommands
    def GetCommands(self)-> list: return self.__Commands
