class Tokenizer:

    def HandleCode(self,Code) -> list:
        if Code[:6] == "!File:":
            file = open(Code[6:],'r')
            lines = file.readlines()
            if not lines: return []
            Code = ''.join(lines)
        
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
            CodeLine = self.Tokenize(Code[counter])
            if CodeLine:CodeLines.append(CodeLine)
        return CodeLines

    def Tokenize(self,line) -> list:
        token,Storetokens = "", []
        if not line: return None
        inquotation,incomments = False,False
        count = 0
        while count < len(line):
            ch = line[count]
            if incomments:
                count += 1 
                continue

            if (ch == '"' and not inquotation) and not incomments:
                inquotation = True
                token += '"'
                count += 1
                continue

            if (ch == '"' and inquotation) and not incomments:
                token += '"'
                Storetokens.append(token)
                token = ""
                inquotation = False
                count += 1
                continue

            if inquotation:
                token += ch
                count += 1
                continue

            if ch == '|' and not incomments:
                incomments = True
                count += 1 
                continue
            if ch == '|' and incomments: 
                incomments = False
                count += 1 
                continue

            if ch == " " or ch == ",":
                if token != "":
                    Storetokens.append(token)
                    token = ""
                count += 1 
                continue

            if ch == ";":
                if Storetokens != "":Storetokens.append(token)
                break

            else: 
                token += ch 
                count += 1
        return Storetokens
