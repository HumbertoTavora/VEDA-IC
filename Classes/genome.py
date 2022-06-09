from multiprocessing.sharedctypes import copy
import os
from quopri import decodestring
from random import *
import random
from Classes.dataStructures import Stack

class Genoma:
    def __init__(self, numberOfGenes = 80, nOutputs = 16, rateMutation = 0.3):
        self.genotipo = []
        self.copyGenotipo = []
        self.numberOfGenes = numberOfGenes
        self.fitness = 0.0
        self.rateMutation = rateMutation
        self.indexDeadGenes = []
        self.indexActiveGenes = []
        self.nOutputs = nOutputs

    def fill_Initial_Genome(self):
        for i in range (0,self.numberOfGenes):
            self.genotipo.append("")

    def fill_firstInputs_Genome(self, input1 = "00", input2 = "00"):

        sin1 = input1
        sin2 = input2
        gene = sin1 + sin2
        self.genotipo.pop(0)
        self.genotipo.insert(0, gene)      

    def generate_parent(self):  
        self.index1, self.index2, self.index3, self.index4 = random.sample(list(range(0,self.numberOfGenes-1)), 4)   # including the 4 inputs in a random position of the genome (Exception by the last position OUTPUT)

        
        self.fill_Initial_Genome()          # fill the genome with the rigth length
        self.fill_firstInputs_Genome()       # make the first genome conect the first input [0][0]

        for i in range(1,self.numberOfGenes):
            in1 = randint(0,i+3)    # returns a number between 0 and n (PS: in randint() both inputs are included)
            in2 = randint(0,i+3)    # returns a number between 0 and n (PS: in randint() both inputs are included)

            if(in1 < 10):
                sin1 = "0" + str(in1)
            else:
                sin1 = str(in1)
            if(in2 < 10):
                sin2 = "0" + str(in2)
            else:
                sin2 = str(in2)

            gene = sin1 + sin2
            self.genotipo.pop(i)
            self.genotipo.insert(i, gene)

    def modela_frase(self, a,b,c):    #Function that models a verilog assign by the Output,input1,input2 in NAND Format
            frase ="assign	"+a+" = ~("+b+" & "+c+");\n\n"
            return frase
    
    def withdraw_deadGenes(self):  #Withdraw the genes that won't be used in any other position of the genome
            count = 1
            s = Stack()
            while(True):
                self.indexDeadGenes = []
                for j in range(0,self.numberOfGenes-1):       
                    for i in range (0,self.numberOfGenes):       #The iº gene of the genome. To each element of the list (each gene of genome) exception by the last (the last one is necessarily the output of the system).
                        nin1 = self.copyGenotipo[i][0:2]  #The fisrt half (the input1)
                        nin2 = self.copyGenotipo[i][2:4]  #The first half (the input2)
                        if(j+4 < 10):
                            elementSearch = "0"+str(j+4)
                        else:
                            elementSearch = str(j+4)

                        if(elementSearch == nin1 or elementSearch == nin2):
                            break

                        elif(i == self.numberOfGenes-1):
                            self.copyGenotipo[j] = "xxxx"
                            self.indexDeadGenes.append(j)

                s.push(len(self.indexDeadGenes))

                if s.size() == 2:
                    felement = s.pop()
                    selement = s.pop()
                    if(selement == felement):
                        break
                    s.push(felement)

            for i in range(0,self.numberOfGenes):
                if(self.copyGenotipo[i] != "xxxx"):
                    self.indexActiveGenes.append(i)
                    
    def modela_inputs(self, nin):

        if(nin == "00"):
            sin = "I0" 
        elif nin == "01":
            sin = "I1" 
        elif nin == "02":
            sin = "I2" 
        elif nin == "03":
            sin = "I3"
        else:
            sin = "WIRE_"+nin    

        return sin

    def modela_outputs(self, nout,i):

        if i==self.numberOfGenes-1:
            out = "paridade_par"
        else:
            out = "WIRE_"+nout

        return out

    def verilog_maker_by_genotipo(self):
 
        
        self.copyGenotipo = self.genotipo.copy()

        self.withdraw_deadGenes()

        with open("GPINAND.v",'w',encoding = 'utf-8') as f:
            
            f.write("module GPINAND(I0,I1,I2,I3,paridade_par);\n\n")
            
            f.write("input wire	I0;\ninput wire  I1;\ninput wire	I2;\ninput wire  I3;\noutput wire    paridade_par;\n\n")
            
            for i in range(4,self.numberOfGenes+4-1):
                f.write("wire	WIRE_"+str(i)+";\n")

            f.write("\n")
       
            count = 4
            for i in range(0,self.numberOfGenes):

                if(count <10):                    # threat <10 cases ( 9 != 09 ) 1,2,3,4,5,6,7,8,9
                    nout = "0"+str(count)
                else:
                    nout = str(count)
                count = count + 1
                nin1 = self.copyGenotipo[i][0:2]            # 0202 0303 0404 0505 0603 0207 0805 0409 1011 1213 0000 0000 1414 1515 0000 0000 1815 1914 0000 0000 0000 0000 0000 2223
                nin2 = self.copyGenotipo[i][2:4]

                if (nin1 != "xx" or nin1 == nout or nin2 == nout):

                    in1 = self.modela_inputs(nin1)
                    in2 = self.modela_inputs(nin2)
                    out = self.modela_outputs(nout,i)

                    frase = self.modela_frase(out,in1,in2)
                    f.write(frase)

            f.write("\n\nendmodule")

    def calculateFitness(self):
        self.indexDeadGenes.clear()
        self.indexActiveGenes.clear()
        self.verilog_maker_by_genotipo()
        os.system('cmd /c "iverilog -o prog GPINAND_tb.v GPINAND.v"') 
        os.system('cmd /c "vvp prog"') 
        
        fnetlist = open("output_NetlistGPINAND.txt", 'r', encoding='utf-8')
        ftrue = open("output_TrueGPINAND.txt", 'r', encoding='utf-8')

        contador = 0

        for i in range(0,self.nOutputs):    # nOutputs (16) is the number of possibles outputs to the 4bitGPINAND
            out1 = ftrue.readline()
            out2 = fnetlist.readline()

            if out1 == out2:
                contador = contador + 1

        fitness = float(contador/self.nOutputs)
        fnetlist.close()
        ftrue.close()

        self.fitness = fitness   

        return self.fitness

    def gpinand(self, in1,in2,in3,in4):
        count = 0
        if(in1 == 1):
            count +=1
        if(in2 == 1):
            count +=1
        if(in3 == 1):
            count +=1
        if(in4 == 1):
            count +=1  
        if(count%2 == 0):
            return 0
        else: 
            return 1

    def f(self,a,b):
        if(not(a and b)):
            return 1
        else:
            return 0

    def newCalculateFitness(self):
        fitnessCounter = 0
        for i0 in range(0,2):
            for i1 in range(0,2):
                for i2 in range(0,2):
                    for i3 in range(0,2):
                        valuesTable = {'00':i0, '01':i1, '02':i2, '03':i3}
                        i = 4
                        for element in self.genotipo:
                            in1 = element[0:2]
                            in2 = element[2:4]
                            out = self.f(valuesTable[in1], valuesTable[in2])
                            if(i<10):
                                si = "0"+str(i)
                            else:
                                si = str(i)
                            valuesTable[si] = out
                            i+=1
                        if(valuesTable[si] == self.gpinand(valuesTable['00'],valuesTable['01'],valuesTable['02'],valuesTable['03'])):
                            fitnessCounter += 1
        self.fitness = float(fitnessCounter/self.nOutputs)

    def copyGene(self, destiny):
        destiny.genotipo = self.genotipo.copy()
        destiny.copyGenotipo = self.copyGenotipo
        destiny.fitness = self.fitness 
        destiny.indexDeadGenes = self.indexDeadGenes
        destiny.indexActiveGenes = self.indexActiveGenes 
        destiny.nOutputs = self.nOutputs 
        destiny.index1 = self.index1
        destiny.index2 = self.index2
        destiny.index3 = self.index3
        destiny.index4 = self.index4
        
    def mutateWithParam(self):
        
        childGenes = Genoma()                                                    # a copy of the parente that will be mutate
        self.copyGene(childGenes)


        deadMutationIndex = int(len(self.indexDeadGenes) * 1)    # 50% of the active genes will be mutate
        i=0
        while(i < deadMutationIndex):
            
            indexMut = random.sample(self.indexDeadGenes, 1)
            index = int(indexMut[0])
            newGene,alternate = random.sample(list(range(0,index+3)),2)

            if newGene < 10:
                newGene = "0"+str(newGene)
            newGene = str(newGene)    
            if alternate < 10:
                alternate = "0"+str(alternate)
            alternate = str(alternate)  

            inputPosition = randint(0,1)                            # in the random input of the gene (the first or second)

            if inputPosition == 0:                                  # if the input that need to be mutate is the first:
                if index == self.index1 or index == self.index2 or index == self.index3 or  index == self.index4:    
                    return self                                     # if the index of any mutate is the same of the inputs index, return parent

                if newGene == childGenes.genotipo[index][0:2]:
                    childGenes.genotipo[index] = alternate + str(childGenes.genotipo[index][2:4])     
                else:
                    childGenes.genotipo[index] = newGene + str(childGenes.genotipo[index][2:4])

            else:
                if newGene == childGenes.genotipo[index][2:4]:               # if the input that need to be mutate is the second:
                    childGenes.genotipo[index] = str(childGenes.genotipo[index][0:2]) + alternate
                else: 
                    childGenes.genotipo[index] = str(childGenes.genotipo[index][0:2]) + newGene

            i+=1

        activeMutationIndex = max(2,int(len(self.indexActiveGenes) * 1) ) # 20% of the active genes will be mutate
        j = 0
        while(j < activeMutationIndex):
            indexMut = random.sample(self.indexActiveGenes, 1)
            index = int(indexMut[0])
            newGene,alternate = random.sample(list(range(0,index+3)),2)

            if newGene < 10:
                newGene = "0"+str(newGene)
            newGene = str(newGene)    
            if alternate < 10:
                alternate = "0"+str(alternate)
            alternate = str(alternate)   
            
            inputPosition = randint(0,1)                            # in the random input of the gene (the first or second)

            if inputPosition == 0:                                  # if the input that need to be mutate is the first:
                if index == self.index1 or index == self.index2 or index == self.index3 or  index == self.index4:    
                    return self                                   # if the index of any mutate is the same of the inputs index, return parent

                if newGene == childGenes.genotipo[index][0:2]:
                    childGenes.genotipo[index] = alternate + str(childGenes.genotipo[index][2:4])     
                else:
                    childGenes.genotipo[index] = newGene + str(childGenes.genotipo[index][2:4])

            else:
                if newGene == childGenes.genotipo[index][2:4]:               # if the input that need to be mutate is the second:
                    childGenes.genotipo[index] = str(childGenes.genotipo[index][0:2]) + alternate
                else: 
                    childGenes.genotipo[index] = str(childGenes.genotipo[index][0:2]) + newGene
            j +=1
        
        return childGenes
    
    def mutate(self):
        
        childGenes = Genoma()                                                    # a copy of the parente that will be mutate
        self.copyGene(childGenes)
        
        numberOfMutations = max(self.numberOfGenes*self.rateMutation,1)

        for i in range(0,int(numberOfMutations)):

            indexMut = randint(1,self.numberOfGenes-1)

            newGene,alternate = random.sample(list(range(0,indexMut+4)),2)

            if newGene < 10:
                newGene = "0"+str(newGene)
            newGene = str(newGene)    
            if alternate < 10:
                alternate = "0"+str(alternate)
            alternate = str(alternate)   

            wichInput = randint(0,1) 
            if(wichInput == 0):
                if newGene == childGenes.genotipo[indexMut][0:2]:
                    childGenes.genotipo[indexMut] = alternate + str(childGenes.genotipo[indexMut][2:4])
                else: 
                    childGenes.genotipo[indexMut] = newGene + str(childGenes.genotipo[indexMut][2:4])
            else:
                if newGene == childGenes.genotipo[indexMut][2:4]:
                    childGenes.genotipo[indexMut] = str(childGenes.genotipo[indexMut][2:4]) + alternate
                else: 
                    childGenes.genotipo[indexMut] = str(childGenes.genotipo[indexMut][2:4]) + newGene

        
        return childGenes