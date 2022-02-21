from operator import index
from random import *
import random
import datetime
import os
#sblawid

n = 24
                                                                        # The random.sample() ensures that each index will not be the repeated
index1, index2, index3, index4 = random.sample(list(range(0,n-1)), 4)   # including the 4 inputs in a random position of the genome (Exception by the last position OUTPUT)
indexDeadGenes = []
eachIndexDeadGenes = [] 
startTime = datetime.datetime.now()                # Start a timer to get each time of improvement of the genome
data_atual = datetime.datetime.today()             # Get the actual time and date to document the in "Netlists improved.txt"
countGeneration = 1

def generate_parent(n):  

    def fill_Initial_Genome(genome):
        for i in range (0,n):
            genome.append("")
    def fill_firstInputs_Genome(genome):

        genome.pop(index1)
        genome.insert(index1, 0)         # the first input is the number 0, so, we have 00 01 02 03 how the 4 inputs

        genome.pop(index2)
        genome.insert(index2, 1)
        
        genome.pop(index3)
        genome.insert(index3, 2)
        
        genome.pop(index4)
        genome.insert(index4, 3)




    genome = []
    fill_Initial_Genome(genome)         # fill the genome with the rigth length
    fill_firstInputs_Genome(genome)     # distributes at least 1 of each entry to ensure its presence in the genome (logical validation)


    for i in range(0,n):
        if(i == index1 or i == index2 or i == index3 or i == index4):
            in1 = genome[i]
            in2 = randint(0,i+3)    # returns a number between 0 and n (PS: in randint() both inputs are included)
        else:
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
        genome.pop(i)
        genome.insert(i, gene)


    return genome

def verilog_maker_by_genome(n,netlist):

    def modela_frase(a,b,c):    #Function that models a verilog assign by the Output,input1,input2 in NAND Format

        frase ="assign	"+a+" = ~("+b+" & "+c+");\n\n"
        return frase

    def withdraw_deadGenes(netlist,n):  #Withdraw the genes that won't be used in any other position of the genome
        
        for j in range(0,n-1):          #
            for i in range (0,n):       #The iº gene of the genome. To each element of the list (each gene of genome) exception by the last (the last one is necessarily the output of the system).
                nin1 = netlist[i][0:2]  #The fisrt half (the input1)
                nin2 = netlist[i][2:4]  #The first half (the input2)

                if(j+4 < 10):
                    elementSearch = "0"+str(j+4)
                else:
                    elementSearch = str(j+4)

                if(elementSearch == nin1 or elementSearch == nin2):
                    break

                elif(i == n-1):
                    eachIndexDeadGenes.append(j)
                    netlist[j] = "xxxx"

    def modela_inputs(nin,i):

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

    def modela_outputs(nout,i,n):

        if i==n-1:
            out = "paridade_par"
        else:
            out = "WIRE_"+nout

        return out

    vmbg_netlist = netlist.copy()

    withdraw_deadGenes(vmbg_netlist,n)

    with open("GPINAND.v",'w',encoding = 'utf-8') as f:
        
        f.write("module GPINAND(I0,I1,I2,I3,paridade_par);\n\n")
        
        f.write("input wire	I0;\ninput wire  I1;\ninput wire	I2;\ninput wire  I3;\noutput wire    paridade_par;\n\n")

        f.write("wire	WIRE_04;\nwire	WIRE_05;\nwire	WIRE_06;\nwire	WIRE_07;\nwire	WIRE_08;\nwire	WIRE_09;\nwire	WIRE_10;\nwire	WIRE_11;\nwire	WIRE_12;\nwire	WIRE_13;\nwire	WIRE_14;\nwire	WIRE_15;\nwire	WIRE_16;\nwire	WIRE_17;\nwire	WIRE_18;\nwire	WIRE_19;\nwire	WIRE_20;\nwire	WIRE_21;\nwire	WIRE_22;\nwire	WIRE_23;\nwire	WIRE_24;\nwire	WIRE_25;\nwire	WIRE_26;\n\n")
    
        count = 4
        for i in range(0,n):
            
            if(count <10):                    # threat <10 cases ( 9 != 09 ) 1,2,3,4,5,6,7,8,9
                nout = "0"+str(count)
            else:
                nout = str(count)
            count = count + 1
            nin1 = vmbg_netlist[i][0:2]            # 0202 0303 0404 0505 0603 0207 0805 0409 1011 1213 0000 0000 1414 1515 0000 0000 1815 1914 0000 0000 0000 0000 0000 2223
            nin2 = vmbg_netlist[i][2:4]
            
            
            if nin1 != "xx":
                
                in1 = modela_inputs(nin1,i)
                in2 = modela_inputs(nin2,i)
                out = modela_outputs(nout,i,n)

                frase = modela_frase(out,in1,in2)
                f.write(frase)

        f.write("\n\nendmodule")

def get_fitness_by_outputs(nOutputs):

    fnetlist = open("output_NetlistGPINAND.txt", 'r', encoding='utf-8')
    ftrue = open("output_TrueGPINAND.txt", 'r', encoding='utf-8')

    contador = 0

    for i in range(0,nOutputs):
        out1 = ftrue.readline()
        out2 = fnetlist.readline()

        if out1 == out2:
            contador = contador + 1

    fitness = float(contador/nOutputs)
    rfitness = fitness

    fnetlist.close()
    ftrue.close()

    return rfitness

def display(n,guess):
  sguess = ' '.join(guess)
  timeDiff = datetime.datetime.now() - startTime
  fitness = get_fitness(n,guess)
  print("{0}\t {1}\t {2}\t Geração: {3}\n ".format(sguess, fitness, str(timeDiff), countGeneration))

def get_fitness(n,genome):
    eachIndexDeadGenes.clear()
    verilog_maker_by_genome(n,genome)
    os.system('cmd /c "iverilog -o prog GPINAND_tb.v GPINAND.v"') 
    os.system('cmd /c "vvp prog"') 
    return get_fitness_by_outputs(16)   # 16 is the number of the n possibles outputs to the 4bitGPINAND

def mutateV1(n,parent):      # a mutate to each input of the gene

    arrayIndex = []
    indexMut1,indexMut2,indexMut3, indexMut4 = random.sample(list(range(0,n)), 4)            # take the 3 index that will be mutate / The range funcion create a sequence of number until n not including itself
    arrayIndex.append(indexMut1)                                                  # append the index1
    arrayIndex.append(indexMut2)                                                  # append the index2
    arrayIndex.append(indexMut3)                                                  # append the index3
    arrayIndex.append(indexMut4)                                                  # append the index4

    childGenes = parent.copy()                                                    # a copy of the parente that will be mutate

    i = 0
    while (i<4):                                                                  # to each index in arrayIndex, do the mutation
        index = int(arrayIndex[i])       
        newGene,alternate = random.sample(list(range(0,index+4)),2)                      # generate the random value by the rule NumberInput < NumberPosition (adding 4 by the inputs) / The range funcion create a sequence of number until n not including itself
                                                                # generate another random value (to the case that the newGene is the same of the oldGene)

        if newGene < 10:
            newGene = "0"+str(newGene)
        newGene = str(newGene)    
        if alternate < 10:
            alternate = "0"+str(alternate)
        alternate = str(alternate)   

        inputPosition = randint(0,1)                            # in the random input of the gene (the first or second)
        
        if inputPosition == 0:                                  # if the input that need to be mutate is the first:
            if index == index1 or index == index2 or index == index3 or  index == index4:    
                return parent                                   # if the index of any mutate is the same of the inputs index, return parent

            if newGene == childGenes[index][0:2]:
                childGenes[index] = alternate + str(childGenes[index][2:4])     
            else:
                childGenes[index] = newGene + str(childGenes[index][2:4])

        else:
            if newGene == childGenes[index][2:4]:               # if the input that need to be mutate is the second:
                childGenes[index] = str(childGenes[index][0:2]) + alternate
            else: 
                childGenes[index] = str(childGenes[index][0:2]) + newGene
        

        i = i + 1
    
    return childGenes

def mutateV2(n,parent):      # a mutate to each gene (both the inputs will be mutates)
       
    arrayIndex = []

    indexMut1,indexMut2,indexMut3 = random.sample(list(range(0,n)), 3)
    arrayIndex.append(indexMut1)
    arrayIndex.append(indexMut2)
    arrayIndex.append(indexMut3)

    childGenes = parent.copy()

    i = 0
    while (i<3):
        index = int(arrayIndex[i])
        newGene0,alternate0,newGene1,alternate1 = random.sample(list(range(0,index+4)),4)

        if newGene0 < 10:
            newGene0 = "0"+str(newGene0)
        newGene0 = str(newGene0)    
        if alternate0 < 10:
            alternate0 = "0"+str(alternate0)
        alternate0 = str(alternate0)   
        if newGene1 < 10:
            newGene1 = "0"+str(newGene1)
        newGene1 = str(newGene1)    
        if alternate1 < 10:
            alternate1 = "0"+str(alternate1)
        alternate1 = str(alternate1) 
        
        if index == index1 or index == index2 or index == index3 or  index == index4:
            return parent
        if newGene0 == childGenes[index][0:2]:
            if newGene1 == childGenes[index][2:4]:
                childGenes[index] = alternate0 + alternate1
            else:
                childGenes[index] = alternate0 + newGene1
        else: 
            if newGene1 == childGenes[index][2:4]:
                childGenes[index] = newGene0 + alternate1
            else:
                childGenes[index] = newGene0 + newGene1
        

        i = i + 1
    
    return childGenes

def mutateV3(n,parent):
    arrayIndex = []

    indexMut1,indexMut2 = random.sample(indexDeadGenes, 2)
    indexMut3 = randint(0,n-1)

    arrayIndex.append(indexMut1)
    arrayIndex.append(indexMut2)
    arrayIndex.append(indexMut3)
    childGenes = parent.copy()

    i = 0
    while (i<3):
        index = int(arrayIndex[i])
        newGene0,alternate0,newGene1,alternate1 = random.sample(list(range(0,index+4)),4)

        if newGene0 < 10:
            newGene0 = "0"+str(newGene0)
        newGene0 = str(newGene0)    
        if alternate0 < 10:
            alternate0 = "0"+str(alternate0)
        alternate0 = str(alternate0)   
        if newGene1 < 10:
            newGene1 = "0"+str(newGene1)
        newGene1 = str(newGene1)    
        if alternate1 < 10:
            alternate1 = "0"+str(alternate1)
        alternate1 = str(alternate1) 
        
        if index == index1 or index == index2 or index == index3 or  index == index4:
            return parent
        if newGene0 == childGenes[index][0:2]:
            if newGene1 == childGenes[index][2:4]:
                childGenes[index] = alternate0 + alternate1
            else:
                childGenes[index] = alternate0 + newGene1
        else: 
            if newGene1 == childGenes[index][2:4]:
                childGenes[index] = newGene0 + alternate1
            else:
                childGenes[index] = newGene0 + newGene1
        

        i = i + 1

    return childGenes

def mutateV4(n,parent):
   
    arrayIndex = []

    indexMut1,indexMut2 = random.sample(indexDeadGenes, 2)            
    indexMut3,indexMut4 = (indexMut1+1, indexMut2+1)            # take the 2 index that will be mutate / The range funcion create a sequence of number until n not including itself
    
    while(indexMut3 in indexDeadGenes):
        indexMut3+=1
    
    while(indexMut4 in indexDeadGenes):
        indexMut4+=1


    
    arrayIndex.append(indexMut1)                                                  # append the index1
    arrayIndex.append(indexMut2)                                                  # append the index2
    arrayIndex.append(indexMut3)                                                  # append the index3
    arrayIndex.append(indexMut4)                                                  # append the index4

    childGenes = parent.copy()                                                    # a copy of the parente that will be mutate

    i = 0

    while (i<4):                                                                  # to each index in arrayIndex, do the mutation
        index = int(arrayIndex[i])  
        if(i == 2):
            newGene = indexMut1 + 4 
            alternate = indexMut1 + 4     
        if(i == 3):
            newGene = indexMut2 + 4
            alternate = indexMut2 + 4
        else:    
            newGene,alternate = random.sample(list(range(0,index+4)),2)                      # generate the random value by the rule NumberInput < NumberPosition (adding 4 by the inputs) / The range funcion create a sequence of number until n not including itself
                                                                                             # generate another random value (to the case that the newGene is the same of the oldGene)

        if newGene < 10:
            newGene = "0"+str(newGene)
        newGene = str(newGene)    
        if alternate < 10:
            alternate = "0"+str(alternate)
        alternate = str(alternate)   

        inputPosition = randint(0,1)                            # in the random input of the gene (the first or second)
        
        if inputPosition == 0:                                  # if the input that need to be mutate is the first:
            if index == index1 or index == index2 or index == index3 or  index == index4:    
                return parent                                   # if the index of any mutate is the same of the inputs index, return parent

            if newGene == childGenes[index][0:2]:
                childGenes[index] = alternate + str(childGenes[index][2:4])     
            else:
                childGenes[index] = newGene + str(childGenes[index][2:4])

        else:
            if newGene == childGenes[index][2:4]:               # if the input that need to be mutate is the second:
                childGenes[index] = str(childGenes[index][0:2]) + alternate
            else: 
                childGenes[index] = str(childGenes[index][0:2]) + newGene
        

        i +=1
    
    return childGenes

def geneticAlgorithm():

    global countGeneration
    global indexDeadGenes
    bestParent = generate_parent(24)
    bestFitness = get_fitness(24,bestParent)
    display(24,bestParent)
    fImprovedNetlist = open("Netlists improved.txt", 'a', encoding='utf-8')                                     # The file that save the improveds genomes
    fImprovedNetlist.write("\n")                                                                                # A \ n in the file to indent
    sbestParent = ' '.join(bestParent)                                                                          # Convert the child in str to append the genome in Netlists improved.txt
    appendFile = sbestParent+" at "+str(data_atual)+ " " + str(bestFitness) + " Geração: "+str(countGeneration) + "\n"  # Make the string format to append
    fImprovedNetlist.write(appendFile)                                                                              # Append the string in Netlists improved.txt 
    indexDeadGenes = eachIndexDeadGenes.copy()
    print(indexDeadGenes)
    while True:
        if(len(indexDeadGenes) >= 6):
            child = mutateV4(n,bestParent)
    
        countGeneration = countGeneration + 1
        if(child == bestParent):                                                                                # if the child is the same of the parent (a failed mutate) try mutate again
            continue
        childFitness = get_fitness(n,child)
        if bestFitness >= childFitness:
            continue
        
        schild = ' '.join(child)                                                                                # Convert the child in str to append the genome in Netlists improved.txt
        appendFile = schild+" at "+str(datetime.datetime.now())+" "+str(childFitness) + " Geração: "+str(countGeneration) + "\n"   # Make the string format to append
        fImprovedNetlist.write(appendFile)                                                                      # Append the string in Netlists improved.txt
        display(24,child)
        indexDeadGenes = eachIndexDeadGenes.copy()
        print(indexDeadGenes)
        if (childFitness >= 1 or countGeneration>=10000):
            break
        bestFitness = childFitness
        bestParent = child

    
    fImprovedNetlist.close()


geneticAlgorithm()