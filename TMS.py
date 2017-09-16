#Set data structure for expanded nodes
#truth3 can add xnew statements successfully and update the kb accordingly, can't deal with negations or retractions yet
class Set:

    def __init__(self):
        self.vals = dict()

    def add(self,val):
        if val in self.vals:
            return
        else:
            self.vals[val] = 1

    def contains(self,val):
        if val in self.vals.keys():
            return True
        else:
            return False


class TMS:
    def __init__(self):
        self.filename = "TMSInput.txt"
        self.f = open(self.filename,"r")
        self.kBase = [] #explicitly added sentences and implications
        self.kDict = dict() #implied sentences
        self.activeStatements = dict() #contains the statements (implications) which are currently active as keys
                                        #and a list of lists of the required values and implied value as a 2-tuple
                                        #eg. activeStatements['A*B->C'] == ([['A','B']],'C')
        self.activeliterals = []
        
        #kBase and kDict combined contain necessary information, kBase contains implications and explicitly added literals,
        #kDict contains the implied literals as keys, and the sentences/literals justifying them as values 

    #main high level algorithm, iterates through lines in the input file, adding them to the knowledge base,
    #and calling parseData, which determines how to adjust the knowledge base after the addition
    def algorithm(self):
        line = self.f.readline()
        while line:
            linesplit = line.split(":")
            if linesplit[0] == "Tell":
                temp = linesplit[1].split("\n")[0]
                self.kBase.append(temp)
                if len(temp) == 2: #negated literal
                    self.parseData(temp,True)
                    self.activeliterals.append(temp)
                    if temp[1] in self.kBase:
                        self.kBase.remove(temp[1])
                elif len(temp) == 1:
                    self.parseData(temp,True)
                    self.activeliterals.append(temp)
                elif len(temp) > 2:
                    self.parseData(temp,True)
                    self.activeliterals.append(temp.split("->")[1])
            
                
                #print(self.kBase)
                #print(self.kDict)
            elif linesplit[0] == "Retract":
                temp = linesplit[1].split("\n")[0]
                if temp in self.kBase:
                    self.kBase.remove(temp)
                if len(temp) > 2:
                    for k in self.kDict.keys():
                        templist = []
                        for val in self.kDict[k]:
                            if temp == val[1]:
                                templist.append(val)
                        for l in templist:
                            self.kDict[k].remove(l)
                self.parseData(temp,False)
                #print(self.kBase)
                #print(self.kDict)
                
            line = self.f.readline()

    #adds a statement to the knowledge base, and parses the and/or parts of it into easily manageable lists
    def addStatement(self,val):
        newvals = val.split("->")
        anotherline = newvals[1].split("\n")
        linev2 = newvals[0].split("+")
        linelist = []
        for subline in linev2:
            nextline = subline.split("*")
            if len(nextline) == 1:
                linelist.append([nextline[0]])
            else:
                templist = []
                for i in range(len(nextline)):
                    templist.append(nextline[i])
                linelist.append(templist)
        self.activeStatements[val] = (linelist,newvals[1])

    #the function that adjusts the knowledge base after a new literal or statement is added
    #it recursively calls itself after making a change until no changes occur, then the main loop will resume
    def parseData(self,q,add):
        if add == True: #if adding something
            if len(q) == 2:
                for x in self.kBase:
                    if x == q[1]:
                        self.kBase.remove(q[1])
                        self.parseData(q[1],False)
                for y in self.activeStatements.keys():
                    for z in self.activeStatements[y][0]:
                        flag = 0
                        for zz in range(len(z)):
                            if zz == len(z)-1 and z[zz] in self.kBase or z[zz] in self.kDict.keys():   ##### changed second and to or
                                flag = 1
                                break
                            if z[zz] not in self.kBase and z[zz] not in self.kDict.keys(): #### changed or to and
                                flag = 0
                                break
                        if flag == 1: #all conditions for implication are met
                            if self.activeStatements[y][1] in self.kDict.keys():
                                if (z,y) not in self.kDict[self.activeStatements[y][1]]:
                                    self.kDict[self.activeStatements[y][1]].append((z,y))
                            elif self.activeStatements[y][1] not in self.kDict.keys():
                                self.kDict[self.activeStatements[y][1]] = [(z,y)]
                                if self.activeStatements[y][1] not in self.kBase:
                                    self.parseData(self.activeStatements[y][1],True)
            elif len(q) == 1:
                for x in self.kBase:
                    if x == ("-" + q):
                        self.kBase.remove(x)
                        self.parseData(x,False)
                for y in self.activeStatements.keys():
                    for z in self.activeStatements[y][0]:
                        flag = 0
                        for zz in range(len(z)):
                            if zz == len(z)-1 and (z[zz] in self.kBase or z[zz] in self.kDict.keys()):
                                flag = 1
                                break
                            if z[zz] not in self.kBase and z[zz] not in self.kDict.keys():
                                flag = 0
                                break
                        if flag == 1: #all conditions for implication are met
                            if self.activeStatements[y][1] in self.kDict.keys():
                                if (z,y) not in self.kDict[self.activeStatements[y][1]]:
                                    self.kDict[self.activeStatements[y][1]].append((z,y))
                            elif self.activeStatements[y][1] not in self.kDict.keys():
                                self.kDict[self.activeStatements[y][1]] = [(z,y)]
                                if self.activeStatements[y][1] not in self.kBase:
                                    self.parseData(self.activeStatements[y][1],True)
            else:
                self.addStatement(q)
                self.parseData(q.split("->")[1],True)

        else: #remove
            if len(q) == 2:
                templist = []
                for k in self.kDict.keys():
                    for lst in self.kDict[k]:
                        flag = 0
                        for l in lst:
                            if q in l:
                                flag = 1
                                break
                        if flag == 1:
                            self.kDict[k].remove(lst)
                    if self.kDict[k] == []:
                        templist.append(k)

                for k in templist:
                    del self.kDict[k]
                    if k not in self.kBase:
                        self.parseData(k,False)
                        
            elif len(q) == 1:
                templist = []
                for k in self.kDict.keys():
                    for lst in self.kDict[k]:
                        flag = 0
                        for l in lst:
                            if q in l:
                                flag = 1
                                break
                        if flag == 1:
                            self.kDict[k].remove(lst)
                    if self.kDict[k] == []:
                        templist.append(k)

                for k in templist:
                    del self.kDict[k]
                    if k not in self.kBase:
                        self.parseData(k,False)
            elif len(q) > 2:
                x = 0

    def parseOutput(self):
        print("State of TMS\n")
        for x in self.kBase:
            print(x)
        for k,v in self.kDict.items():
            
            print(k + " : ",end="")
            print(v)
        
            
                        
                
        
            
                
            
x = TMS()
x.algorithm()
x.parseOutput()
