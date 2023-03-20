import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'  # doesnt show any annoying tensorflow warnings

from tensorflow import keras
from keras import layers,losses
from keras.optimizers import Adam
from keras.utils import plot_model
from keras.models import load_model

class Model:
    # Basic class definition
    def __init__(self, NumLayers, width, BatchSize, LearningRate, InputDimension, OutputDimension, model=None):
        self.InputDimension = InputDimension
        self.OutputDimension = OutputDimension
        self.BatchSize = BatchSize
        self.LearningRate = LearningRate
        if model:
            self.model = model
        else:
            self.model = self.BuildModel(NumLayers, width)
    
    #Builds a fully connected nueral network
    def BuildModel(self, NumLayers, width):
        Input=keras.Input(shape=(self.InputDimension,))
        Output=layers.Dense(width, activation='relu')(Input)
        for _ in range(NumLayers):
            Output=layers.Dense(width, activation='relu')(Output)
        Output=layers.Dense(self.OutputDimension,activation='linear')(Output)
        Model=keras.Model(inputs=Input,outputs=Output,name='MyModel')
        Model.compile(loss=losses.mean_squared_error,optimizer=Adam(LearningRate=self.LearningRate))
        return Model