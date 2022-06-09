from Classes.genome import Genoma
import datetime
import bisect
#import rapids

class GeneticAlgorithm():
    def __init__(self, step = 1/16, alpha = 0, y = 10, maxGeneration = 400000):
        self.step = step
        self.alpha = alpha
        self.y = y
        self.startTime = datetime.datetime.now()
        self.data_atual = datetime.datetime.today()
        self.countGeneration = 0
        self.totalGeneration = 0
        self.maxGeneration = maxGeneration
        self.histogram= []

    def display(self, guess, fitness):
        sguess = ' '.join(guess)
        timeDiff = datetime.datetime.now() - self.startTime
        print("{0}\t {1}\t {2}\t Geração: {3}\n ".format(sguess, fitness, str(timeDiff), self.totalGeneration))

    def saveNetlists(self, generation, fitness, countGeneration):
        fImprovedNetlist = open("Netlists improved.txt", 'a', encoding='utf-8')      # The file that save the improveds genomes
        
        data_atual = datetime.datetime.today()
        sbestParent = ' '.join(generation)                                           # Convert the child in str to append the genome in Netlists improved.txt
        appendFile = sbestParent+" at "+str(data_atual)+ " " + str(fitness) + " Geração: "+str(countGeneration) + "\n"  # Make the string format to append
        fImprovedNetlist.write(appendFile)                                           # Append the string in Netlists improved.txt 
        fImprovedNetlist.close()

    def makeHistgram(self, childFitness):                                                  # make the histogram list                                                         
        bisect.insort(self.histogram,str(childFitness))                                # Using the bisect library, insert the fitness garanting the sorting

    def saveHistogram(self):
        fHistogram = open("histgramArray.txt", 'a', encoding='utf-8')
        sHistogramList = ','.join(self.histogram)                                           # Convert the histogram in str to append in histgramArray.txt
        appendFile = sHistogramList
        fHistogram.write(appendFile)                                                     
        fHistogram.close()

    def getBestChild(self, listChild):
        bestChild = listChild[0]
        for child in listChild:
            if(child.fitness > bestChild.fitness):
                bestChild = child
        return bestChild

    def evolution(self):
        
        fImprovedNetlist = open("Netlists improved.txt", 'a', encoding='utf-8')      # 
        fImprovedNetlist.write("\n")                                                 # Put a \n in the end of the file to indent
        fImprovedNetlist.close()    
        
        bestParent = Genoma() 
        bestParent.generate_parent() # Generate the first generation (The first Parent)
        bestParent.newCalculateFitness()  # Get the first generation fitness
        bestFitness = bestParent.fitness
        self.display(bestParent.genotipo, bestParent.fitness)

        self.saveNetlists(bestParent.genotipo, bestParent.fitness, self.countGeneration) # The file that save the improveds genomes

        
        while True:
            #self.countGeneration = self.countGeneration + 1
            self.totalGeneration = self.totalGeneration + 1        
            #if(self.countGeneration>=100):
            #    self.alpha = 3*self.step
            if(self.totalGeneration>=self.maxGeneration):
                break
            listChild = []
            for i in range(0, self.y):
                child = Genoma()
                bestParent.mutate().copyGene(child)   
                child.newCalculateFitness()
                listChild.append(child)
            
            child = self.getBestChild(listChild)    
            
            self.makeHistgram(child.fitness)
            if(child.genotipo == bestParent.genotipo):          # if the child is the same of the parent (a failed mutate) try mutate again
                continue
            if ((bestFitness - self.alpha) >= child.fitness):   # if the child is better than the parent (a successful mutate)
                continue
            
            self.saveNetlists(child.genotipo, child.fitness, self.totalGeneration) # The file that save the improveds genomes
            
            self.display(child.genotipo, child.fitness)

            self.countGeneration = 0
            #self.alpha = 0
            if (child.fitness >= 1):    # if the child fitness is 1 or the we have more than 10000 tries of mutation to that child, end the algorithm
                break
            bestFitness = child.fitness
            child.copyGene(bestParent)
            
    def evolution2(self):

        bestParent = Genoma() 
        bestParent.generate_parent(24) # Generate the first generation (The first Parent)
        bestParent.calculateFitness(24)  # Get the first generation fitness
        bestFitness = bestParent.fitness
        self.display(bestParent.genotipo, bestParent.fitness)
        while True:
            listChild = []
            for i in range(0, self.y):
                childaux = Genoma()
                bestParent.mutate(self.n).copyGene(childaux)   
                childaux.calculateFitness(24)
                listChild.append(childaux)
        
            for child in listChild:
                print("Child Genotipo: ", child.genotipo)
                print("Child fitness: ", child.fitness)
                print("-------------------------------------------------------")
            print("List[0]: ", listChild[0].fitness)
            child = Genoma()

            child = self.getBestChild(listChild)
            print("Best child: ", child.genotipo)

            if(child.genotipo == bestParent.genotipo):          # if the child is the same of the parent (a failed mutate) try mutate again
                continue
            if ((bestFitness - self.alpha) >= child.fitness):   # if the child is better than the parent (a successful mutate)
                continue

            self.display(child.genotipo, child.fitness)
            print(child.indexDeadGenes)
            print(child.indexActiveGenes)
            self.countGeneration = 0
            #self.alpha = 0
            if (child.fitness >= 1):    # if the child fitness is 1 or the we have more than 10000 tries of mutation to that child, end the algorithm
                break
            bestFitness = child.fitness
            child.copyGene(bestParent)
            