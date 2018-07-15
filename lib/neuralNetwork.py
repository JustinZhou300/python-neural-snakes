import math as m
import numpy as np

BIAS = -1
RELU  = lambda x: (x>0) * x 

SOFTMAX= lambda x : np.exp(x)/np.sum(np.exp(x))
RANDOM_WEIGHT =  lambda x: (np.random.random()-0.5)  * x
TANH = lambda x: np.tanh(x)
WEIGHT_RANGE = 2

class NeuronLayer():

    def __init__(self,numNeurons,numInputs,weightRange):
        self.numInputs = numInputs
        self.numNeurons = numNeurons
        self.weights = ( np.random.random((numNeurons,numInputs)) - np.ones((numNeurons,numInputs),float) * 0.5 ) * weightRange
        self.biasVector = np.zeros((numNeurons,1),float)

    def update(self,inputs):
        rawOutputs = self.weights @ inputs + self.biasVector*BIAS
        normalisedOutputs =  [ RELU(rawOutputs[i]) for i in range(0,self.numNeurons) ]
        return normalisedOutputs


class NeuralNet():

    def __init__(self,numInputs,numOutputs,numHiddenLayers,neuronsPerHiddenLyr):
        self.numInputs = numInputs
        self.numOutputs = numOutputs
        self.numHiddenLayers = numHiddenLayers
        self.neuronsPerHiddenLyr = neuronsPerHiddenLyr
        self.netLayers = []
        self.totalNumNeurons =  numHiddenLayers * neuronsPerHiddenLyr + numOutputs
        self.totalNumWeights = (numInputs+1)*neuronsPerHiddenLyr + (numHiddenLayers-1)*(neuronsPerHiddenLyr+1)*neuronsPerHiddenLyr + (neuronsPerHiddenLyr+1)*numOutputs

    def createNet(self):
        if self.numHiddenLayers > 0:
            self.netLayers.append(NeuronLayer(self.neuronsPerHiddenLyr,self.numInputs,WEIGHT_RANGE))
            for i in range(0,self.numHiddenLayers-1):
                self.netLayers.append(NeuronLayer(self.neuronsPerHiddenLyr,self.neuronsPerHiddenLyr,WEIGHT_RANGE))
            self.netLayers.append(NeuronLayer(self.numOutputs,self.neuronsPerHiddenLyr,WEIGHT_RANGE))
        else:
            self.netLayers.append(NeuronLayer(self.numOutputs,self.numInputs,WEIGHT_RANGE))

    def updateNet(self,inputs):
        self.outputs = self.netLayers[0].update(inputs)
        for i in range(1,self.numHiddenLayers+1):
            self.outputs = self.netLayers[i].update(self.outputs)
        return self.outputs

    def changeLayers(self,Layers):
        if len(Layers) == len(self.netLayers):
            for i in range( len(Layers) ):
                if self.netLayers[i].weights.shape == Layers[i].weights.shape:
                   self.netLayers[i].weights = Layers[i].weights
                   self.netLayers[i].biasVector = Layers[i].biasVector
                else: 
                    print("error: miss-matched weights matrix")
                    return
        else:
            print("error: miss-matched number of layers")
            return

