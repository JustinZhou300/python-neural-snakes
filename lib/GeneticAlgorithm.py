import random
import numpy as np
import copy

def FitnessProportionateSelection(fitnessScores,numSelections):
    '''
     Inputs-> fitnessScores : row vector of scores unordered
     numSelections: integer of for num of outputs
     Outputs-> selectionIndex: list of index numbers
    '''
    descendingScores = np.sort(fitnessScores)[::-1]
    descendingScoresIndex = np.argsort(fitnessScores)[::-1]
    normalisedDescendingScores = descendingScores /sum(fitnessScores)
    selectionsIndex = []
    for i in range(numSelections):
        randomNum = random.random()
        cumulativeScore = 0
        for j in range(len(normalisedDescendingScores)):
            cumulativeScore += normalisedDescendingScores[j]
            if randomNum < cumulativeScore:
                selectionsIndex.append(descendingScoresIndex[j])
                break
    return selectionsIndex


def CrossOverFFNN(parentA,parentB,mutationRate,mutationRange):
    '''
    Inputs-> parentA and parentB: Parent Neural Nets
             mutationRate: Probability of mutation
             mutationRange: mutate by up to [-mutationRange/2 to mutationRange/2] 
    Outputs -> Child Neural Net         
    '''
    random.seed()
    child = copy.deepcopy(parentA)
    numLayers = len(child.netLayers)
    for i in range(numLayers):
        numNeurons = child.netLayers[i].numNeurons
        for j in range(numNeurons):
            randomNum = random.random()
            if randomNum > 0.5:
                child.netLayers[i].weights[j] = parentB.netLayers[i].weights[j]
                child.netLayers[i].biasVector[j] = parentB.netLayers[i].biasVector[j]
            numWeights = len(child.netLayers[i].weights[j])
            for k in range( numWeights + 1 ): # +1 for bias
                mutationNum = random.random()
                if mutationNum < mutationRate:
                    if k  == numWeights: 
                        child.netLayers[i].biasVector[j]+= (random.random()-0.5) * mutationRange
                    else: 
                        child.netLayers[i].weights[j][k] += (random.random()-0.5) * mutationRange

    return child 